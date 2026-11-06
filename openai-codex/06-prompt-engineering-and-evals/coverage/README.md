# Chapter 6 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

IDs come from this repo's requirement checklists: OpenAI Academy courses, bootcamps and developer tracks (`OAI/...`), and the role competency matrix (`ROLE/...`). Items marked **[INFERRED]** in the checklist are likely curriculum, not confirmed course content, because the Academy course internals are behind sign-in. **Primary** means a section of this chapter teaches the item and the notebooks practice it; **Supporting** means this chapter covers part of it and another chapter is its main home.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/api/evaluate-ai-applications/1` | Use evals to measure how a system performs | [6.9](../README.md#69-building-your-own-eval-harness); practice mini-project | Primary |
| `OAI/api/evaluate-ai-applications/2` | Use evals to decide whether a change makes the system better | [6.10](../README.md#610-regression-testing-and-promptfoo) (baseline vs candidate gate); practice mini-project | Primary |
| `OAI/api/evaluate-ai-applications/3` | Build representative test cases | 6.9 (datasets: production, expert, synthetic; edge and adversarial cases), [6.12](../README.md#612-error-analysis-judge-calibration-and-accuracy-targets) (structured synthetic data) | Primary |
| `OAI/api/evaluate-ai-applications/4` | Choose an eval approach that fits the task and its risks | 6.9 (ground truth vs rubric, judge modes, evals per architecture), 6.12 (accuracy targets) | Primary |
| `OAI/api/evaluate-ai-applications/5` | Diagnose failures (failure analysis) | 6.12 (open and axial coding); practice failure tally | Primary |
| `OAI/api/evaluate-ai-applications/6` | Use eval results to guide improvements | 6.12 (the flywheel, "Pull the right lever"), 6.2 (migration workflow) | Primary |
| `OAI/api/evaluate-ai-applications/7` | Prevent quality regressions | 6.10 (per-case regression gate); homework Exercise 5 | Primary |
| `OAI/api/evaluate-ai-applications/8` | Build an eval system the team can act on | 6.9–6.10; practice mini-project (harness + gate) | Primary |
| `OAI/api/evaluate-ai-applications/13` [INFERRED] | Ground-truth evals, including order-insensitive matching | 6.9 (approach table, grader types); homework Exercise 2 | Primary |
| `OAI/api/evaluate-ai-applications/14` [INFERRED] | Rubric-based evals for tasks with no ground truth | 6.9 (rubric judge, pairwise, reference-guided grading) | Primary |
| `OAI/api/evaluate-ai-applications/15` [INFERRED] | Model-graded evaluation (LLM-as-judge) and graders | 6.9 (judge guidance), 6.10 (legacy grader types), 6.12 (judge alignment) | Primary |
| `OAI/api/evaluate-ai-applications/16` [INFERRED] | Evaluation-driven development | 6.2 (migration workflow), 6.10 (evals on every change), 6.12 (flywheel) | Primary |
| `OAI/api/evaluate-ai-applications/17` [INFERRED] | Benchmark against baselines | 6.10 (baseline vs candidate) | Supporting |
| `OAI/api/evaluate-ai-applications/18` [INFERRED] | Pair evals with input and output guardrails (Moderations API) | [6.11](../README.md#611-moderation-and-safety-basics) | Supporting |
| `OAI/api/evaluate-ai-applications/19` [INFERRED] | Evals platform deprecation; tool-independent eval design | Note at the top of Concepts, 6.9, 6.10 (Promptfoo, reading and migrating a legacy eval) | Primary |
| `OAI/api/optimize-ai-app-performance/3` | Decide whether an update is ready to release | 6.10 (gate, staged rollout) | Supporting |
| `OAI/api/optimize-ai-app-performance/4` | Compare system versions | 6.10; practice mini-project (three prompt versions) | Supporting |
| `OAI/api/optimize-ai-app-performance/5` | Spot regressions across traffic segments | 6.10 (per-version, per-segment production signals) | Supporting |
| `OAI/api/optimize-ai-app-performance/13` [INFERRED] | Three levers: prompt, context (RAG), model (fine-tuning) | 6.12 ("Pull the right lever") | Supporting |
| `OAI/bootcamp/api-builder/4` | API Foundations: prompting | [6.1](../README.md#61-instructions-roles-and-message-formatting)–[6.5](../README.md#65-prompt-chaining), [6.13](../README.md#613-the-prompt-structure-toolkit) | Primary |
| `OAI/bootcamp/api-builder/5` | API Foundations: structured outputs | [6.6](../README.md#66-validation-and-retry-with-feedback), 6.13 (output constraints) | Supporting |
| `OAI/bootcamp/api-builder/14` | Agents: evals incl. model-graded evaluation; outputs that can be evaluated | 6.9 (agent evals, traces, judge), 6.6 (structured outputs) | Supporting |
| `OAI/bootcamp/api-builder/28` | Evals for quality, latency and cost trade-offs | 6.2 (effort, mode), 6.13 (few-shot token cost); cost depth in [chapter 07](../../07-batch-and-cost/README.md) | Supporting |
| `OAI/bootcamp/api-builder/29` | Benchmark model performance and compare baselines | 6.10 | Supporting |
| `OAI/bootcamp/api-builder/30` | Choose a model and optimization from eval results | 6.2 (one variable at a time), 6.12 (levers) | Supporting |
| `OAI/tracks/ai-app-development/6` | Evals with vs without ground truth | 6.9 (approach table) | Primary |
| `OAI/tracks/ai-app-development/7` | Prompt engineering; instruction following differs by model; system, developer, user prompts | 6.1 (roles, `system` vs `developer`), 6.2 (reasoning models), 6.13 (placement, delimiters) | Primary |
| `OAI/tracks/ai-app-development/9` | Structured outputs and strict schemas | 6.6, 6.13 (Structured Outputs vs JSON mode); main home [Chapter 2](../../02-function-calling-and-structured-outputs/README.md) | Supporting |
| `OAI/tracks/ai-app-development/16` | Testing and evaluation (phase) | 6.9–6.12 | Primary |
| `OAI/tracks/ai-app-development/17` | Build evals to verify correctness, benchmark with rubrics, detect regressions | 6.9, 6.10 | Primary |
| `OAI/tracks/ai-app-development/18` | Exact match vs holistic scoring for long text | 6.9 (grader types); homework Exercise 2 and Q6 | Primary |
| `OAI/tracks/ai-app-development/19` | Evals API and dashboard | 6.10 ("Reading a legacy Evals API eval": `data_source_config`, `testing_criteria`, graders, runs, results) taught for migration only, since the platform is read-only from 2026-10-31 and shuts down 2026-11-30 | Primary |
| `OAI/tracks/ai-app-development/20` | Input and output guardrails | 6.11, 6.6 (output validation) | Supporting |
| `OAI/tracks/ai-app-development/21` | Moderations API (`omni-moderation-latest`, free) as a guardrail | 6.11; practice moderation cells; homework Exercise 6 | Primary |
| `OAI/tracks/building-agents/3` | Reasoning vs non-reasoning models, reasoning effort, latency and cost | 6.2, 6.13 (chain-of-thought on reasoning models) | Supporting |
| `OAI/tracks/building-agents/20` | Input guardrails scaled to risk | 6.11 | Supporting |
| `OAI/tracks/building-agents/21` | Structured outputs for app-consumed output; output guardrails | 6.6, 6.11, 6.13 | Supporting |
| `OAI/tracks/model-optimization/3` | Use evals to monitor and optimize | 6.10, 6.12 (fine-tuning is restricted; see deprecations) | Supporting |
| `ROLE/PROMPT/1` | Advanced prompt engineering | 6.1–6.5, 6.13 | Primary |
| `ROLE/PROMPT/2` | Context engineering and context-window management | 6.1 and 6.13 (static first, placement, caching the examples) | Supporting |
| `ROLE/PROMPT/3` | Structured outputs and schema enforcement with validation and retry | 6.6, 6.7, 6.13 | Primary |
| `ROLE/PROMPT/4` | Prompt management, versioning and regression testing | [6.8](../README.md#68-prompts-as-versioned-code), 6.10 | Primary |
| `ROLE/PROMPT/5` | Reasoning control and inference parameters | 6.2, 6.13 | Supporting |
| `ROLE/PROMPT/6` | Prompt chaining and workflow decomposition | 6.5 | Supporting |
| `ROLE/EVAL/1` | Use-case-specific evaluation frameworks | 6.9, 6.12 | Primary |
| `ROLE/EVAL/2` | Automated graders, LLM-as-judge, judge calibration | 6.9, 6.12 | Primary |
| `ROLE/EVAL/3` | Representative datasets, baselines, human judgment | 6.9, 6.10, 6.12 | Primary |
| `ROLE/EVAL/4` | Online evaluation and production feedback | 6.10 (staged rollout, production signals); monitoring tooling in later chapters | Supporting |
| `ROLE/EVAL/5` | Error and transcript analysis | 6.12 | Primary |
| `ROLE/EVAL/6` | Agent evaluation | 6.9 (tool selection, argument precision, handoffs, traces) | Supporting |
| `ROLE/EVAL/7` | Regression testing and release gates | 6.10 | Primary |
| `ROLE/EVAL/8` | Red teaming and adversarial testing | 6.9 (adversarial cases), 6.10 (Promptfoo red teaming) | Supporting |
| `ROLE/EVAL/9` | Safety, bias and fairness evaluation | 6.11 | Supporting |
| `ROLE/SAFE/1` | Prompt-injection and jailbreak defense | 6.1 and 6.13 (untrusted text in the user turn, in tags) | Supporting |
| `ROLE/SAFE/2` | Guardrails, content filters and moderation | 6.11 | Supporting |
| `ROLE/SAFE/3` | Hallucination mitigation | 6.6 (nullable fields, escape hatches), 6.7, 6.9 (faithfulness judge) | Supporting |

Not covered here: Batch API, flex processing and prompt-caching economics in depth ([Chapter 07](../../07-batch-and-cost/README.md)) and RAG design (`OAI/api/build-with-rag`, see [Chapter 4](../../04-built-in-tools-and-mcp/README.md) for file search).

## More self-check questions

**1.** A team calls `gpt-6.1-sol` with `temperature=0` to "make extraction deterministic" and gets HTTP 400. What should they do?

- A) Switch to `gpt-6-astra`, which accepts `temperature`
- B) Remove `temperature`, and get consistency from the schema, examples, explicit rules and evals
- C) Set `reasoning.effort="none"` on `gpt-6.1-sol` so `temperature` is allowed
- D) Retry the request with exponential backoff

<details><summary>Answer</summary>

**B.** With reasoning effort other than `none`, GPT-6 models do not support `temperature`, `top_p` or `top_logprobs`. A is wrong: Astra does not support `none` either. C is wrong: `gpt-6.1-sol` does not support `none`. D treats a request error as a transient failure.
</details>

**2.** A prompt written for an older model begins with "Think step by step and explain all your reasoning before answering. CRITICAL: you MUST follow every rule." On `gpt-6-luna` it is slow and verbose, and quality did not improve. What is the best first change?

- A) Raise `reasoning.effort` to `max`
- B) Remove the chain-of-thought instruction and the shouting; state the goal, success criteria and output contract; set `text.verbosity`; then compare on evals
- C) Add ten more few-shot examples
- D) Move the prompt into a `v1/prompts` object so it can be tuned in the dashboard

