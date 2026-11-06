# Chapter 11 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

IDs come from this repo's requirement checklists: OpenAI Academy courses, bootcamps and developer tracks (`OAI/...`) and the role competency matrix (`ROLE/...`). This chapter is the main home for context engineering on the OpenAI path, so the three context, token-budget and agent-memory rows are **Primary**. The other rows are taught here only from the context-management angle; the chapter named in the Depth column covers them fully. Items marked **[INFERRED]** are mapped from a related bootcamp session or developer track, not stated on the course page itself (see the requirements checklist's marker key).

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `ROLE/PROMPT/2` | Context engineering and context-window management: what goes into context, compaction, long context | Whole chapter: [11.1](../README.md#111-what-fills-the-window-and-what-it-costs) (what fills the window, budget), [11.4](../README.md#114-compaction-server-side-and-standalone) (compaction), [11.6](../README.md#116-the-case-facts-block)–[11.8](../README.md#118-position-aware-input) (facts, trimming, position); practice mini-project; homework exercises 1–5 | Primary |
| `ROLE/COST/5` | Token efficiency and budgeting: estimation, pruning and compaction, output limits, budgets | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs) (`input_tokens.count`, quadratic re-billing, soft/hard budget, 272K threshold), [11.3](../README.md#113-truncation-the-blunt-instrument), [11.4](../README.md#114-compaction-server-side-and-standalone), [11.7](../README.md#117-trimming-verbose-tool-outputs); homework exercise 1 | Primary |
| `ROLE/AGENT/5` | Agent memory and state management: history, long-term memory, persistence | [11.2](../README.md#112-conversation-state-for-long-running-work-who-can-edit-the-history) (state strategies), [11.5](../README.md#115-long-runs-in-the-agents-sdk-limits-filters-trimmers-and-compacting-sessions) (sessions, callbacks, compacting session), [11.9](../README.md#119-scratchpad-files-and-memory-across-sessions) (scratchpads), [11.11](../README.md#1111-structured-state-persistence-and-crash-recovery) (manifest, `RunState`); homework exercise 6 | Primary |
| `OAI/tracks/building-agents/2` | Platform primitives: models, tools, state and memory, orchestration | [11.2](../README.md#112-conversation-state-for-long-running-work-who-can-edit-the-history), [11.9](../README.md#119-scratchpad-files-and-memory-across-sessions) (the state-and-memory primitive only) | Supporting (primitives overview in chapter 03) |
| `OAI/tracks/building-agents/5` | Responses API server-side conversation state vs the Agents SDK | [11.2](../README.md#112-conversation-state-for-long-running-work-who-can-edit-the-history) (strategy table: stateless, `previous_response_id`, Conversations, Agents SDK sessions; plus the managed Agents API note) | Supporting (chapter 03) |
| `OAI/tracks/ai-app-development/12` | Stateful Responses API, Agents SDK on top | [11.2](../README.md#112-conversation-state-for-long-running-work-who-can-edit-the-history), [11.4](../README.md#114-compaction-server-side-and-standalone) (compaction with stateless and chained state) | Supporting (chapter 03) |
| `OAI/api/design-build-agentic-systems/15` [INFERRED] | Choose the Responses API (stateful, more control) or the Agents SDK | [11.2](../README.md#112-conversation-state-for-long-running-work-who-can-edit-the-history) (who can edit the history under each runtime), [cheat-sheet](../README.md#cheat-sheet) | Supporting (chapter 03) |
| `OAI/api/design-build-agentic-systems/14` [INFERRED] | Agents SDK primitives, including Session | [11.2](../README.md#112-conversation-state-for-long-running-work-who-can-edit-the-history), [11.5](../README.md#115-long-runs-in-the-agents-sdk-limits-filters-trimmers-and-compacting-sessions) (`SessionSettings`, `session_input_callback`, `OpenAIResponsesCompactionSession`, backends) | Supporting (chapter 03) |
| `OAI/tracks/building-agents/15` | Agents SDK primitives: Agent, Handoff, Guardrail, Session | [11.5](../README.md#115-long-runs-in-the-agents-sdk-limits-filters-trimmers-and-compacting-sessions) (Session for long runs) | Supporting (chapter 03) |
| `OAI/tracks/ai-app-development/5` | What agents can do, including keeping context and memory | [11.6](../README.md#116-the-case-facts-block), [11.9](../README.md#119-scratchpad-files-and-memory-across-sessions) | Supporting (chapter 03) |
| `OAI/api/design-build-agentic-systems/17` [INFERRED] | The agent-as-tool pattern | [11.10](../README.md#1110-delegating-to-sub-agents-to-protect-context) (`as_tool` with `custom_output_extractor` to protect the coordinator's context); practice explorer | Supporting (chapter 03) |
| `OAI/bootcamp/api-builder/15` | From a single agent to agent-as-tool delegation and multi-step patterns | [11.10](../README.md#1110-delegating-to-sub-agents-to-protect-context) | Supporting (chapter 03) |
| `OAI/tracks/building-agents/18` | Multi-agent benefits; agent-as-tool and shared memory keyed by conversation ID | [11.2](../README.md#112-conversation-state-for-long-running-work-who-can-edit-the-history) (Conversations and sessions keyed by ID, shared across workers), [11.10](../README.md#1110-delegating-to-sub-agents-to-protect-context), [11.11](../README.md#1111-structured-state-persistence-and-crash-recovery) | Supporting (chapter 08) |
| `OAI/api/design-build-agentic-systems/5` | Preserve ownership at every handoff | [11.10](../README.md#1110-delegating-to-sub-agents-to-protect-context) ("Ownership at a handoff is a context decision": facts plus filtered history for the new owner), [11.11](../README.md#1111-structured-state-persistence-and-crash-recovery) (phase owners in the manifest); practice `restore` reports who resumes each phase | Supporting (chapter 03, 3.10) |
| `OAI/api/design-build-agentic-systems/8` | Agents that use tools and coordinate on multistep tasks | [11.5](../README.md#115-long-runs-in-the-agents-sdk-limits-filters-trimmers-and-compacting-sessions), [11.10](../README.md#1110-delegating-to-sub-agents-to-protect-context), mini-project | Supporting (chapter 03) |
| `OAI/bootcamp/api-builder/9` | A production-grade customer-support agent with the Agents SDK | [11.5](../README.md#115-long-runs-in-the-agents-sdk-limits-filters-trimmers-and-compacting-sessions) (support agent with a file-backed session, trimmer and compacting session); the mini-project adds facts, budget and crash recovery (it uses app-side retrieval, not the Agents SDK) | Supporting (chapter 03) |
| `OAI/api/optimize-ai-app-performance/14` [INFERRED] | Prompt caching to cut latency and cost | [11.12](../README.md#1112-context-management-and-prompt-caching) (how compaction, trimming and facts placement interact with the cache) | Supporting (chapter 07) |
| `OAI/tracks/ai-app-development/25` | Prompt caching | [11.12](../README.md#1112-context-management-and-prompt-caching) | Supporting (chapter 07) |
| `ROLE/COST/2` | Prompt caching: stable prefixes, breakpoints | [11.6](../README.md#116-the-case-facts-block) (facts placement), [11.12](../README.md#1112-context-management-and-prompt-caching) | Supporting (chapter 07; Claude chapter 16) |
| `OAI/api/optimize-ai-app-performance/6` | Deliberate trade-offs between quality, latency, throughput, reliability and cost | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs), [11.4](../README.md#114-compaction-server-side-and-standalone) (latency tip, billed compaction pass), [11.12](../README.md#1112-context-management-and-prompt-caching) (cache-hit rate vs total cost), [cheat-sheet](../README.md#cheat-sheet); More self-check questions 4 | Supporting (applied-ai-architect chapter 15) |
| `OAI/api/optimize-ai-app-performance/7` | Improve speed and cost while keeping the required accuracy | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs), [11.7](../README.md#117-trimming-verbose-tool-outputs), [11.12](../README.md#1112-context-management-and-prompt-caching) (smaller context, same facts) | Supporting (applied-ai-architect chapter 15) |
| `OAI/bootcamp/api-builder/31` | Latency and cost optimization | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs), [11.12](../README.md#1112-context-management-and-prompt-caching) | Supporting (applied-ai-architect chapter 15) |
| `ROLE/COST/1` | Cost-latency-quality trade-off analysis | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs) (cost of a 60-turn chat), [11.12](../README.md#1112-context-management-and-prompt-caching) (before/after compaction cost model) | Supporting (applied-ai-architect chapter 15) |
| `OAI/api/optimize-ai-app-performance/13` [INFERRED] | Three performance levers: prompt, context, model | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs), [11.6](../README.md#116-the-case-facts-block)–[11.8](../README.md#118-position-aware-input): the context lever only | Supporting (full three-lever decision in [chapter 06](../../06-prompt-engineering-and-evals/README.md), 6.12) |
| `OAI/tracks/ai-app-development/23` | Three performance levers: prompt, context or RAG, model or fine-tuning | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs), [11.6](../README.md#116-the-case-facts-block)–[11.8](../README.md#118-position-aware-input): the context lever only | Supporting (chapter 06, 6.12) |
| `OAI/bootcamp/api-builder/32` | Observability, guardrails and reliability | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs) (per-turn usage logging), [11.11](../README.md#1111-structured-state-persistence-and-crash-recovery) (checkpoints, idempotent side effects) | Supporting (applied-ai-architect chapter 16) |
| `ROLE/OBS/1` | Tracing and token analytics | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs) (per-turn `usage` fields), [11.12](../README.md#1112-context-management-and-prompt-caching) (`usage.input_tokens_details.cached_tokens` and `.cache_write_tokens`, hit rate) | Supporting (applied-ai-architect chapter 16) |
| `ROLE/OBS/4` | Troubleshooting GenAI failures such as context overflow | [11.1](../README.md#111-what-fills-the-window-and-what-it-costs), [11.3](../README.md#113-truncation-the-blunt-instrument) (400 on overflow, silent `auto` truncation); Self-check 1 and More self-check questions 3 | Supporting (applied-ai-architect chapter 16) |
| `ROLE/AGENT/4` | Multi-agent orchestration and sub-agents | [11.10](../README.md#1110-delegating-to-sub-agents-to-protect-context) (agent-as-tool, handoff filters, Responses Multi-agent) | Supporting (chapter 08) |
| `ROLE/ARCH/5` | Resilience and reliability patterns | [11.3](../README.md#113-truncation-the-blunt-instrument) (fail loudly on overflow), [11.11](../README.md#1111-structured-state-persistence-and-crash-recovery) (crash recovery, idempotency keys) | Supporting (applied-ai-architect chapter 04) |

## More self-check questions

**1.** A stateless agent loop uses server-side compaction. The engineer wants smaller requests. Which statement is correct?

- A) After appending output items, items before the most recent compaction item may be dropped; with `previous_response_id` chaining you must not prune manually, and the output of `/responses/compact` must never be pruned
- B) Any items may be dropped at any time, since compaction will recover them
- C) The compaction item can be dropped once it has been read, because the model has already seen it
- D) Compaction only works with `store=True`

<details><summary>Answer</summary>

**A.** This matches the compaction guide: the latest compaction item carries the necessary context in stateless chaining; `previous_response_id` chains are not pruned manually; the compacted window from the standalone endpoint is the canonical next window. B and C lose state. D is wrong: server-side compaction is ZDR-friendly with `store=False`.
</details>

**2.** An Agents SDK support agent with a file-backed session calls `search_kb` a few times per turn; each result is about 6,000 characters. After 30 turns, most of every request is old `search_kb` results that are rarely needed again. Which change is most targeted?

- A) `session_input_callback` that keeps only the last 10 history items
- B) `RunConfig(call_model_input_filter=ToolOutputTrimmer(recent_turns=2, max_output_chars=800, trimmable_tools={"search_kb"}))`, plus returning fewer fields from `search_kb` itself
- C) `truncation="auto"` in `ModelSettings`
- D) Deleting `function_call_output` items for `search_kb` from the session

<details><summary>Answer</summary>

**B.** The trimmer previews `search_kb` outputs from turns older than the last two user messages before every model call, without touching the stored session or the call/output pairs, and trimming at the source shrinks every result. A runs once per run, before the loop, and cuts by count, not by relevance (it can also drop the case's early turns). C drops the oldest items blindly. D breaks call/output pairing. Note the limit: `ToolOutputTrimmer` never trims inside the current turn, and it should not: items since the last user message must reach the model untouched. If the growth were inside **one** long run, you would shrink results at the source, delegate, or rely on compaction. Also wrap the trimmer so error outputs stay readable; it has no error exemption.
</details>

**3.** A coordinator agent planning a change to the inventory service reads 22 files to find every caller, and its later answers start citing "typical patterns" instead of the specific classes it read. What should change?

- A) Give the coordinator a larger `max_output_tokens`
- B) Delegate the dependency exploration to an agent-as-tool with a minimal toolset that returns a structured report (dependencies, file:line evidence, gaps) through `custom_output_extractor`, and record key findings in a scratchpad
- C) Hand off to an explorer agent with the full history and never return
- D) Put all 22 files in the coordinator's `instructions` so they are cached

<details><summary>Answer</summary>

**B.** Delegation keeps verbose discovery out of the coordinator's context, and a structured result plus scratchpad preserves what matters. A changes output length only. C moves the whole problem to another agent and loses coordination. D puts large, changing content in the prefix and still floods the context.
</details>

**4.** After the team enabled compaction, the dashboard shows the cache hit rate falling from 85% to 60%, and someone proposes disabling compaction. Average input per turn fell from 180K to 30K tokens on `gpt-6-astra`. What is the right response?

- A) Disable compaction; cache hit rate is the key metric
- B) Compare total input cost and quality before and after; compaction resets the prefix once, but much smaller requests are usually cheaper overall. Keep the prefix stable, keep history append-only between compactions, and compact in batches
- C) Change `reasoning.effort` per turn to compensate
- D) Add a timestamp to `instructions` so each compaction gets a fresh cache

<details><summary>Answer</summary>

**B.** OpenAI's caching guide says compaction can reduce reuse and that fewer input tokens can still save money when the hit rate falls. A optimizes the wrong metric. C changes the prefix even more. If effort must change, use a `configuration_update` item, but not with automatic compaction: turn it off and compact explicitly with a `compaction_trigger` item as the final input item. D guarantees cache misses.
</details>

**5.** An Agents SDK returns agent adds the latest case facts through a `session_input_callback`. In one run the agent calls `lookup_order`, then `send_return_label`, and that tool changes the case status to "label sent". On its next model call in the same run, the agent still sees the old status and offers to send the label again. What is the right fix?

- A) Lower `SessionSettings(limit=...)` so less old history is loaded
- B) Render the facts block in a `call_model_input_filter`, which runs before every model call in the loop, so each call sees the facts as they are now
- C) Tell the model in `instructions` to call `lookup_order` again before every action
- D) Set `ModelSettings(truncation="auto")` so the old facts drop out of the context

<details><summary>Answer</summary>

**B.** `session_input_callback` runs once per `Runner.run`, before the loop, so the facts it adds stay fixed for the whole run. `call_model_input_filter` runs before each model call, which is where fresh facts belong. A changes how much history is loaded, not when facts are refreshed. C relies on the model, adds a tool call per step, and the order system may not even hold the label status. D drops the oldest items first; it refreshes nothing.
</details>

**6.** A stateless returns assistant keeps a case-facts block. After each user message, a structured extraction proposes field values, and the code writes them straight into the block. A customer says, "I paid 120 USD," but the order system recorded 74.95 USD. The block now says 120 USD, and the agent offers a 120 USD refund. Which design prevents this?

- A) Let the model rewrite the whole facts block each turn from the conversation, so it can weigh both values
- B) Merge in code with field ownership: a value such as `order_total` may only come from the system of record. A different value from the user is logged as a conflict (with a version bump), and the agent confirms or escalates instead of overwriting
- C) Move the facts block to the top of `instructions` so the model trusts it more
- D) Compact the history more often so the wrong amount drops out of the context

