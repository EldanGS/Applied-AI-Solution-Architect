# Chapter 7 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Requirement IDs come from the official exam guides and Academy course outlines (see the [Claude path overview](../../README.md)). This table feeds the repo coverage matrix. **Primary** means this chapter is where the item is taught in full; **Supporting** means it is applied or introduced here and taught in full elsewhere (or is listed for context).

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `CCAR-F/D4/4.5/K1` | Batches: 50% savings, up to 24 h, no latency SLA | [7.1](../README.md#71-what-the-message-batches-api-is), [7.8](../README.md#78-sla-planning-and-submission-cadence); practice 7.1, 7.8 | Primary |
| `CCAR-F/D4/4.5/K2` | Batch fits non-blocking, latency-tolerant work; not blocking pre-merge checks | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements); practice batch-vs-sync classifier | Primary |
| `CCAR-F/D4/4.5/K3` | No multi-turn tool calling within a single batch request | [7.3](../README.md#73-what-can-and-cannot-be-batched) (client tools vs server tools, `tool_use` vs `pause_turn`) | Primary |
| `CCAR-F/D4/4.5/K4` | `custom_id` for request/response correlation | [7.4](../README.md#74-designing-custom_id), [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures); homework Exercise 1 | Primary |
| `CCAR-F/D4/4.5/S1` | Match API to latency needs: sync for pre-merge, batch for overnight/weekly | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [Self-check 1](../README.md#self-check); homework Exercise 2 | Primary |
| `CCAR-F/D4/4.5/S2` | Submission frequency from SLA (4 h windows for a 30 h SLA) | [7.8](../README.md#78-sla-planning-and-submission-cadence), [Self-check 4](../README.md#self-check); practice SLA calculator; homework Exercise 4 | Primary |
| `CCAR-F/D4/4.5/S3` | Resubmit only failed documents by `custom_id`, with modifications (chunking) | [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures), [Self-check 3](../README.md#self-check); homework Exercise 6 | Primary |
| `CCAR-F/D4/4.5/S4` | Prompt refinement on a sample before large batches | [7.7](../README.md#77-pre-flight-refine-on-a-sample-before-the-big-run), [More self-check questions 3](#more-self-check-questions); practice sample-refinement section | Primary |
| `CCAR-F/APPX/TECH/6` | Batches: savings, 24 h window, `custom_id`, polling, no multi-turn tool calling | [7.1](../README.md#71-what-the-message-batches-api-is), [7.3](../README.md#73-what-can-and-cannot-be-batched), [7.4](../README.md#74-designing-custom_id), [7.5](../README.md#75-tracking-a-batch-polling-streaming-results-cancel-and-delete) | Primary |
| `CCAR-F/APPX/IN/15` | Batch appropriateness, latency tolerance, failure handling by `custom_id` | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures) | Primary |
| `CCAR-F/SQ11` | Official sample: batch the overnight report only, keep the pre-merge check synchronous | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [Self-check 1](../README.md#self-check) | Primary |
| `CCAR-F/SQ10` | Official sample: there is no `--batch` flag in Claude Code (use `claude -p`) | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements) (vocabulary trap; full treatment in [Chapter 5](../../05-claude-code/README.md)) | Supporting |
| `CCAR-F/EX3/4` | Exercise: 100 docs in a batch, failures by `custom_id`, resubmit with chunking, SLA calculation | [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures), [7.8](../README.md#78-sla-planning-and-submission-cadence); practice mini-project (100 documents) | Primary |
| `CCAR-F/PREP/4` | Practice batch processing in a structured extraction pipeline | Practice mini-project (Pydantic validation, nullable fields, resubmission) | Supporting |
| `CCAR-F/D4/4.4/K2` | Retries cannot help when the information is absent from the source | [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures) ("Information absent from the source" row), [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5); full treatment in [Chapter 6](../../06-prompt-engineering/README.md) | Supporting |
| `CCAR-F/D4/4.4/S2` | Tell when a retry will work (format errors) and when it will not (missing info) | [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures) triage table, [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) | Supporting |
| `CCAR-F/D5/5.3/K4` | Neither silently suppress errors nor stop the whole workflow on one failure | [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) (reconciliation; one errored request never blocks the rest) | Supporting |
| `CCAR-F/D5/5.3/S1` | Structured error context: failure type, what was attempted, partial results | [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) (structured failure records) | Supporting |
| `CCAR-F/D5/5.3/S4` | Coverage annotations on output | [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) (coverage report); practice mini-project report | Supporting |
| `CCAR-F/D5/5.4/K4` | Structured state persistence / manifests for crash recovery | [7.5](../README.md#75-tracking-a-batch-polling-streaming-results-cancel-and-delete) (`submit_once`), [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5); full treatment in [Chapter 11](../../11-context-management/README.md) | Supporting |
| `CCAR-F/D5/5.5/K1` | Aggregate accuracy can hide weak document types or fields | [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) (exam trap), practice sample refinement by document type | Supporting |
| `CCAR-F/D5/5.5/S4` | Route low-confidence or ambiguous extractions to human review | [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5); full treatment in [Chapter 9](../../09-escalation-human-in-the-loop/README.md) | Supporting |
| `CCAR-F/EX3/5` | Exercise: human review routing and accuracy by document type and field | [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5), practice mini-project review queue; full treatment in [Chapter 9](../../09-escalation-human-in-the-loop/README.md) | Supporting |
| `CCAR-F/APPX/OUT/11` | Out of scope for CCAR-F: rate limiting, quotas, pricing calculations | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (exam-scope note); taught anyway for CCDV-F and the job | Supporting |
| `CCDV-F/PURPOSE/6` | Manage model tiers, tokens, caching and batch processing for cost and latency | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Primary |
| `CCDV-F/D2/2.3/K9` | Batch API use | [7.1](../README.md#71-what-the-message-batches-api-is), [7.3](../README.md#73-what-can-and-cannot-be-batched), [7.5](../README.md#75-tracking-a-batch-polling-streaming-results-cancel-and-delete), [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures); practice `FakeBatchAPI` sections | Primary |
| `CCDV-F/D2/2.3/K10` | Trade-offs between realtime and batch API selection | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements); homework Exercise 2 | Primary |
| `CCDV-F/SQ1` | Official sample: 10,000 overnight documents, cost-driven: Message Batches API | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements) (workload table) | Primary |
| `CCDV-F/D5/5.4/K1` | Token budgeting | [7.7](../README.md#77-pre-flight-refine-on-a-sample-before-the-big-run) (`count_tokens` pre-flight), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `CCDV-F/D5/5.4/K2` | Token usage tracking | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (sum `usage` from results) | Supporting |
| `CCDV-F/D5/5.4/K3` | Cost modeling | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (worked example); homework Exercise 5 | Primary |
| `CCDV-F/D5/5.4/K4` | Prompt caching | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (caching stacked on the batch discount) | Supporting |
| `CCDV-F/D5/5.4/K5` | Cache check-pointing (breakpoints) | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (explicit `cache_control` on the last shared block) | Supporting |
| `CCDV-F/D5/5.3/K3` | Quality / latency / cost trade-offs | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `CCDV-F/MQC/3` | Trade-offs in model selection (cost, latency, capability) | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (model-tier rows: Haiku 5.5, legacy Haiku 4.5; quality check first) | Supporting |
| `CCDV-F/D2/2.4/K3` | Asynchronous programming | [7.5](../README.md#75-tracking-a-batch-polling-streaming-results-cancel-and-delete) (submit, persist, poll with backoff, stream results) | Supporting |
| `ACAD/claude-certified-developer-foundations/1/LO4` | Sync vs streaming access, and async patterns for high-volume work | [7.1](../README.md#71-what-the-message-batches-api-is), [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [7.5](../README.md#75-tracking-a-batch-polling-streaming-results-cancel-and-delete) | Supporting |
| `ACAD/claude-certified-developer-foundations/2/LO8` | Submit high-volume workloads with the Message Batches API | [7.1](../README.md#71-what-the-message-batches-api-is)–[7.6](../README.md#76-result-types-and-resubmitting-only-the-failures) | Primary |
| `ACAD/claude-with-the-anthropic-api/LO6` | Tool use with custom tools, batch operations and web search | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements) (batch-tool vocabulary), [7.3](../README.md#73-what-can-and-cannot-be-batched) (tools inside batches) | Supporting |
| `ACAD/claude-with-the-anthropic-api/LO9` | Prompt caching strategies to optimize API usage | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `ACAD/claude-in-amazon-bedrock/38` | "Batch tool use" lesson (disambiguated from this API) | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements) (vocabulary trap: what the pattern is, and why it is not this API) | Supporting |
| `ACAD/claude-in-amazon-bedrock/LO3` | Custom tools with JSON Schema, and batch processing | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements) (vocabulary trap), [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (Bedrock batch inference) | Supporting |
| `ACAD/claude-with-google-vertex/41` | "The batch tool" lesson (disambiguated from this API) | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements) (vocabulary trap: what the pattern is, and why it is not this API) | Supporting |
| `CCAR-P/D1/1.6/S1` | Align solutions to business value pillars, including performance SLAs | [7.8](../README.md#78-sla-planning-and-submission-cadence) (SLA arithmetic), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (cost) | Supporting |
| `CCAR-P/D1/1.6/K4` | Cost as a value pillar | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `CCAR-P/D1/1.6/K5` | Performance SLAs as a value pillar | [7.8](../README.md#78-sla-planning-and-submission-cadence) | Supporting |
| `CCAR-P/D4/4.1/K2` | Latency as an evaluation metric | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [7.8](../README.md#78-sla-planning-and-submission-cadence) | Supporting |
| `CCAR-P/D4/4.1/K3` | Cost as an evaluation metric | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (cost per document from `usage`), [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) (coverage report) | Supporting |
| `CCAR-P/D4/4.5/S1` | Optimize token usage, latency and cost-performance trade-offs | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice), [cheat-sheet](../README.md#cheat-sheet) | Supporting |
| `CCAR-P/MQC/3` | Trade-offs in cost, latency, performance, safety and maintainability | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice), [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) | Supporting |
| `ACAD/claude-certified-architect-professional/2/LO2` | Map cost and latency to a budget; reliability patterns | [7.8](../README.md#78-sla-planning-and-submission-cadence), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice), [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) | Supporting |
| `ACAD/claude-certified-architect-professional/2/LO3` | Estimate call volume, token consumption and cost | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (worked example) | Supporting |
| `ACAD/claude-certified-architect-professional/4/LO5` | Choose the deployment entry point (direct API, Bedrock, Vertex, third party) | [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (batch availability per platform) | Supporting |
| `CCAO-F/PURPOSE/4` | Balance quality, efficiency and cost | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (Haiku 5.5 and Haiku 4.5 batch rows) | Supporting |
| `CCAO-F/D3/3.3/S1` | Faster, cheaper model for high-volume simple work | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (Haiku 5.5 batch row, quality check first) | Supporting |
| `ROLE/COST/3` | Batch processing for non-interactive workloads | Whole chapter | Primary |
| `ROLE/COST/1` | Cost-latency-quality trade-off analysis | [7.2](../README.md#72-batch-vs-synchronous-matching-the-api-to-latency-requirements), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `ROLE/COST/2` | Prompt caching | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `ROLE/COST/4` | Model routing and tiering | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice), [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures) (fallback model for refusals) | Supporting |
| `ROLE/COST/5` | Token efficiency and budgeting | [7.7](../README.md#77-pre-flight-refine-on-a-sample-before-the-big-run), [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `ROLE/COST/7` | Throughput and scaling at production volume | [7.1](../README.md#71-what-the-message-batches-api-is) (limits), [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (queue limits) | Supporting |
| `ROLE/CLOUD/7` | Quotas and rate limits | [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (batch rate-limit table) | Supporting |
| `ROLE/ARCH/5` | Resilience patterns (retries, fallbacks, idempotency) | [7.5](../README.md#75-tracking-a-batch-polling-streaming-results-cancel-and-delete), [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures), [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) | Supporting |
| `ROLE/ENT/5` | Async / queue integration patterns | [7.5](../README.md#75-tracking-a-batch-polling-streaming-results-cancel-and-delete), [7.12](../README.md#712-reliability-around-a-batch-pipeline-domain-5) | Supporting |
| `ROLE/SAFE/4` | Data privacy, zero-retention options, PHI handling | [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (not ZDR- or HIPAA-eligible) | Supporting |
| `ROLE/ENT/3` | Data governance and retention | [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (29-day retention, workspace scoping, delete) | Supporting |
| `ROLE/PROMPT/3` | Schema-validated outputs | [7.6](../README.md#76-result-types-and-resubmitting-only-the-failures) (Pydantic triage) | Supporting |
| `ROLE/OBS/1` | Token usage analytics | [7.9](../README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) (per-batch `usage` totals) | Supporting |
| `ROLE/CLOUD/1` | Claude on Amazon Bedrock | [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (no `/v1/messages/batches`; Bedrock batch inference) | Supporting |
| `ROLE/CLOUD/2` | Claude on Google Cloud (Vertex AI) | [7.11](../README.md#711-operations-rate-limits-retention-privacy-and-platforms) (Anthropic managed: Message Batches API; Google managed, formerly Vertex AI: Google Cloud batch predictions) | Supporting |

Syllabus source: community study guide by paullarionov, [Chapter 7 and Domain 4.5](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-7-message-batches-api), restructured and expanded here in my own words.

## More self-check questions

**1.** A developer writes the extraction results to the database by zipping the results stream with the original document list. QA finds that values are attached to the wrong documents. What is the fix?

- A) Sort the results by message ID before zipping
- B) Submit smaller batches so the order is preserved
- C) Key each result by its `custom_id` and look up the source document in the ledger
- D) Poll more often so results arrive in submission order

<details><summary>Answer</summary>

**C.** Batch results are not guaranteed to be in request order, at any batch size. `custom_id` is the correlation key. A, B and D all assume an ordering the API does not provide.
</details>

**2.** A nightly batch of 20,000 requests shares a 6,000-token system prompt and few-shot block marked with `cache_control`. The cache-read share is lower than expected. Which change most improves it?

- A) Remove caching, because it does not work with batches
- B) Make the prefix byte-identical with the same `cache_control` breakpoint in every request, use the 1-hour TTL, and submit the requests that share it together
- C) Move the few-shot examples to the end of each user message
- D) Switch the batch to `stream: true` so requests run in order

<details><summary>Answer</summary>

**B.** Batch cache hits are best-effort; identical `cache_control` blocks in every request, as much shared content as possible and requests that run close together are what the batch guide recommends, and the 1-hour TTL gives entries longer to be reused. A is false: caching works with batches and the discounts stack. C moves shared content after the varying content, which destroys the shared prefix. D is rejected by the Batches API.
</details>

**3.** Before running 50,000 contracts through a new extraction prompt in a batch, the team wants to keep resubmission cost down. What should they do first?

- A) Submit all 50,000 and resubmit whatever fails
- B) Run the prompt on a representative sample, measure first-pass success by document type, refine, and dry-run the exact request shape
- C) Use the largest model for the whole batch to avoid failures
- D) Split the job into 500 batches of 100 so failures are smaller

<details><summary>Answer</summary>

**B.** Refining on a sample maximizes first-pass success before you pay at scale, and a dry run catches invalid parameters that a batch would only report hours later. A pays for every flaw 50,000 times. C costs more and does not fix prompt problems. D changes the packaging, not the success rate.
</details>

**4.** A batch ends with `request_counts.succeeded = 1000`. Your pipeline marks all 1,000 documents complete. Later, analysts find some outputs cut off mid-JSON and a few that are polite refusals. What went wrong?

- A) Nothing; succeeded results are guaranteed to be complete and valid
- B) The pipeline did not check `stop_reason` and validate each succeeded result; truncated items need a higher `max_tokens` and refusals need a fallback model or review
- C) The batch should have been canceled and resubmitted
- D) Errored results were misreported as succeeded

<details><summary>Answer</summary>

**B.** `succeeded` only means a message was created. `stop_reason: "max_tokens"` and `stop_reason: "refusal"` both arrive as succeeded results (so does `model_context_window_exceeded`), so validate every one. A is the misconception. C and D misread how result types work.
</details>

## Share your progress

```text
Chapter 7 of my Claude Certified Architect journey: the Message Batches API. Half price, if you can wait.

3 takeaways:
1. Batch only what nobody is blocked on. Pre-merge checks stay sync; nightly reports go batch.
2. custom_id is your primary key. Results come back unordered, so resubmit only the failures.
3. Plan SLAs from the 24h bound: a 30h SLA means ~4h submission windows, not "most batches finish in an hour".

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #AIArchitecture #LLMOps #LearningInPublic
```
