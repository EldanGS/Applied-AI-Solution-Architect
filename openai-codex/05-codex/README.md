# Chapter 5 — Codex: Configuration, Sandboxing and CI

> Claude counterpart: [Chapter 5 — Claude Code: Configuration and Workflows](../../anthropic-claude/05-claude-code/README.md) · Academy course(s): Get Started with Codex (primary); Extend Codex Workflows and Scale Codex Across Governed Teams and Systems as Supporting, with depth in planned chapters 19–20 · Est. time: 7–8 hours (reading 2.5 h, notebooks 4.5–5.5 h) · Status: [ ] not started

Codex is OpenAI's coding agent: a CLI, an IDE extension, a cloud task runner, a pull-request reviewer, and the harness behind the Agents API from [Chapter 3](../03-agents-sdk-and-agents-api/README.md). As the architect, you decide where team knowledge and guardrails live (`AGENTS.md`, `config.toml`, skills, sandbox, approvals, rules, hooks) and how the agent runs unattended in CI. The core skill is the pair that Claude Code does not split: the OS-enforced **sandbox** and the separate **approval policy**.

## What you'll learn

- Pick the right Codex surface, and predict which `AGENTS.md` files load for a working directory
- Layer `config.toml` correctly: precedence, profile files, project trust
- Choose a `sandbox_mode` and an `approval_policy` for local work and for CI
- Place workflows in skills, and enforcement in rules, hooks and `requirements.toml`
- Run Codex in CI with `codex exec` and `openai/codex-action@v1` without leaking the key
- Scope a task, set "done when" criteria, steer it, and hand a reviewer the evidence

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md) (Python env, `.env` with `OPENAI_API_KEY`, git) and [Chapter 4 — Built-in tools and MCP](../04-built-in-tools-and-mcp/README.md) (MCP transports, tool approvals). The Codex CLI installed and signed in (`codex --version` works; see [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)). Optional: [Claude Chapter 5 — Claude Code](../../anthropic-claude/05-claude-code/README.md), since this chapter is written as a delta from it.

## Concepts

### 5.1 The Codex surfaces

"Codex" is one agent harness behind several surfaces. The CLI, IDE extension and desktop app **share** `~/.codex/config.toml` and MCP setup. Codex Cloud is configured through its published cloud environment (repos, setup, network, secrets).

| Surface | Where it runs | Typical use |
|---|---|---|
| **Codex CLI**, **IDE extension**, **desktop app** | Your machine, inside the OS sandbox | Interactive coding, focused edits, parallel chats |
| **Codex Cloud** | OpenAI-managed containers, one workspace per task | Long or parallel tasks in a published cloud environment |
| **Code review** (`@codex review`, `/review`, `codex review`) | GitHub or local | A second review pass; on GitHub it flags only P0 and P1 issues |
| **`codex exec`** | CI runners, scripts | Headless runs; final message on stdout |
| **`openai/codex-action@v1`** | GitHub Actions runner | PR review, autofix, release prep |
| **Codex SDK** (`openai-codex`, `@openai/codex-sdk`) | Your service or CI | Embedding the agent in your own tools |

### 5.2 `AGENTS.md`: discovery, hierarchy and override

`AGENTS.md` is the Codex counterpart of `CLAUDE.md`. Codex builds the instruction chain once per run, so there is no cache to clear.

1. **Global.** In `~/.codex` (or `$CODEX_HOME`), `AGENTS.override.md` if it exists, otherwise `AGENTS.md`.
2. **Project.** From the project root (normally the Git root) down to the working directory, each directory adds **at most one file**: `AGENTS.override.md`, else `AGENTS.md`, else a name in `project_doc_fallback_filenames`.
3. **Merge.** Files are concatenated root → cwd, so closer files override earlier guidance.

Codex stops adding files once the combined size reaches `project_doc_max_bytes` (**32 KiB** by default). In the current source, the file that crosses the limit is truncated, and the global file does not count toward the budget. Directories *below* the working directory are never read, and in a project marked `trust_level = "untrusted"` only the global file loads. There are **no `@path` imports** and no lazy loading, so keep files short. **Code review rules:** For GitHub code review, add a `## Code Review Rules` section to the `AGENTS.md` closest to the code. `/init` generates a starter `AGENTS.md`.