<details><summary>Answer</summary>

**B.** Facts are updated from tool results and merged in code, and every change is logged (11.6). A is the "rewrite from memory" pattern: the model can keep the wrong value, and nothing records why. C does not change which value is stored, and dynamic data at the top of `instructions` breaks the cache. D: the wrong value sits in the block your code renders into every request, so compaction cannot remove it.
</details>

**7.** A claims agent chains every turn with `previous_response_id` and stores nothing else. One claim waits seven weeks for a medical report. When the report arrives, the resume request with the saved response ID fails, because that response is no longer stored. What should the design have kept?

- A) Nothing more: retry the request with exponential backoff until the response is available again
- B) Its own state: the versioned case facts, a manifest with phase statuses and side-effect IDs, and dated notes. On resume, start a new request seeded with them and tell the agent what changed
- C) Only the last response ID and the customer's latest message; anything else can be asked again
- D) A rule to re-run the claim from the first message so the model rebuilds its context

<details><summary>Answer</summary>

**B.** Stored responses expire after 30 days, so a chain cannot be the record of a case that runs longer (11.2, 11.11). A: the failure is not transient; the data is gone. C makes the customer repeat everything and loses the commitments already made. D re-bills the whole case and can repeat side effects such as payouts unless they have idempotency keys.
</details>

## Share your progress

```text
Chapter 11 of the OpenAI branch: context management for long-running agents.

3 takeaways:
1. A 1M window isn't a plan. Re-sent history grows the bill every turn, and >272K input tokens doubles the input rate.
2. OpenAI compaction is opaque. Amounts, IDs and promises live in a case-facts block my app owns.
3. Trim tool output at the source, delegate verbose exploration, checkpoint with idempotency keys.

#OpenAI #AIArchitecture #AIAgents #ContextEngineering #BuildInPublic
```
