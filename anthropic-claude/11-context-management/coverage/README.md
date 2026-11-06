# Chapter 11 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix. Requirement IDs come from the four official Anthropic exam guides (CCAR-F, CCAR-P, CCDV-F, CCAO-F), the Anthropic Academy course outcomes, and the Applied AI architect competency map used for this repo (`ROLE/…`). **Primary** means this chapter is where the requirement is taught in full; **Supporting** means it is applied here and taught in full in another chapter. "Practice" is `01_practice.ipynb`, "homework" is `02_homework.ipynb`. The CCAR-F guide lists prompt caching details and tokenization specifics as out of scope (`CCAR-F/APPX/OUT/15`, `OUT/16`); 11.8 and 11.12 cover them for CCAR-P and CCDV-F.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `CCAR-F/D5/5.1/K1` | Progressive summarization loses numbers, dates, customer expectations | [11.1](../README.md#111-extract-facts-into-a-persistent-case-facts-block), [11.9](../README.md#119-server-side-compaction-beyond-the-guide); practice 11.1; Self-check 1 | Primary |
| `CCAR-F/D5/5.1/K2` | Lost-in-the-middle effect | [11.3](../README.md#113-position-aware-input-lost-in-the-middle); practice 11.3 first-mention positions | Primary |
| `CCAR-F/D5/5.1/K3` | Tool results accumulate tokens out of proportion to relevance | [11.2](../README.md#112-trim-verbose-tool-results); practice 11.2 re-billing | Primary |
| `CCAR-F/D5/5.1/K4` | Send the complete conversation history on every request | [11.1](../README.md#111-extract-facts-into-a-persistent-case-facts-block); homework Q1 | Primary |
| `CCAR-F/D5/5.1/S1` | Persistent case-facts block outside summarized history | [11.1](../README.md#111-extract-facts-into-a-persistent-case-facts-block); practice 11.1 + mini-project; homework Ex 1 | Primary |
| `CCAR-F/D5/5.1/S2` | Per-issue structured layer for multi-issue sessions | [11.1](../README.md#111-extract-facts-into-a-persistent-case-facts-block); homework Q2, Ex 1 | Primary |
| `CCAR-F/D5/5.1/S3` | Trim verbose tool outputs to relevant fields | [11.2](../README.md#112-trim-verbose-tool-results); practice 11.2; homework Ex 2 | Primary |
| `CCAR-F/D5/5.1/S4` | Key findings first, explicit section headers | [11.3](../README.md#113-position-aware-input-lost-in-the-middle); practice 11.3; homework Ex 3 | Primary |
| `CCAR-F/D5/5.1/S5` | Subagents return metadata (dates, sources, method) | [11.3](../README.md#113-position-aware-input-lost-in-the-middle), [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context); homework Q4 | Primary |
| `CCAR-F/D5/5.1/S6` | Upstream agents return structured data, not verbose content | [11.2](../README.md#112-trim-verbose-tool-results); practice 11.2 output contract; homework Q3 | Primary |
| `CCAR-F/D5/5.4/K1` | Context degradation in extended sessions | [11.4](../README.md#114-scratchpad-files); Self-check 3 | Primary |
| `CCAR-F/D5/5.4/K2` | Scratchpad files persist findings across context boundaries | [11.4](../README.md#114-scratchpad-files), [11.11](../README.md#1111-the-memory-tool-beyond-the-guide); practice 11.4 | Primary |
| `CCAR-F/D5/5.4/K3` | Subagents isolate verbose exploration | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context); practice 11.5 | Primary |
| `CCAR-F/D5/5.4/K4` | Structured state persistence for crash recovery (manifest) | [11.6](../README.md#116-structured-state-persistence-and-crash-recovery); practice 11.6 | Primary |
| `CCAR-F/D5/5.4/S1` | Spawn subagents for specific investigation questions | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context); practice 11.5 | Primary |
| `CCAR-F/D5/5.4/S2` | Agents maintain and consult scratchpad files | [11.4](../README.md#114-scratchpad-files); practice 11.4 | Primary |
| `CCAR-F/D5/5.4/S3` | Summarize one phase, inject the summary into the next phase's subagents | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context); practice 11.5 phase-1 hand-off | Primary |
| `CCAR-F/D5/5.4/S4` | Crash recovery from agent state exports loaded by the coordinator | [11.6](../README.md#116-structured-state-persistence-and-crash-recovery); practice 11.6; homework Ex 4 | Primary |
| `CCAR-F/D5/5.4/S5` | `/compact` during long exploration | [11.4](../README.md#114-scratchpad-files), [11.9](../README.md#119-server-side-compaction-beyond-the-guide), [Session hygiene](../README.md#session-hygiene) | Primary |
| `CCAR-F/APPX/TECH/12` | Context window management: budgets, summarization, lost in the middle, extraction, scratchpads | [11.1](../README.md#111-extract-facts-into-a-persistent-case-facts-block), [11.2](../README.md#112-trim-verbose-tool-results), [11.3](../README.md#113-position-aware-input-lost-in-the-middle), [11.4](../README.md#114-scratchpad-files), [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide) | Primary |
| `CCAR-F/APPX/IN/3` | Subagent context passing, state persistence, manifest crash recovery | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context), [11.6](../README.md#116-structured-state-persistence-and-crash-recovery) | Primary |
| `CCAR-F/APPX/IN/16` | Trim tool outputs, extract facts, position-aware ordering | [11.1](../README.md#111-extract-facts-into-a-persistent-case-facts-block), [11.2](../README.md#112-trim-verbose-tool-results), [11.3](../README.md#113-position-aware-input-lost-in-the-middle) | Primary |
| `CCAR-F/MQC/5` | Manage context across long documents, conversations and handoffs | Whole chapter; mini-project in practice notebook | Primary |
| `CCAR-F/D1/1.7/K1` | Named session resumption with `--resume <name>` | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17) | Supporting |
| `CCAR-F/D1/1.7/K2` | `fork_session` for divergent branches | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17); homework Q6 | Supporting |
| `CCAR-F/D1/1.7/K3` | Tell a resumed agent which files changed | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17); practice 11.7 change notice | Supporting |
| `CCAR-F/D1/1.7/K4` | Fresh session + structured summary beats stale resume | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17) | Supporting |
| `CCAR-F/D1/1.7/S1` | Resume named investigation sessions | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17) | Supporting |
| `CCAR-F/D1/1.7/S2` | Fork to compare two approaches | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17); homework Q6 | Supporting |
| `CCAR-F/D1/1.7/S3` | Choose resume vs fresh-with-summary | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17); practice 11.7; homework Ex 6 | Supporting |
| `CCAR-F/D1/1.7/S4` | Targeted re-analysis after file changes | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17); Self-check 4 | Supporting |
| `CCAR-F/D1/1.3/K2` | Subagents do not inherit parent context | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context) | Supporting |
| `CCAR-F/D1/1.3/K4` | Fork-based session management | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17) | Supporting |
| `CCAR-F/D3/3.4/S3` | Explore subagent for verbose discovery | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context); homework Q5 | Supporting |
| `CCAR-F/D3/3.2/S2` | `context: fork` skills isolate verbose output | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context) | Supporting |
| `CCAR-F/APPX/TECH/13` | Session management: resume, fork, named sessions | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17) | Supporting |
| `CCAR-F/PREP/6` | Practice fact extraction, scratchpads, subagent delegation | Practice notebook 11.1–11.5; homework Ex 1–3 | Supporting |
| `CCAR-F/SC1` | Scenario: customer support resolution agent | [Self-check](../README.md#self-check) 1; [More self-check questions](#more-self-check-questions) 1, 4; mini-project | Supporting |
| `CCAR-F/SC2` | Scenario: code generation with Claude Code | [Self-check](../README.md#self-check) 4 | Supporting |
| `CCAR-F/SC3` | Scenario: multi-agent research system | [Self-check](../README.md#self-check) 2; [More self-check questions](#more-self-check-questions) 2 | Supporting |
| `CCAR-F/SC4` | Scenario: developer productivity with Claude | [Self-check](../README.md#self-check) 3 | Supporting |
| `CCAR-P/D2/2.4/S1` | Optimize context windows and manage token usage | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.9](../README.md#119-server-side-compaction-beyond-the-guide), [11.10](../README.md#1110-context-editing-clearing-tool-results-and-thinking-beyond-the-guide); practice 11.8–11.10 | Primary |
| `CCAR-P/D2/2.5/S1` | Prompt reuse strategies (caching) | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCAR-P/D2/2.5/K1` | Caching: static content first | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCAR-P/SQ2` | Sample Q: static 8K prompt every request -> static first + caching | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCAR-P/D3/3.8/S1` | Progressive discovery vs monolithic context | [11.13](../README.md#1113-putting-it-together-progressive-discovery-vs-monolithic-context); practice 11.13; homework Q10 | Supporting |
| `CCAR-P/D3/3.8/K1` | Progressive discovery | [11.13](../README.md#1113-putting-it-together-progressive-discovery-vs-monolithic-context) | Supporting |
| `CCAR-P/D3/3.8/K2` | Monolithic context | [11.13](../README.md#1113-putting-it-together-progressive-discovery-vs-monolithic-context) | Supporting |
| `CCAR-P/D4/4.5/S1` | Token usage, latency and cost trade-offs | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCDV-F/D1/1.3/K4` | Context-window management (agent patterns) | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.9](../README.md#119-server-side-compaction-beyond-the-guide), [11.10](../README.md#1110-context-editing-clearing-tool-results-and-thinking-beyond-the-guide) | Primary |
| `CCDV-F/D2/2.5/K4` | Session hygiene | [Session hygiene](../README.md#session-hygiene); practice 11.7 session linter; homework Q11 | Primary |
| `CCDV-F/D6/6.1/S1` | Context engineering: window management, drift and bloat, pruning, compaction, isolation, memory | Whole chapter | Primary |
| `CCDV-F/D6/6.1/K1` | Context window management | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide) | Primary |
| `CCDV-F/D6/6.1/K2` | Prevent context drift and bloat | [11.1](../README.md#111-extract-facts-into-a-persistent-case-facts-block), [11.2](../README.md#112-trim-verbose-tool-results) (instruction drift in 11.1) | Primary |
| `CCDV-F/D6/6.1/K3` | Tool output pruning | [11.2](../README.md#112-trim-verbose-tool-results), [11.10](../README.md#1110-context-editing-clearing-tool-results-and-thinking-beyond-the-guide) | Primary |
| `CCDV-F/D6/6.1/K4` | Compaction | [11.9](../README.md#119-server-side-compaction-beyond-the-guide); practice 11.9; homework Q7, Ex 5 | Primary |
| `CCDV-F/D6/6.1/K5` | Context isolation through subagents or multi-step workflows | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context) | Primary |
| `CCDV-F/D6/6.1/K6` | Memory management techniques | [11.4](../README.md#114-scratchpad-files), [11.11](../README.md#1111-the-memory-tool-beyond-the-guide) | Supporting |
| `CCDV-F/D5/5.1/K1` | Tokens | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide) | Supporting |
| `CCDV-F/D5/5.1/K2` | Context windows | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide); homework Q9 | Supporting |
| `CCDV-F/D5/5.4/K1` | Token budgeting | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide) | Supporting |
| `CCDV-F/D5/5.4/K2` | Token usage tracking | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide); homework Ex 6 | Supporting |
| `CCDV-F/D5/5.4/K3` | Cost modeling | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide), [11.13](../README.md#1113-putting-it-together-progressive-discovery-vs-monolithic-context) | Supporting |
| `CCDV-F/D5/5.4/K4` | Prompt caching | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCDV-F/D5/5.4/K5` | Cache check-pointing | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCDV-F/PURPOSE/4` | Context engineering to prevent context drift | Whole chapter | Supporting |
| `CCDV-F/PURPOSE/6` | Manage tokens and caching for cost and latency | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCDV-F/D1/1.3/K2` | Sub-agents | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context) | Supporting |
| `CCDV-F/D1/1.3/K3` | Memory | [11.11](../README.md#1111-the-memory-tool-beyond-the-guide) | Supporting |
| `CCDV-F/D2/2.3/K5` | Thinking (kept in context; prefix check) | [11.2](../README.md#112-trim-verbose-tool-results), [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.9](../README.md#119-server-side-compaction-beyond-the-guide) | Supporting |
| `CCDV-F/D2/2.3/K6` | Caching | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `CCDV-F/D3/3.1/K6` | Claude Code session management | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17), [Session hygiene](../README.md#session-hygiene) | Supporting |
| `CCAO-F/D3/3.4/S1` | When to restart, summarize or persist | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17), [Session hygiene](../README.md#session-hygiene) | Supporting |
| `CCAO-F/D3/3.4/K1` | When to restart | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17), [Session hygiene](../README.md#session-hygiene) | Supporting |
| `CCAO-F/D3/3.4/K2` | When to summarize | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17), [11.9](../README.md#119-server-side-compaction-beyond-the-guide) | Supporting |
| `CCAO-F/D3/3.4/K3` | When to persist | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17), [11.4](../README.md#114-scratchpad-files), [11.11](../README.md#1111-the-memory-tool-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-developer-foundations/2/LO5` | Context window, compaction, clearing, subagent handoffs | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context), [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.9](../README.md#119-server-side-compaction-beyond-the-guide), [11.10](../README.md#1110-context-editing-clearing-tool-results-and-thinking-beyond-the-guide), [Session hygiene](../README.md#session-hygiene) | Primary |
| `ACAD/claude-platform-101/10` | Context management (Claude Platform 101 lesson) | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.9](../README.md#119-server-side-compaction-beyond-the-guide), [11.10](../README.md#1110-context-editing-clearing-tool-results-and-thinking-beyond-the-guide), [11.11](../README.md#1111-the-memory-tool-beyond-the-guide) | Primary |
| `ACAD/claude-certified-developer-foundations/1/LO1` | Context window as a fixed budget | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-developer-foundations/2/LO7` | Agent memory across sessions | [11.11](../README.md#1111-the-memory-tool-beyond-the-guide), [11.6](../README.md#116-structured-state-persistence-and-crash-recovery) | Supporting |
| `ACAD/claude-certified-developer-foundations/4/LO4` | Multi-agent system inside its cost and latency budget | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context), [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-associate-foundations/1/LO4` | Manage context limits and memory for continuity | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17), [11.11](../README.md#1111-the-memory-tool-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-associate-foundations/LO1` | Manage context to keep continuity in a session | [11.7](../README.md#117-sessions-resume-fork-or-start-fresh-task-17), [Session hygiene](../README.md#session-hygiene) | Supporting |
| `ACAD/claude-with-the-anthropic-api/LO9` | Prompt caching strategies | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `ACAD/claude-code-101/LO6` | `/compact`, `/clear`, `/context` | [11.4](../README.md#114-scratchpad-files), [11.9](../README.md#119-server-side-compaction-beyond-the-guide), [Session hygiene](../README.md#session-hygiene) | Supporting |
| `ACAD/claude-code-in-action/LO1` | Direct compaction so summaries keep what matters | [11.9](../README.md#119-server-side-compaction-beyond-the-guide), [Session hygiene](../README.md#session-hygiene) | Supporting |
| `ACAD/introduction-to-subagents/LO1` | Subagents get a separate context window and return summaries | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context) | Supporting |
| `ROLE/PROMPT/2` | Context engineering and context-window management | Whole chapter | Primary |
| `ROLE/AGENT/4` | Sub-agent delegation | [11.5](../README.md#115-delegate-exploration-to-subagents-to-protect-the-coordinators-context) | Supporting |
| `ROLE/AGENT/5` | Agent memory and state persistence | [11.6](../README.md#116-structured-state-persistence-and-crash-recovery), [11.11](../README.md#1111-the-memory-tool-beyond-the-guide) | Supporting |
| `ROLE/COST/2` | Prompt caching | [11.12](../README.md#1112-prompt-caching-and-context-management-beyond-the-guide) | Supporting |
| `ROLE/COST/5` | Token efficiency and budgeting | [11.8](../README.md#118-context-windows-token-budgets-and-counting-beyond-the-guide), [11.2](../README.md#112-trim-verbose-tool-results) | Supporting |
| `ROLE/ARCH/5` | Resilience: crash recovery | [11.6](../README.md#116-structured-state-persistence-and-crash-recovery) | Supporting |
| `ROLE/OBS/4` | Diagnose context-related failures | Diagnosis table in [Concepts](../README.md#concepts) | Supporting |

## More self-check questions

**1. (Customer support agent)** `lookup_order` returns 43 fields per call. A typical return case calls it 4–6 times, and by turn 30 most of the input tokens are order data the agent never uses. What should you change first?

- A) Move to a model with a larger context window
- B) Trim each `lookup_order` result to the return-relevant fields before it is appended to history (in the tool, the loop, or a `PostToolUse` hook)
- C) Add a system-prompt instruction to ignore irrelevant order fields
- D) Summarize each tool result with an extra model call before appending it

<details><summary>Answer</summary>

**B.** Deterministic trimming at ingest removes the tokens for every later turn at no extra model cost. A pays for the same noise in a bigger window. C still sends (and bills) all 43 fields. D adds a lossy, paid model call for something code can do exactly.
</details>

**2. (Multi-agent research system)** The coordinator process crashed after the web-search agent finished and while document analysis was running. Restarting from scratch costs about 40 minutes. Which design supports correct recovery?

- A) Each agent writes its structured state (status, key findings, coverage, gaps) to a known file; the coordinator keeps a manifest, loads it on restart, skips completed agents, re-runs the in-progress one and injects completed findings into the remaining agents' prompts
- B) Re-run the whole pipeline on every restart to guarantee consistency
- C) Restore the coordinator's full conversation transcript and continue from the last message
- D) Ask each subagent on restart to report what it found last time

<details><summary>Answer</summary>

**A.** Structured state plus a manifest preserves completed work and gives the coordinator compact, injectable results. B wastes completed work. C brings back stale, bulky tool output and may be incomplete after a crash. D fails because subagents keep no memory between runs.
</details>

**3. (Current platform)** A Sonnet 5.5 coding agent with thinking makes hundreds of tool calls per task, and old file reads and test logs dominate the context. A teammate proposes a client-side job that deletes the content of `tool_result` blocks older than 20 turns before each request. What is the better design?

- A) Keep the teammate's job, because client-side trimming is the documented approach
- B) Enable server-side context editing with `clear_tool_uses_20250919` (a trigger, `keep`, `clear_at_least` so cache breaks are worth it, and `exclude_tools` for results that must stay), and keep trimming new results at ingest
- C) Add the memory tool and remove all tool results from history after each turn
- D) Switch to the legacy Haiku 4.5 to make the extra tokens cheaper