<details><summary>Answer</summary>

**B.** OpenAI's reasoning guidance says "think step by step" prompts are unnecessary for reasoning models and absolute words should be kept for true invariants. A adds cost without fixing the prompt. C adds tokens without a measured reason. D uses an API that shuts down on 2026-11-30.
</details>

**3.** After launch, a support bot's eval suite still passes, but escalations are rising. The team has 60 failing production traces and wants new graders. What is the right order of work?

- A) Write a generic "helpfulness" judge first, then read only the traces it flags
- B) Generate 1,000 synthetic cases first and see which ones fail
- C) Read the failing traces and label each error in your own words (open coding), group the labels into a few categories and count them (axial coding), then turn the largest categories into graders and dataset slices
- D) Raise `reasoning.effort` and re-run the existing suite

<details><summary>Answer</summary>

**C.** The evaluation-flywheel cookbook starts with error analysis on real traces: open coding, then axial coding, and each category becomes a grader and a dataset slice. A relies on a generic metric, an anti-pattern in OpenAI's evaluation guide. B produces cases before you know which failure modes matter; structured synthetic data comes after the analysis. D changes the system before you know what is wrong.
</details>

**4.** Your LLM judge rates answers on a 1–10 scale. You notice it prefers longer answers and whichever answer is shown first. What change makes it most trustworthy?