> **Exam trap:** "We added `services/payments/AGENTS.md`, but Codex uses a different rule set there." Look for an `AGENTS.override.md` in that directory or in `~/.codex`. "Clear the AGENTS.md cache" describes a cache that does not exist.

### 5.3 `config.toml`: layers, precedence, profiles and trust

Precedence, highest first:

1. CLI flags and `-c key=value` (e.g. `-c sandbox_workspace_write.network_access=true`)
2. Project `.codex/config.toml`, root → cwd, closest wins (**trusted projects only**)
3. Profile file `~/.codex/<name>.config.toml`, selected with `--profile <name>`
4. User config `~/.codex/config.toml`
5. Cloud-managed defaults, then system `/etc/codex/config.toml`, then built-ins

```toml
# ~/.codex/config.toml
model = "gpt-6.1-sol"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[projects."/Users/me/work/legacy-app"]
trust_level = "untrusted"     # skip .codex/ layers and project AGENTS.md; commands ask unless a rule allows them
```

**Profiles are separate files.** Since Codex 0.134.0, `--profile ci` overlays `~/.codex/ci.config.toml` (top-level keys such as `approval_policy = "never"`, `sandbox_mode = "read-only"`). The legacy forms are **rejected with a startup error**: a `profile = "..."` selector always, and a `[profiles.ci]` table as soon as you pass `--profile ci`.

**Project trust.** Project `.codex/` layers (config, hooks, rules) load only in trusted projects. Even then, a project config cannot set `openai_base_url`, `model_provider`, `notify`, `profile`, `otel` and a few others, so a malicious repo cannot redirect your credentials. Organizations **enforce** limits with `requirements.toml` (for example, disallow `approval_policy = "never"`). `/status` and `/debug-config` show what is in effect.

### 5.4 Sandbox modes and approval policies

Codex has **two separate controls**. The **sandbox mode** sets what spawned commands can technically do; the OS enforces it (Seatbelt on macOS, bubblewrap on Linux and WSL2, a native sandbox on Windows) for every command. The **approval policy** sets when Codex must stop and ask before crossing that boundary.

| `sandbox_mode` | Files | Network | Use |
|---|---|---|---|
| `read-only` | Read only | Off | Planning, review, the `codex exec` default |
| `workspace-write` | Write in cwd, temp dirs and `writable_roots` | **Off by default** | Normal local work ("Auto" preset) |
| `danger-full-access` | No restrictions | On | Only in an already-isolated VM or container |

- **Approval policies.** `on-request` asks before going beyond the sandbox. `never` never prompts; requests fail back to the model, and it grants **no** extra access. `granular` keeps some prompt types interactive and auto-rejects others. `untrusted` is **retired** (it can stop Codex from starting) and `on-failure` is deprecated. To migrate, use `read-only` + `on-request`, or mark the project `trust_level = "untrusted"`, which makes every command ask unless a rule allows it.
- **Presets.** Auto is `--sandbox workspace-write --ask-for-approval on-request`. `--yolo` removes both controls. `codex exec` is read-only and runs with `approval_policy = "never"` (unless you opt into automatic review with `--approve-for-me`), so in CI you choose only the sandbox. **Permission profiles** (`default_permissions = ":read-only"` or `":workspace"`) are the newer replacement for `sandbox_mode` + `[sandbox_workspace_write]`; the old keys still work, but don't mix the two.
- **Protected paths and network.** In `workspace-write`, `.git`, `.agents` and `.codex` stay read-only, so `git commit` may need approval. Prefer `--add-dir` or `writable_roots` over full access. If you turn network on, you can also enable the opt-in `network_proxy` feature (off by default) to enforce domain allow/deny rules for commands (`deny` wins).
- **Rules** (experimental). `.rules` files in `~/.codex/rules/` or `<repo>/.codex/rules/` hold `prefix_rule(pattern=[...], decision="allow" | "prompt" | "forbidden")`; the most restrictive match wins. Test one with `codex execpolicy check --pretty --rules ~/.codex/rules/default.rules -- gh pr view 7888`.
- **Secrets.** `[shell_environment_policy]` controls which env vars reach commands; filtering of `KEY`/`SECRET`/`TOKEN` names is **off** by default.