<details><summary>Answer</summary>

**B.** Server-side clearing leaves your history unmodified, so earlier thinking stays valid and the result is predictable. A edits the conversation prefix on the client, which invalidates every later thinking block on Sonnet 5.5 (and is rejected by default on newer accounts). C deletes results the model may still need, which is not what the memory tool is for. D changes the price, not the size, and legacy Haiku 4.5 has a smaller (200K) window.
</details>

**4. (Customer support agent, cost)** To keep case facts current, the team re-renders the top-level `system` prompt (an 8K-token policy plus the facts block) on every turn. Costs rose, and `cache_read_input_tokens` is always 0. What should they change?

- A) Remove the policy from the prompt to save tokens
- B) Keep `system` static and cached (policy first, with a breakpoint), and send the current facts block in the newest turn (verified, system-sourced facts may also go in a mid-conversation system message; customer claims stay in the user turn)
- C) Switch to the 1-hour cache lifetime
- D) Send the facts block only every 10 turns

<details><summary>Answer</summary>

**B.** Any change to `system` changes the cached prefix, so nothing after it can be read from cache. Moving the changing part to the end keeps the static prefix cacheable while the facts stay in every request. A loses required context. C does not help, because the prefix still changes every turn. D defeats the purpose of the facts block.
</details>

