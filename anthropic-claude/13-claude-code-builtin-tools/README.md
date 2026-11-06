# Chapter 13 — Claude Code Built-in Tools

> **Exam domain(s):** Domain 2 — Tool Design & MCP Integration (**18%**, task 2.5 in full; supports 2.4 built-in vs MCP tools) · Domain 5 — Context Management & Reliability (**15%**, task 5.4 large-codebase exploration) · also Domain 1 — Agentic Architecture & Orchestration (**27%**, 1.6 mapping a legacy codebase before planning) and Domain 3 — Claude Code Configuration & Workflows (**20%**, plan mode, permissions)
> **Est. time:** 4–6 hours (reading + 2 notebooks) · **Status:** [ ] not started

Claude Code and the Claude Agent SDK give the model a small set of purpose-built tools: search by path, search by content, read, write, targeted edit and shell. Customers always ask three things about coding agents: *Can it understand our codebase? Will it change only what we asked? What can it touch?* The built-in tools and the permission rules keyed to their names answer all three.

## What you'll learn

- Pick the right one of the six core tools (`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`) for a request
- Tell Grep (file *contents*) from Glob (file *paths*) and keep results small
- Apply the Edit contract and fall back to Read + Write when no unique anchor exists
- Investigate a codebase incrementally and trace callers through wrapper modules
- Fix MCP tool selection with better descriptions, and scope tools with permission rules
- Plan the codebase-understanding phase of a modernization project

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md) (only the optional live cell needs `ANTHROPIC_API_KEY`), [Chapter 2 — Tool Use](../02-tool-use/README.md), [Chapter 3 — Agent SDK](../03-agent-sdk/README.md), [Chapter 4 — MCP](../04-model-context-protocol/README.md), [Chapter 5 — Claude Code](../05-claude-code/README.md) and [Chapter 11 — Context Management](../11-context-management/README.md).

---

## Concepts

The whole chapter is one loop: **find a small set of candidates, read only those, decide what to look for next, and change code only with the narrowest tool that does the job.**

### 13.1 The six core tools and how Claude chooses among them

