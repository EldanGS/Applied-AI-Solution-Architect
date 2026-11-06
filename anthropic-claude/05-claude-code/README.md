# Chapter 5 — Claude Code: Configuration and Workflows

> **Exam:** Domain 3 — Claude Code Configuration & Workflows (20%), plus parts of Domains 1 (task 1.7), 4 (task 4.6) and 5 (task 5.4). Scenarios: *Code Generation with Claude Code*, *Claude Code for Continuous Integration*.

Claude Code is the agent loop from [Chapter 3](../03-agent-sdk/README.md) with a terminal UI, and it is how most teams first put Claude into daily work. As the architect, you decide where team knowledge lives (CLAUDE.md, rules, skills, permissions and hooks) and how the same agent runs unattended in CI. Each choice trades **context cost** against **reliability** and **team consistency**, and the exam tests those trade-offs, not syntax trivia.

## What you'll learn

- Place an instruction at the right CLAUDE.md scope, and split a large file with `@path` imports and `.claude/rules/`
- Choose between CLAUDE.md (always), path-scoped rules (per file type) and skills (per task), and write SKILL.md frontmatter
- Choose plan mode or direct execution, and keep context clean with the Explore subagent, `context: fork` and `/compact`
- Run Claude Code headless in CI with `-p`, `--output-format json` and `--json-schema`, and resume or fork sessions
- Iterate with examples and failing tests, follow explore → plan → code → commit, and tell Claude Code from Computer Use

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md) (Python env, `.env` with `ANTHROPIC_API_KEY`, git), [Chapter 3 — Agent SDK](../03-agent-sdk/README.md) (agent loop, subagents, sessions) and [Chapter 4 — Model Context Protocol](../04-model-context-protocol/README.md) (`.mcp.json`). Claude Code installed and signed in (`claude --version` works). See the [setup guide](https://code.claude.com/docs/en/setup).

## Concepts

### 5.1 The CLAUDE.md hierarchy

CLAUDE.md files are plain-markdown instructions that Claude Code reads at the start of every session. They are **concatenated, not overridden**: every file that applies goes into context, from the broadest scope to the most specific.

| Scope | Location | Shared via git? | Typical content |
|---|---|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `/etc/claude-code/CLAUDE.md` (Linux/WSL) | Deployed by IT | Company security and compliance rules |
| User | `~/.claude/CLAUDE.md` (+ `~/.claude/rules/`) | **No**, only you | Personal style, your shortcuts |
| Project | `./CLAUDE.md` **or** `./.claude/CLAUDE.md` | **Yes** | Build/test commands, architecture, team conventions |
| Local | `./CLAUDE.local.md` (add to `.gitignore`) | No | Your sandbox URLs, personal test data |
| Subdirectory | `packages/api/CLAUDE.md` | Yes | Conventions for that part of the tree |

- **At launch**, Claude Code loads CLAUDE.md and CLAUDE.local.md from the working directory and **every directory above it**. Subdirectory files below it load **lazily**, the first time Claude reads, writes or edits a file there.
- CLAUDE.md is **context, not enforcement**. If an action must never happen, use a permission `deny` rule or a `PreToolUse` hook.
- Keep each file **under ~200 lines**. Write instructions you can verify ("Run `npm test` before committing", not "Test your changes") and remove contradictions, because Claude may follow either side of a conflict. `/init` generates a starter CLAUDE.md (see 5.12). `/context all` (or `/context` outside fullscreen mode) lists the memory files that actually loaded. Claude Code also reads **`AGENTS.md`** when no CLAUDE.md exists, which matters if you share a repo with [OpenAI Codex](../../openai-codex/README.md).

> **Exam trap:** A new teammate does not get an instruction everyone else follows. The instruction almost always lives in the veterans' **user-level** `~/.claude/CLAUDE.md`. Move it to the **project** `CLAUDE.md` or `.claude/CLAUDE.md`. To confirm, run `/context all` on both machines and compare the **Memory files** lists.

### 5.2 `@path` imports: modular CLAUDE.md

A CLAUDE.md can pull in other files with `@path`. Claude Code expands the imported file into context at launch.

```markdown
# Project CLAUDE.md
Build with `make build`; run tests with `make test`.

- Coding standards: @./standards/coding-style.md
- Testing requirements: @./standards/testing.md
- Personal, cross-worktree prefs: @~/.claude/my-project-prefs.md
```

- Relative paths resolve from **the file that contains the import**. Imports nest up to **four hops** deep. Text in backticks (`` `@README` ``) is **not** imported.
- In a monorepo, each package's CLAUDE.md imports only the shared standards that apply to it, for example `@../../standards/python.md`.

> **Exam trap:** "Use `@import` to split CLAUDE.md into category files" does not fix an overloaded context: imported files still load at launch. To load guidance **conditionally**, use path-scoped rules (5.3). To load it **on demand**, use skills (5.4).

### 5.3 `.claude/rules/`: topic files and path-scoped rules

`.claude/rules/` holds one markdown file per topic, discovered recursively. Rules come in two kinds:

- **Unscoped rule** (no frontmatter): loads at launch, like `.claude/CLAUDE.md`. It is a tidier way to split a monolithic file.
- **Path-scoped rule**: YAML frontmatter with `paths:`. It loads **only when Claude reads, writes or edits a file whose path matches the glob**.

```markdown
---
paths:
  - "**/*.test.ts"
---
# Test conventions
- Use describe/it blocks; one behavior per `it`.
- Never mock the database. Use the dockerized test DB.
```

| Conventions apply to… | Use |
|---|---|
| Files **scattered** across the tree by *type* (tests, migrations, `*.tf`) | `.claude/rules/` with `paths:` globs |
| One **self-contained directory** (`packages/billing/`) | CLAUDE.md inside that directory |
| Everything, always | Project CLAUDE.md or an unscoped rule |
| You only, every project | `~/.claude/rules/` |

> **Exam trap:** For "tests live next to source files all over the codebase and must follow the same conventions", the answer is `.claude/rules/` with glob `paths`. A CLAUDE.md in every directory scales badly. One root CLAUDE.md relies on Claude to infer which section applies. A skill is on demand, so it is not applied automatically.

### 5.4 Custom slash commands → skills

Custom commands **have been merged into skills**. `.claude/commands/review.md` and `.claude/skills/review/SKILL.md` both create `/review`. Old command files still work, and the skill wins on a name clash. The exam was written around `.claude/commands/`, so learn both names.

| Location | Path | Shared? | Precedence |
|---|---|---|---|
| Personal | `~/.claude/skills/<name>/SKILL.md` (legacy: `~/.claude/commands/<name>.md`) | Only you, all projects | 2 (managed enterprise skills are 1) |
| Project | `.claude/skills/<name>/SKILL.md` (legacy: `.claude/commands/<name>.md`) | Everyone who clones the repo | 3 |

**Team-wide `/review`:** put it in the **project** `.claude/skills/` (or `.claude/commands/`), which arrives with `git clone`. **Personal tweak of a team skill:** create `~/.claude/skills/<same-name>/SKILL.md`. Personal outranks project, so it shadows the team version **for you only**.

### 5.5 Skills in depth: SKILL.md frontmatter

A skill is a **directory**. `SKILL.md` holds the instructions, and supporting files load only when Claude needs them. Claude sees each skill's `description` up front and loads the body only when the skill is invoked, by you (`/name args`) or by Claude when the description matches the task.

```markdown
---
name: migration
description: >
  Generate a new database migration file following team conventions.
  Use when the user asks to create, add or scaffold a migration.
argument-hint: "[migration-name]"
context: fork            # run in an isolated subagent
agent: general-purpose   # subagent type for the fork (Explore = read-only)
allowed-tools: Read Write Bash(cat db/VERSION)  # pre-approves only
disallowed-tools: WebFetch WebSearch            # actually removes tools
disable-model-invocation: true   # side effects -> only a human triggers it
---
Create a migration named `$ARGUMENTS` in `db/migrations/`.
Current schema version: !`cat db/VERSION`
Read `db/MIGRATIONS.md` first and follow its conventions.
Never modify existing migrations.
```

| Field | What it does |
|---|---|
| `description` | Claude's trigger for auto-invocation. Vague descriptions mean the skill never fires, or fires at the wrong time |
| `argument-hint` | Autocomplete hint such as `[migration-name]`, so runs don't miss the required argument |
| `context: fork` | Runs the skill in a **fresh subagent context** that returns only its result. Verbose output stays out of the main session |
| `allowed-tools` | **Pre-approves** the listed tools. Every other tool stays callable through normal permissions |
| `disallowed-tools` | Removes tools while the skill is active. This is the real restriction |
| `disable-model-invocation: true` | Only a human can invoke it. Protects `/deploy` and `/commit` |
| `` !`cmd` `` | Runs a shell command **before** Claude sees the skill and injects its output |

> **Note: changed since the official exam guide.** The exam guide (task 3.2) says `allowed-tools` *restricts* tools. Current docs say it **pre-approves** them. To restrict, use `disallowed-tools`, `context: fork` with `agent: Explore`, or `deny` rules. In exam questions, "restrict `allowed-tools` to safe operations" is still the intended answer for "a skill with broad tool access did something destructive".

**Skill vs CLAUDE.md vs rule: the core decision**

| Guidance should load… | Mechanism | Example |
|---|---|---|
| Every session, always | CLAUDE.md / unscoped rule | "Use pnpm", build commands |
| When touching certain files | Path-scoped rule | Test conventions for `**/*.test.ts` |
| Only for a particular **task** | Skill | PR-review checklist, deploy runbook |
| Must be guaranteed | Permissions / hooks | "Never push to main" |

> **Exam trap:** Guidance tied to a *task* (cutting a release, writing an incident report) is a **skill**, even when the task happens to touch certain files. A path-scoped rule would fire on every edit of those files for any reason, and not at all before the first one.
>
> **Exam trap:** When a skill's own bulky output pushes the session's goal out of view, add **`context: fork`** so only the result comes back. Running `/compact` afterwards is cleanup, not isolation.

### 5.6 Plan mode vs direct execution

**Plan mode** is a permission mode. Claude researches the codebase and writes a plan, but it **cannot edit your source until you approve the plan**. Enter it with `Shift+Tab`, a `/plan` prefix, `claude --permission-mode plan`, or `"permissions": { "defaultMode": "plan" }` in `.claude/settings.json`. `Ctrl+G` opens the plan in your editor so you can change it. The common pattern combines both: **plan mode to investigate and propose**, human approval, then **direct execution of the approved plan**.

| Use **plan mode** when… | Use **direct execution** when… |
|---|---|
| Change spans dozens of files (a library migration across 45+ files) | Single-file fix with a clear stack trace |
| Several valid architectures exist (index vs cache vs read replica for a slow page) | Adding one validation check |
| Requirements are ambiguous, or the codebase is unfamiliar | You already know exactly what to change |

**Explore subagent.** For discovery-heavy work, such as "map every feature-flag read in the monorepo", hand the job to the built-in read-only **Explore** subagent. Its verbose output stays in its own context and only a summary returns.

### 5.7 `/compact` and managing the context window

Every file read, tool output and reply accumulates in the session's context.

| Command | Effect |
|---|---|
| `/context` | Shows what is using context, including which memory files loaded |
| `/compact [focus]` | Replaces the history with a structured summary, e.g. `/compact keep the auth bug repro steps` |
| `/clear` | Starts an empty context. The old conversation can still be resumed |

After compaction, the project-root CLAUDE.md, unscoped rules, auto memory and the plan are **re-injected from disk**. Path-scoped rules and nested CLAUDE.md files are **summarized away** until Claude reads a matching file again. Instructions you typed in chat survive **only if the summary kept them**. **Risk:** summaries lose exact numbers, IDs and error strings first. Write critical facts to a file before you compact, or give `/compact` a focus instruction.

> **Exam trap:** When discovery output is what fills the context, prefer the answer that **prevents** the bloat (an **Explore subagent** or a `context: fork` skill) over one that cleans up afterwards with `/compact`.

### 5.8 `/memory` and auto memory

`/memory` **lists every memory file** (user, project and local CLAUDE.md, plus auto memory), opens the one you pick, and toggles auto memory. In exam questions about "verify which memory files are loaded", `/memory` is the intended answer. Today `/context all` is the more precise tool for the current session. **Auto memory** is written by Claude from your corrections ("remember: always use pnpm") and lives in `~/.claude/projects/<project>/memory/MEMORY.md`. It is machine-local and not shared. Architect rule: **team knowledge goes into the project CLAUDE.md through a reviewed PR**. Auto memory is personal convenience that nobody reviews.

### 5.9 Claude Code in CI/CD: headless mode

`claude -p "<prompt>"` (`--print`) runs **non-interactively**: it prints the result and exits with code 0 on success. Without `-p`, a CI job waits for keyboard input and hangs.

| Flag | Purpose in CI |
|---|---|
| `--output-format json` | Returns `result`, `session_id`, usage and `total_cost_usd`. For `stream-json` see [5.12](#512-getting-started-and-the-core-loop) |
| `--json-schema '<schema>'` | Validated structured output in the **`structured_output`** field |
| `--allowedTools "Read,Bash(git diff *)"` | Pre-approve exactly the tools the job needs |
| `--permission-mode dontAsk` | Deny anything not pre-approved instead of prompting (locked-down CI) |
| `--max-turns N`, `--max-budget-usd X` | Cap runaway loops and spend |
| `--bare` | Skip CLAUDE.md, hooks, plugins, MCP servers and skills discovery for reproducible runs. Needs an API key (or cloud-provider credentials), not a subscription login |

```bash
gh pr diff "$PR" | claude -p \
  --append-system-prompt "Report only concrete, exploitable issues." \
  --output-format json \
  --json-schema "$(cat review.schema.json)" \
  --allowedTools "Read,Grep,Glob" --max-turns 8 \
  | jq '.structured_output.findings'
```

**CI design patterns the exam keeps coming back to:**

1. **Structured output over format instructions.** Inline PR comments need file, line, severity and fix as data. Use `--output-format json` + `--json-schema`, not "please output `[FILE:x]`" in the prompt.
2. **Independent reviewer.** The session that wrote the code tends to confirm its own reasoning. Review with a **separate** instance that never saw it.
3. **Re-review without duplicates.** On new commits, pass the **previous findings** and ask only for *new or still-unresolved* issues.
4. **CLAUDE.md as CI context.** CI-run Claude Code reads the project CLAUDE.md, so document testing standards, fixtures and review criteria there. A `--bare` run skips CLAUDE.md, so pass it with `--append-system-prompt-file CLAUDE.md`. Include existing test files when generating tests, to avoid duplicate cases.

> **Exam trap:** Distractors for "the CI job hangs": `CLAUDE_HEADLESS=true`, `--batch`, `< /dev/null`. The answer is **`-p`**.

### 5.10 Sessions: resume, name, fork

| Goal | CLI | Inside a session | Agent SDK (Python) |
|---|---|---|---|
| Name a session | `claude -n auth-bug` | `/rename auth-bug` | track `session_id` |
| Continue the latest | `claude -c` / `--continue` | — | `ClaudeAgentOptions(continue_conversation=True)` |
| Resume a specific one | `claude --resume auth-bug` | `/resume` | `ClaudeAgentOptions(resume=session_id)` |
| Branch (fork) | `claude --resume <id> --fork-session` | `/branch try-oauth` | `ClaudeAgentOptions(resume=session_id, fork_session=True)` |

- A session is a saved conversation, stored as JSONL under `~/.claude/projects/<project>/`. A fork copies the **conversation history only, not the filesystem**. If both forks write code, give each a **git worktree** (`claude -w <name>`).
- Sessions created with `-p` or the SDK do **not** appear in the `/resume` picker. Capture `session_id` from the JSON output and resume by ID.
- **Resume vs fresh start.** If files changed since the session, its tool results are **stale**. Tell Claude what changed, or start a **new session seeded with a short structured summary**, which is often more reliable.

### 5.11 Iterative refinement with Claude Code

Claude stops when the work *looks* done, so give it something that produces a pass/fail signal. The exam (task 3.5) tests four techniques.

**1. Concrete input/output examples beat prose.** When a prose description keeps being misread, give **2–3 examples** of the transformation, including an edge case. They also turn straight into tests (compare few-shot prompting in [Chapter 6, 6.1](../06-prompt-engineering/README.md#61-few-shot-prompting)).

```text
Rewrite normalize_name() so these hold:
  "  ada LOVELACE "  -> "Ada Lovelace"
  "o'brien"          -> "O'Brien"
  None               -> None        (do not raise)
Then run tests/test_normalize.py and fix any failures.
```

**2. Test-driven iteration.** Write the tests **first**, let Claude implement and run them, then feed back the **specific failures**: test name, input, expected value and actual traceback. "It still doesn't work" gives Claude nothing to aim at. You can also enforce the loop with a `Stop` hook that blocks the turn until tests pass ([Chapter 3, 3.5](../03-agent-sdk/README.md#35-hooks-in-the-agent-sdk)).

**3. The interview pattern.** In an unfamiliar domain, ask Claude to **interview you before it implements**, so it surfaces cache invalidation, failure modes and data volumes. Have it write a spec to SPEC.md, then implement in **a fresh session** ([Chapter 6, 6.4](../06-prompt-engineering/README.md#64-the-interview-pattern)).

**4. One message or one at a time?**

| The issues are… | Do this |
|---|---|
| **Interacting**: fixing one changes the right fix for another (a parser and the validator that consumes its output) | Describe **all of them in one detailed message**, so Claude designs one consistent fix |
| **Independent**: different files, no shared behavior (a typo, a slow query) | Fix them **sequentially**, one message each, and verify each fix |

> **Exam trap:** "Claude's migration script mishandles `NULL` values. What is the most effective next prompt?" The answer gives **specific test cases with example input and expected output** for the null rows. A longer prose explanation is the distractor. For three bugs on the same date-parsing path, send one message listing all three.

### 5.12 Getting started and the core loop

**What Claude Code is.** A chat assistant answers in text. Claude Code is an **agentic coding tool**: it runs in your project with tools to read, search, edit, run commands and tests, and use git. It loops through **gather context → take action → verify results** until the task is done. It manages the **context window**, **permissions** decide what runs without asking, and **checkpoints** let you rewind file edits (`Esc Esc` or `/rewind`).

| Surface | How to get it |
|---|---|
| Terminal (CLI) | `curl -fsSL https://claude.ai/install.sh \| bash` (macOS, Linux, WSL), `brew install --cask claude-code` or `winget install Anthropic.ClaudeCode` |
| VS Code (and forks), JetBrains | Claude Code extension / plugin from the marketplace (JetBrains needs the CLI installed separately) |
| Desktop app | Claude Desktop, Code tab |
| Web | [claude.ai/code](https://claude.ai/code), a cloud session that keeps running after you close your laptop |

On a cloud provider, pick **3rd-party platform** at login (or run `/setup-bedrock` / `/setup-vertex`), or set `CLAUDE_CODE_USE_BEDROCK=1` / `CLAUDE_CODE_USE_VERTEX=1`. For a team rollout, pin model versions with `ANTHROPIC_DEFAULT_SONNET_MODEL` and similar variables.

**First session.** `cd` into the project, run `claude` and ask questions first. Then run **`/init`**, which is **repository initialization**: Claude analyzes the codebase and writes a starter `CLAUDE.md`. Review it and commit it. Press `Shift+Tab` to cycle **permission modes**:

| Mode (status bar) | Config value | What runs without asking |
|---|---|---|
| Manual, the "approval" mode | `default` | Reads only; you approve each edit and command |
| Accept edits ("auto-accept") | `acceptEdits` | Reads, file edits and common filesystem commands |
| Plan | `plan` | Reads and exploration; no source edits until you approve |
| Auto | `auto` | Most actions; a classifier blocks the risky ones |

`dontAsk` (5.9) is not in the `Shift+Tab` cycle; set it with `--permission-mode dontAsk`.

> **Note: changed since the Academy course (Claude Code 101).** Since v2.1.283, interactive sessions **start in auto mode** by default. Pick the mode on purpose: Manual for sensitive work, Plan before big changes.

**Explore → plan → code → commit.** (1) **Explore** in plan mode: "read `src/auth` and explain how login works". (2) **Plan**: "I want to add Google OAuth. Which files change?" (3) **Code**: approve the plan, then "implement it, write tests, run the suite and fix failures". (4) **Commit**: "commit and open a PR". Skip steps 1 and 2 when you could describe the diff in one sentence.

**Streaming mode.** `--output-format json` prints one object at the end. **`--output-format stream-json`** prints newline-delimited JSON events while the run is in progress. It normally starts with a `system`/`init` event, and the **last line is the `result` message**.

```bash
claude -p "Explain recursion" \
  --output-format stream-json --verbose --include-partial-messages \
  | jq -rj 'select(.type == "stream_event"
      and .event.delta.type? == "text_delta") | .event.delta.text'
```

**Claude Code and Computer Use.** Claude Code automates development tasks. Computer Use automates graphical user interfaces, in two different forms:

- **The Computer Use API tool: you build and host the app.** Add `{"type": "computer_toolset_20260801"}` to a Messages API request. Claude replies with actions such as `screenshot` and `left_click`, and **your** app runs them on a virtual display ([Chapter 2](../02-tool-use/README.md#anthropic-schema-client-tools-in-brief)). It is generally available on the Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud and Microsoft Foundry (Claude 5.5 or later models; no beta header). Start from the [`computer-use-demo`](https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-demo) container, and run it in a sandbox with minimal privileges, a domain allowlist and human confirmation for real consequences.
- **Computer use inside Claude Code: Claude drives your own desktop.** It is a **research preview** for **Pro, Max and Ultra** plans (not Team or Enterprise): **macOS only** in the CLI, macOS or Windows in the Desktop app. It needs a claude.ai login and an **interactive** session: it is **not available with `-p`**, so it cannot run in CI.

| Need | Choose |
|---|---|
| Automated code changes, PR reviews or test fixes in CI | Claude Code headless (`claude -p`; 5.9) |
| Unattended GUI automation of a legacy app with no API | Your own app on the Computer Use API toolset, in a sandbox |
| The target system has an API, CLI or MCP server | A normal tool or MCP server: faster and cheaper than reading pixels |

## Lesson code

Video-lesson code: [../../presentations/05-claude-code-and-codex/code/acme-shop/](../../presentations/05-claude-code-and-codex/code/acme-shop/). Its tests run with pytest, which the course venv does not include, so run `pip install pytest` first.

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Work through 5.1–5.12 in a sandbox repo, then build a CI review bot with `--json-schema` (live `claude -p` cells are off by default) |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: 12-question quiz, 7 auto-checked exercises and an architecture scenario |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Instruction every teammate must get | Project `CLAUDE.md` / `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Conventions for a file *type* spread across dirs | `.claude/rules/` + `paths:` glob | CLAUDE.md in every dir |
| Guidance needed only for a *task* | Skill | CLAUDE.md / rules |
| Must **never** happen | Permission deny / `PreToolUse` hook | CLAUDE.md "never do X" |
| Big, ambiguous or architectural change | Plan mode → approve → execute | Direct execution |
| Claude Code in a pipeline | `claude -p` (+ `--bare` for reproducibility) | Interactive `claude` |
| Machine-readable CI output | `--output-format json --json-schema` | Format instructions in prompt |
| Unattended GUI automation of an app with no API | Computer Use API toolset in a sandbox | Claude Code computer use |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **Team rules in the user file.** Everything works on your laptop and fails for the next hire.
- **Treating `@imports` as a token saver.** Imports load at launch. Use path-scoped rules or skills for conditional loading.
- **Assuming `allowed-tools` sandboxes a skill.** It pre-approves. Use `disallowed-tools`, a read-only fork or deny rules.
- **Relying on `/compact` to hold exact values.** Numbers, IDs and error strings get paraphrased. Save them to a file first.
- **Running `claude` without `-p` in CI**, or letting the generating session review its own code.

## Self-check

**Q1.** On laptops, Claude Code follows "amounts always use the `Money` type", a line in the committed root `CLAUDE.md`. The nightly CI job ignores it. The job checks out the repo and runs `claude -p --bare "..."` from the repo root. What is the most likely cause?

- A) The line lives in `CLAUDE.local.md`, which is gitignored and never reaches CI
- B) `--bare` skips CLAUDE.md discovery, so the job must pass the file with `--append-system-prompt-file CLAUDE.md`
- C) A `claudeMdExcludes` setting in the repo hides the root CLAUDE.md on runners
- D) The root CLAUDE.md loads lazily, only after Claude opens a file in the root directory

<details><summary>Answer</summary>

**B.** Bare mode never reads CLAUDE.md, hooks or MCP config, so anything the job needs must be passed explicitly. A contradicts the question: the line is in the committed root file. C would hide the file on laptops too, because it is a repo setting. D is wrong because files in the working directory and above it load at launch; only subdirectory files load lazily.
</details>

**Q2.** Your team writes a 30-step checklist for shipping a hotfix (branch from the release tag, changelog entry, backport). It matters only during a hotfix, about twice a month, and Claude must never start a hotfix on its own. Where should the checklist live?

- A) An unscoped `.claude/rules/hotfix.md`
- B) A rule with `paths: "CHANGELOG.md"`, so it loads when the changelog is touched
- C) A project skill, `.claude/skills/hotfix/SKILL.md`, with `disable-model-invocation: true`
- D) A section in the project CLAUDE.md titled "Only for hotfixes"

<details><summary>Answer</summary>

**C.** A skill loads only when invoked, and `disable-model-invocation: true` means only a person can start it. A and D load in every session and leave it to Claude to judge when the text applies. B ties a task to a file: it fires on every changelog edit and stays silent until the changelog is opened, which is late in a hotfix.
</details>

**Q3.** Users report that the order-history page is slow. Nobody has profiled it yet. The fix could be a database index, a cache in front of the query or a read replica, and each one touches different services and runbooks. You are new to this codebase. How do you start in Claude Code?

- A) Direct execution: "add Redis caching to the order-history endpoint"
- B) Plan mode: have Claude trace the query path, compare the options and their impact, and approve a plan before any edit
- C) Direct execution in Manual mode, approving each edit as it appears
- D) Ask Claude to implement all three options in one session and keep the fastest

<details><summary>Answer</summary>

**B.** The cause is unknown, several designs are valid and the code is unfamiliar, which is the plan-mode case. A commits to one design before the cause is known. C approves edits one at a time, but nobody has agreed on a design: Manual mode controls approvals, not planning. D turns an architecture decision into three overlapping changes in one context.
</details>

**Q4.** A CI step runs `claude -p "Return the findings as JSON" --output-format json` and calls `json.loads()` on the `result` field. Most nights it works. On some nights the parse fails, because Claude wrapped the JSON in a sentence or a code fence. What is the most reliable fix?

- A) Add "reply with raw JSON only, no prose" to the prompt and to CLAUDE.md
- B) Pass `--json-schema '<schema>'` and read the validated object from `structured_output` instead of `result`
- C) Strip code fences with a regex before calling `json.loads()`
- D) Switch to `--output-format stream-json` and parse the last line

<details><summary>Answer</summary>

**B.** With `--json-schema`, the CLI validates the output against your schema and returns it as data in `structured_output`. A is an instruction the model can still drift from. C patches one symptom, and the next failure will look different. D changes how events arrive, but the last line is the same `result` message with the same free text.
</details>

## Official documentation

- [Claude Code overview](https://code.claude.com/docs/en/overview)
- [Memory: CLAUDE.md, imports, `.claude/rules/`, auto memory, `/memory`](https://code.claude.com/docs/en/memory)
- [Skills (custom commands merged into skills)](https://code.claude.com/docs/en/skills)
- [Permission modes, including plan mode](https://code.claude.com/docs/en/permission-modes)
- [Run Claude Code programmatically (headless / `-p`)](https://code.claude.com/docs/en/headless)

[← Chapter 4 — Model Context Protocol](../04-model-context-protocol/README.md) | [↑ Claude path overview](../README.md) | [Chapter 6 — Prompt Engineering →](../06-prompt-engineering/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