**5. (Conversational assistant)** A trip-planning assistant's system prompt says "always show prices in the user's home currency". In chats longer than about 60 turns, the assistant starts quoting prices in US dollars only. The rule is still in `system`, and the static prefix is cached. What is the cheapest reliable fix?

- A) Re-render the top-level `system` prompt each turn with the rule moved to the end
- B) Re-inject a short reminder of the rule at breakpoints, for example as a mid-conversation system message every N turns, and leave `system` unchanged
- C) Start a new chat automatically every 60 turns with no summary
- D) Move the chat to a model with a larger context window

<details><summary>Answer</summary>

**B.** This is instruction drift: the rule is far behind a lot of newer text. A short reminder near the end of the conversation puts it back in view, and appending it leaves the cached prefix untouched. A changes the prefix, so the cache breaks every turn. C throws away the trip details the user already gave. D adds room, not attention; the rule only gets further away.
</details>

**6. (Conversational assistant)** A home-repair helper chat nears its token budget, so the app runs on-demand compaction on the whole history. The facts block (the user's measurements and a warning that the house has old aluminum wiring) sits in an early user turn, so it is compacted along with the rest. After compaction, the assistant gives a shelf measurement that is 2 cm off. What should change?

- A) Compact more often, so each summary covers fewer turns
- B) Keep the facts block out of the compacted range: put the compaction block first, then any recent turns you kept, then the current facts block in the newest user turn
- C) Ask the user to repeat their measurements after every compaction
- D) Stop compacting and drop the oldest turns instead