Each built-in tool is a tool definition (name, description, input schema), like the ones in [Chapter 2](../02-tool-use/README.md#22-tool-definition). Claude chooses by matching your request against those descriptions.

| Tool | Purpose | Use it when | Key inputs |
|---|---|---|---|
| `Glob` | Find files by **path pattern** | You know a name or extension shape: `**/*.test.tsx` | `pattern`, `path` |
| `Grep` | Search file **contents** with a regex | You know a symbol, string, error message, import or config key | `pattern`, `path`, `glob`, `type`, `output_mode`, `multiline`, `head_limit` |
| `Read` | Load a file (with line numbers) | You need the code of a file a search surfaced | `file_path`, `offset`, `limit` |
| `Write` | Create a file, or **overwrite** one completely | New files; full rewrites; the Edit fallback | `file_path`, `content` |
| `Edit` | Replace an **exact, unique** string | A targeted change to existing code | `file_path`, `old_string`, `new_string`, `replace_all` |
| `Bash` | Run a shell command | Tests, builds, `git`, linters, listing directories | `command`, `timeout`, `run_in_background` |

Three rules of thumb cover most exam questions:

1. **Search before you read.** Glob or Grep narrows thousands of files to a handful; Read is for the handful.
2. **Paths → Glob, contents → Grep.** "All test files" is a path question. "Every caller of `issue_refund`" is a content question.
3. **Smallest change that is safe.** Edit for a snippet, Write for a new file or a full rewrite, Bash for running things, not for editing them.

The tool names are exact strings. You use them in permission rules (`Edit(/src/**)`), `--allowedTools`, a subagent's `tools:` list and hook matchers (`"matcher": "Edit|Write"`).

> **Note: changed since the guide.** The exam still tests six tools. The current product has many more (13.9). Also, on macOS, Linux and WSL, `Glob` and `Grep` are no longer in the default tool set: Claude searches with `find` and `grep` through `Bash`, and those searches reach hooks and permission rules as `Bash` calls. You get the dedicated tools back when you name them in `--tools` / `--allowedTools` (or the SDK's `tools` / `allowed_tools`), when the whole Bash tool is removed (a bare `Bash` deny, `--disallowedTools Bash` or `--restricted`; a scoped rule such as `Bash(rm *)` is not enough), or in a subagent whose `tools` list names them without Bash. The selection logic is the same either way. Ask a session "What tools do you have access to?" to check.

> **Exam trap:** "Add instructions to CLAUDE.md telling Claude to use Grep" or "build a routing layer that picks the tool" are distractors. Give the agent the right tools, and phrase tasks so the right tool is obvious.

### 13.2 Grep vs Glob: content search vs path search

**Glob** answers "which files exist whose *path* matches this shape?" Results are **capped at 100 files**; when the cap is hit, narrow the pattern. Glob does **not** respect `.gitignore` by default.

**Grep** answers "which files *contain* text matching this regex?" It uses **ripgrep regex syntax**, so escape metacharacters (`process_refund\(`). It **respects `.gitignore`**, so `node_modules/` and `dist/` stay out. Three output modes control size: `files_with_matches` (paths only, the default and cheapest), `content` (matching lines with line numbers) and `count`. Narrow with `type` (`py`) or the `glob` parameter (`**/*.tsx`).

| Request | Tool and input |
|---|---|
| "Find every Storybook file in the monorepo" | `Glob {"pattern": "**/*.stories.tsx"}` |
| "Where is *Refund declined by processor* produced?" | `Grep {"pattern": "Refund declined by processor", "output_mode": "content"}` |
| "Who calls `issue_refund`?" | `Grep {"pattern": "issue_refund\\(", "type": "py", "output_mode": "content"}` |
| "How many TODOs per file in `src/`?" | `Grep {"pattern": "TODO", "path": "src", "output_mode": "count"}` |

> **Exam trap:** "Use Glob with `*issue_refund*`" to find callers is wrong: Glob matches *file names*. "Use Grep for `**/*.test.tsx`" is the mirror-image mistake. An empty Grep on a gitignored path, or a Glob capped at 100, is not proof that something does not exist.

### 13.3 Read, Write and Edit: full-file vs targeted changes

**Read** returns a file with line numbers. It also reads images, PDFs (`pages: "1-5"`) and notebooks. A whole file over the token limit (25,000 tokens by default) comes back as a **`PARTIAL view`**; a whole file over 256 KB returns an error. Either way, Claude continues with `offset` and `limit`, or with Grep. Read does not list directories; use `ls` through Bash.

**Write** creates a file or **overwrites it completely**. It never appends or merges. Overwriting an existing file normally requires that Claude has read it in the current conversation (the same model-dependent rule as read-before-edit below; notebooks and `PARTIAL view` files always need the read).

**Edit** performs an **exact string replacement**: `old_string` → `new_string`. Three checks must pass:

| Check | What it means | Typical failure |
|---|---|---|
| **Read before edit** | Claude has read the file in this conversation (a `PARTIAL view` does not count) | Editing a file the agent never opened |
| **Match** | `old_string` appears exactly as written: no regex, every space and tab counts | Wrong indentation, tabs vs spaces, a stale read |
| **Uniqueness** | `old_string` appears **exactly once**, unless `replace_all: true` | `"timeout": 30` appears in three config blocks |

The exam treats read-before-edit as always required, and reading first is the safe habit. In current Claude Code, Opus 4.6, Haiku 4.5 and older models always need the read; newer models (such as Sonnet 5.5) may skip it when reading would not need a permission prompt. Viewing one file with `cat`, `head` or `grep` through Bash also counts as the read.

The Messages API [text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool) (`str_replace_based_edit_tool`) has the same contract: its `str_replace` command needs an exact `old_str` that matches one location. If you build your own coding agent, implement the same checks.

**NotebookEdit** targets one notebook cell by `cell_id`. Use it for `.ipynb` files; Edit or Write on notebook JSON is how notebooks get corrupted.

### 13.4 When Edit fails: anchors, `replace_all` and the Read + Write fallback

Edit failures are **deterministic**: the same call gives the same error. Find which check failed, then climb this ladder:

1. **Not read** → Read the file, then retry.
2. **No match** → re-read and copy `old_string` exactly (indentation, tabs, CRLF).
3. **More than one match, change all** → `replace_all: true`.
4. **More than one match, change one** → widen `old_string` with nearby lines (function name, section key).
5. **No small unique anchor exists** → the **Read + Write fallback**.

The fallback, which the exam names explicitly:

1. **Read** the full file, immediately before changing it.
2. **Modify the content** by structure (the block under `[payments]`), not by a guessed line number.
3. **Write** the complete updated file.
4. **Verify**: re-read the changed region or run `git diff`, and run the tests.

It costs something: Write replaces the **whole** file, so anything missing from your content is lost, and so are changes made between your Read and your Write. Keep the two close together.

> **Exam trap:** Distractors are: retry the same Edit, `replace_all` when only one occurrence should change, `sed -i` on a guessed line number, or recreating the file without reading it. The exam's answer is **Read the full file, then Write the modified version**. In practice, widening the anchor comes first when it is possible.

### 13.5 Bash: the general-purpose tool and its limits

Bash runs tests, builds, `git`, package managers, linters and `ls`. Know four things:

- **Each command runs in a separate process.** `cd` carries over only inside the project; `export` does **not** persist.
- **Output is bounded.** A successful result is inline up to roughly 30,000 characters, then saved to a file. A noisy test suite is a context problem, so run it in a subagent and report only the failures.
- **Timeouts.** Two minutes by default, up to ten for a foreground command. Start long-running servers with `run_in_background`.
- **Prefer the dedicated tool.** Read and Edit give line numbers and the read-before-edit check; `sed -i` on a remembered line number has neither. Bash is the escape hatch, and the tool to scope most carefully (13.10).

These numbers match the [tools reference](https://code.claude.com/docs/en/tools-reference) as checked on 2026-10-03; re-check them before quoting them.

### 13.6 Incremental investigation: Grep, Read, repeat

Do not read a codebase to understand it. Even a 200-file repo fills the window with unrelated code, and long sessions drift toward generic answers (task 5.4). Investigate incrementally: start from the most specific clue, read only what each search surfaces, let what you read decide the next search, and stop as soon as the question is answered.

Worked example: *"Customers see 'Refund declined by processor'. What code path produces it, and where is the amount checked?"*

| Step | Call | What it tells you |
|---|---|---|
| 1 | `Grep "Refund declined by processor"` | One hit: `app/payments/gateway.py:18` |
| 2 | `Read app/payments/gateway.py` | `Gateway.submit_refund()` raises it |
| 3 | `Grep "\.submit_refund\("` | Called from `app/billing/refunds.py` |
| 4 | `Read app/billing/refunds.py` | `create_refund()` calls `check_policy()`, then `submit_refund()` |
| 5 | `Grep "def check_policy"` | `app/billing/policy.py` |
| 6 | `Read app/billing/policy.py` | The amount limit lives here |

Six calls, three files read. Reading all 23 Python files costs about nine times as much context in that small repo, and buries the answer.

- **Start from the most specific string you have**, such as an exact error message.
- **Use `files_with_matches` first**, then `content` on the few files that matter.
- **Write findings down** in a scratchpad file (file, line, what it does) and read it back before the next phase ([Chapter 11](../11-context-management/README.md#114-scratchpad-files)).
- **Delegate verbose discovery** to the built-in **Explore** subagent (read-only, own context window, returns a summary) ([Chapter 11](../11-context-management/README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context)).

> **Exam trap:** "Read all files in the module first so the agent has complete context" is wrong. So are "increase the context window" and "summarize every file up front". Start with a targeted search and follow the evidence.

### 13.7 Tracing through wrapper modules

A **wrapper module** (a Python `__init__.py`, a TypeScript barrel `index.ts`, a facade class) re-exports names, often under **aliases**:

```python
# app/billing/__init__.py   (a wrapper module)
from .refunds import create_refund as issue_refund, cancel_refund
from .ledger import post_entry

__all__ = ["issue_refund", "cancel_refund", "post_entry"]
```

`Grep "create_refund"` finds the definition, the wrapper's import, one test and a dead legacy copy. You might conclude the function is barely used. That is wrong: the rest of the code calls it `issue_refund`, and one worker re-aliases it as `refund`.

The method:

1. **List every name the wrapper exports**: each `import X as Y` (the name is `Y`), each `__all__` entry, each `export { a as b }`.
2. **Search for each exported name**, not only the definition name.
3. **Follow second-level aliases** (`issue_refund as refund`) and module-qualified calls (`billing.issue_refund`).
4. Record a map: exported name → definition → callers.

| Name searched | Finds |
|---|---|
| `create_refund` (definition name) | definition, wrapper import, one test, dead legacy copy |
| `issue_refund` (wrapper alias) | the API route, the support macros, the worker's import |
| `refund(` after the re-alias | the actual call in the nightly worker |

### 13.8 Built-in tools vs MCP tools

MCP tools join the same list as the built-ins. Agents tend to **prefer built-in tools** such as Grep when an MCP tool looks similar, because the built-ins have well-tested descriptions. (This framing comes from the exam guide, task 2.4.) The fix the exam expects is a **better MCP tool description** that says what the MCP tool can do that the built-in cannot:

```text
Weak:   code_search: Search code.
Strong: code_search: Semantic search over the pre-built index of ALL 40
        service repositories (including repos not checked out locally),
        with ownership and last-deploy metadata. Use this instead of Grep
        when the question spans services. Returns: up to 20 hits with
        repo, path, line, owner team.
```

Do not remove Grep to force the MCP tool, and do not add a routing classifier. Claude Code cuts server instructions and upfront tool descriptions at 4,096 characters, and descriptions loaded through tool search at 16,384, by default. Tool search matches only against the first 4,096, so put the decisive information first.

**Built-in vs custom tool vs skill vs MCP (CCDV-F 8.3):**

| Need | Choose | Why |
|---|---|---|
| Files, search, shell in the working directory | Built-in tools | Already there, permissioned by path and command |
| A reusable integration other apps also need | MCP server | One implementation, many clients |
| A capability only this one application needs | Custom tool (or an in-process SDK MCP tool) | No separate server to run |
| A repeatable *procedure* or house style | Skill | Loaded on demand through the `Skill` tool |

### 13.9 Other current built-in tools *(beyond the guide)*

The exam stops at six tools. You should still recognize these, because they appear in permission configs, hook matchers and transcripts. The [tools reference](https://code.claude.com/docs/en/tools-reference) is the source of truth.

| Tool | What it does | Note for architects |
|---|---|---|
| `Agent` | Spawns a subagent with its own context window | Built-in types: `Explore` (read-only search), `Plan`, `general-purpose`. Formerly `Task` |
| `WebFetch` | Fetches a URL and runs an extraction prompt on it | Lossy by design; refuses `localhost` |
| `WebSearch` | Web search; returns titles and URLs | 200 calls per interactive session by default (refills about 100/hour; raise with `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`); per turn in `-p` and the Agent SDK |
| `Monitor` | Runs a command in the background and feeds each output line back | Uses the `Bash` permission rules |
| `NotebookEdit` | Replaces, inserts or deletes one cell by `cell_id` | Governed by `Edit(...)` path rules |
| `LSP` | Definitions and references from a language server | Needs a code intelligence plugin; replaces many Grep + Read rounds |
| `EnterPlanMode` / `ExitPlanMode` | Enter plan mode / present a plan for approval | Plan mode: explore and plan, no edits |
| `Skill` | Runs a skill in the main conversation | Skills add procedures, not new tools |
| `ToolSearch` | Loads deferred (MCP) tool definitions on demand | Why many MCP tools no longer cost context up front |

### 13.10 Permission rules per tool *(beyond the guide)*

Tool names are the vocabulary of the permission system. Settings `allow` / `ask` / `deny`, `--allowedTools` and the SDK's `allowed_tools` all use **`Tool` or `Tool(specifier)`**:

| Rule | Applies to | Matches |
|---|---|---|
| `Bash(npm run *)` | `Bash`, `Monitor` | Command text with `*`; each subcommand of `&&`, `;`, `\|` must be allowed |
| `Read(./.env)` | `Read`, `Grep`, `Glob`, `LSP` | gitignore-style paths |
| `Edit(/src/**)` | `Edit`, `Write`, `NotebookEdit` | gitignore-style paths |
| `WebFetch(domain:example.com)` | `WebFetch` | Host name |
| `Agent(Explore)` | `Agent` | A subagent type |
| `mcp__github`, `mcp__github__get_issue` | MCP tools | A server's tools, or one tool |

What trips people up:

- **Order is deny → ask → allow**; the first match wins. A broad `deny: Bash(aws *)` beats a narrow `allow: Bash(aws s3 ls)`.
- **There is no `Write(path)`, `Glob(path)` or `Grep(path)` rule.** File checks consult only `Edit(path)` and `Read(path)`. Use `Edit(docs/**)`, which covers Write and NotebookEdit, or `Read(docs/**)` for searches.
- **A `Read(path)` deny also blocks Edit and Write** on that path (not NotebookEdit; add `Edit(path)` for that). Read and Edit deny rules also cover recognized Bash file commands (`cat`, `head`, `tail`, `sed`, `tee`) and redirect targets, but not scripts that open files themselves.
- **A bare tool name in `deny` removes the tool**; `Bash(rm *)` keeps it and blocks matching calls.
- **`/path` is relative to the settings source**, not the filesystem root; `//abs/path` is absolute.
- **Bash rules match command text, not programs.** `deny: Bash(curl *)` misses `sh -c 'curl …'`. Use the sandbox or a `PreToolUse` hook for real limits. CLAUDE.md shapes what Claude *tries*; only rules, modes, hooks and the sandbox *enforce*.

A project `.claude/settings.json` for a modernization team:

```json
{
  "permissions": {
    "allow": ["Bash(npm run test *)", "Bash(git diff *)"],
    "ask": ["Bash(git push *)"],
    "deny": [
      "Read(./.env)",
      "Read(secrets/**)",
      "Edit(/migrations/**)",
      "Bash(curl *)"
    ]
  }
}
```

A bare `secrets/**` deny matches a `secrets` directory at any depth; `/migrations/**` is anchored at the project root.

**In the Agent SDK**, three options do different jobs:

| Option | Effect |
|---|---|
| `tools=["Read", "Grep", "Glob"]` | The **base set** of built-in tools the agent has at all |
| `allowed_tools=["Read", "Grep", "Glob"]` | **Auto-approves** these tools; it does *not* remove the others |
| `disallowed_tools=["Bash"]` | A bare name **removes** the tool; `"Bash(rm *)"` denies matching calls in every mode |

> **Exam trap:** `allowed_tools=["Read"]` with `permission_mode="bypassPermissions"` still lets the agent run Bash, Write and Edit. To restrict, use `tools` or `disallowed_tools`, and prefer `permission_mode="dontAsk"` for unattended read-only agents.

### 13.11 Codebase understanding for modernization work

Modernization work (a framework upgrade, extracting a service, adding tests to a legacy system) starts with a phase whose output is **understanding**, not code:

1. **Map the structure.** `ls` the top level, Glob by extension, read the build files (`pyproject.toml`, `package.json`), Grep for entry points.
2. **Find high-impact areas** with numbers: **fan-in** (Grep imports with `output_mode: "count"`), **churn** (`git log --name-only` through Bash), **test gaps** (Glob `tests/**`) and **risk** (payments, auth). High fan-in × high churn × no tests is where to start.
3. **Trace the critical flows** incrementally (13.6) and through wrappers (13.7). Record findings in a scratchpad file.
4. **Plan in plan mode**: read-only exploration and a written plan before any edit. The plan adapts as dependencies appear (task 1.6).
5. **Execute in slices** with Edit, running tests after each slice.

Keep the main context for decisions. Delegate discovery to the Explore subagent or a read-only subagent (`tools: Read, Grep, Glob`), summarize each phase before the next, and use `/compact` only as a secondary measure.

> **Exam trap:** For "add comprehensive tests to a legacy codebase", "write tests file by file in alphabetical order" and "generate tests for every function in one pass" are distractors. Map the structure, find high-impact areas, and make a prioritized plan that adapts.

---

## Lesson code

Video-lesson code: [../../presentations/13-claude-code-builtin-tools/code/](../../presentations/13-claude-code-builtin-tools/code/)

The video runs on the Chapter 5 `acme-shop` repository with a cancelled-order bug; the notebooks use a smaller simulated `acme-shop` with a refund flow.

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run simulated Glob, Grep, Read, Write, Edit and Bash on a small offline repo (13.1–13.11), then build an investigation agent that traces the refund flow; optional live Agent SDK cell |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 offline coding exercises, one architecture scenario and a scorecard |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Find files by name or extension | `Glob` (`**/*.test.tsx`) | Grep, reading directories |
| Find callers, error strings, imports | `Grep` (start with `files_with_matches`) | Glob, reading files |
| Understand a flow in an unfamiliar repo | Grep → Read → Grep usages → Read consumers | Reading all files up front |
| Function re-exported through a wrapper | Search every exported name and alias | Searching only the definition name |
| Change one snippet | `Edit` with a unique `old_string` | `Write` of the whole file, `sed -i` |
| Same text, change only some; no unique anchor | Read → modify → Write → verify | Retrying Edit, `replace_all` |
| Agent ignores a capable MCP tool | Rewrite the MCP tool's description | Removing Grep, a routing classifier |
| Read-only investigation agent (SDK) | `tools=[Read, Grep, Glob]`, `dontAsk` | `allowed_tools` with `bypassPermissions` |
| Restrict which files can change | `Edit(path)` / `Read(path)` deny rules | `Write(path)` rules, CLAUDE.md |
| Modernization kickoff | Map → hotspots → plan mode → slices | Starting edits immediately |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Reading the whole repository "for context".** The window fills with irrelevant code.
- **Swapping Grep and Glob**, or treating an empty result as proof (gitignored files, the 100-result cap).
- **Searching only the definition name** when the function is re-exported under an alias.
- **Retrying a failed Edit unchanged**, or using `replace_all` when only one occurrence should change.
- **Writing `Write(...)` path rules** and assuming they restrict anything.
- **Treating `allowed_tools` as a restriction**, especially with `bypassPermissions`.

## Self-check

**1. (Developer productivity)** A developer asks Claude to find every place the string `ERR_QUOTA_EXCEEDED` is raised or handled across a 3,000-file service. Which approach fits best?

- A) Glob for `**/*ERR_QUOTA_EXCEEDED*`
- B) Grep for `ERR_QUOTA_EXCEEDED` (paths only first), then look closer at the hits
- C) Read every file under `src/` so no raise or handler is missed
- D) Ask the developer to list the relevant files first

<details><summary>Answer</summary>

**B.** The string lives inside files, so it is a content search; paths-only output first keeps the result small, then you look closer at the few hits. A matches file names, not contents. C wastes the context window. D pushes the tool's job onto the user.
</details>

**2. (Developer productivity)** In `deploy.yaml`, the block `replicas: 2` / `maxSurge: 1` appears identically under three services. Claude must change it only for the `billing` service, and Edit fails because the text is not unique. What is the most reliable next step?

- A) Retry the Edit with the same `old_string`, in case the failure was transient
- B) Use `replace_all: true` so every copy of the block changes together
- C) Widen `old_string` with the `billing:` key; if no unique anchor exists, Read the file and Write it back with only that block changed
- D) Run `sed -i` on the line number an earlier Read reported for the `billing` block