- A) Switch to a 1–100 scale for finer resolution
- B) Use pass/fail or pairwise comparison with a detailed rubric, control for length, swap positions, have the judge give its rationale before the verdict, and check agreement with human labels before relying on it
- C) Run the judge three times and average the scores
- D) Replace the judge with exact-match grading on the free-text answers

<details><summary>Answer</summary>

**B.** This is OpenAI's own judge guidance: pairwise or pass/fail is more reliable, length and position bias must be controlled, reasoning before scoring helps, and the judge must agree with human annotations before you scale it. A makes the scale harder to calibrate. C averages the same bias. D cannot grade paraphrased free text.
</details>

**5.** A consumer app passes user messages straight to the Responses API. It has no abuse controls, and the team wants to add some cheaply. Which combination fits OpenAI's guidance?

- A) A developer message that says "refuse harmful requests", nothing else
- B) Moderation with `omni-moderation-latest` (free) on input and output, routed by your policy; a hashed per-user `safety_identifier`; adversarial cases in the eval set; human review for high-stakes outputs
- C) Send each user's email address as `safety_identifier` so OpenAI can contact them
- D) Automatically ban any user whose message has any non-zero `category_scores`

<details><summary>Answer</summary>

**B.** It layers the documented controls. A relies on a probabilistic prompt alone. C sends PII; the docs say to hash it. D treats scores as verdicts, which the moderation guide warns against.
</details>