> **Exam trap:** "A package install fails with a network error in `workspace-write`." Make a **scoped** change: approve the escalation, enable `network_access` for that project (ideally with `network_proxy` rules), or pre-install dependencies. `danger-full-access` for the team is the anti-pattern.

### 5.5 The interactive loop and slash commands

The TUI commands to know: `/init` (starter `AGENTS.md`), `/permissions` (switch preset, e.g. Auto ↔ Read Only), `/status` and `/debug-config`, `/plan` (plan mode), `/review` (review the working tree), `/diff` (Git diff including untracked files), `/compact`, `/resume` and `/fork`, `/skills`, `/mcp`, `/hooks`, and `/import` (bring in a Claude Code or Cursor setup). From the shell, `codex review --uncommitted | --base <branch> | --commit <sha>` runs the same review. Compaction is lossy, so save exact errors and IDs to a file first.

### 5.6 Skills (and why custom prompts are deprecated)

A skill is a **directory** with a `SKILL.md` (required `name` and `description`) plus optional `scripts/`, `references/`, `assets/` and `agents/openai.yaml`, following the open [agent skills standard](https://agentskills.io).

```markdown
---
name: pr-review
description: Review a diff for correctness, security and missing tests.
  Use when the user asks for a PR or diff review.
---
1. Run `git diff --stat` against the base branch and read the changed files.
2. Check each change against the "Code Review Rules" in AGENTS.md.
3. Report findings as: file, line, severity, issue, fix.
```

Codex first sees only each skill's name, description and path (about **2% of the context window**) and reads the full `SKILL.md` only when it uses it. Invoke a skill with `/skills` or `$pr-review`, or implicitly when the task matches the description. For skills with side effects, set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Repo skills live in **`.agents/skills/`** (any directory from cwd up to the repo root; not `.codex/skills/` or `.claude/skills/`) and travel with git. User skills live in `$HOME/.agents/skills/`, admin skills in `/etc/codex/skills/`. **Custom prompts are deprecated.** They lived in `~/.codex/prompts/`, ran only as `/prompts:<name>` and were not shared. Migrate each one to `.agents/skills/<name>/SKILL.md`.

### 5.7 Hooks, subagents and plugins (concept level)

**Hooks** run your scripts at lifecycle events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `Stop`, and more), configured in `hooks.json` or `[hooks]` tables next to any config layer. Each hook gets one JSON object on stdin. A `PreToolUse` hook blocks a call with `"permissionDecision": "deny"`, `{"decision": "block"}`, or exit code `2`. An unsupported output marks the hook failed and **the call continues**, so test the deny path. Non-managed hooks must be **trusted** in `/hooks`, by hash.

**Subagents** run in parallel and return summaries, keeping noisy exploration out of the main thread. Built-ins: `default`, `worker`, `explorer`. Custom agents are TOML files in `~/.codex/agents/` or `.codex/agents/`:

```toml
# .codex/agents/reviewer.toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
developer_instructions = """
Lead with concrete findings and reproduction steps. Do not make code changes.
"""
```

A custom agent can change the model, instructions and features, but **not** `sandbox_mode` or `approval_policy`: subagents inherit the parent session's sandbox and approvals. Use subagents mainly for read-heavy work: they cost more tokens, and parallel writers conflict. **Plugins** bundle skills, MCP servers and optional hooks into one package (`/plugins`, `codex plugin add`).

> **Exam trap:** "Block any `rm -rf`, for every developer." `AGENTS.md` is guidance. Enforce with a rule (`decision = "forbidden"`), a `PreToolUse` hook, or admin `requirements.toml`, plus the sandbox.

### 5.8 MCP in Codex