<details><summary>Answer</summary>

**B.** Compaction is summarization, so anything inside the compacted range can be blurred. A facts block that is re-sent in the newest turn never passes through the summarizer. A still sends the facts through a lossy step, only more often. C moves the app's job to the user. D drops the early turns, which is where the wiring warning was given.
</details>

**7. (Conversational assistant)** A business-coaching product serves hundreds of small firms. Each session ends with agreed action items, and months later an owner asks, "What did we decide about spring pricing?" The team must decide how past conclusions reach new sessions. What is the best design?

- A) One shared `/memories` directory for all firms, so the assistant can learn across customers
- B) Write each session's conclusions to a store scoped to that firm (a memory tool directory per firm, or a CRM note), and give the assistant a tool to look up the entries the current question needs
- C) Append every past session transcript for the firm to the system prompt of each new session
- D) Ask the owner to paste the notes from earlier sessions at the start of each session

<details><summary>Answer</summary>

**B.** Conclusions are stored outside the request, scoped per firm, and only the relevant entries come back. A mixes firms in one store, so one customer's notes can reach another, which is a security failure. C grows without limit, costs more every session and soon passes the window. D pushes the app's job onto the user and fails for sessions they did not keep notes on.
</details>

## Share your progress

```text
Chapter 11 of my Claude Certified Architect journey: context management.

A 1M-token window is a ceiling, not a strategy.

3 takeaways:
1. Summaries turn "25% off" into "a discount came up". Keep exact facts in their own block.
2. Trim tool results before they enter history; every extra field is re-billed every turn.
3. Long work survives crashes through state files + a manifest, not transcripts.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #ContextEngineering #AIArchitecture #LearningInPublic
```
