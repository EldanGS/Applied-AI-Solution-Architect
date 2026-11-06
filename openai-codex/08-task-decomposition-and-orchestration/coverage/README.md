# Chapter 8 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

OpenAI has no public architect exam; its formal certification is enterprise or invite-only, so this repo targets the Academy API and Codex pathway certificates. This table maps the chapter to the OpenAI Academy courses, bootcamps and developer tracks this repo targets (`OAI/...` IDs) and to the applied AI solution architect competency matrix (`ROLE/...` IDs). Items marked **[INFERRED]** are not stated on the course page itself; they are mapped from the matching bootcamp session or developer track and should be treated as likely, not confirmed, curriculum. **Primary** means this chapter is a main place the requirement is taught; **Supporting** means it is applied or extended here and taught in depth in another chapter.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/api/design-build-agentic-systems/1` | Design agentic systems in which every agent has a clear role | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/api/design-build-agentic-systems/3` | Design reliable, safe handoffs between agents | [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier), [8.7](../README.md#87-orchestrating-via-llm-vs-via-code) | Supporting |
| `OAI/api/design-build-agentic-systems/4` | Route work between agents | [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier), [8.7](../README.md#87-orchestrating-via-llm-vs-via-code) | Primary |
| `OAI/api/design-build-agentic-systems/5` | Preserve ownership at every handoff | [8.7](../README.md#87-orchestrating-via-llm-vs-via-code), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/api/design-build-agentic-systems/6` | Define outcome and safety requirements for the workflow | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) (verification contracts) | Supporting |
| `OAI/api/design-build-agentic-systems/7` | Test whether agent decisions and handoffs meet those requirements | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) (scripted tests, coverage and handoff-accuracy evals) | Supporting |
| `OAI/api/design-build-agentic-systems/8` | Design agents that use tools and coordinate to complete multistep tasks | [8.2](../README.md#82-fixed-pipelines-prompt-chaining-with-the-agents-sdk)–[8.6](../README.md#86-evaluator-optimizer-loops) | Supporting |
| `OAI/api/design-build-agentic-systems/9` | Deliverable: a multi-agent workflow built and tested against outcome and safety requirements | Mini-project in [`01_practice.ipynb`](../01_practice.ipynb) | Supporting |
| `OAI/api/design-build-agentic-systems/17` **[INFERRED]** | Agent-as-tool pattern | [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers), [8.7](../README.md#87-orchestrating-via-llm-vs-via-code) | Supporting |
| `OAI/api/design-build-agentic-systems/18` **[INFERRED]** | Triage / routing agents; multiple agents only for non-overlapping tasks, complex instructions or many similar tools | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier) | Primary |
| `OAI/api/design-build-agentic-systems/21` **[INFERRED]** | Fast model for conversation, delegate demanding work to the flagship | [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier) (model tiering) | Supporting |
| `OAI/api/design-build-agentic-systems/22` **[INFERRED]** | Structured outputs for agent output the application consumes | [8.2](../README.md#82-fixed-pipelines-prompt-chaining-with-the-agents-sdk), [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers) | Supporting |
| `OAI/api/design-build-agentic-systems/23` **[INFERRED]** | Model-graded evaluation; moving from a single agent to multi-agent patterns | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.6](../README.md#86-evaluator-optimizer-loops), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/bootcamp/api-builder/11` | Agents session: handoffs, routing and orchestration, including triage routing | [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier), [8.7](../README.md#87-orchestrating-via-llm-vs-via-code) | Primary |
| `OAI/bootcamp/api-builder/14` | Agents session: evals, model-graded evaluation, outputs that can be evaluated | [8.6](../README.md#86-evaluator-optimizer-loops), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/bootcamp/api-builder/15` | Agents session: from a single agent to agent-as-tool delegation and multi-step patterns | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers) | Supporting |
| `OAI/tracks/building-agents/4` | Model selection: start with the flagship, use smaller models for latency, a conversational model that delegates heavy tasks | [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier) (model tiering) | Supporting |
| `OAI/tracks/building-agents/14` | Orchestration: multi-step flows, handoffs, guardrails, context | [8.2](../README.md#82-fixed-pipelines-prompt-chaining-with-the-agents-sdk)–[8.7](../README.md#87-orchestrating-via-llm-vs-via-code) | Primary |
| `OAI/tracks/building-agents/16` | Built-in tracing of tools, agents and guardrails | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/tracks/building-agents/17` | When to use multiple agents; use a routing agent | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier) | Primary |
| `OAI/tracks/building-agents/18` | Multi-agent benefits: separation of concerns, parallelism, focused evals; agent-as-tool; shared memory keyed by `conversation_id` | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.4](../README.md#84-parallelization-fan-out-voting-and-parallel-tool-calls), [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers) (agent-as-tool, shared memory) | Primary |
| `OAI/codex/get-started-with-codex/7` | Produce the evidence a reviewer needs | [8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/extend-codex-workflows/4` | Keep review evidence visible to reviewers | [8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/extend-codex-workflows/5` | Keep ownership clear when work runs in parallel | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/extend-codex-workflows/19` **[INFERRED]** | Worktrees for parallel work | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/scale-codex-governed-teams/2` | Split a large change into workstreams the team can verify | [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/scale-codex-governed-teams/3` | Define the evidence each workstream must produce | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/scale-codex-governed-teams/4` | Define what each workstream does when its verification fails | [8.4](../README.md#84-parallelization-fan-out-voting-and-parallel-tool-calls), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/scale-codex-governed-teams/5` | Bring parallel outputs back together safely | [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers), [8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/scale-codex-governed-teams/6` | Coordinate parallel Codex workstreams | [8.8](../README.md#88-hosted-subagents-responses-api-multi-agent-agents-api-codex), [8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers) | Supporting |
| `OAI/codex/scale-codex-governed-teams/10` | Deliverable: a verification contract per workstream | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/scale-codex-governed-teams/11` | Deliverable: a method to split a complex change into workstreams and reintegrate them | [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers), [8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers), [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `OAI/codex/scale-codex-governed-teams/17` **[INFERRED]** | Sub-agents | [8.8](../README.md#88-hosted-subagents-responses-api-multi-agent-agents-api-codex) | Supporting |
| `OAI/codex/scale-codex-governed-teams/23` **[INFERRED]** | Integrate Codex into CI, security and code-review workflows | [8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers) | Supporting |
| `ROLE/PROMPT/6` | Prompt chaining and workflow decomposition before reaching for autonomous agents | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.2](../README.md#82-fixed-pipelines-prompt-chaining-with-the-agents-sdk) | Primary |
| `ROLE/AGENT/1` | Agent architecture and agentic workflows (agent vs workflow, control flow, stop conditions) | [8.1](../README.md#81-workflows-vs-agents-choosing-a-decomposition-shape), [8.6](../README.md#86-evaluator-optimizer-loops), [8.7](../README.md#87-orchestrating-via-llm-vs-via-code) | Supporting |
| `ROLE/AGENT/4` | Multi-agent orchestration and sub-agents: delegation, parallelism, coordination | [8.4](../README.md#84-parallelization-fan-out-voting-and-parallel-tool-calls), [8.5](../README.md#85-dynamic-decomposition-orchestrator-workers), [8.8](../README.md#88-hosted-subagents-responses-api-multi-agent-agents-api-codex) | Primary |
| `ROLE/AGENT/8` | OpenAI agent stack (API agents, Codex) | [8.7](../README.md#87-orchestrating-via-llm-vs-via-code)–[8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers) | Supporting |
| `ROLE/COST/4` | Model routing, cascading and tiering | [8.3](../README.md#83-routing-by-code-by-handoff-and-by-model-tier) | Supporting |
| `ROLE/EVAL/2` | Automated graders and LLM-as-judge | [8.6](../README.md#86-evaluator-optimizer-loops), [8.9](../README.md#89-multi-pass-code-review-and-independent-reviewers) | Supporting |
| `ROLE/EVAL/6` | Agent evaluation: task completion, tool use, trajectory quality | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |
| `ROLE/OBS/1` | LLM / agent tracing and observability | [8.10](../README.md#810-verification-contracts-testing-and-tracing-an-orchestration) | Supporting |

## More self-check questions

**1.** A team must add tests to a legacy codebase they have never seen. The modules, the gaps, and the external dependencies are unknown until the code is explored. Which decomposition fits?

- A) A fixed five-step pipeline (scan → plan → write tests → run → report) with the steps hard-coded
- B) Orchestrator-workers: map the code first, plan subtasks from what is found, run independent workers in parallel, and re-plan with a cap when new dependencies appear
- C) A single call with the whole repository in a 1M-token context
- D) A triage agent that hands off to a "testing" specialist

<details><summary>Answer</summary>

**B.** When the subtasks depend on intermediate results, decomposition has to be dynamic. A is right for predictable work, but this work is not predictable. C runs into attention dilution and cannot adapt. D just moves the whole open-ended job to one agent.
</details>


**2.** An evaluator-optimizer loop for marketing copy sometimes runs 14 rounds and costs more than the campaign. The evaluator receives the drafter's full conversation and returns free-text comments. Which redesign is best?

- A) Remove the evaluator and ship the first draft
- B) Cap the rounds (with a defined fallback at the cap), give the evaluator a fresh context with only the brief, the draft and an explicit rubric, and return a structured pass/revise verdict with specific feedback items
- C) Ask the drafter to grade its own draft at the end of the same prompt
- D) Raise the evaluator's `reasoning.effort` to `max`

<details><summary>Answer</summary>

**B.** It bounds cost, removes shared-context bias, and gives the loop a machine-readable stop signal. A loses the quality gain. C is self-review in the same context. D adds cost and does not fix an unbounded loop or a vague rubric.
</details>


**3.** Your app enables Responses API Multi-agent. The output contains `multi_agent_call` items with `action: "spawn_agent"` and several `function_call` items for your `get_proposal` tool, some emitted by `/root/agent_a`. What must your code do?

- A) Execute every `multi_agent_call` and return outputs for it, then ignore the function calls
- B) Leave `multi_agent_call` items to the API (preserve them if you replay or trace), execute every pending `function_call` whichever agent emitted it, and return each `function_call_output` (in a continuation request over HTTP, or with `response.inject` over WebSocket)
- C) Execute only function calls from `/root`; subagent calls are handled by OpenAI
- D) Disable `multi_agent` because function tools are not supported with it

<details><summary>Answer</summary>

**B.** `multi_agent_call` items are hosted actions that the API executes. Developer-defined function calls work as usual for any agent in the tree. C is wrong: subagents' function calls are yours too. D confuses Responses Multi-agent with Agents API subagents, which do not support function tools.
</details>

**4.** A team wants hosted parallel subagents for a review workflow. One branch must call an internal pricing function and run on a cheaper model; another needs read-only access only. Which option fits these requirements best?

- A) Agents API with `multi_agent.enabled`, giving the pricing subagent a function tool
- B) Responses API Multi-agent with a different model per subagent
- C) Orchestrate in the Agents SDK: per-branch agents with their own `model` and least-privilege tools, run in parallel via `as_tool()` or `asyncio.gather`
- D) One agent with every tool and a prompt that says which branch may use what

<details><summary>Answer</summary>

**C.** Per-branch models and tool scopes need your own orchestration. A fails because Agents API subagents do not support function tools. B fails because Responses Multi-agent subagents share the request's model and tools. D relies on instructions for an access-control requirement.
</details>

## Share your progress

```text
Chapter 8 of my OpenAI path: task decomposition and orchestration.

3 takeaways:
1. Code outside, LLM inside: code owns stages, caps and gates; the model only plans, routes or picks the next worker
2. Handoffs can't fan out (one per turn). Parallel specialists = as_tool() or asyncio.gather, with a concurrency cap
3. Never let the author review its own work. Fresh reviewer instance, like Codex /review

#OpenAI #AIAgents #MultiAgent #SolutionArchitect #LearningInPublic
```