Codex is an MCP **client**. Add servers with `codex mcp add context7 -- npx -y @upstash/context7-mcp` (stdio), `codex mcp add docs --url https://developers.openai.com/mcp` (HTTP), or in `config.toml`:

```toml
[mcp_servers.figma]             # streamable HTTP
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
enabled_tools = ["get_file", "get_node"]
default_tools_approval_mode = "prompt"   # auto | prompt | writes | approve
required = true                 # codex exec fails if it can't start
```

In CI, a server that silently fails to start gives a run that "worked" with fewer tools, so set `required = true` on servers the pipeline needs. `codex mcp-server` (Codex **as** an MCP server) has been **removed**; use the app server or the Codex SDK.

### 5.9 `codex exec`: Codex in CI and scripts

`codex exec "<task>"` runs without the TUI. Progress goes to stderr; only the **final agent message** goes to stdout. It is **read-only by default**; add `--sandbox workspace-write` to allow edits (`--full-auto` was removed; the CLI rejects it). `--json` turns stdout into **JSONL events**, `--output-schema <file>` makes the final message match a JSON Schema, `-o <file>` saves it, `--ephemeral` skips session files, and `codex exec resume --last` continues a previous run. Events: `thread.started`, `turn.started`, `item.started` / `item.updated` / `item.completed`, `turn.completed` (with `usage`), `turn.failed`, `error`. Item types include `agent_message`, `command_execution`, `file_change` and `mcp_tool_call`; ignore types you don't know.

```python
import json, os, subprocess
def codex_exec_json(prompt: str, schema_path: str) -> dict:
    argv = ["codex", "exec", "--json", "--ephemeral", "--sandbox",
            "read-only", "--output-schema", schema_path, prompt]
    # Key from a step-scoped secret env var; only Codex gets it (as CODEX_API_KEY).
    env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
    env["CODEX_API_KEY"] = os.environ["OPENAI_API_KEY"]
    proc = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=900)
    if proc.returncode != 0:
        raise RuntimeError(f"exit {proc.returncode}: {proc.stderr[-500:]}")
    final, completed = None, False
    for line in proc.stdout.splitlines():
        if not line.strip().startswith("{"):
            continue  # skip blank and non-JSON lines
        event = json.loads(line)
        kind, item = event["type"], event.get("item", {})
        if kind == "item.completed" and item.get("type") == "agent_message":
            final = item["text"]
        elif kind == "turn.completed":
            completed = True
        elif kind in ("turn.failed", "error"):
            raise RuntimeError(event)
    if not completed or final is None:
        raise RuntimeError("codex exec ended without a completed turn")
    return json.loads(final)  # the final message is a JSON string
```

Accept a run only on exit 0, a `turn.completed` event and no `turn.failed` or top-level `error`. A `file_change` item can be `"completed"` or `"failed"`, so check its status. Set **`CODEX_API_KEY` inline for the Codex call only**, never as a job-level env var in a job that runs repo code. For machine-readable findings, use `--output-schema`, not "JSON only" in the prompt.

### 5.10 GitHub: `openai/codex-action@v1` and `@codex review`

1. **Managed code review.** Connect the repo, then comment `@codex review` or turn on automatic reviews. It follows `## Code Review Rules` in `AGENTS.md`, focuses on P0/P1 issues, and needs no workflow file.
2. **`openai/codex-action@v1`.** Installs the CLI, starts a Responses API proxy for your key, and runs `codex exec`. Key inputs: `openai-api-key`, `prompt-file`, `permission-profile` (`:read-only` or `:workspace`; the older `sandbox` input is legacy, and leaving both empty falls back to workspace-write), `output-schema-file`, `safety-strategy` (default `drop-sudo`), `allow-users`. The output `final-message` carries the result.

```yaml
jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read        # the job that holds the key cannot push
    outputs:
      final_message: ${{ steps.codex.outputs.final-message }}
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0    # full history, so there is a base to diff
          persist-credentials: false
      - id: codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt-file: .github/codex/prompts/review.md
          permission-profile: ":read-only"
          output-schema-file: .github/codex/review.schema.json
  comment:
    needs: review
    if: needs.review.outputs.final_message != ''
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write  # can write, but never sees the API key
    steps:
      - uses: actions/github-script@v7
        env:
          CODEX_FINAL_MESSAGE: ${{ needs.review.outputs.final_message }}
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner, repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body: process.env.CODEX_FINAL_MESSAGE,
            });
```

