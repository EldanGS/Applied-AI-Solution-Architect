# Chapter 10 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

OpenAI has no architect exam. These are the OpenAI Academy, bootcamp and developer-track items from the repo's requirements checklist (`OAI/...`), plus the role competencies (`ROLE/...`) that this chapter teaches. Items marked **[INFERRED]** are mapped from a bootcamp session or developer track, so they are likely, not confirmed, course content. One requirement (`ROLE/ARCH/5`) has this chapter as a primary home; the other rows are **Supporting**: the chapter teaches the error-handling side of a topic that is introduced elsewhere.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/api/design-build-agentic-systems/3` | Design reliable, safe handoffs between agents | [10.5](../README.md#105-structured-worker-results-with-partial-results) (a typed `WorkerResult` contract at every agent boundary), [10.7](../README.md#107-coordinator-decisions-and-the-anti-patterns); [cheat-sheet](../README.md#cheat-sheet) (agents-as-tools vs handoffs when the coordinator must handle failures) | Supporting |
| `OAI/api/design-build-agentic-systems/5` | Preserve ownership at every handoff | [10.5](../README.md#105-structured-worker-results-with-partial-results) (what the coordinator sees in each wiring pattern), [10.7](../README.md#107-coordinator-decisions-and-the-anti-patterns) (the coordinator owns the final decision) | Supporting |
| `OAI/api/design-build-agentic-systems/7` | Test whether agent decisions and handoffs meet outcome and safety requirements | [10.7](../README.md#107-coordinator-decisions-and-the-anti-patterns), [10.8](../README.md#108-coverage-annotations-in-the-final-synthesis) (output guardrail that blocks over-claimed coverage); fault-injection mini-project; homework Exercise 5 (coordinator decision tests) | Supporting |
| `OAI/api/design-build-agentic-systems/8` | Design agents that use tools and coordinate on multistep tasks | [10.5](../README.md#105-structured-worker-results-with-partial-results), mini-project in [`01_practice.ipynb`](../01_practice.ipynb) | Supporting |
| `OAI/api/design-build-agentic-systems/9` | Deliverable: a multi-agent workflow built and tested against outcome and safety requirements | Mini-project in [`01_practice.ipynb`](../01_practice.ipynb) (three workers, injected failures, coverage-annotated report) | Supporting |
| `OAI/api/design-build-agentic-systems/17` | Agent-as-tool pattern **[INFERRED]** | [10.5](../README.md#105-structured-worker-results-with-partial-results) (wiring table: `as_tool` with `failure_error_function` and `custom_output_extractor`) | Supporting |
| `OAI/api/design-build-agentic-systems/19` | Input/output guardrails and tripwires **[INFERRED]** | [10.3](../README.md#103-agents-sdk-exceptions-and-run-level-handlers), [10.5](../README.md#105-structured-worker-results-with-partial-results), [10.7](../README.md#107-coordinator-decisions-and-the-anti-patterns): the failure side only (the four tripwire exceptions become non-retryable `policy_blocked` results). Designing guardrails is in [Chapter 03](../../03-agents-sdk-and-agents-api/README.md) and [Chapter 09](../../09-escalation-human-in-the-loop/README.md) | Supporting |
| `OAI/api/design-build-agentic-systems/20` | Tracing to monitor and debug agent workflows **[INFERRED]** | [10.9](../README.md#109-tracing-for-debugging-failures); More self-check questions 4 | Supporting |
| `OAI/api/design-build-agentic-systems/22` | Structured outputs for agent output the app consumes **[INFERRED]** | [10.5](../README.md#105-structured-worker-results-with-partial-results) (`WorkerResult` as `output_type`) | Supporting |
| `OAI/api/optimize-ai-app-performance/1` | Use production evidence to judge behavior under real traffic | [10.9](../README.md#109-tracing-for-debugging-failures) (function-span errors, request IDs, production failures as eval cases) | Supporting |
| `OAI/api/optimize-ai-app-performance/6` | Trade-offs between quality, latency, throughput, reliability and cost | [10.2](../README.md#102-openai-client-errors-retries-and-timeouts), [10.6](../README.md#106-local-recovery-before-propagation): the reliability side (retry budgets, deadlines, concurrency caps vs latency and cost); More self-check questions 1 | Supporting |
| `OAI/api/optimize-ai-app-performance/12` | Production observability, guardrails and reliability **[INFERRED]** | [10.2](../README.md#102-openai-client-errors-retries-and-timeouts), [10.9](../README.md#109-tracing-for-debugging-failures), [10.10](../README.md#1010-background-mode-and-managed-runtime-failure-statuses) | Supporting |
| `OAI/api/optimize-ai-app-performance/17` | Production readiness: rate-limit tiers, billing limits **[INFERRED]** | [10.1](../README.md#101-error-categories-on-the-openai-platform), [10.2](../README.md#102-openai-client-errors-retries-and-timeouts): the error side only (rate-limit and billing/spend-limit `429`s); Self-check Q2. Usage tiers and setting the limits are in [Chapter 07](../../07-batch-and-cost/README.md) | Supporting |
| `OAI/bootcamp/api-builder/12` | Guardrails and guardrail tripwires | [10.3](../README.md#103-agents-sdk-exceptions-and-run-level-handlers): handling tripwire exceptions | Supporting |
| `OAI/bootcamp/api-builder/13` | Tracing | [10.9](../README.md#109-tracing-for-debugging-failures) | Supporting |
| `OAI/bootcamp/api-builder/15` | From a single agent to agent-as-tool delegation | [10.5](../README.md#105-structured-worker-results-with-partial-results) | Supporting |
| `OAI/bootcamp/api-builder/32` | Observability, guardrails and reliability | [10.2](../README.md#102-openai-client-errors-retries-and-timeouts), [10.6](../README.md#106-local-recovery-before-propagation), [10.9](../README.md#109-tracing-for-debugging-failures) | Supporting |
| `OAI/tracks/building-agents/16` | Built-in tracing (which tools, agents and guardrails fired) | [10.9](../README.md#109-tracing-for-debugging-failures) | Supporting |
| `OAI/tracks/building-agents/18` | Multi-agent benefits: separation of concerns, parallelism | [10.5](../README.md#105-structured-worker-results-with-partial-results) (parallel workers that fail independently); Self-check Q4 | Supporting |
| `OAI/tracks/building-agents/21` | Structured outputs for app-consumed output, and output guardrails | [10.5](../README.md#105-structured-worker-results-with-partial-results), [10.8](../README.md#108-coverage-annotations-in-the-final-synthesis) | Supporting |
| `OAI/tracks/ai-app-development/28` | Production setup: rate-limit tiers, billing limits, best practices | [10.2](../README.md#102-openai-client-errors-retries-and-timeouts): handling rate-limit and billing-limit errors. Tiers and limits themselves are in [Chapter 07](../../07-batch-and-cost/README.md) | Supporting |
| `ROLE/ARCH/5` | Resilience patterns: retries/backoff, fallbacks, rate-limit handling, circuit breakers | [10.2](../README.md#102-openai-client-errors-retries-and-timeouts), [10.6](../README.md#106-local-recovery-before-propagation) (one owning retry layer, deadlines, half-open circuit breaker), [10.7](../README.md#107-coordinator-decisions-and-the-anti-patterns) (reroute as fallback); More self-check questions 1. Cross-region inference is not covered here | Primary |
| `ROLE/AGENT/2` | Tool design, including tool errors and tool-result flow | [10.4](../README.md#104-tool-errors-as-data): the tool-error half (errors as data, timeouts, idempotency); Self-check Q3. Schema design is in [Chapter 02](../../02-function-calling-and-structured-outputs/README.md) | Supporting |
| `ROLE/AGENT/4` | Multi-agent orchestration and sub-agents | [10.5](../README.md#105-structured-worker-results-with-partial-results), [10.7](../README.md#107-coordinator-decisions-and-the-anti-patterns) | Supporting |
| `ROLE/AGENT/6` | Human-in-the-loop, escalation paths, stop conditions | [10.3](../README.md#103-agents-sdk-exceptions-and-run-level-handlers) (`max_turns`, `error_handlers`), [10.7](../README.md#107-coordinator-decisions-and-the-anti-patterns) (escalate permission/policy, stop on billing); More self-check questions 2 | Supporting |
| `ROLE/SAFE/3` | Hallucination mitigation (no invented content for missing sections) | [10.1](../README.md#101-error-categories-on-the-openai-platform) (silent suppression), [10.8](../README.md#108-coverage-annotations-in-the-final-synthesis) (coverage annotations computed in code); Self-check Q1 | Supporting |
| `ROLE/OBS/1` | LLM/agent tracing and observability | [10.9](../README.md#109-tracing-for-debugging-failures) | Supporting |
| `ROLE/OBS/4` | Troubleshooting and root-cause analysis (tool errors, context overflow) | [10.9](../README.md#109-tracing-for-debugging-failures), [10.10](../README.md#1010-background-mode-and-managed-runtime-failure-statuses): tool errors and terminal statuses; context overflow appears only as an error code here (see [Chapter 11](../../11-context-management/README.md)) | Supporting |
| `ROLE/OBS/5` | Operational readiness and incident response | [10.2](../README.md#102-openai-client-errors-retries-and-timeouts), [10.10](../README.md#1010-background-mode-and-managed-runtime-failure-statuses) (request IDs for support, recovery procedure) | Supporting |

## More self-check questions

**1.** The client has default retries, the agent has `ModelRetrySettings(max_retries=3)`, a decorator retries each worker run twice, and the coordinator re-dispatches failed workers once. During an outage, one report triggers hundreds of model calls. What is the architect's fix?

- A) Add a fifth retry layer with a circuit breaker on top
- B) Give each failure type one owning layer with a small bounded budget and a wall-clock deadline, set the other layers to zero or account for them, and cap concurrency
- C) Remove all retries everywhere
- D) Switch to background mode so retries don't count

<details><summary>Answer</summary>

**B.** Nested retries multiply. OpenAI's rate-limit guide says to limit attempts and total time and to disable SDK retries or count them when your application manages retries. A adds yet another layer. C loses legitimate recovery from transient errors. D doesn't change the arithmetic.
</details>

**2.** A worker queries a licensed database and gets "403: subscription expired" for one source. Which response is correct?

- A) Retry with exponential backoff until the subscription is renewed
- B) Report `failure_type="permission"`, `retryable=False`, keep any findings from other sources, annotate the section as partial or not covered, and escalate the access problem
- C) Ask the model to find the same data on the open web and present it as the licensed source
- D) Abort the whole report

<details><summary>Answer</summary>

**B.** Permission errors are not retryable and need a human or an admin. A loops on a non-transient error. C misattributes data (and [Claude Chapter 12](../../../anthropic-claude/12-provenance/README.md) covers why provenance matters). D throws away the healthy sections.
</details>

**3.** A background response for a long analysis comes back with `status == "incomplete"` and `incomplete_details.reason == "max_output_tokens"`. A teammate proposes resubmitting it until it completes. What do you say?

- A) Agree; `incomplete` is a transient failure
- B) Disagree: `incomplete` is not `failed`. A resubmission with the same settings will hit the same budget. Raise `max_output_tokens` (or split the task), and never parse the partial output
- C) Agree, but add exponential backoff
- D) Cancel the response and switch to Chat Completions

<details><summary>Answer</summary>

**B.** `incomplete` with `max_output_tokens` is a budget problem, so retrying unchanged repeats it, and partial output (especially partial JSON) is not trustworthy. A and C misclassify the failure. D changes API without addressing the cause.
</details>

**4.** A run "succeeded", but the final report is thin. You want to find out which tool calls failed and why. Where do you look first?

- A) The coordinator's final output text
- B) The trace: function spans of the failing tool carry the error ("Error running tool (non-fatal)" with the error data), your `custom_span` per worker shows `partial_failure`, and logged request IDs link to API-level failures
- C) The OpenAI usage dashboard
- D) Re-run the workflow with `temperature=0` to reproduce it

<details><summary>Answer</summary>

**B.** Handled tool errors don't fail the run, but they are recorded on the function span, and worker-level spans with `set_error` make partial failures visible. A shows only what the model chose to say. C shows spend, not causes. D doesn't show which tool failed or why.
</details>

## Share your progress

```text
OpenAI Chapter 10: error handling in multi-agent systems.

3 takeaways:
1. A 429 isn't always "slow down". credit_balance_exhausted is a 429 too. Classify by error.code, and remember the SDK already retried twice.
2. The Agents SDK's default tool error is "An error occurred... Please try again." Replace it with category + retryable + suggestion.
3. Workers return a structured result with partial findings; the report says FULL / PARTIAL / NOT COVERED, computed in code.

#OpenAI #AgentsSDK #MultiAgent #AIArchitecture #BuildInPublic
```
