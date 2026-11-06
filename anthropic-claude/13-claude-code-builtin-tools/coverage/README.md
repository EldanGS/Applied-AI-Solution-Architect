# Chapter 13 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Requirement IDs come from the official exam guides (via the repo's requirements checklist) and the Applied AI architect role map. "Primary" means this chapter is the main place the item is taught; "supporting" means it is taught mainly in another chapter and reinforced here.

| Requirement ID | What it asks | Where in this chapter | Depth |
|---|---|---|---|
| `CCAR-F/D2/2.5/K1` | Grep for content search (function names, error messages, imports) | [13.2](../README.md#132-grep-vs-glob-content-search-vs-path-search) | Primary |
| `CCAR-F/D2/2.5/K2` | Glob for file path pattern matching | [13.2](../README.md#132-grep-vs-glob-content-search-vs-path-search) | Primary |
| `CCAR-F/D2/2.5/K3` | Read/Write for full-file operations; Edit for targeted changes by unique text match | [13.3](../README.md#133-read-write-and-edit-full-file-vs-targeted-changes) | Primary |
| `CCAR-F/D2/2.5/K4` | Read + Write as the fallback when Edit fails on non-unique matches | [13.4](../README.md#134-when-edit-fails-anchors-replace_all-and-the-read--write-fallback) | Primary |
| `CCAR-F/D2/2.5/S1` | Selecting Grep to find callers and error messages | [13.2](../README.md#132-grep-vs-glob-content-search-vs-path-search), [13.6](../README.md#136-incremental-investigation-grep-read-repeat) | Primary |
| `CCAR-F/D2/2.5/S2` | Selecting Glob for naming patterns such as `**/*.test.tsx` | [13.2](../README.md#132-grep-vs-glob-content-search-vs-path-search) | Primary |
| `CCAR-F/D2/2.5/S3` | Read the full file, then Write, when Edit cannot find a unique anchor | [13.4](../README.md#134-when-edit-fails-anchors-replace_all-and-the-read--write-fallback) | Primary |
| `CCAR-F/D2/2.5/S4` | Incremental understanding: Grep for entry points, Read to follow imports, not reading everything up front | [13.6](../README.md#136-incremental-investigation-grep-read-repeat) | Primary |
| `CCAR-F/D2/2.5/S5` | Tracing usage across wrapper modules by listing exported names and searching each | [13.7](../README.md#137-tracing-through-wrapper-modules) | Primary |
| `CCAR-F/APPX/TECH/9` | Built-in tools Read, Write, Edit, Bash, Grep, Glob: purposes and selection criteria | [13.1](../README.md#131-the-six-core-tools-and-how-claude-chooses-among-them)–[13.5](../README.md#135-bash-the-general-purpose-tool-and-its-limits) | Primary |
| `CCAR-F/SC4` | Scenario: Developer Productivity with Claude (built-in tools plus MCP for exploring legacy code) | Whole chapter, mini-project, homework Part C | Supporting (primary: [exam prep](../../exam-prep/README.md) scenario drills) |
| `CCAR-F/D2/2.4/S3` | Better MCP descriptions so the agent stops preferring built-in tools like Grep | [13.8](../README.md#138-built-in-tools-vs-mcp-tools) | Supporting (primary: [Chapter 4](../../04-model-context-protocol/README.md)) |
| `CCAR-F/D5/5.4/K1` | Context degradation in long exploration sessions | [13.6](../README.md#136-incremental-investigation-grep-read-repeat) | Supporting (primary: [Chapter 11](../../11-context-management/README.md)) |
| `CCAR-F/D5/5.4/K2`, `CCAR-F/D5/5.4/S2` | Scratchpad files that persist key findings | [13.6](../README.md#136-incremental-investigation-grep-read-repeat), [13.11](../README.md#1311-codebase-understanding-for-modernization-work), mini-project | Supporting (primary: [Chapter 11](../../11-context-management/README.md)) |
| `CCAR-F/D5/5.4/K3`, `CCAR-F/D5/5.4/S1` | Subagents (Explore) isolate verbose exploration | [13.6](../README.md#136-incremental-investigation-grep-read-repeat), [13.9](../README.md#139-other-current-built-in-tools-beyond-the-guide), [13.11](../README.md#1311-codebase-understanding-for-modernization-work) | Supporting (primary: [Chapter 11](../../11-context-management/README.md)) |
| `CCAR-F/D5/5.4/S3`, `CCAR-F/D5/5.4/S5` | Summarize a phase before the next; `/compact` during long exploration | [13.11](../README.md#1311-codebase-understanding-for-modernization-work) | Supporting (primary: [Chapter 11](../../11-context-management/README.md)) |
| `CCAR-F/D1/1.6/S3` | Legacy test work: map structure, find high-impact areas, prioritized adaptive plan | [13.11](../README.md#1311-codebase-understanding-for-modernization-work), More self-check questions 4 | Supporting (primary: [Chapter 8](../../08-task-decomposition/README.md)) |
| `CCAR-F/D3/3.4/K3` | Plan mode for safe exploration before changes | [13.11](../README.md#1311-codebase-understanding-for-modernization-work) | Supporting (primary: [Chapter 5](../../05-claude-code/README.md)) |
| `CCDV-F/D8/8.3/S1`, `CCDV-F/D8/8.3/K1` | Trade-offs among built-in tools, custom tools, Skills and MCP | [13.8](../README.md#138-built-in-tools-vs-mcp-tools) | Supporting (primary: planned Chapter 17) |
| `CCDV-F/PURPOSE/8` | Weighing built-in tools, custom tools, Skills and MCPs | [13.8](../README.md#138-built-in-tools-vs-mcp-tools) | Supporting (primary: planned Chapter 17) |
| `CCDV-F/MQC/2` | Operate Claude Code for codebase modernization | [13.11](../README.md#1311-codebase-understanding-for-modernization-work) | Supporting (primary: planned Chapter 20) |
| `CCDV-F/D3/3.1/S1` | Claude Code operation | [13.10](../README.md#1310-permission-rules-per-tool-beyond-the-guide) | Supporting (primary: [Chapter 5](../../05-claude-code/README.md)) |
| `CCDV-F/D3/3.1/K13` | `settings.json` configuration (permission rules) | [13.10](../README.md#1310-permission-rules-per-tool-beyond-the-guide) | Supporting (primary: planned Chapter 19) |
| `ACAD/claude-platform-101/7` | Academy lesson: built-in tools | [13.1](../README.md#131-the-six-core-tools-and-how-claude-chooses-among-them), [13.9](../README.md#139-other-current-built-in-tools-beyond-the-guide) | Supporting (primary: [Chapter 2, 2.7](../../02-tool-use/README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide)) |
| `ACAD/claude-with-the-anthropic-api/41`, `ACAD/claude-with-google-vertex/43` | Academy lesson: the text edit tool (same exact-and-unique contract as Edit) | [13.3](../README.md#133-read-write-and-edit-full-file-vs-targeted-changes) | Supporting (primary: [Chapter 2, 2.7](../../02-tool-use/README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide)) |
| `ROLE/BUILD/6` | AI coding agents in customer SDLCs (configuration, permissions) | [13.10](../README.md#1310-permission-rules-per-tool-beyond-the-guide), [13.11](../README.md#1311-codebase-understanding-for-modernization-work) | Supporting (primary: planned Chapter 19) |
| `ROLE/AGENT/7` | Claude agent stack: Agent SDK, subagents, Claude Code permissions | [13.9](../README.md#139-other-current-built-in-tools-beyond-the-guide), [13.10](../README.md#1310-permission-rules-per-tool-beyond-the-guide) | Supporting (primary: [Chapter 3](../../03-agent-sdk/README.md)) |
| `ROLE/AGENT/2` | Tool selection and tool descriptions | [13.1](../README.md#131-the-six-core-tools-and-how-claude-chooses-among-them), [13.8](../README.md#138-built-in-tools-vs-mcp-tools) | Supporting (primary: [Chapter 2](../../02-tool-use/README.md)) |
| `ROLE/SAFE/10`, `ROLE/SAFE/5` | Tool-access controls and least privilege for agents | [13.10](../README.md#1310-permission-rules-per-tool-beyond-the-guide) | Supporting (primary: planned applied-architect chapter on LLM application security) |
| `ROLE/PROMPT/2` | Context engineering during exploration | [13.6](../README.md#136-incremental-investigation-grep-read-repeat), [13.11](../README.md#1311-codebase-understanding-for-modernization-work) | Supporting (primary: [Chapter 11](../../11-context-management/README.md)) |
| `ROLE/EVAL/6` | Agent trajectory quality (tool-call traces) | [Practice notebook](../01_practice.ipynb) (tool-call ledger) | Supporting (primary: planned applied-architect chapter on evaluation design) |

## More self-check questions

**1. (Developer productivity)** A team wants to apply a lint fix to every Storybook story file, which live next to their components in dozens of folders and are named `*.stories.tsx`. What should the agent use to list them?

- A) Grep for `stories` in all `.tsx` files
- B) Read `src/` recursively
- C) Glob with `**/*.stories.tsx`
- D) Bash `cat` on each component folder

<details><summary>Answer</summary>

**C.** A naming pattern across directories is exactly what Glob is for. A matches any file that mentions "stories" in its content, including imports in non-story files. B reads directories, which Read does not do. D reads contents instead of listing paths.
</details>

**2. (Tool design, current docs)** A platform team writes `"deny": ["Write(./infra/**)"]` to stop Claude from changing infrastructure files, but Claude still edits them. Why, and what is the fix?

- A) Deny rules need absolute paths, so the rule must be written as `Write(//infra/**)`
- B) `Write(path)` rules are never consulted; deny `Edit(./infra/**)`, which also covers Write
- C) Add "never edit infra" to CLAUDE.md so every session sees the rule
- D) Move the rule to `allow` with a `!` prefix

<details><summary>Answer</summary>

**B.** A `Write(path)` rule is accepted but never consulted; `Edit(path)` rules govern every built-in tool that changes files. A misreads the problem (and `//` would point at the filesystem root, not the project). C shapes behavior but does not enforce anything. D is not how negation or allow rules work.
</details>

**3. (Agent SDK, current docs)** A service runs an Agent SDK agent that should only read and search a repository. The config is `allowed_tools=["Read", "Grep", "Glob"]` and `permission_mode="bypassPermissions"`. In testing, the agent ran a shell command. What is the right change?

- A) Add `"Bash"` to `allowed_tools` with a comment that it should not be used
- B) Set `tools=["Read", "Grep", "Glob"]` and use `permission_mode="dontAsk"`
- C) Lower `max_turns` so the agent has fewer chances to run a command
- D) Add "do not use Bash" to the system prompt

<details><summary>Answer</summary>

**B.** `allowed_tools` auto-approves the tools it lists but does not remove the others, and `bypassPermissions` approves everything that reaches it. Restrict the base tool set (or remove tools by bare name) and use `dontAsk` so anything not pre-approved is denied. A expands access. C and D do not enforce anything.
</details>

**4. (Developer productivity, modernization)** A customer wants Claude to "add comprehensive tests" to a ten-year-old billing system with 900 files and almost no tests. Which plan is best?

- A) Generate tests for every public function in alphabetical order so none is skipped
- B) Map the structure, rank modules by fan-in, churn, test gaps and risk, then follow a plan that adapts
- C) Read all 900 files in one session so Claude has full context, then write tests
- D) Start with the smallest modules, because quick wins build coverage and confidence fastest

<details><summary>Answer</summary>

**B.** Mapping first and prioritizing by evidence puts effort where risk is, and the plan adapts as hidden dependencies appear. A and D optimize for ease, not impact. C does not fit in a context window and degrades answer quality.
</details>

## Share your progress

```text
Chapter 13 of my Claude Certified Architect journey: Claude Code's built-in tools.

3 takeaways:
1. Paths -> Glob, contents -> Grep, and search before you read. Grep the entry point, Read it, Grep what it calls. Never read the whole repo "for context".
2. Edit needs an exact, unique match. Not unique? Widen the anchor, or Read the full file and Write it back. Then verify.
3. Re-exports hide callers: list every name a wrapper module exports and search for each one.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeCode #AIArchitecture #DeveloperTools #LearningInPublic
```
