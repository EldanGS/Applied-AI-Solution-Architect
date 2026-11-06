# Chapter 3 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| OAI/api/design-build-agentic-systems/1 | Every agent has a clear role | [3.4](../README.md#34-handoffs-vs-agents-as-tools) (`handoff_description` as the routing signal, "start with one agent, split only when…"), [3.10](../README.md#310-testing-agent-decisions-and-handoffs) step 2 (non-overlapping descriptions); homework Ex 1 | Primary |
| OAI/api/design-build-agentic-systems/2 | Control tool access within safety limits | [3.3](../README.md#33-function-tools-and-local-context) (least-privilege tool lists, `is_enabled`), [3.5](../README.md#35-guardrails-and-tripwires) (tool input/output guardrails, fail-closed money checks), [3.6](../README.md#36-human-review-approvals-and-resumable-state) (`needs_approval`); homework Ex 1, 3, 5 | Primary |
| OAI/api/design-build-agentic-systems/3 | Reliable, safe handoffs between agents | [3.4](../README.md#34-handoffs-vs-agents-as-tools) (`handoff()`, `input_type`, `input_filter`, `on_handoff`), [3.5](../README.md#35-guardrails-and-tripwires) (guardrails at workflow boundaries), [3.10](../README.md#310-testing-agent-decisions-and-handoffs) | Primary |
| OAI/api/design-build-agentic-systems/5 | Preserve ownership at every handoff | [3.10](../README.md#310-testing-agent-decisions-and-handoffs) step 2 (one owner, intended edges only, `result.last_agent` next turn), [3.4](../README.md#34-handoffs-vs-agents-as-tools), [3.7](../README.md#37-conversation-state-and-sessions) architect note | Primary |
| OAI/api/design-build-agentic-systems/6 | Define outcome and safety requirements | [3.10](../README.md#310-testing-agent-decisions-and-handoffs) step 1 (outcome / safety / ownership table); practice 3.10 `Case`; homework Ex 6 `Requirement` | Primary |
| OAI/api/design-build-agentic-systems/7 | Test decisions and handoffs against those requirements | [3.10](../README.md#310-testing-agent-decisions-and-handoffs) step 3 (assert on handoff, function and guardrail spans; offline then live with repetition); practice 3.10 regression suite; homework Ex 6; More self-check questions 5 | Primary |
| OAI/api/design-build-agentic-systems/8 | Agents that use tools and coordinate multistep tasks | [3.2](../README.md#32-agent-and-runner-the-sdk-agent-loop) (the runner loop), [3.3](../README.md#33-function-tools-and-local-context), [3.4](../README.md#34-handoffs-vs-agents-as-tools) (handoffs, agents-as-tools, code orchestration); practice mini-project | Primary |
| OAI/api/design-build-agentic-systems/14 | SDK primitives: Agent, Handoff, Guardrail, Session | [3.2](../README.md#32-agent-and-runner-the-sdk-agent-loop), [3.4](../README.md#34-handoffs-vs-agents-as-tools), [3.5](../README.md#35-guardrails-and-tripwires), [3.7](../README.md#37-conversation-state-and-sessions) | Primary |
| OAI/api/design-build-agentic-systems/15 | Responses API vs Agents SDK | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) (comparison table and decision notes); [Cheat-sheet](../README.md#cheat-sheet) | Primary |
| OAI/api/design-build-agentic-systems/17 | Agent-as-tool pattern | [3.4](../README.md#34-handoffs-vs-agents-as-tools) (`Agent.as_tool()`, `parameters`, `custom_output_extractor`); homework Ex 4; [Self-check](../README.md#self-check) Q2 | Primary |
| OAI/api/design-build-agentic-systems/19 | Input/output guardrails, tripwires, jailbreak and irrelevant-input protection | [3.5](../README.md#35-guardrails-and-tripwires) (all four guardrail types, `run_in_parallel`, relevance and jailbreak guardrails), [3.10](../README.md#310-testing-agent-decisions-and-handoffs); homework Ex 2, 3 | Primary |
| OAI/api/design-build-agentic-systems/20 | Tracing shows which tools, agents and guardrails fired | [3.8](../README.md#38-tracing-and-lifecycle-hooks) (spans, controls, ZDR limit), [3.10](../README.md#310-testing-agent-decisions-and-handoffs) (span types used in tests) | Primary |
| OAI/bootcamp/api-builder/9 | Production-grade customer-support agent with the Agents SDK | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) (OpenAI's customer service agents demo); practice mini-project (triage desk with billing and refund specialists, guardrails, approvals, session, audit hook); homework Ex 5 (`cancel_order` with approval). FAQ answering and complaint intake are not built here | Supporting |
| OAI/bootcamp/api-builder/10 | Agents: tools and instructions | [3.2](../README.md#32-agent-and-runner-the-sdk-agent-loop) (`instructions`, model choice), [3.3](../README.md#33-function-tools-and-local-context) (`@function_tool`, dynamic instructions) | Primary |
| OAI/bootcamp/api-builder/12 | Guardrails and tripwires | [3.5](../README.md#35-guardrails-and-tripwires); homework Ex 2, 3; [Self-check](../README.md#self-check) Q3; More self-check questions 2 | Primary |
| OAI/bootcamp/api-builder/13 | Agents: tracing | [3.8](../README.md#38-tracing-and-lifecycle-hooks), [3.10](../README.md#310-testing-agent-decisions-and-handoffs) | Primary |
| OAI/bootcamp/api-builder/15 | From one agent to agent-as-tool delegation and multistep patterns | [3.4](../README.md#34-handoffs-vs-agents-as-tools) ("You can combine them": handoffs plus agents-as-tools, chaining, `asyncio.gather`, classifier + `if`) | Primary |
| OAI/tracks/ai-app-development/5 | What an agent is and what it can do | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) ("What counts as an agent"), [3.3](../README.md#33-function-tools-and-local-context) (tools), [3.7](../README.md#37-conversation-state-and-sessions) (context and memory) | Primary |
| OAI/tracks/ai-app-development/10 | Phase 2: building agents, RAG, fine-tuning | Building agents: the whole chapter ([3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api)–[3.10](../README.md#310-testing-agent-decisions-and-handoffs)). How RAG and fine-tuning fit into an agent: [3.3, "Knowledge and behavior"](../README.md#knowledge-and-behavior-where-rag-and-fine-tuned-models-plug-into-an-agent) (RAG as a retrieval tool, a fine-tuned model as `model=`, the three RAG steps, SFT/DPO/RFT at a glance, platform wind-down); practice 3.3 "Knowledge and behavior" cells; homework Ex 4 part B; More self-check questions 6. Tracked elsewhere: hosted file search in depth in [Chapter 4, 4.3](../../04-built-in-tools-and-mcp/README.md#43-file-search-and-vector-stores-hosted-rag); the full RAG pipeline (OAI/tracks/ai-app-development/14) in [Applied 06 — RAG pipelines](../../../applied-ai-architect/06-rag-pipelines/README.md); fine-tuning methods and the RAG-vs-fine-tuning decision (OAI/tracks/ai-app-development/8, /15) in [Applied 05 — Model strategy and customization](../../../applied-ai-architect/05-model-strategy-and-customization/README.md); distillation (OAI/tracks/ai-app-development/24) in `openai-codex/16-models-migration-and-model-optimization` (planned) | Primary (building agents); Supporting (RAG, fine-tuning) |
| OAI/tracks/ai-app-development/12 | Responses API features, and the Agents SDK as a layer on top | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) (the SDK is built on Responses; runtime table). The Responses API features themselves are in [Chapter 1](../../01-responses-api-fundamentals/README.md) | Supporting |
| OAI/tracks/ai-app-development/13 | Reference demos: HITL support agent, multi-agent customer service, computer-use testing agent | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) (demo table mapped to sections) | Primary |
| OAI/tracks/ai-app-development/14 | RAG pipeline steps (prepare, retrieve, generate) and the built-in file search tool | [3.3, "Knowledge and behavior"](../README.md#knowledge-and-behavior-where-rag-and-fine-tuned-models-plug-into-an-agent) (the three steps; `FileSearchTool` on an agent and what it hides; own retriever as a function tool); practice 3.3 "Knowledge and behavior" cells | Supporting (primary: [Applied 06 — RAG pipelines](../../../applied-ai-architect/06-rag-pipelines/README.md); hosted file search: [Chapter 4, 4.3](../../04-built-in-tools-and-mcp/README.md#43-file-search-and-vector-stores-hosted-rag)) |
| OAI/tracks/building-agents/1 | Agent = instructions + guardrails + tools, acting for the user; a chatbot is not an agent | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) ("What counts as an agent") | Primary |
| OAI/tracks/building-agents/2 | Platform primitives: models, tools, state and memory, orchestration | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) | Primary |
| OAI/tracks/building-agents/5 | Responses API vs Agents SDK (state, loop, guardrails, tracing, other providers) | [3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api) (table, decision notes, `litellm/` and custom `ModelProvider`) | Primary |
| OAI/tracks/building-agents/15 | SDK primitives; automatic agent loop and handoffs | [3.2](../README.md#32-agent-and-runner-the-sdk-agent-loop), [3.4](../README.md#34-handoffs-vs-agents-as-tools), [3.5](../README.md#35-guardrails-and-tripwires), [3.7](../README.md#37-conversation-state-and-sessions) | Primary |
| OAI/tracks/building-agents/16 | Built-in tracing | [3.8](../README.md#38-tracing-and-lifecycle-hooks) | Primary |
| OAI/tracks/building-agents/20 | Input guardrails for jailbreaks and irrelevant input, scaled to risk | [3.5](../README.md#35-guardrails-and-tripwires) ("Which guardrails to build, and how strong") | Primary |
| OAI/tracks/building-agents/21 | Structured outputs for app-consumed output; output guardrails for user-facing agents | [3.5](../README.md#35-guardrails-and-tripwires) ("Which guardrails to build"), [3.3](../README.md#33-function-tools-and-local-context) (`output_type`); homework Ex 2 | Primary |
| ROLE/AGENT/8 | OpenAI agent stack (Codex, ChatGPT apps, API agents) | This chapter covers the API side: Agents SDK and Agents API ([3.1](../README.md#31-choosing-a-runtime-responses-api-agents-sdk-or-agents-api)–[3.9](../README.md#39-the-managed-agents-api-beta)). Codex is [Chapter 5](../../05-codex/README.md) | Supporting |

## More self-check questions

**Q1.** A refund call paused for approval. The supervisor approves it two hours later in a web dashboard. How should the backend continue?

- A) Send "The supervisor approved it" as a new user message
- B) Load the stored `RunState` on the server, call `state.approve(item)`, and resume with `Runner.run(original_top_level_agent, state)`
- C) Call `issue_refund` directly and start a fresh run
- D) Accept the serialized state from the dashboard's request body and resume it

<details><summary>Answer</summary>

**B.** An approval resumes the same paused run. A creates a new turn and leaves the call unexecuted. C bypasses the agent's history. D trusts an unauthenticated client blob, which the SDK docs warn against.
</details>

**Q2.** An expensive agent with side-effecting tools sits behind a cheap moderation guardrail. Tripped requests are blocked, but logs show some tools still ran first. What change fixes it?

- A) Move the check into `instructions`
- B) Set `run_in_parallel=False` on the input guardrail
- C) Make it an output guardrail
- D) Disable tracing

<details><summary>Answer</summary>

**B.** The default (parallel) mode starts the agent alongside the guardrail. Blocking mode finishes the guardrail first, so a tripped request never reaches the agent or its tools.
</details>

**Q3.** A bank wants an agent that edits files in a sandbox, runs for long periods, and resumes later. The bank's contract requires Zero Data Retention. Which runtime do you propose?

- A) The Agents API with an OpenAI-hosted sandbox
- B) The Agents API with a self-hosted sandbox, which makes it ZDR-eligible
- C) The Agents SDK in the bank's own service, with its own storage and sandbox integration
- D) The Assistants API with threads

<details><summary>Answer</summary>

**C.** The Agents API currently does not support ZDR, and a self-hosted sandbox does not change that (B is a trap). D was retired on 2026-08-26. Also note that SDK tracing is unavailable for ZDR organizations, so plan observability with your own trace processor.
</details>

**Q4.** A chat backend runs on four workers behind a load balancer. Each request does `Runner.run(agent, msg, session=SQLiteSession(user_id))`. Users report the agent forgets everything they said earlier. What is the problem?

- A) Only that `SQLiteSession` is slow
- B) `SQLiteSession` without a db path is an in-memory database, and a new one is created on every request
- C) Sessions only work with `run_streamed`
- D) Sessions require `max_turns=None`

<details><summary>Answer</summary>

**B.** Without a db path, each `SQLiteSession` object opens its own empty `:memory:` database, so a session built per request starts with no history, even on the same worker. Use a shared backend (Redis, SQLAlchemy) or server-side state (`conversation_id` / `previous_response_id`) alone. Don't add `previous_response_id` next to the session: the SDK raises `UserError` for that combination.
</details>

**Q5.** Your CI test for a triage desk sends "I want my money back for order A-17" and asserts `result.last_agent.name == "Refund agent"`. It passes. A week later you find that triage now routes refunds to the billing agent, which hands them on to the refund agent. What should the test have asserted as well?

- A) That `result.final_output` contains the word "refund"
- B) That the trace has exactly one handoff span, from the triage agent to the refund agent, and no function span for tools the request must not use
- C) That `max_turns` was not exceeded
- D) Nothing more: the outcome was correct, so the workflow is correct