The `comment` job posts `final_message` to the PR as one comment (inline comments would use `pulls.createReview`). Autofix uses the same split: the Codex job uploads a `codex.patch` artifact, and a separate `contents: write` job opens the PR without the key. Also limit who can trigger the workflow, sanitize PR text before it reaches the prompt (prompt injection), and never use `safety-strategy: unsafe` on shared runners.

### 5.11 The Codex SDK (Python)

To drive Codex from your own program, use **`openai-codex`** (`pip install openai-codex`, Python 3.10+). It drives a local Codex **app server** over JSON-RPC and pins a matching CLI runtime.

```python
from openai_codex import Codex, Sandbox
with Codex() as codex:
    thread = codex.thread_start(model="gpt-6.1-sol",
                                sandbox=Sandbox.workspace_write)
    result = thread.run("Make a plan to diagnose and fix the CI failures")
    print(result.final_response)
    # Same thread, narrower sandbox for this and later turns:
    review = thread.run("Review the diff only.", sandbox=Sandbox.read_only)
    print(thread.id)  # resume later with codex.thread_resume(thread.id)
```

`thread.run()` returns a `TurnResult` with `final_response`, `items` and `usage`, and accepts `output_schema=`. The **Codex SDK** runs the harness locally; the **Agents API** ([Chapter 3](../03-agents-sdk-and-agents-api/README.md)) runs it managed by OpenAI. PyPI `openai-codex-sdk` is **not** the official package.

### 5.12 Scoping, completion criteria and reviewer evidence

