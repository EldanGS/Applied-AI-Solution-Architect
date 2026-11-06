# Chapter 5 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

There is no OpenAI architect exam (see the [OpenAI path README](../../README.md#certification-status-read-this-first)). This table maps the chapter to the Academy **Get Started with Codex** course (part of the Codex pathway), the Codex Bootcamp, and role competencies in this repo's requirement lists. Items marked **[INFERRED]** come from a related bootcamp session or resource, not from the course page itself. Rows marked Supporting are planned in depth in a later chapter (Codex for teams, Codex automation at scale).

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/codex/get-started-with-codex/1` | Use Codex for well-scoped engineering work in a real repository | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) (scope, context, done-when, review, evidence); practice 5.12; [Self-check](../README.md#self-check) Q4 | Primary |
| `OAI/codex/get-started-with-codex/2` | Where Codex helps in a real development workflow | [5.1](../README.md#51-the-codex-surfaces) (surfaces); [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) "Where Codex helps" table; practice 5.1 | Primary |
| `OAI/codex/get-started-with-codex/3` | Scope coding and repository tasks | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 1 (one coherent unit, plan first); practice 5.12 brief linter | Primary |
| `OAI/codex/get-started-with-codex/4` | Give Codex the right repository context | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 2 (Goal / Context / Constraints / Done when); [5.2](../README.md#52-agentsmd-discovery-hierarchy-and-override) `AGENTS.md`; [5.8](../README.md#58-mcp-in-codex) MCP; practice 5.2, 5.12 | Primary |
| `OAI/codex/get-started-with-codex/5` | Define completion criteria so Codex stays on task | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 3 ("Done when", `/goal`); [5.13](../README.md#513-iterative-refinement-with-codex) (tests as the check); practice 5.12; homework Q11 | Primary |
| `OAI/codex/get-started-with-codex/6` | Verify code changes | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 6; [5.13](../README.md#513-iterative-refinement-with-codex) test-driven iteration; [5.9](../README.md#59-codex-exec-codex-in-ci-and-scripts) run acceptance rules; practice 5.9, 5.12, 5.13 | Primary |
| `OAI/codex/get-started-with-codex/7` | Produce the evidence a reviewer needs | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 6 evidence table; practice 5.12 `evidence_pack`; [Self-check](../README.md#self-check) Q4 | Primary |
| `OAI/codex/get-started-with-codex/8` | Everyday tasks: explore a codebase, fix bugs, build features | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) everyday-task table; practice 5.12 | Primary |
| `OAI/codex/get-started-with-codex/14` **[INFERRED]** | Steer Codex while the work is in progress | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 4 (Enter steers, Tab queues, Esc Esc) and step 3 (`/goal edit`, `/goal pause`); practice 5.12 steering drill; [More self-check questions](#more-self-check-questions) 6 | Primary |
| `OAI/codex/get-started-with-codex/15` **[INFERRED]** | Review changes before they are applied | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 5 (plan or read-only first, `/diff`, `/review`, worktrees) and setup (Git checkpoints); [5.4](../README.md#54-sandbox-modes-and-approval-policies); [5.5](../README.md#55-the-interactive-loop-and-slash-commands) | Primary |
| `OAI/codex/get-started-with-codex/16` **[INFERRED]** | Install and set up the Codex CLI and IDE extension; configure the workflow | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) setup and first session; [Prerequisites](../README.md#prerequisites); [5.3](../README.md#53-configtoml-layers-precedence-profiles-and-trust) (`config.toml`); practice 5.3 | Primary |
| `OAI/codex/get-started-with-codex/17` **[INFERRED]** | Write `AGENTS.md` guidance and use Codex prompting patterns | [5.2](../README.md#52-agentsmd-discovery-hierarchy-and-override); [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 2; [5.13](../README.md#513-iterative-refinement-with-codex); homework Ex 1, Q12 | Primary |
| `OAI/codex/get-started-with-codex/18` **[INFERRED]** | Codex surfaces and sign-in with a ChatGPT plan | [5.1](../README.md#51-the-codex-surfaces) (surfaces); [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) setup (ChatGPT vs API-key sign-in; Codex Cloud needs ChatGPT) | Primary |
| `OAI/bootcamp/codex/1` | 101: scope tasks | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 1 | Primary |
| `OAI/bootcamp/codex/2` | 101: provide effective context | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 2; [5.2](../README.md#52-agentsmd-discovery-hierarchy-and-override) | Primary |
| `OAI/bootcamp/codex/3` | 101: steer work as it progresses | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 4; [More self-check questions](#more-self-check-questions) 6 | Primary |
| `OAI/bootcamp/codex/4` | 101: review real code changes before they are applied | [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence) step 5; [5.5](../README.md#55-the-interactive-loop-and-slash-commands) (`/diff`, `/review`) | Primary |
| `OAI/bootcamp/codex/5` | 101: set up Codex, navigate repositories, core concepts, prompting patterns | [5.1](../README.md#51-the-codex-surfaces)–[5.5](../README.md#55-the-interactive-loop-and-slash-commands); [5.12](../README.md#512-scoping-completion-criteria-and-reviewer-evidence); [5.13](../README.md#513-iterative-refinement-with-codex) | Primary |
| `OAI/bootcamp/codex/7` | 201: approval and sandboxing defaults | [5.4](../README.md#54-sandbox-modes-and-approval-policies); practice 5.4 | Supporting |
| `OAI/bootcamp/codex/8` | 201: MCP and tool connections | [5.8](../README.md#58-mcp-in-codex); practice 5.8 | Supporting |
| `OAI/bootcamp/codex/9` | 201: reusable skills | [5.6](../README.md#56-skills-and-why-custom-prompts-are-deprecated); practice 5.6 | Supporting |
| `OAI/bootcamp/codex/14` | 301: sub-agents | [5.7](../README.md#57-hooks-subagents-and-plugins-concept-level) (custom agents) | Supporting |
| `OAI/bootcamp/codex/17` | 301: writable roots and execution rules | [5.4](../README.md#54-sandbox-modes-and-approval-policies) (`writable_roots`, protected paths, rules, `execpolicy check`); practice 5.4 | Supporting |
| `OAI/bootcamp/codex/18` | 301: Codex SDK | [5.11](../README.md#511-the-codex-sdk-python) | Supporting |
| `OAI/bootcamp/codex/19` | 301: `codex exec` | [5.9](../README.md#59-codex-exec-codex-in-ci-and-scripts); practice 5.9 and mini-project; homework Ex 4–5 | Supporting |
| `OAI/bootcamp/codex/20` | 301: Codex in CI, security and code-review workflows | [5.10](../README.md#510-github-openaicodex-actionv1-and-codex-review); practice 5.10 | Supporting |
| `ROLE/BUILD/6` | AI coding agents in customer SDLCs (config, permissions, CI) — Codex half | [5.2](../README.md#52-agentsmd-discovery-hierarchy-and-override)–[5.10](../README.md#510-github-openaicodex-actionv1-and-codex-review); Part C scenario in homework | Supporting |
| `ROLE/AGENT/8` | OpenAI agent stack (Codex, plugins, API agents) | [5.1](../README.md#51-the-codex-surfaces), [5.7](../README.md#57-hooks-subagents-and-plugins-concept-level) (plugins), [5.11](../README.md#511-the-codex-sdk-python) (SDK) | Supporting |
| `ROLE/SAFE/10` | Securing agent and tool access | [5.3](../README.md#53-configtoml-layers-precedence-profiles-and-trust) (project trust), [5.4](../README.md#54-sandbox-modes-and-approval-policies) (sandbox, rules, env filtering), [5.10](../README.md#510-github-openaicodex-actionv1-and-codex-review) (key isolation) | Supporting |

## More self-check questions

**Q1.** Your team wants a shared "release notes" workflow that any developer can trigger and that Codex can also use on its own when someone asks for release notes. Where does it go?

- A) `~/.codex/prompts/release-notes.md` on every laptop
- B) A `## Release notes` section in the root `AGENTS.md`
- C) `.agents/skills/release-notes/SKILL.md` in the repo, with a precise `description`
- D) `.codex/skills/release-notes/SKILL.md` in the repo