**6.** A pipeline reviews each pull request with one call per changed file for local issues, then one call for cross-file issues. A teammate wants to replace it with an agent that decides on its own which file to read next, "because it is more flexible". No step depends on what an earlier step found. What should the architect say?

- A) Switch to the agent; dynamic decomposition is always more capable
- B) Replace both steps with one call that sends every file at once, since the context window is 1M tokens
- C) Keep the chain but run the per-file calls one after another so that later files see earlier findings
- D) Keep the fixed chain: code owns the flow, the per-file calls run in parallel, and each step can be inspected and evaluated on its own; use an agent loop only when the next step depends on what the last one found

<details><summary>Answer</summary>

**D.** This is the 6.5 rule: a prompt chain fits when the steps are known in advance, and it keeps intermediate outputs testable. A adds cost and unpredictability without a need for it. B brings back attention dilution, which a large window does not fix. C removes the parallelism and couples steps that are independent.
</details>

**7.** A team is migrating an existing Evals API eval before the platform shuts down. It has `data_source_config` with an `item_schema`, a `string_check` grader on `{{ sample.output_text }}` against `{{ item.correct_label }}`, and a `score_model` grader for tone. What is the right migration?

- A) Export the old run scores and keep comparing new releases against them
- B) Recreate the dataset rows as test vars, the `string_check` as an exact-match assertion (`equals`), and the `score_model` as a rubric judge (`llm-rubric` or your harness's judge); validate the recreated judge against human labels; treat the first new run as a fresh baseline
- C) Keep calling the graders API directly, since only the dashboard is shutting down
- D) Replace both graders with a single `similar` embedding assertion

<details><summary>Answer</summary>

**B.** OpenAI's migration cookbook maps testing criteria to Promptfoo assertions and says recreated graders, especially LLM-as-judge graders, must be validated before they drive regression decisions. Scores may not match across systems. A compares numbers from two different systems. C: the graders API is deprecated as part of the same transition. D throws away the exact-match check on a task that has ground truth.
</details>

## Share your progress

```text
Chapter 6 of the OpenAI branch: prompts and evals now live in git, not in a dashboard.

3 takeaways:
1. instructions is per request. Chain with previous_response_id and it's gone unless you resend it.
2. GPT-6 wants goal + success criteria + output contract. "Think step by step" and temperature=0 are out.
3. v1/prompts and the Evals platform shut down 2026-11-30. My own harness: exact match, schema, LLM judge, per-case regression gate.

#OpenAI #PromptEngineering #LLMEvals #AIArchitecture #BuildInPublic
```