This is how you *work with* Codex on a real task, as taught in **Get Started with Codex** and Codex Bootcamp 101 (from the official [Best practices](https://learn.chatgpt.com/guides/best-practices) and [Long-running work](https://learn.chatgpt.com/docs/long-running-work) pages).

**Setup and first session.** Install the CLI (`npm install -g @openai/codex`, `brew install --cask codex`, or the standalone installer) and the IDE extension. Sign in with **ChatGPT** (plan access) or an **API key** (usage-based); **Codex Cloud requires ChatGPT sign-in.** Ask "Tell me about this project", run `/init`, and make a **Git checkpoint before and after each task**.

**Where Codex helps in everyday work.**

| Everyday task | Context you supply | How you verify |
|---|---|---|
| Explore a codebase (IDE, or CLI with `@file`) | The flow you care about | Numbered request flow plus file list; spot-check |
| Fix a bug (CLI at repo root) | **Repro steps**, suspect files, constraints | Re-run the repro, lint, smallest relevant tests |
| Write a test | The function; "follow existing test conventions" | Fails before the fix, passes after |
| Build a feature (`/plan` first) | Goal, constraints, a screenshot for UI | Dev server or tests; you review the diff |
| Long refactor (plan locally, run in Codex Cloud) | A committed plan, clean tree | Review the cloud diff and tests before a PR |

**1. Scope the task.** One coherent unit of work per chat: one bug, one feature slice, one refactor step. If the task is ambiguous, plan first with `/plan`.

**2. Give the right repository context.** Write four parts: **Goal**, **Context** (files, error output, `@path` mentions), **Constraints** ("don't touch" boundaries) and **Done when**. Context you repeat, including build and test commands, belongs in `AGENTS.md` (5.2); external data in MCP (5.8).

**3. Define completion criteria.** "Done when" makes Codex stop when the work *is* finished, not when it *looks* finished. `/goal <objective>` sets a persistent goal that is both the prompt and the completion check (up to 4,000 characters; `/goal edit`, `pause`, `resume`, `clear`). Name an outcome, constraints and verification. A goal does not widen the sandbox.

**4. Steer while it works.** Press **Enter** to correct the *current* turn, **Tab** to queue a follow-up for *after* it, and **Esc Esc** to edit your last message and fork. If you revert or hand-edit Codex's work, tell it, or it may overwrite your edit.

**5. Review changes before they are applied.** Git is the gate. Use plan mode or a read-only preset for a proposal first; after edits, use `/diff` and `/review`. Give parallel chats separate Git worktrees.

**6. Verify, then produce the evidence a reviewer needs.** Have Codex run tests and lint, then add an independent pass (`/review`, a review subagent run from a read-only session, or `@codex review`). The reviewer should not need to re-run your session:

| Evidence | Where it comes from |
|---|---|
| The task and its "done when" criteria | Your prompt or `/goal` |
| Files changed plus a short rationale | Codex's final message; `/diff` |
| Commands run, with exit codes | Transcript; in CI, `command_execution` items (5.9) |
| Tests and results (fail before, pass after); repro re-run | Test output; Codex's verification step |
| What was **not** verified, risks, follow-ups | Ask: "List anything you could not verify." |

> **Exam trap:** "Codex says done, but the bug still reproduces." Fix it upstream with a verifiable "done when" plus the evidence package. "Be more careful" or "use a bigger model" gives no pass/fail signal.

### 5.13 Iterative refinement with Codex

These techniques mirror [Claude Chapter 5, 5.11](../../anthropic-claude/05-claude-code/README.md#511-iterative-refinement-with-claude-code) and make 5.12 work in practice.

1. **Examples beat prose.** Give 2–3 input/output examples with an edge case; each becomes a test ([Chapter 6, 6.3](../06-prompt-engineering-and-evals/README.md#63-few-shot-examples)).
2. **Test-driven iteration.** Tests first, then implement until they pass. On failure, send the test name, input, and expected vs. actual value.
3. **The interview pattern.** In an unfamiliar domain, ask Codex in `/plan` to interview you, then turn the answers into a `/goal`.
4. **One message or one at a time?** Send **interacting** issues (a parser and its validator) in one message; fix **independent** ones one at a time.

```text
Rewrite normalize_name() so these hold:
  "  ada LOVELACE "  -> "Ada Lovelace"
  "o'brien"          -> "O'Brien"
  None               -> None        (do not raise)
Done when: tests/test_normalize.py passes, with a case for each line.
```

## Lesson code

Video-lesson code: [../../presentations/05-claude-code-and-codex/code/acme-shop/](../../presentations/05-claude-code-and-codex/code/acme-shop/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | One drill per section 5.1–5.13 in a throwaway temp project, then a mini-project: a CI review gate on `codex exec --json --output-schema` (live calls off by default, `RUN_CODEX = False`) |
| [`02_homework.ipynb`](02_homework.ipynb) | 12 scenario questions, 5 offline exercises (`AGENTS.md`, chain resolution, `config.toml` + CI profile, `codex exec` argv, JSONL summary), a rollout scenario, scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>
## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Rule every teammate must get | Repo `AGENTS.md` | `~/.codex/AGENTS.md` |
| Workflow only for some tasks | Repo skill in `.agents/skills/` | `AGENTS.md` or custom prompts |
| Different settings for CI vs. laptop | `~/.codex/ci.config.toml` + `--profile ci` | `[profiles.ci]` table |
| Normal local work | `workspace-write` + `on-request` | `danger-full-access` |
| Must **never** happen | `prefix_rule(..., decision="forbidden")`, hook, `requirements.toml` | "Never do X" in `AGENTS.md` |
| Codex in CI, report only | `codex exec --sandbox read-only --json --output-schema` | Prose output |
| Autofix in CI | Read-only Codex job → patch artifact → separate write job | One job with key + write perms |
| Codex keeps "finishing" too early | A verifiable "Done when" or `/goal` | "Be more thorough" |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **Team rules in `~/.codex/AGENTS.md`**, or a forgotten `AGENTS.override.md` silently replacing the shared file.
- **`[profiles.ci]` in `config.toml`** or `approval_policy = "untrusted"`: both are legacy and stop Codex at startup.
- **Confusing approvals with the sandbox.** `-a never` removes prompts; it does not grant writes or network.
- **Using `AGENTS.md` as a security control.** Use the sandbox, rules, hooks and `requirements.toml`.
- **Running `codex exec` expecting edits** without `--sandbox workspace-write`, or setting the API key job-wide.
- **No "done when" and no evidence:** Codex can't see whether its work is right, and the reviewer can't check it.

## Self-check

**Q1.** You start Codex in `repo/services/payments/`. That directory has both `AGENTS.md` and `AGENTS.override.md`; the repo root has `AGENTS.md`; `~/.codex/` has `AGENTS.md`. Which files are in the instruction chain, in order?

- A) Only `services/payments/AGENTS.override.md`, because overrides replace everything above them
- B) `~/.codex/AGENTS.md`, `repo/AGENTS.md`, `services/payments/AGENTS.override.md`
- C) `~/.codex/AGENTS.md`, `repo/AGENTS.md`, `services/payments/AGENTS.md`, `services/payments/AGENTS.override.md`
- D) `repo/AGENTS.md` only, because global files are ignored inside a Git repo

<details><summary>Answer</summary>

**B.** Codex loads the global file, then walks from the project root down to the working directory, taking at most one file per directory. In `payments/`, the override wins and the plain `AGENTS.md` is ignored. A is wrong: an override only replaces the `AGENTS.md` in its own directory. C is wrong: each directory adds at most one file. D is wrong: the global file is always included.
</details>

**Q2.** A nightly job runs `codex exec "fix all lint errors"`. It exits 0 and prints a plan, but no files change. What is the fix?

- A) Add `--ask-for-approval never`
- B) Add `--sandbox workspace-write`
- C) Add `--full-auto`
- D) Add `--dangerously-bypass-approvals-and-sandbox`

