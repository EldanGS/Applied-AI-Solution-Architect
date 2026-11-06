# Chapter 07 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

There is no public OpenAI architect exam (see the [OpenAI path README](../../README.md#certification-status-read-this-first)). This table maps the chapter to the Academy, bootcamp and developer-track items, and to role competencies. Items marked **[INFERRED]** are not stated on the course page; they come from the related bootcamp session or developer track. "Practice" means `01_practice.ipynb`, and "homework" means `02_homework.ipynb`.

Section numbers (7.x), "self-check" and "cheat-sheet" refer to the [chapter README](../README.md); "More self-check questions" refers to the section below.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/api/optimize-ai-app-performance/14` | [INFERRED] Prompt caching to cut latency and cost | [7.7](../README.md#77-prompt-caching); practice 7.7 (cache break-even, `cached_tokens` / `cache_write_tokens`); self-check 3; homework Q1 | Primary |
| `OAI/api/optimize-ai-app-performance/15` | [INFERRED] Batch API (50% off) and Flex processing | 7.2–7.6; practice 7.2–7.6 and mini-project; self-check 1–2; More self-check questions 1–3; homework Q4, Q5, Q7–Q9, exercises 1–3 and 5 | Primary |
| `OAI/api/optimize-ai-app-performance/17` | [INFERRED] Production readiness: usage tiers (Build/Launch/Grow), billing limits, cost API monitoring, production best practices | 7.8, 7.10 (Costs API), 7.12; practice 7.8, 7.10, 7.12; self-check 4; More self-check questions 5; homework Q11 | Primary |
| `OAI/tracks/ai-app-development/25` | Ph4: prompt caching | 7.7; practice 7.7 | Primary |
| `OAI/tracks/ai-app-development/26` | Ph4: Batch API and Flex processing | 7.2–7.6; practice 7.2–7.6 and mini-project | Primary |
| `OAI/tracks/ai-app-development/27` | Ph4: monitor usage and cost with the cost API | 7.10 (monitoring, Costs API), 7.12; practice 7.10 (optional Costs API cell) | Primary |
| `OAI/tracks/ai-app-development/28` | Ph4: production account setup: usage tiers, billing limits, production best practices | 7.8, 7.12; practice 7.8, 7.12; More self-check questions 5; homework Q11 | Primary |
| `OAI/api/optimize-ai-app-performance/6` | Trade off quality, latency, throughput, reliability and cost | 7.1, 7.5, 7.6, 7.11; [Cheat-sheet](../README.md#cheat-sheet); homework Part C | Primary |
| `OAI/api/optimize-ai-app-performance/7` | Improve speed and cost while keeping required accuracy | 7.7, 7.11 (eval-gated cascade); practice 7.11 | Primary |
| `OAI/bootcamp/api-builder/31` | Latency and cost optimization | 7.1, 7.5–7.7; practice 7.1, 7.5–7.7 | Primary |
| `OAI/api/optimize-ai-app-performance/1` | Use production evidence to judge behavior under real traffic | 7.8 (rate-limit headers), 7.10 (usage logging, served tier, Costs API) | Supporting |
| `OAI/api/optimize-ai-app-performance/4` | Compare system versions | 7.10 (cost per successful task), 7.11 (eval-gated routing) | Supporting |
| `OAI/api/optimize-ai-app-performance/11` | [INFERRED] Benchmark models against baselines; pick a model and optimization from eval results | 7.11; practice 7.11 (strategy comparison); More self-check questions 4 | Supporting |
| `OAI/bootcamp/api-builder/28` | Evals for production trade-offs between quality, latency and cost | 7.10, 7.11 | Supporting |
| `OAI/bootcamp/api-builder/29` | Benchmark model performance and compare baselines | 7.11; practice 7.11 | Supporting |
| `OAI/bootcamp/api-builder/30` | Choose a model and optimization from eval results | 7.11; homework Q10 | Supporting |
| `OAI/bootcamp/api-builder/32` | Observability, guardrails and reliability | 7.9 (retries), 7.10 (monitoring); guardrails are in chapter 06 | Supporting |
| `OAI/tracks/ai-app-development/22` | Ph4: scalability and maintenance | 7.8, 7.9, 7.12 (scaling) | Supporting |
| `OAI/tracks/ai-app-development/23` | Ph4: three performance levers (prompt, context, model) | 7.1 (levers table), 7.11 | Supporting |
| `OAI/tracks/building-agents/3` | Reasoning effort, latency and cost trade-offs | 7.1 (reasoning tokens are output), 7.11 (effort as a lever) | Supporting |
| `OAI/tracks/building-agents/4` | Model selection: flagship vs smaller models | 7.11 | Supporting |
| `OAI/tracks/building-agents/19` | Optimize for speed, reliability or cost per use case | 7.5, 7.6; [Cheat-sheet](../README.md#cheat-sheet) | Supporting |
| `ROLE/COST/3` | Batch processing for non-interactive workloads | 7.2–7.5; practice mini-project; More self-check questions 3; homework exercises 1–3 and 5 | Primary |
| `ROLE/COST/2` | Prompt caching | 7.7; practice 7.7 | Primary |
| `ROLE/COST/1` | Cost-latency-quality trade-offs, unit economics | 7.1, 7.10; practice 7.10; homework exercise 4 | Primary |
| `ROLE/COST/4` | Model routing, cascading and tiering | 7.6 (processing tiers), 7.11 (cascade); practice 7.11 | Primary |
| `ROLE/COST/5` | Token efficiency and budgeting | 7.1, 7.8 (`max_output_tokens` and TPM), 7.10 (token counting); homework Q3 | Primary |
| `ROLE/ARCH/5` | Retries, backoff, fallbacks, rate-limit handling | 7.6 (Flex fallback), 7.9; practice 7.6, 7.9; homework Q2, Q5, Q6, exercise 6 | Primary |
| `ROLE/COST/7` | Throughput and scaling at production volume | 7.2 (limits), 7.8 (capacity planning), 7.12 (scaling) | Supporting |
| `ROLE/ARCH/3` | Model selection and trade-off reasoning | 7.11 | Supporting |
| `ROLE/CLOUD/7` | Quotas, rate limits and throughput options | 7.6 (Scale/Reserved Tier, project tier restrictions), 7.8 | Supporting |
| `ROLE/DISC/3` | Business value case and ROI | 7.10 (cost per successful task) | Supporting |
| `ROLE/OBS/1` | Token analytics and latency breakdowns | 7.10 (monitoring) | Supporting |

**Not taught here:** `OAI/api/optimize-ai-app-performance/16` and `OAI/tracks/ai-app-development/24` (distillation into smaller fine-tuned models). Self-serve fine-tuning is closed to new organizations ([7.11](../README.md#711-model-routing-and-cascades)), and these items are planned for chapter 16 (models, migration and model optimization).

## More self-check questions

**1.** A batch of 10,000 lines ends with status `expired`. 9,200 lines are in the output file; 800 are in the error file with `error.code == "batch_expired"`. The report is due in 3 hours. What should you do?

- A) Re-run all 10,000 lines in a new batch
- B) Resubmit the 800 expired `custom_id`s through Flex with a Standard fallback (or Standard directly), and keep the 9,200 results
- C) Resubmit the 800 lines as a new batch and wait
- D) Nothing; expired batches are not billed, so try again tomorrow

<details><summary>Answer</summary>

**B.** Completed requests from an expired batch are in the output file (and billed); only the 800 need to run again, and a new batch could take up to 24 hours, which misses the deadline. A pays twice for 9,200 results. C ignores the SLA. D is wrong on billing and on the deadline.
</details>

**2.** Your batch completes, but 40 lines have a `400` status: the input exceeds the model's context window. What is the right handling?

- A) Resubmit the 40 lines unchanged in a retry batch
- B) Raise `max_output_tokens` and resubmit
- C) Split or shorten those 40 documents (for example, chunk them), then resubmit only those documents, with new IDs that encode the chunk (for example `inv-7-c1__invoice-v3`) recorded in the manifest
- D) Switch the whole job to `gpt-6-astra`

<details><summary>Answer</summary>

**C.** Identify failures by `custom_id`, change the strategy, resubmit only the failures. A fails the same way. B does not affect input size. D changes cost by 100× without fixing input size (all three models share a 1.05M context window with a 922K input cap).
</details>

**3.** You must deliver extraction results for a regulatory filing 30 hours from now. Volume is 40,000 documents. What plan is sound?

- A) Submit a batch at hour 20; most batches finish in about an hour
- B) Submit by 30 − 24 − (Flex/Standard retry time) − buffer, for example within 2 hours if recovering failed lines takes 3 hours and you keep a 1-hour buffer, and keep that Flex or Standard path ready for expired or failed lines
- C) Submit at hour 6 and plan to resubmit failures as a second batch
- D) Use Fast mode for all 40,000 to be safe

<details><summary>Answer</summary>

**B.** 30 − 24 = 6 hours is the latest submission time with **no** retry path: a batch submitted at hour 6 that uses its full window leaves zero time to recover. Subtract the retry path and a buffer from that. C submits at the zero-slack point and then plans a second 24-hour batch that cannot fit. A plans on the typical case. D pays 4× the batch price when there is no user waiting.
</details>

**4.** A team proposes running every request on `gpt-6-astra` "to be safe". Volume is 2M short classification requests per month. Which recommendation best fits OpenAI's guidance?

- A) Agree: the most capable model always has the lowest error cost
- B) Evaluate Luna and Sol on a representative labeled set; route each task to the cheapest model that meets the quality bar, consider a Luna → Sol cascade on validation failure, and report cost per successful task
- C) Use Luna everywhere, since it is 100× cheaper, and skip evals
- D) Use Astra with `reasoning.effort="none"` to cut cost

<details><summary>Answer</summary>

**B.** The deployment checklist says to choose the model that performs well on representative tasks rather than routing everything to the most capable one, and the eval decides. A ignores a 100× price gap. C skips the measurement. D: Astra does not support `none`.
</details>

**5.** A company runs a nightly Batch pipeline and an interactive assistant in one OpenAI project. Last week a staging load test, also in that project, reached the hard spend limit and the assistant went down; and an ETL script quietly ran with `service_tier="fast"` for a month. Which setup addresses both problems?

- A) Raise the organization's hard spend limit and remove the spend alerts, since they only create noise
- B) Separate projects for staging and production (and for batch vs interactive work), each with its own spend limit and alerts below it; restrict the batch project's allowed service tiers so `priority`/`fast` requests fail with a `400`; log the served tier
- C) Keep one project, but wrap every call in a retry loop that backs off on `project_spend_limit_exceeded`
- D) Give the ETL team an owner role so they can see the bill

<details><summary>Answer</summary>

**B.** OpenAI's production best practices recommend separate staging and production projects with their own rate and spend limits. A project's allowed service tiers turn a wrong tier into a `400` "Invalid service_tier argument" instead of a 2× bill. A removes the early warning and keeps the shared blast radius. C retries a billing error, which cannot help. D widens billing access without preventing anything.
</details>

## Share your progress

```text
Chapter 07 of the OpenAI branch: same model, 2x-100x cost difference depending on how you call it.

3 takeaways:
1. Batch = 50% off, separate rate limits, 24h worst case. Join by custom_id, resubmit only what failed.
2. Flex is batch pricing on a sync call. Fast is 2x for latency. Log the tier that actually served you.
3. On GPT-6, cache writes cost 1.25x and reads 0.1x. Stable prefix first, explicit breakpoint after it.

#OpenAI #AIArchitecture #FinOps #LLMOps #BuildInPublic
```