<details><summary>Answer</summary>

**C.** Repo skills live in `.agents/skills/`, are shared through git, and can be invoked explicitly (`$release-notes`) or implicitly when the description matches. A is a deprecated custom prompt and is not shared. B loads in every session and wastes context. D is the wrong directory, so Codex never finds the skill.
</details>

**Q2.** A developer put `[profiles.ci]` with `sandbox_mode = "read-only"` into `~/.codex/config.toml`. Now `codex exec --profile ci ...` fails at startup with a config error about legacy `[profiles.ci]`. Why?

- A) `--profile` only works in the interactive TUI
- B) Profiles must be set with `profile = "ci"` at the top of `config.toml`
- C) Current Codex reads profiles only from `~/.codex/ci.config.toml`, and it rejects a leftover `[profiles.ci]` table with the same name
- D) A project `.codex/config.toml` sets `sandbox_mode`, which conflicts with the profile

<details><summary>Answer</summary>

**C.** Since Codex 0.134.0, `--profile ci` overlays `~/.codex/ci.config.toml` with top-level keys. A `[profiles.ci]` table (or a `profile = "ci"` selector) is legacy, and Codex refuses to start until you move those settings into `ci.config.toml` and delete the table. A is wrong: `codex exec` accepts `-p/--profile`. B is the other legacy form, which is also rejected. D is wrong: a trusted project config simply sits above the profile in precedence; it is not a startup error.
</details>

