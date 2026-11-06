# Chapter 8 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix. IDs come from the official-guide checklist (`req_anthropic`) and the role competency matrix (`req_role`). **Primary** means this chapter is where the item is taught in depth; **Supporting** means it is applied or reinforced here and taught more fully elsewhere.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `CCAR-F/D1/1.6/K1` | Fixed pipelines (prompt chaining) vs dynamic adaptive decomposition | [8.1](../README.md#81-fixed-pipelines-prompt-chaining), [8.2](../README.md#82-dynamic-adaptive-decomposition) (comparison table), decision list in [Concepts](../README.md#concepts); practice §8.1–8.2 | Primary |
| `CCAR-F/D1/1.6/K2` | Prompt chaining that splits reviews into per-file steps plus a cross-file pass | [8.1](../README.md#81-fixed-pipelines-prompt-chaining), [8.3](../README.md#83-multi-pass-code-review); practice §8.3 | Primary |
| `CCAR-F/D1/1.6/K3` | Adaptive investigation plans that generate subtasks from discoveries | [8.2](../README.md#82-dynamic-adaptive-decomposition) (planner loop); practice §8.2, homework exercise 6 | Primary |
| `CCAR-F/D1/1.6/S1` | Pick chaining for predictable reviews, dynamic decomposition for open-ended tasks | [8.2](../README.md#82-dynamic-adaptive-decomposition), [cheat-sheet](../README.md#cheat-sheet), Self-check 3, More self-check questions 1; homework exercise 1 | Primary |
| `CCAR-F/D1/1.6/S2` | Per-file local passes plus a separate integration pass | [8.3](../README.md#83-multi-pass-code-review), Self-check 1; homework exercise 2 | Primary |
| `CCAR-F/D1/1.6/S3` | Map structure, rank high-impact areas, prioritized plan that adapts to dependencies | [8.2](../README.md#82-dynamic-adaptive-decomposition) (legacy-tests walkthrough), Self-check 3 | Primary |
| `CCAR-F/D4/4.6/K1` | Self-review limitation: the model keeps its generation reasoning | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak) | Primary |
| `CCAR-F/D4/4.6/K2` | Independent instances beat self-review instructions and extended thinking | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak) (exam trap and its note), Self-check 2 | Primary |
| `CCAR-F/D4/4.6/K3` | Multi-pass review avoids attention dilution and contradictory findings | [8.3](../README.md#83-multi-pass-code-review) | Primary |
| `CCAR-F/D4/4.6/S1` | Second independent instance reviews without the generator's context | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak) (`independent_review`); homework exercise 3 | Primary |
| `CCAR-F/D4/4.6/S2` | Per-file passes plus integration passes for cross-file data flow | [8.3](../README.md#83-multi-pass-code-review) (`multi_pass_review`) | Primary |
| `CCAR-F/D4/4.6/S3` | Verification passes with self-reported confidence for calibrated routing | [8.5](../README.md#85-verification-passes-and-confidence-based-routing), Self-check 4, More self-check questions 6; homework exercise 5 | Primary |
| `CCAR-F/D1/1.4/S2` | Decompose multi-concern requests, investigate in parallel with shared context, synthesize | [8.9](../README.md#89-decomposing-multi-concern-requests), More self-check questions 2 | Primary |
| `CCAR-F/D3/3.6/K4` | Session context isolation: the generating session reviews its own changes less well | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak) | Primary |
| `CCAR-F/D1/1.2/K3` | Coordinator's role in decomposition, delegation and aggregation | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) (taught fully in [Chapter 3](../../03-agent-sdk/README.md#33-hub-and-spoke-coordinator-and-subagents)) | Supporting |
| `CCAR-F/D1/1.2/K4` | Risk of overly narrow decomposition by the coordinator | [8.2](../README.md#82-dynamic-adaptive-decomposition) (coverage map, exam trap), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) (`Decomposition.coverage`), More self-check questions 5 | Primary |
| `CCAR-F/D1/1.3/S3` | Parallel subagents via several subagent-tool calls in one coordinator response | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) (taught fully in [Chapter 3](../../03-agent-sdk/README.md#34-the-subagent-tool-agent-formerly-task)) | Supporting |
| `CCAR-F/D5/5.5/K3` | Confidence calibrated on labeled validation sets to route review attention | [8.5](../README.md#85-verification-passes-and-confidence-based-routing) (`precision_by_bucket`); field-level version in [Chapter 9](../../09-escalation-human-in-the-loop/README.md) | Supporting |
| `CCAR-F/SQ12` | Sample question: 14-file PR gets inconsistent review | [8.3](../README.md#83-multi-pass-code-review), Self-check 1 | Primary |
| `CCAR-F/SC5` | Scenario: Claude Code for CI | [8.3](../README.md#83-multi-pass-code-review)–[8.5](../README.md#85-verification-passes-and-confidence-based-routing), Self-check 1, 2, 4, More self-check questions 6 | Supporting |
| `CCAR-F/SQ7` | Sample question: too-narrow coordinator decomposition | [8.2](../README.md#82-dynamic-adaptive-decomposition) (coverage map), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Supporting |
| `CCAR-F/SC3` | Scenario: multi-agent research system | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api), More self-check questions 3 and 5 | Supporting |
| `CCAR-F/SC4` | Scenario: developer productivity on legacy codebases | [8.2](../README.md#82-dynamic-adaptive-decomposition), Self-check 3 | Supporting |
| `CCAR-F/EX1/5` | Prep exercise: multi-concern messages are decomposed, handled and synthesized | [8.9](../README.md#89-decomposing-multi-concern-requests), More self-check questions 2 | Primary |
| `CCAR-F/SC1` | Scenario: customer support resolution agent | [8.9](../README.md#89-decomposing-multi-concern-requests), More self-check questions 2 | Supporting |
| `CCAR-F/PREP/5` | Design multi-pass review architectures for large code reviews | [8.3](../README.md#83-multi-pass-code-review)–[8.5](../README.md#85-verification-passes-and-confidence-based-routing), [notebooks](../README.md#notebooks) | Supporting |
| `CCAR-F/APPX/TECH/11` | Prompt chaining: sequential decomposition into focused passes | [8.1](../README.md#81-fixed-pipelines-prompt-chaining), [8.6](../README.md#86-the-workflow-pattern-catalog) | Primary |
| `CCAR-F/APPX/IN/2` | Coordinator-subagent patterns, decomposition, parallel execution, iterative refinement | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api), evaluator-optimizer row in [8.6](../README.md#86-the-workflow-pattern-catalog) | Supporting |
| `CCAR-F/APPX/IN/12` | Sequential vs parallel issue resolution (the iterative-refinement item's last part) | [8.9](../README.md#89-decomposing-multi-concern-requests) | Supporting |
| `CCAR-F/MQC/6` | CI/CD code review and PR feedback | [8.3](../README.md#83-multi-pass-code-review)–[8.5](../README.md#85-verification-passes-and-confidence-based-routing), [8.10](../README.md#810-decomposition-in-claude-code-today-beyond-the-guide) | Supporting |
| `CCAR-F/MQC/7` | Self-evaluation patterns | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak), [8.5](../README.md#85-verification-passes-and-confidence-based-routing) | Supporting |
| `CCAR-P/D1/1.3/S1` | Select workflow, agentic or augmented-LLM patterns | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), More self-check questions 4 | Primary |
| `CCAR-P/D1/1.3/K1` | Workflow pattern | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `CCAR-P/D1/1.3/K2` | Agentic pattern | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `CCAR-P/D1/1.3/K3` | Augmented LLM pattern | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), decision list in [Concepts](../README.md#concepts) | Primary |
| `CCAR-P/D1/1.4/S1` | Design multi-agent systems and orchestration strategies | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Supporting |
| `CCAR-P/D1/1.5/S1` | Apply decomposition techniques for complex problem solving | Whole chapter, esp. [8.1](../README.md#81-fixed-pipelines-prompt-chaining), [8.2](../README.md#82-dynamic-adaptive-decomposition) | Primary |
| `CCAR-P/D4/4.5/S1` | Token usage, latency and cost-performance trade-offs | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) (4×/15× tokens), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) (cost, caching, batches) | Supporting |
| `CCDV-F/D1/1.1/S1` | Agent architecture: workflow vs agent, manager/supervisor hierarchies, subagents | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `CCDV-F/D1/1.1/K1` | Principles, patterns and trade-offs of agent and workflow architecture | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `CCDV-F/D1/1.1/K2` | Decision criteria for workflow vs agent | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), decision list in [Concepts](../README.md#concepts) | Primary |
| `CCDV-F/D1/1.1/K3` | Structure of manager/supervisor hierarchies | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) (manager/supervisor paragraph), agent teams row in [8.10](../README.md#810-decomposition-in-claude-code-today-beyond-the-guide) | Primary |
| `CCDV-F/D1/1.1/K4` | Role of subagents in improving task execution | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) ("What subagents buy you") | Primary |
| `CCDV-F/D1/1.3/S1` | Agent patterns and agentic frameworks | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Supporting |
| `CCDV-F/D1/1.3/K1` | Tool-use loops | [8.6](../README.md#86-the-workflow-pattern-catalog) (agent row); taught fully in [Chapter 3](../../03-agent-sdk/README.md#31-the-agentic-loop) | Supporting |
| `CCDV-F/D1/1.3/K2` | Sub-agents | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Supporting |
| `CCDV-F/D1/1.3/K5` | Agentic frameworks (Strands, LangGraph, PydanticAI) | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) (frameworks paragraph) | Supporting |
| `CCDV-F/D2/2.4/K3` | Asynchronous programming | [8.3](../README.md#83-multi-pass-code-review), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) (`asyncio`, `AsyncAnthropic`); homework exercise 4 | Supporting |
| `CCDV-F/D2/2.4/K6` | Code review | [8.3](../README.md#83-multi-pass-code-review)–[8.5](../README.md#85-verification-passes-and-confidence-based-routing) | Supporting |
| `CCDV-F/D6/6.1/K5` | Context isolation through subagents or multi-step workflows | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Supporting |
| `CCDV-F/D6/6.3/K4` | Skepticism toward confident output | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak), [8.5](../README.md#85-verification-passes-and-confidence-based-routing) | Supporting |
| `CCAO-F/D1/1.2/S1` | Apply task decomposition to structure complex requests | [8.11](../README.md#811-decomposition-for-everyday-claude-use-associate-lens), [8.9](../README.md#89-decomposing-multi-concern-requests) | Primary |
| `CCAO-F/PREP/3` | Practice structuring prompts, decomposing tasks, iterating | [8.11](../README.md#811-decomposition-for-everyday-claude-use-associate-lens) | Supporting |
| `CCAO-F/D2/2.4/S1` | When human review or extra verification is required | [8.5](../README.md#85-verification-passes-and-confidence-based-routing), [8.11](../README.md#811-decomposition-for-everyday-claude-use-associate-lens) | Supporting |
| `ACAD/claude-with-the-anthropic-api/LO12` | Architect agent systems with parallelization, chaining and routing | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Primary |
| `ACAD/claude-with-the-anthropic-api/76` | Lesson: agents and workflows | [8.6](../README.md#86-the-workflow-pattern-catalog) (intro), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `ACAD/claude-with-the-anthropic-api/77` | Lesson: parallelization workflows | [8.6](../README.md#86-the-workflow-pattern-catalog) (sectioning, voting), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Primary |
| `ACAD/claude-with-the-anthropic-api/78` | Lesson: chaining workflows | [8.1](../README.md#81-fixed-pipelines-prompt-chaining), [8.6](../README.md#86-the-workflow-pattern-catalog) | Primary |
| `ACAD/claude-with-the-anthropic-api/79` | Lesson: routing workflows | [8.6](../README.md#86-the-workflow-pattern-catalog) (`route_request`) | Primary |
| `ACAD/claude-with-the-anthropic-api/82` | Lesson: workflows vs agents | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `ACAD/claude-with-google-vertex/LO10` | Design workflows with parallelization, chaining and routing (Vertex edition) | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Primary |
| `ACAD/claude-with-google-vertex/84` | Lesson: agents and workflows | [8.6](../README.md#86-the-workflow-pattern-catalog) (intro), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `ACAD/claude-with-google-vertex/85` | Lesson: parallelization workflows | [8.6](../README.md#86-the-workflow-pattern-catalog), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Primary |
| `ACAD/claude-with-google-vertex/86` | Lesson: chaining workflows | [8.1](../README.md#81-fixed-pipelines-prompt-chaining), [8.6](../README.md#86-the-workflow-pattern-catalog) | Primary |
| `ACAD/claude-with-google-vertex/87` | Lesson: routing workflows | [8.6](../README.md#86-the-workflow-pattern-catalog) (`route_request`) | Primary |
| `ACAD/claude-with-google-vertex/90` | Lesson: workflows vs agents | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `ACAD/claude-certified-architect-professional/1/LO2` | Choose augmented call vs workflow vs agent by naming the cost | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `ACAD/claude-certified-architect-professional/5/LO2` | Review discipline that keeps AI-generated work trustworthy | [8.4](../README.md#84-independent-review-instances-why-self-review-is-weak), [8.5](../README.md#85-verification-passes-and-confidence-based-routing) | Supporting |
| `ACAD/claude-certified-developer-foundations/2/LO6` | Choose between workflow and agent patterns | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Primary |
| `ACAD/claude-certified-developer-foundations/4/LO4` | Stay inside cost, latency and reliability budgets across coordinating agents | [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) (cost, observability and concurrency/rate-limit rows) | Supporting |
| `ACAD/claude-certified-associate-foundations/LO2` | Decompose complex requests (course outcome) | [8.11](../README.md#811-decomposition-for-everyday-claude-use-associate-lens) | Supporting |
| `ACAD/claude-certified-associate-foundations/2/LO2` | Apply task decomposition to complex, multi-part requests | [8.11](../README.md#811-decomposition-for-everyday-claude-use-associate-lens) | Primary |
| `ROLE/PROMPT/6` | Prompt chaining and workflow decomposition before reaching for agents | [8.1](../README.md#81-fixed-pipelines-prompt-chaining) (gated chain), [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) (simplest structure first, routing exam trap) | Primary |
| `ROLE/AGENT/1` | Agent architecture: agent vs workflow, control flow, stop conditions | [8.2](../README.md#82-dynamic-adaptive-decomposition), [8.6](../README.md#86-the-workflow-pattern-catalog), [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy) | Supporting |
| `ROLE/AGENT/4` | Orchestrator/sub-agent patterns, delegation, parallelism | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Primary |
| `ROLE/ARCH/4` | Reusable reference patterns | [8.6](../README.md#86-the-workflow-pattern-catalog), [cheat-sheet](../README.md#cheat-sheet) | Supporting |
| `ROLE/ARCH/5` | Resilience: retries/backoff, rate-limit handling, partial failure | [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) (production table, `run_worker`), More self-check questions 3 | Supporting |
| `ROLE/COST/1` | Cost-latency-quality trade-offs | [8.7](../README.md#87-workflow-or-agent-choosing-the-level-of-autonomy), [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) | Supporting |
| `ROLE/COST/4` | Routing and model tiering | [8.6](../README.md#86-the-workflow-pattern-catalog) (routing to Haiku) | Supporting |
| `ROLE/EVAL/2` | Automated graders and LLM-as-judge with calibration | [8.5](../README.md#85-verification-passes-and-confidence-based-routing), evaluator-optimizer row in [8.6](../README.md#86-the-workflow-pattern-catalog) | Supporting |
| `ROLE/OBS/1` | Tracing agent steps, tokens and latency | [8.8](../README.md#88-fan-out-in-code-orchestrator-workers-with-asyncio-and-the-messages-api) (observability row) | Supporting |

Acknowledgement: the topic list was cross-checked against the community study guide by paullarionov ([Chapter 8 and Domain notes 1.6 / 4.6](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-8-task-decomposition-strategies)).

## More self-check questions

**1. (Structured data extraction)** Every incoming vendor contract must be checked for the same five clauses (liability cap, termination, data protection, payment terms, governing law), with a report in a fixed format. A teammate proposes an orchestrator agent that decides at runtime which checks to run. What do you recommend?

- A) The orchestrator, because it can adapt to unusual contracts
- B) A fixed prompt chain (one focused step per clause, gates between steps, a final assembly step), with an "unclear" route to human review
- C) A single call that checks all five clauses and writes the report
- D) A multi-agent system with one subagent per clause that negotiates the final report

<details><summary>Answer</summary>

**B.** The steps are known and identical for every input, so a fixed chain is cheaper, more consistent and testable step by step. A adds cost and unpredictability for no benefit. C risks uneven attention across clauses and leaves nothing to inspect between steps. D is heavy over-engineering.
</details>

**2. (Customer support agent)** An internal IT helpdesk agent closes one-problem tickets in about 15 seconds. A ticket like "my VPN drops every hour, I lost access to the finance share, and I need a second monitor" takes more than a minute, and employees complain about the wait. Traces show the agent works on the three problems strictly one after another and loads the employee's directory profile and device list again for each one. Which change fixes both problems in the trace?

- A) Move the agent to a larger model so each step finishes faster
- B) Cache the directory and device lookups for the session, but keep working on the problems one after another
- C) Split the ticket into its problems, load the profile and device list once, look into the problems in parallel with that shared context, then send one combined reply
- D) Raise `max_tokens` so the agent can plan all three problems in a single turn

<details><summary>Answer</summary>

**C.** The trace shows two problems: shared context loaded again for every problem, and problems handled in sequence. Decomposition with shared context removes both. B removes the repeated lookups, but the wait still adds up across all three problems. A does not remove the repeated work or the sequential order. D does not change how the work is structured. Few-shot examples are the fix for a different symptom (mixed-up parameters between issues, [8.9](../README.md#89-decomposing-multi-concern-requests)), not wasted calls.
</details>

**3. (Multi-agent research system)** Your orchestrator fans out 120 worker calls with `asyncio.gather` and no limit. Many fail with HTTP 429, and the run takes longer than before. What should you do?

- A) Switch to sequential calls so you never exceed the limit
- B) Set `max_retries=0` so failures surface immediately
- C) Bound concurrency with a semaphore, let the SDK retry with `retry-after`, keep the shared worker prefix cacheable, and return failed workers as structured partial results
- D) Move to a larger model, which has higher rate limits

<details><summary>Answer</summary>

**C.** The burst exceeds the per-model RPM/ITPM/OTPM token buckets. Bounded concurrency keeps the parallel speedup without overload, the SDK already backs off on 429 using `retry-after`, cached reads do not count toward ITPM, and structured partial results keep the run going. A throws away the latency gain. B turns transient errors into lost work. D does not address the burst (limits are set per model and tier).
</details>

**4. (Solution design)** A client wants "an autonomous multi-agent system" to sort incoming support emails into four queues (billing, technical, refunds, other). Each queue already has a fixed handling process. What do you propose?

- A) A coordinator agent with four specialist subagents that decide how to handle each email
- B) An evaluator-optimizer loop that refines each classification three times
- C) A single agent loop with tools for all four processes
- D) A routing workflow: a fast model classifies each email into a structured category (with an `other` route), and code dispatches it to the existing process

<details><summary>Answer</summary>

**D.** Distinct categories with known handling are the textbook case for routing. It is cheap (a small model can classify), predictable and easy to evaluate. A and C add autonomy the task does not need. B adds cost to a decision that a single structured classification handles well.
</details>

**5. (Multi-agent research system)** A due-diligence orchestrator splits "assess the risks of acquiring this logistics company" into subtasks, fans out workers and writes a report. Twice last quarter a report went out with no section on labor and union risk, even though every worker returned status `ok`. You want to catch this before any money is spent on workers. What do you add?

- A) A line in the synthesis prompt: "Mention any risk areas the workers did not cover"
- B) Have the planner return a coverage map (which subtask covers each risk area on the deal checklist), check it in code against the checklist before the fan-out, and re-plan with the missing areas named
- C) Double the number of workers so each risk area is more likely to be picked up
- D) Raise the workers' effort so each one researches beyond its brief

<details><summary>Answer</summary>

**B.** The gap starts in the decomposition, so check the decomposition before you fan out ([8.2](../README.md#82-dynamic-adaptive-decomposition): coverage map). A asks the synthesis to notice a topic nobody researched, but it sees only the worker results. C adds cost and still leaves coverage to chance. D pushes workers outside their boundaries, which creates overlap, and still does not guarantee the missing area.
</details>

**6. (Claude Code for CI)** Your verification pass tags each finding high, medium or low confidence. Engineers labeled last month's findings: high was 96% real (n = 240), medium 95% real (19 of 20) and low 61% real (n = 90). Inline PR comments need at least 95% precision, and the team wants as many findings inline as the policy allows. Which buckets should go inline?

- A) High and medium, because both reach 95%
- B) High only for now; keep medium in the triage queue and label more medium findings until that bucket has enough samples to trust
- C) None, because self-reported confidence can never be trusted
- D) All three, sorted by confidence

<details><summary>Answer</summary>

**B.** Calibration needs precision per bucket **and** enough samples ([8.5](../README.md#85-verification-passes-and-confidence-based-routing)). Medium's 95% comes from 20 findings: one more false alarm would bring it to about 90%, so it is not yet evidence. High is well sampled and above the target. A treats a tiny sample as proof. C throws away a signal you have measured on 240 findings. D posts a bucket that is wrong almost 40% of the time.
</details>

## Share your progress

```text
Chapter 8 of my Claude Certified Architect journey: how to split work for LLMs.

3 takeaways:
1. Known steps? Use a gated chain. Unknown scope? Map first, then plan adaptively.
2. A 14-file PR in one pass dilutes attention. Review per file, then do one cross-file pass.
3. Never let the author review itself. Use a fresh instance, then calibrated verification.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #AIAgents #AIArchitecture #LearningInPublic
```