<details><summary>Answer</summary>

**B.** `codex exec` runs in a read-only sandbox by default. `--sandbox workspace-write` allows edits inside the workspace and keeps everything else sandboxed. A fails: `codex exec` has no approval flag (it already runs with approvals set to `never`), and approvals never grant write access anyway. C was removed from the CLI and now fails with an unrecognized-argument error. D removes the sandbox entirely, which is only acceptable on an externally isolated runner.
</details>

**Q3.** Security asks you to guarantee that Codex never runs `terraform apply` on any developer machine, even if someone writes "go ahead and apply" in a prompt. What is the strongest control?

- A) "Never run terraform apply" in the root `AGENTS.md`
- B) A `prefix_rule(pattern=["terraform", "apply"], decision="forbidden")`, enforced for everyone through admin `requirements.toml`
- C) A repo skill that explains the safe Terraform workflow
- D) Setting `approval_policy = "never"` so Codex cannot ask to run it

<details><summary>Answer</summary>

**B.** Rules are enforcement, and admin-enforced requirements apply to every user. A and C are guidance the model can be talked out of. D removes prompts but does not forbid anything; a command that the sandbox allows would still run.
</details>

**Q4.** You ask Codex to "fix the settings page bug". It edits two files and reports success. The reviewer can still reproduce the bug and can't tell what was tested. What should you have changed first?

- A) Switch to a larger model and raise the reasoning effort
- B) Give a repro recipe and the suspect files as context, a "Done when" ("the repro no longer shows the bug and `npm test -- settings` passes"), and ask for the commands run, their results and anything not verified
- C) Add "be careful and test everything" to the root `AGENTS.md`
- D) Run the task with `--yolo` so Codex can test without approval prompts

<details><summary>Answer</summary>

**B.** Scoping, context and verifiable completion criteria give Codex a pass/fail signal. The evidence request gives the reviewer something to check. A changes capacity, not the target. C is vague guidance with no check. D removes safety controls and doesn't define "done".
</details>

## Official documentation

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Sandbox](https://learn.chatgpt.com/docs/sandboxing)
- [Non-interactive mode (`codex exec`)](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action)

[← Chapter 4 — Built-in tools and MCP](../04-built-in-tools-and-mcp/README.md) | [↑ OpenAI path](../README.md) | [Chapter 6 — Prompt engineering and evals →](../06-prompt-engineering-and-evals/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
