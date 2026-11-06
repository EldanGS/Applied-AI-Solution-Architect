# Chapter 5 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

How this chapter maps to the requirement IDs in the repo's requirements checklist (`K` = knowledge item, `S` = skill item; `ACAD/...` = Anthropic Academy course objectives and lessons). **Primary** means this chapter is the main place the item is taught. **Supporting** means it is covered here in part and completed elsewhere.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| CCAR-F/MQC/2 | Configure Claude Code for team workflows: CLAUDE.md, skills, MCP, plan mode | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.6](../README.md#56-plan-mode-vs-direct-execution); MCP project config is in [Chapter 4](../../04-model-context-protocol/README.md) | Primary |
| CCAR-F/MQC/6 | Claude Code in CI/CD: automated review, test generation, PR feedback | [5.9](../README.md#59-claude-code-in-cicd-headless-mode); mini-project in [`01_practice.ipynb`](../01_practice.ipynb) | Primary |
| CCAR-F/D3/3.1/K1, CCAR-F/D3/3.1/K2 | CLAUDE.md hierarchy (user, project, directory); user-level is not shared via git | [5.1](../README.md#51-the-claudemd-hierarchy) (scope table, loading rules) | Primary |
| CCAR-F/D3/3.1/S1 | Diagnose hierarchy issues (new teammate missing instructions) | [5.1](../README.md#51-the-claudemd-hierarchy) (exam trap); Self-check Q1; [`02_homework.ipynb`](../02_homework.ipynb) Exercise 2 (s1) | Primary |
| CCAR-F/D3/3.1/K3, CCAR-F/D3/3.1/S2 | `@import` for modular CLAUDE.md; per-package imports | [5.2](../README.md#52-path-imports-modular-claudemd); [`02_homework.ipynb`](../02_homework.ipynb) Q2 | Primary |
| CCAR-F/D3/3.1/K4, CCAR-F/D3/3.1/S3 | Split a large CLAUDE.md into `.claude/rules/` topic files | [5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules) (unscoped rules); [5.2](../README.md#52-path-imports-modular-claudemd) exam trap | Primary |
| CCAR-F/D3/3.1/S4 | `/memory` to verify which memory files are loaded | [5.8](../README.md#58-memory-and-auto-memory) (with `/context` for the current session) | Primary |
| CCAR-F/D3/3.2/K1, CCAR-F/D3/3.2/S1 | Project `.claude/commands/` (shared) vs user `~/.claude/commands/` (personal) | [5.4](../README.md#54-custom-slash-commands--skills) (location table, merge into skills) | Primary |
| CCAR-F/D3/3.2/K2 | Skills in `.claude/skills/` with SKILL.md frontmatter (`context: fork`, `allowed-tools`, `argument-hint`) | [5.5](../README.md#55-skills-in-depth-skillmd-frontmatter); [`02_homework.ipynb`](../02_homework.ipynb) Exercise 1 | Primary |
| CCAR-F/D3/3.2/K3, CCAR-F/D3/3.2/S2 | `context: fork` isolates verbose or exploratory skills | [5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) (exam trap); More self-check questions 2 | Primary |
| CCAR-F/D3/3.2/K4 | Personal skill variants in `~/.claude/skills/` that don't affect teammates | [5.4](../README.md#54-custom-slash-commands--skills) (personal shadowing) | Primary |
| CCAR-F/D3/3.2/S3 | `allowed-tools` to restrict tool access during a skill | [5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) (note: pre-approves today; `disallowed-tools` restricts); [`02_homework.ipynb`](../02_homework.ipynb) Q5 | Primary |
| CCAR-F/D3/3.2/S4 | `argument-hint` to prompt for required parameters | [5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) (field table) | Primary |
| CCAR-F/D3/3.2/S5 | Skills (on demand) vs CLAUDE.md (always loaded) | [5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) (decision table, exam trap); Self-check Q2 | Primary |
| CCAR-F/D3/3.3/K1, CCAR-F/D3/3.3/K2, CCAR-F/D3/3.3/S1 | Path-scoped rules: `paths:` globs load only for matching files | [5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules); [`02_homework.ipynb`](../02_homework.ipynb) Q3, Exercise 3 | Primary |
| CCAR-F/D3/3.3/K3, CCAR-F/D3/3.3/S2, CCAR-F/D3/3.3/S3 | Glob rules vs subdirectory CLAUDE.md for conventions spread across the tree | [5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules) (comparison table, exam trap); More self-check questions 1 | Primary |
| CCAR-F/D3/3.4/K1, CCAR-F/D3/3.4/K2, CCAR-F/D3/3.4/K3, CCAR-F/D3/3.4/S1, CCAR-F/D3/3.4/S2 | Plan mode for large, ambiguous or architectural work; direct execution for clear, small changes | [5.6](../README.md#56-plan-mode-vs-direct-execution); Self-check Q3; [`02_homework.ipynb`](../02_homework.ipynb) Q7 | Primary |
| CCAR-F/D3/3.4/K4, CCAR-F/D3/3.4/S3 | Explore subagent to keep verbose discovery out of the main context | [5.6](../README.md#56-plan-mode-vs-direct-execution), [5.7](../README.md#57-compact-and-managing-the-context-window) (exam trap) | Primary |
| CCAR-F/D3/3.4/S4 | Plan mode for investigation, then direct execution for implementation | [5.6](../README.md#56-plan-mode-vs-direct-execution) (plan to investigate, then direct execution of the approved plan); [5.12](../README.md#512-getting-started-and-the-core-loop) (explore → plan → code → commit) | Primary |
| CCAR-F/D3/3.5/K1, CCAR-F/D3/3.5/S1 | 2–3 concrete input/output examples when prose is misread | [5.11](../README.md#511-iterative-refinement-with-claude-code) (technique 1); [`01_practice.ipynb`](../01_practice.ipynb) 5.11 | Primary |
| CCAR-F/D3/3.5/K2, CCAR-F/D3/3.5/S2, CCAR-F/D3/3.5/S4 | Test-driven iteration; specific edge-case test cases (null values in migrations) | [5.11](../README.md#511-iterative-refinement-with-claude-code) (technique 2, exam trap); More self-check questions 5; [`02_homework.ipynb`](../02_homework.ipynb) Q11, Exercise 6 | Primary |
| CCAR-F/D3/3.5/K3, CCAR-F/D3/3.5/S3 | Interview pattern before implementing in an unfamiliar domain | [5.11](../README.md#511-iterative-refinement-with-claude-code) (technique 3); prompt design in [Chapter 6, 6.4](../../06-prompt-engineering/README.md#64-the-interview-pattern) | Primary |
| CCAR-F/D3/3.5/K4, CCAR-F/D3/3.5/S5 | One message for interacting issues vs sequential fixes for independent ones | [5.11](../README.md#511-iterative-refinement-with-claude-code) (technique 4); More self-check questions 6; [`02_homework.ipynb`](../02_homework.ipynb) Exercise 6 | Primary |
| CCAR-F/D3/3.6/K1, CCAR-F/D3/3.6/S1 | `-p` / `--print` so CI doesn't hang on input | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) (exam trap); More self-check questions 3 | Primary |
| CCAR-F/D3/3.6/K2, CCAR-F/D3/3.6/S2 | `--output-format json` + `--json-schema` for inline PR comments | [5.9](../README.md#59-claude-code-in-cicd-headless-mode); Self-check Q4; [`02_homework.ipynb`](../02_homework.ipynb) Exercises 4–5; mini-project in [`01_practice.ipynb`](../01_practice.ipynb) | Primary |
| CCAR-F/D3/3.6/K3, CCAR-F/D3/3.6/S5 | CLAUDE.md as CI context: testing standards, fixtures, review criteria | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) (CI pattern 4, including `--bare`) | Primary |
| CCAR-F/D3/3.6/K4 | Independent reviewer instance instead of the generating session | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) (CI pattern 2) | Primary |
| CCAR-F/D3/3.6/S3 | Pass prior findings on re-review; report only new or unresolved issues | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) (CI pattern 3); re-review step of the mini-project in [`01_practice.ipynb`](../01_practice.ipynb) | Primary |
| CCAR-F/D3/3.6/S4 | Provide existing test files so generated tests don't duplicate coverage | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) (CI pattern 4) | Primary |
| CCAR-F/D1/1.7 | Session management: resume, fork, fresh session with a summary | [5.10](../README.md#510-sessions-resume-name-fork) (CLI side); More self-check questions 4. Taught in [Chapter 3](../../03-agent-sdk/README.md) | Supporting |
| CCAR-F/D4/4.6 | Independent review instance instead of self-review | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) (CI pattern 2). Taught in [Chapter 8](../../08-task-decomposition/README.md) | Supporting |
| CCAR-F/D5/5.4 | Keep verbose exploration out of the main context; save key facts to a file | [5.6](../README.md#56-plan-mode-vs-direct-execution) (Explore), [5.7](../README.md#57-compact-and-managing-the-context-window) (write facts down before `/compact`). Taught in [Chapter 11](../../11-context-management/README.md) | Supporting |
| CCAR-F/APPX/TECH/3 | Claude Code configuration: CLAUDE.md hierarchy, rules, commands, skills | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) | Primary |
| CCAR-F/APPX/TECH/4 | Claude Code CLI: `-p`, `--output-format json`, `--json-schema` | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) | Primary |
| CCAR-F/APPX/IN/9 | CLAUDE.md hierarchy, `@import`, `.claude/rules/` globs | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules) | Primary |
| CCAR-F/APPX/IN/10 | Commands and skills: scope, `context: fork`, `allowed-tools`, `argument-hint` | [5.4](../README.md#54-custom-slash-commands--skills)–[5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) | Primary |
| CCAR-F/APPX/IN/11 | Plan mode vs direct execution | [5.6](../README.md#56-plan-mode-vs-direct-execution) | Primary |
| CCAR-F/APPX/IN/12 | Iterative refinement: I/O examples, test-driven iteration, interview, sequential vs combined fixes | [5.11](../README.md#511-iterative-refinement-with-claude-code) | Primary |
| CCDV-F/D2/2.6/K1 | Configuration management: CLAUDE.md files | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules) (scopes, imports, rules, reviewed through PRs) | Primary |
| CCDV-F/D3/3.1/S1 | Claude Code operation: core components, features, CLAUDE.md hierarchy, `/init`, settings | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.12](../README.md#512-getting-started-and-the-core-loop). Agents (subagents), auto mode and `settings.json` appear here only as far as 5.6 and 5.12 need them | Primary |
| CCDV-F/D3/3.1/K1 | Core component: Rules | [5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules) | Primary |
| CCDV-F/D3/3.1/K2 | Core component: Skills | [5.4](../README.md#54-custom-slash-commands--skills)–[5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) | Primary |
| CCDV-F/D3/3.1/K3 | Core component: Commands | [5.4](../README.md#54-custom-slash-commands--skills) | Primary |
| CCDV-F/D3/3.1/K5 | Core component: Agent Memory | [5.8](../README.md#58-memory-and-auto-memory) (auto memory) | Primary |
| CCDV-F/D3/3.1/K6 | Feature: session management | [5.10](../README.md#510-sessions-resume-name-fork); More self-check questions 4; [`02_homework.ipynb`](../02_homework.ipynb) Q8–Q9 | Primary |
| CCDV-F/D3/3.1/K7 | Feature: built-in and custom slash commands | [5.4](../README.md#54-custom-slash-commands--skills) (custom); built-ins `/init`, `/memory`, `/context`, `/compact`, `/clear`, `/rewind`, `/branch` in [5.7](../README.md#57-compact-and-managing-the-context-window), [5.8](../README.md#58-memory-and-auto-memory), [5.10](../README.md#510-sessions-resume-name-fork), [5.12](../README.md#512-getting-started-and-the-core-loop) | Primary |
| CCDV-F/D3/3.1/K8 | Feature: headless mode | [5.9](../README.md#59-claude-code-in-cicd-headless-mode) | Primary |
| CCDV-F/D3/3.1/K9 | Feature: streaming mode | [5.12](../README.md#512-getting-started-and-the-core-loop) (streaming mode); [`01_practice.ipynb`](../01_practice.ipynb) 5.12; [`02_homework.ipynb`](../02_homework.ipynb) Q12 | Primary |
| CCDV-F/D3/3.1/K11 | The CLAUDE.md hierarchy | [5.1](../README.md#51-the-claudemd-hierarchy) | Primary |
| CCDV-F/D3/3.1/K12 | Repository initialization | [5.12](../README.md#512-getting-started-and-the-core-loop) (`/init`); More self-check questions 7 | Primary |
| ACAD/claude-certified-developer-foundations/3/LO3 | Durable project context: CLAUDE.md, rules, hooks, subagents | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules) (CLAUDE.md, rules). Hooks and subagents only as needed: [5.6](../README.md#56-plan-mode-vs-direct-execution) (Explore), [5.11](../README.md#511-iterative-refinement-with-claude-code) (Stop hook), [Chapter 3](../../03-agent-sdk/README.md#35-hooks-in-the-agent-sdk) | Supporting |
| ACAD/claude-platform-101/13 | Building with Claude Code | Whole chapter, especially [5.12](../README.md#512-getting-started-and-the-core-loop) | Primary |
| ACAD/claude-with-the-anthropic-api/LO11, ACAD/claude-with-google-vertex/LO9 | Deploy Anthropic apps: Claude Code for automated development tasks and Computer Use for UI automation | Claude Code part: [5.9](../README.md#59-claude-code-in-cicd-headless-mode), [5.12](../README.md#512-getting-started-and-the-core-loop). Computer Use part: [5.12](../README.md#512-getting-started-and-the-core-loop) ("Claude Code and Computer Use": API toolset vs Claude Code computer use, deployment and decision table), More self-check questions 8, [`01_practice.ipynb`](../01_practice.ipynb) 5.12 (automation surface router), [`02_homework.ipynb`](../02_homework.ipynb) Exercise 7. The toolset's request shape, batch actions and safety are taught in [Chapter 2, "Anthropic-schema client tools in brief"](../../02-tool-use/README.md#anthropic-schema-client-tools-in-brief) (§2.7) | Primary |
| ACAD/claude-with-the-anthropic-api/72, ACAD/claude-with-google-vertex/76 | Anthropic apps | [5.12](../README.md#512-getting-started-and-the-core-loop) (Claude Code surfaces) | Supporting |
| ACAD/claude-with-the-anthropic-api/73, ACAD/claude-in-amazon-bedrock/74, ACAD/claude-with-google-vertex/77 | Claude Code setup (including on Bedrock / Google Cloud) | [5.12](../README.md#512-getting-started-and-the-core-loop) (install, cloud-provider sign-in, model pinning) | Primary |
| ACAD/claude-with-the-anthropic-api/74, ACAD/claude-in-amazon-bedrock/75, ACAD/claude-with-google-vertex/78 | Claude Code in action | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.12](../README.md#512-getting-started-and-the-core-loop); [`01_practice.ipynb`](../01_practice.ipynb) | Primary |
| ACAD/claude-code-101/LO1, ACAD/claude-code-101/1 | What an AI coding agent is; how Claude Code differs from chat tools | [5.12](../README.md#512-getting-started-and-the-core-loop) (what Claude Code is) | Primary |
| ACAD/claude-code-101/LO2, ACAD/claude-code-101/2 | Agentic loop, context window, tools and permissions working together | [5.12](../README.md#512-getting-started-and-the-core-loop); context in [5.7](../README.md#57-compact-and-managing-the-context-window); modes in [5.6](../README.md#56-plan-mode-vs-direct-execution) | Primary |
| ACAD/claude-code-101/LO3, ACAD/claude-code-101/3 | Install on terminal, VS Code, JetBrains, Desktop, web | [5.12](../README.md#512-getting-started-and-the-core-loop) (surfaces table); [`01_practice.ipynb`](../01_practice.ipynb) 5.12 | Primary |
| ACAD/claude-code-101/4 | Your first prompt | [5.12](../README.md#512-getting-started-and-the-core-loop) (first session) | Primary |
| ACAD/claude-code-101/LO4 | Prompting with approval mode, auto-accept and plan mode | [5.12](../README.md#512-getting-started-and-the-core-loop) (modes table, note on auto mode); [5.6](../README.md#56-plan-mode-vs-direct-execution) | Primary |
| ACAD/claude-code-101/LO5, ACAD/claude-code-101/5 | Explore → plan → code → commit | [5.12](../README.md#512-getting-started-and-the-core-loop); More self-check questions 7; [`01_practice.ipynb`](../01_practice.ipynb) 5.12 | Primary |
| ACAD/claude-code-101/LO6, ACAD/claude-code-101/6 | Context management with `/compact`, `/clear`, `/context` | [5.7](../README.md#57-compact-and-managing-the-context-window); [`02_homework.ipynb`](../02_homework.ipynb) Q10 | Primary |
| ACAD/claude-code-101/LO7, ACAD/claude-code-101/8 | Create and maintain CLAUDE.md | [5.1](../README.md#51-the-claudemd-hierarchy)–[5.3](../README.md#53-clauderules-topic-files-and-path-scoped-rules); `/init` in [5.12](../README.md#512-getting-started-and-the-core-loop) | Primary |
| ACAD/claude-code-101/10 | Skills | [5.4](../README.md#54-custom-slash-commands--skills)–[5.5](../README.md#55-skills-in-depth-skillmd-frontmatter) | Primary |
| ACAD/claude-code-101/13 | Course quiz | [Self-check](../README.md#self-check) and [More self-check questions](#more-self-check-questions); quiz in [`02_homework.ipynb`](../02_homework.ipynb) | Supporting |
| ACAD/claude-code-in-action/2 | A CLAUDE.md that Claude actually follows | [5.1](../README.md#51-the-claudemd-hierarchy) (concrete instructions, under ~200 lines, no contradictions); [Common mistakes](../README.md#common-mistakes) | Primary |

## More self-check questions

**Q1.** Your monorepo has SQL migrations under `services/*/db/migrations/` in 14 services. Every migration must be reversible and must have a `down` step. How do you make Claude apply this automatically, without spending context in unrelated work?

- A) Add the rule to the root CLAUDE.md under a "Migrations" heading
- B) Put a CLAUDE.md in each of the 14 migration folders
- C) Create `.claude/rules/migrations.md` with `paths: "services/*/db/migrations/**"`
- D) Create a `/migration-rules` skill developers invoke before editing migrations

<details><summary>Answer</summary>

**C.** A path-scoped rule loads deterministically, and only when Claude touches a matching file, however many directories those files are spread across. A loads in every session and relies on Claude to infer that the section applies. B duplicates the rule 14 times and drifts. D depends on people remembering to invoke it.
</details>

**Q2.** Your team's `/trace-request` skill follows one request through 30 services and reads hundreds of log lines. Developers run it in the middle of a debugging session. Afterwards the session is full of log noise, and Claude has drifted away from the bug they were fixing. Which single frontmatter change fixes this?

- A) `agent: Explore` on its own
- B) `context: fork`, optionally with `agent: Explore` for a read-only fork
- C) `disallowed-tools: Bash`
- D) `disable-model-invocation: true`

<details><summary>Answer</summary>

**B.** `context: fork` runs the skill in its own subagent context, and only its result returns to the main session. A does nothing on its own: `agent` picks the subagent type only when `context: fork` is set. C removes a tool the trace may need, and the output still lands in the main session. D controls who can start the skill, not where its output goes.
</details>

**Q3.** A nightly job runs `claude "Summarize yesterday's failed builds"` and never finishes. Logs show it waiting for input. What is the fix?

- A) `CLAUDE_HEADLESS=1 claude "..."`
- B) `claude --batch "..."`
- C) `claude -p "..." --max-turns 10`
- D) `claude "..." < /dev/null`

<details><summary>Answer</summary>

**C.** `-p`/`--print` is the documented non-interactive mode. Adding `--max-turns` is good CI hygiene. A and B are not real mechanisms. D is a Unix workaround, not the supported approach.
</details>

**Q4.** On Monday you spent two hours in a session named `billing-map`, mapping the billing module. By Thursday, teammates have merged a refactor that renamed half of the files you explored. You want to continue the investigation. What is the most reliable way to start?

- A) `claude --resume billing-map` and carry on as before
- B) `claude --resume billing-map --fork-session`, so the original session stays untouched
- C) Start a new session seeded with a short structured summary of Monday's findings, and let Claude re-read the renamed files
- D) `claude --continue`, then run `/compact` to shrink the old tool output

<details><summary>Answer</summary>

**C.** Monday's tool results describe files that have since moved, so a resumed session reasons from stale reads. A trusts those stale results. B copies the same stale history under a new ID. D picks the latest session, which may not be `billing-map`, and compacting stale content gives a stale summary. If only one or two files had changed, resuming and telling Claude exactly what changed would be fine.
</details>

**Q5.** Claude Code is writing a migration script that copies `users` into a new schema. You have explained twice in prose that "null emails must be preserved", and the script still crashes on rows where `email` is `NULL`. What is the most effective next step?

- A) Explain the requirement a third time in more detail, in capital letters
- B) Add a test with a concrete input row (`email=None`), the expected output row, and the current traceback, and ask Claude to make it pass
- C) Switch to a larger model and repeat the same instruction
- D) Add "always handle null values carefully" to CLAUDE.md

<details><summary>Answer</summary>

**B.** A specific test case with example input and expected output gives Claude an exact, checkable target, and the failure output shows where it breaks. A and D repeat the prose that is already being misread. C changes cost, not clarity.
</details>

**Q6.** A code review found three problems in the order-import module. (1) The CSV parser drops the time zone from timestamps. (2) The deduplication step compares those timestamps to detect duplicates. (3) The `--help` text has a typo. How do you hand these to Claude Code?

- A) One message per problem, in the order found: 1, then 2, then 3
- B) One message with all three, so everything is fixed in one round
- C) One detailed message covering 1 and 2 together, then a separate message for 3
- D) Fix 3 first, because it is the easiest, then decide on the others

<details><summary>Answer</summary>

**C.** Problems 1 and 2 interact: the right deduplication fix depends on how timestamps are parsed, so Claude should see both at once and design one consistent change. Problem 3 is independent, so it gets its own small, easily reviewed change. A risks churn between 1 and 2. B mixes an unrelated change into a risky diff. D postpones the real decision.
</details>

**Q7.** A teammate is new to Claude Code. They open a 300-file service they have never seen and must add OAuth login. Which sequence matches the recommended workflow?

- A) Start in auto mode and ask Claude to "add OAuth login and commit when done"
- B) Run `/init` and review the generated CLAUDE.md; in plan mode, ask Claude to explain the auth flow and propose a plan; edit and approve the plan; let Claude implement it with tests; then ask it to commit and open a PR
- C) Write the full implementation spec by hand first, then paste it into `claude -p`
- D) Use direct execution in Manual mode and approve each edit as it comes

<details><summary>Answer</summary>

**B.** It is explore → plan → code → commit, with `/init` as repository initialization. The service is unfamiliar and the change touches several files, so planning pays for itself. A skips exploration and review. C makes the human do Claude's exploration and loses the interactive plan review. D approves edits one by one without ever agreeing on a design.
</details>

**Q8.** An insurance company must re-key claim forms into a 20-year-old Windows desktop application that has no API. The job should run every night without a person present, on the company's Google Cloud account. Which design fits?

- A) Enable the `computer-use` server in Claude Code and run `claude -p "re-key tonight's claims"` from a cron job
- B) A service that calls the Messages API with the `computer_toolset_20260801` toolset and runs the actions on a virtual display in an isolated VM, with a domain allowlist, credentials kept out of reach and a human review queue for exceptions
- C) A Claude Code skill with `allowed-tools: Bash` that types into the application window
- D) Ask Claude Code in the Desktop app to do it, and leave the laptop open overnight

<details><summary>Answer</summary>

**B.** Unattended GUI automation of an app with no API is the Computer Use API tool in your own sandboxed deployment, and the toolset is generally available on Google Cloud. A fails twice: Claude Code's computer use is not available with `-p`, and it needs a claude.ai login on a Pro, Max or Ultra plan, not cloud-provider credentials. C confuses shell access with screen control: Bash cannot click in a GUI, and `allowed-tools` only pre-approves tools. D is an interactive research-preview feature on someone's real desktop, which is not a production deployment.
</details>

## Share your progress

```text
Day N of my AI Solution Architect journey: Claude Code config is architecture, not dotfiles.

3 takeaways:
1. CLAUDE.md = always-on; .claude/rules/ + globs = per file type; skills = per task
2. Plan mode first for anything ambiguous or multi-file. Isolate noisy discovery in a subagent
3. In CI: claude -p + --json-schema. Never let the author session review its own code

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeCode #AIArchitecture #Anthropic #LearningInPublic
```