<details><summary>Answer</summary>

**B.** The outcome requirement (who owns the reply) held, but the ownership and safety requirements did not: control moved twice, and for one step a specialist without refund authority owned the conversation. Handoff and function spans show this; the final text (A) and the turn count (C) do not. D is the "outcome-only test" trap from [3.10](../README.md#310-testing-agent-decisions-and-handoffs).
</details>

**Q6.** A retail support agent built with the Agents SDK quotes last month's return rules. The rules change every few weeks and are stored as documents per region. The product owner asks you to fine-tune the agent's model on the new rules. What do you propose?

- A) Fine-tune on the new rules, then fine-tune again after every change
- B) Paste all regions' rules into the agent's `instructions`
- C) A retrieval tool on the agent (`FileSearchTool` over a vector store, or your own `search_kb` function tool), with the region filter set in code and the index refreshed when rules change
- D) Switch the agent to a larger model so it remembers the rules better

<details><summary>Answer</summary>

**C.** The rules are knowledge that changes, so they belong behind retrieval, scoped by region in code ([3.3](../README.md#knowledge-and-behavior-where-rag-and-fine-tuned-models-plug-into-an-agent)). A is the "fine-tuning teaches data" misconception: fine-tuning shapes tone, style, and format, goes stale on the next change, and OpenAI's fine-tuning platform no longer accepts new users. B mixes regions and bloats every request. D changes nothing about what the model knows today.
</details>

## Share your progress

```text
Chapter 3 of my OpenAI path: agents with the OpenAI Agents SDK, plus the new managed Agents API.

3 takeaways:
1. Handoff = the specialist takes over. Agent-as-tool = the manager keeps control and synthesizes
2. Input guardrails run only on the first agent, output guardrails only on the agent that writes the final answer. Refund limits go on the tool
3. Approvals pause the run; you resume the same RunState, not a new chat turn

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#OpenAI #AIAgents #SolutionArchitect #LearningInPublic
```