<details><summary>Answer</summary>

**C.** First try a unique anchor; when that is impossible, Read + Write with a structural change (the block under `billing:`) is the reliable fallback, followed by verification. A repeats a deterministic failure. B changes all three services. D edits a line number that may be stale and skips the read-before-edit safety.
</details>

**3. (Developer productivity)** An engineer asks: "How does an order move from checkout to fulfillment?" in a codebase Claude has never seen. Which first moves are best?

- A) Glob `**/*` and Read the 50 most recently modified files, since they reflect current behavior
- B) Grep for the checkout route or handler, Read it, then follow the functions it calls the same way
- C) Ask Claude to describe how e-commerce systems usually handle fulfillment
- D) Summarize every module first, then answer from those summaries to save context

<details><summary>Answer</summary>

**B.** Incremental investigation follows real evidence from an entry point. A reads by recency, not relevance. C produces "typical patterns" instead of this codebase's facts. D spends the context window on summaries of unrelated code and loses the details.
</details>

**4. (Developer productivity)** `pricing/__init__.py` contains `from .engine import compute_price as quote, apply_discount`. A Grep for `compute_price(` finds only the definition and one test, so a teammate wants to delete what looks like dead code. What should happen first?

- A) Delete it; the search shows no callers outside the test
- B) Grep for every name the wrapper exports (`quote`, `__all__` entries) and follow further aliases
- C) Grep for `compute_price` case-insensitively, in case callers use other casing
- D) Read the whole `pricing` package to see how its functions are used

<details><summary>Answer</summary>

**B.** The wrapper re-exports `compute_price` as `quote`, so callers use the alias. Searching for each exported name is the method for tracing through wrapper modules. A acts on an incomplete search. C still searches the wrong name. D reads the provider, not the callers.
</details>

## Official documentation

- [Tools reference](https://code.claude.com/docs/en/tools-reference): every built-in tool, Edit checks, Glob/Grep defaults, Bash limits
- [Configure permissions](https://code.claude.com/docs/en/permissions): rule syntax, deny → ask → allow, path anchors
- [Subagents](https://code.claude.com/docs/en/sub-agents): Explore, Plan and general-purpose; `tools` / `disallowedTools`
- [Agent SDK permissions](https://code.claude.com/docs/en/agent-sdk/permissions): `allowed_tools` vs `disallowed_tools`, `dontAsk`
- [Text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool): the Messages API `str_replace` contract
- Engineering post: [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

**Source / credit:** community study guide by paullarionov, [Chapter 13 and Domain 2.5](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-13-claude-code-built-in-tools), restructured here in my own words.

---

[← Chapter 12 — Preserving Provenance](../12-provenance/README.md) | [↑ Claude path overview](../README.md) | [Exam prep →](../exam-prep/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