**Q3.** You need a structured PR comment listing file, line, severity and fix for each finding from a Codex step in GitHub Actions. What is the most reliable design?

- A) Put "respond only in JSON" in `AGENTS.md` and parse the final message with a regex
- B) Use `openai/codex-action@v1` with `output-schema-file`, read the `final-message` output in a separate job, and post the comment from there
- C) Run `codex exec` in the same job with `OPENAI_API_KEY` as a job-level env var and `pull-requests: write`, then post the comment from a shell step
- D) Turn on `@codex review` and scrape its comment text

<details><summary>Answer</summary>

**B.** The schema makes the output parseable, the action keeps the key behind its proxy, and the job that writes to the PR never holds the key. A is fragile prose formatting. C exposes the key to every step in the job and mixes write permissions with the key, which the docs explicitly warn against. D gives you managed P0/P1 reviews, not a structured payload.
</details>

**Q4.** In `workspace-write`, Codex can edit source files but every `git commit` asks for approval. A teammate proposes switching to `danger-full-access`. What is the better answer?

- A) Agree; `git commit` needs full access
- B) This is expected: `.git` is a protected read-only path inside writable roots. Approve commits when needed or add a narrow rule, and keep the sandbox.
- C) Add `.git` to `writable_roots`
- D) Set `approval_policy = "never"` so the commit runs without asking

<details><summary>Answer</summary>

**B.** `.git`, `.agents` and `.codex` stay read-only even in `workspace-write`, by design. Use approvals or a scoped rule for the commit step instead of removing the whole sandbox. A over-grants. C fights a protection that exists on purpose. D just makes the commit fail back to the model instead of asking.
</details>

**Q5.** A pipeline depends on a docs MCP server for API lookups. Occasionally the server fails to start, and `codex exec` still produces a (worse) result. What should you change?

- A) Raise `tool_timeout_sec`
- B) Set `required = true` on `[mcp_servers.docs]`
- C) Add "always use the docs MCP server" to `AGENTS.md`
- D) Move the server to the project `.codex/config.toml`

<details><summary>Answer</summary>

**B.** With `required = true`, `codex exec` exits with an error when an enabled required server cannot initialize, so the pipeline fails loudly instead of degrading silently. A affects tool calls, not startup. C cannot make an absent server appear. D changes where the config lives, not whether startup failures are fatal.
</details>

**Q6.** Codex is midway through a refactor in the CLI. You notice it is about to edit `legacy/` (which must not change), and you also want it to update the changelog once it's finished. What do you do?

- A) Press Enter with "Don't touch legacy/", then press Tab with "When you're done, update CHANGELOG.md"
- B) Press Tab for both messages, so nothing interrupts the current turn
- C) Press Ctrl+C, then start a new chat with both instructions
- D) Press Enter for both messages; Codex will order them correctly

<details><summary>Answer</summary>

**A.** Enter steers the current turn, which is what an urgent correction needs. Tab queues a follow-up for the next turn. With B, the `legacy/` correction arrives too late. C throws away the session's context. D injects the changelog request into the current turn, so Codex may switch tasks mid-edit.
</details>

## Share your progress

```text
Day N of my AI Solution Architect journey: Codex config is architecture, not dotfiles.

3 takeaways:
1. AGENTS.md: one file per dir, root -> cwd, AGENTS.override.md wins, 32 KiB cap
2. Sandbox (what's possible) and approval policy (when to ask) are two separate knobs
3. CI: codex exec is read-only by default; --sandbox workspace-write, --json, --output-schema, key inline only

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#OpenAI #Codex #AIArchitecture #LearningInPublic
```
