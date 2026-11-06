# Chapter 10 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Requirement IDs come from the official exam guides (via the repo's requirements checklist), the Anthropic Academy course outcomes and the Applied AI architect role map. This table feeds the repo coverage matrix. "Primary" means this chapter is the main place the item is taught; "Supporting" means it is taught mainly in another chapter (or a capstone or exam-prep page) and reinforced here. "(that part)" marks a broad requirement of which this chapter covers only the slice named.

| Requirement ID | What it asks | Where in this chapter | Depth |
|---|---|---|---|
| `CCAR-F/D5/5.3/K1` | Structured error context (failure type, attempted query, partial results, alternatives) enables coordinator recovery | [10.6](../README.md#106-the-structured-subagent-result); 01_practice 10.6 | Primary |
| `CCAR-F/D5/5.3/K2` | Access failures (timeouts needing retry decisions) vs valid empty results | [10.3](../README.md#103-access-failure-vs-valid-empty-result); 01_practice 10.3 | Primary |
| `CCAR-F/D5/5.3/K3` | Why generic statuses ("search unavailable") hide context from the coordinator | [10.4](../README.md#104-structured-error-responses-from-tools), [10.6](../README.md#106-the-structured-subagent-result), [10.7](../README.md#107-error-handling-anti-patterns) | Primary |
| `CCAR-F/D5/5.3/K4` | Silent suppression and terminating the whole workflow are both anti-patterns | [10.3](../README.md#103-access-failure-vs-valid-empty-result), [10.7](../README.md#107-error-handling-anti-patterns), [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide); 01_practice 10.7 | Primary |
| `CCAR-F/D5/5.3/S1` | Return failure type, what was attempted, partial results and alternatives | [10.6](../README.md#106-the-structured-subagent-result); 01_practice 10.6 (`parse_final_message`); mini-project (`research_subagent`, `run_job`) | Primary |
| `CCAR-F/D5/5.3/S2` | Distinguish access failures from valid empty results in error reporting | [10.3](../README.md#103-access-failure-vs-valid-empty-result), [10.6](../README.md#106-the-structured-subagent-result); 02_homework Ex. 3 | Primary |
| `CCAR-F/D5/5.3/S3` | Subagents recover locally from transient failures; propagate only what they cannot resolve, with attempts and partial results | [10.5](../README.md#105-local-recovery-before-propagation); 02_homework Ex. 2 | Primary |
| `CCAR-F/D5/5.3/S4` | Synthesis output with coverage annotations (well-supported vs gaps from unavailable sources) | [10.9](../README.md#109-coverage-annotations-in-the-final-synthesis); mini-project; 02_homework Ex. 5 | Primary |
| `CCAR-F/D2/2.2/S3` | Local error recovery inside subagents; propagate unresolved errors with partial results and what was attempted | [10.5](../README.md#105-local-recovery-before-propagation), [10.6](../README.md#106-the-structured-subagent-result); 02_homework Ex. 2 | Primary |
| `CCAR-F/APPX/IN/7` | Error handling and propagation: structured errors, transient vs business vs permission, local recovery before escalation | [10.2](../README.md#102-error-categories-and-the-retryable-flag), [10.4](../README.md#104-structured-error-responses-from-tools), [10.5](../README.md#105-local-recovery-before-propagation), [10.6](../README.md#106-the-structured-subagent-result) | Primary |
| `CCAR-F/D2/2.2/K1` | MCP `isError` flag pattern | [10.2](../README.md#102-error-categories-and-the-retryable-flag), [10.4](../README.md#104-structured-error-responses-from-tools) (MCP server side in Chapter 4) | Supporting |
| `CCAR-F/D2/2.2/K2` | Transient vs validation vs business vs permission errors | [10.2](../README.md#102-error-categories-and-the-retryable-flag); 02_homework Ex. 1 | Supporting |
| `CCAR-F/D2/2.2/K3` | Uniform "Operation failed" responses prevent recovery decisions | [10.4](../README.md#104-structured-error-responses-from-tools), [10.7](../README.md#107-error-handling-anti-patterns) | Supporting |
| `CCAR-F/D2/2.2/K4` | Retryable vs non-retryable errors; metadata prevents wasted retries | [10.2](../README.md#102-error-categories-and-the-retryable-flag), [10.5](../README.md#105-local-recovery-before-propagation) | Supporting |
| `CCAR-F/D2/2.2/S1` | `errorCategory`, `isRetryable` and a human-readable description | [10.4](../README.md#104-structured-error-responses-from-tools) | Supporting |
| `CCAR-F/D2/2.2/S2` | `retriable: false` plus a customer-friendly explanation for business-rule violations | [10.4](../README.md#104-structured-error-responses-from-tools) | Supporting |
| `CCAR-F/D2/2.2/S4` | Access failures vs valid empty results | [10.3](../README.md#103-access-failure-vs-valid-empty-result) | Supporting |
| `CCAR-F/D1/1.2/K1` | Hub-and-spoke: the coordinator owns error handling and routing | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.6](../README.md#106-the-structured-subagent-result) | Supporting |
| `CCAR-F/D1/1.2/S4` | Route subagent communication through the coordinator for consistent error handling | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.6](../README.md#106-the-structured-subagent-result) | Supporting |
| `CCAR-F/SC3` | Scenario: Multi-Agent Research System | Whole chapter; mini-project | Supporting |
| `CCAR-F/SQ8` | Sample question: subagent timeout → structured error context | [10.6](../README.md#106-the-structured-subagent-result); Self-check Q1 | Supporting |
| `CCAR-F/EX4/4` | Exercise: simulate a subagent timeout, continue with partial results, annotate gaps | Mini-project (01_practice) | Supporting |
| `CCAR-F/EX1/3` | Exercise: structured tool errors; agent retries transient errors and explains business errors | [10.4](../README.md#104-structured-error-responses-from-tools); 01_practice 10.4 tool loop | Supporting |
| `CCAR-F/PREP/1` | Preparation: Agent SDK agentic loop with error handling (error-handling part) | [10.5](../README.md#105-local-recovery-before-propagation), [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide); notebooks | Supporting |
| `CCAR-F/PREP/3` | Preparation: structured error responses with categories and retry flags | [10.4](../README.md#104-structured-error-responses-from-tools) | Supporting |
| `CCAR-F/MQC/7` | Sound reliability decisions, including error handling | Whole chapter | Supporting |
| `CCAR-F/APPX/TECH/2` | MCP `isError` flag (that part of the MCP technology list) | [10.4](../README.md#104-structured-error-responses-from-tools) | Supporting |
| `CCAR-F/APPX/IN/18` | Coverage-gap reporting (that part of information provenance) | [10.9](../README.md#109-coverage-annotations-in-the-final-synthesis) (claim-level provenance in Chapter 12) | Supporting |
| `CCAR-F/APPX/IN/3` | Crash recovery using manifests (that part of subagent context management) | [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) (full treatment in Chapter 11) | Supporting |
| `CCDV-F/D4/4.1/S1` | Debugging and error handling for Claude applications | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.2](../README.md#102-error-categories-and-the-retryable-flag), [10.6](../README.md#106-the-structured-subagent-result), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D4/4.1/K1` | Error type identification | [10.2](../README.md#102-error-categories-and-the-retryable-flag); 02_homework Ex. 1 | Supporting |
| `CCDV-F/D4/4.1/K2` | Recovery strategy selection | [10.5](../README.md#105-local-recovery-before-propagation), [10.6](../README.md#106-the-structured-subagent-result) | Supporting |
| `CCDV-F/D4/4.1/K3` | Trace analysis to identify failure modes | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D4/4.1/K4` | Problem origin isolation: integration layer vs model output | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide); 01_practice 10.1 | Supporting |
| `CCDV-F/PURPOSE/5` | Debug failure modes through trace analysis; monitor production quality (that part) | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D8/8.1/K4` | Error handling in tool implementation | [10.4](../README.md#104-structured-error-responses-from-tools), [10.5](../README.md#105-local-recovery-before-propagation) | Supporting |
| `CCDV-F/PURPOSE/2` | Error handling when integrating the API and SDKs (that part) | [10.2](../README.md#102-error-categories-and-the-retryable-flag) | Supporting |
| `ACAD/claude-certified-developer-foundations/4/LO3` | Distinguish retriable errors from terminal ones | [10.2](../README.md#102-error-categories-and-the-retryable-flag), [10.5](../README.md#105-local-recovery-before-propagation) | Supporting |
| `ACAD/claude-certified-developer-foundations/4/LO4` | Stay inside cost, latency and reliability budgets across coordinating agents | [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-developer-foundations/LO6` | Keep a system inside its cost, latency and reliability budget (that part) | [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-architect-professional/2/LO2` | Reliability patterns: retries, fallbacks, circuit breakers (that part) | [10.5](../README.md#105-local-recovery-before-propagation), [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-architect-professional/LO2` | Reliability patterns from POC to production (that part) | [10.5](../README.md#105-local-recovery-before-propagation), [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D5/5.2/S1` | Risks, limitations and failure modes of LLM systems | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.7](../README.md#107-error-handling-anti-patterns) | Supporting |
| `CCAR-P/D4/4.4/S1` | Diagnose system issues | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D4/4.6/S1` | Monitor with logging and observability | [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D3/3.4/S1` | Observability challenges and monitoring strategies at scale | [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/PURPOSE/5` | Evaluation, monitoring and observability practices (observability part) | [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/D2/2.1/S1` | Judge Claude outputs for accuracy and completeness | [10.9](../README.md#109-coverage-annotations-in-the-final-synthesis) | Supporting |
| `CCAO-F/D2/2.4/S1` | Decide when human review or more verification is needed | [10.9](../README.md#109-coverage-annotations-in-the-final-synthesis) | Supporting |
| `ROLE/ARCH/5` | Resilience patterns: retries/backoff, fallbacks, rate limits, circuit breakers | [10.2](../README.md#102-error-categories-and-the-retryable-flag), [10.5](../README.md#105-local-recovery-before-propagation), [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide) | Supporting |
| `ROLE/AGENT/2` | Handle tool errors and tool-result flow | [10.4](../README.md#104-structured-error-responses-from-tools) | Supporting |
| `ROLE/AGENT/4` | Multi-agent orchestration and coordination | [10.6](../README.md#106-the-structured-subagent-result), [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide) | Supporting |
| `ROLE/OBS/1` | Trace prompts, tool calls and agent steps | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `ROLE/OBS/4` | Troubleshoot GenAI-specific failures (tool errors) | [10.1](../README.md#101-where-failures-happen-in-a-multi-agent-system-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `ROLE/OBS/5` | Operational readiness for AI systems (that part) | [10.8](../README.md#108-timeouts-budgets-and-graceful-degradation-expanded-beyond-the-guide), [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) | Supporting |
| `ROLE/EVAL/5` | Cluster failures from traces and iterate (that part) | [10.10](../README.md#1010-observing-and-debugging-failures-expanded-beyond-the-guide) ("Read failures as data") | Supporting |

## More self-check questions

**Q1. (Customer support agent, MCP tools)** A `process_refund` tool rejects a $820 refund because the self-service limit is $500. The agent currently sees `isError: true` with the text "Operation failed", and it retries the call three times before apologizing vaguely. What fix addresses the root cause?

- A) Add a system-prompt rule: "never retry refunds"
- B) Return a structured error: `errorCategory: "business"`, `isRetryable: false`, a clear message about the limit, customer-friendly wording and the alternatives (escalate, partial credit)
- C) Return the rejection as a successful result with `"refunded": false`
- D) Raise a protocol-level (JSON-RPC) error so the client stops the conversation

<details><summary>Answer</summary>

**B.** The agent retried because it could not tell a policy rejection from a glitch. A category and a retry flag remove the guess, and customer-friendly wording lets it explain the outcome properly and offer escalation. A patches one symptom with a prompt rule. C hides the failure from any logic that checks `isError`. D misuses the protocol channel, which is meant for unknown tools and malformed requests. Clients may not pass a protocol error to the model at all, and even when they do, it carries no category or retry guidance, so the model is unlikely to recover.
</details>

**Q2. (Production reliability)** A coordinator starts four independent research subagents with `asyncio.TaskGroup`. When one of them raises an unexpected `KeyError`, the run ends with an `ExceptionGroup` and no report, although the other three were nearly finished. What is the best fix?

- A) Retry the whole run up to three times
- B) Wrap each subagent so it always returns a structured result (catching timeouts and unexpected exceptions into a failed envelope with its own deadline), and let the coordinator continue with the others
- C) Run the subagents sequentially so a failure is easier to debug
- D) Catch the `ExceptionGroup` at the top level and return a generic "research failed" message

<details><summary>Answer</summary>

**B.** `TaskGroup` cancels sibling tasks on the first failure, which turns one bug into a lost run. Isolating each subagent behind an envelope keeps the other results and reports the failure precisely. A repeats the same failure and multiplies cost. C gives up the parallelism without solving anything. D is a generic status that discards all completed work.
</details>

**Q3. (Production reliability)** During a period of `529 overloaded_error` responses, your API bill and latency spike. Each Messages API call uses the SDK defaults, each subagent makes up to three attempts per call, and the coordinator runs a failed subagent up to three times. What should you change first?

- A) Raise every retry count so more tasks eventually succeed
- B) Retry each failure at one layer only (keep the SDK's bounded backoff, or the subagent's, not both), make the coordinator change approach rather than repeat, and add a circuit breaker that fails fast while the API is overloaded
- C) Switch all calls to `max_retries=0` and fail immediately
- D) Treat 529 as a permission error and escalate every occurrence to a human

<details><summary>Answer</summary>

**B.** Stacked retries multiply: up to 3 (SDK attempts) × 3 × 3 = 27 calls per task, which makes an overload worse. Bounded retries at one layer, plus a circuit breaker, keep the system responsive and let the coordinator degrade gracefully. A amplifies the problem. C over-corrects and throws away cheap recoveries from brief blips. D misclassifies a transient error.
</details>

**Q4. (Multi-agent research system)** Every subagent reports `status: "success"`, yet the final report on "AI in creative industries" covers only digital art, graphic design and photography. The coordinator logs show exactly those three subtasks. What is the most likely cause?

- A) The subagents are suppressing timeouts as empty results
- B) The synthesis step lacks coverage-annotation instructions
- C) The coordinator decomposed the topic too narrowly, so music, film and literature were never assigned
- D) The web-search subagent's queries are too short

<details><summary>Answer</summary>

**C.** No component failed; the plan itself was incomplete. Error handling and coverage annotations can only report gaps in work that was assigned. A has no supporting evidence, since every subagent succeeded. B would not help, because the missing topics were never in the plan. D does not explain why whole domains are absent.
</details>

## Share your progress

```text
Chapter 10 of my Claude Certified Architect journey: multi-agent error handling.

Multi-agent systems don't fail loudly. They fail politely, with a confident report built on a timeout.

3 takeaways:
1. "0 results" is a finding. "Timeout" is not. Never let one pose as the other.
2. Recover locally, propagate the rest with context: what failed, what you tried, what you kept.
3. Ship partial results with coverage annotations instead of hiding gaps or failing the run.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #MultiAgent #AIArchitecture #BuildInPublic
```
