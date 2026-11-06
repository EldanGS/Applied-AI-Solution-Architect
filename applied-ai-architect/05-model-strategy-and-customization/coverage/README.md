# Chapter 05 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix. IDs come from the OpenAI Academy course and track checklists (`req_openai`), the Anthropic exam guides and Academy courses (`req_anthropic`) and the role competency matrix (`req_role`). **Primary** means this chapter is where the item is taught in depth; **Supporting** means it is applied or reinforced here and taught more fully elsewhere.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/api/scope-ai-solutions/14` | Pick the technique: prompting, RAG for knowledge, fine-tuning for behavior | [5.1](../README.md#51-the-customization-ladder-knowledge-vs-behavior) (ladder table), [cheat-sheet](../README.md#cheat-sheet), Self-check 1; practice §5.1, homework exercise 2 | Primary |
| `OAI/api/build-with-rag/23` | RAG adds knowledge; fine-tuning does not teach a model your data | [5.1](../README.md#51-the-customization-ladder-knowledge-vs-behavior) (knowledge vs behavior, exam trap), Self-check 1, More self-check questions 1 | Primary |
| `OAI/tracks/ai-app-development/8` | RAG for knowledge vs fine-tuning for behavior and format; the "fine-tuning teaches facts" misconception | [5.1](../README.md#51-the-customization-ladder-knowledge-vs-behavior), [5.5](../README.md#55-just-enough-ml-how-models-learn-and-how-to-measure-them) (why tuning shifts behavior) | Primary |
| `OAI/tracks/ai-app-development/15` | Fine-tuning methods: SFT for tone, style and format; DPO for preferred vs rejected answers | [5.6](../README.md#56-fine-tuning-methods-and-parameter-efficient-tuning-lora) (methods table), [5.7](../README.md#57-training-data-curation-formats-and-governance) (SFT and DPO formats), More self-check questions 3; homework exercise 3 | Primary |
| `ROLE/TUNE/1` | Choose the cheapest effective customization: prompting, RAG or fine-tuning | [5.1](../README.md#51-the-customization-ladder-knowledge-vs-behavior), [5.8](../README.md#58-the-fine-tuning-lifecycle-hosting-and-total-cost) (TCO); practice mini-project | Primary |
| `ROLE/TUNE/2` | PEFT/LoRA and the custom-model lifecycle: hosting and versioning fine-tuned models | [5.6](../README.md#56-fine-tuning-methods-and-parameter-efficient-tuning-lora) (LoRA, adapters per tenant), [5.8](../README.md#58-the-fine-tuning-lifecycle-hosting-and-total-cost) (lifecycle, `TunedModel` record, platform status), More self-check questions 2 | Primary |
| `ROLE/TUNE/3` | ML and data-science foundations: learning types, splits, metrics, data quality | [5.5](../README.md#55-just-enough-ml-how-models-learn-and-how-to-measure-them), Self-check 4; practice §5.5, homework exercise 3 | Primary |
| `ROLE/TUNE/4` | Curate, label and govern data for tuning and evaluation | [5.7](../README.md#57-training-data-curation-formats-and-governance), Self-check 4; practice §5.7 | Primary |
| `ROLE/COMM/7` | Track new model capabilities and turn them into recommendations | [5.9](../README.md#59-staying-current-a-release-radar), More self-check questions 5; practice §5.9, homework exercise 5 | Primary |
| `ROLE/ARCH/3` | Model selection and trade-off reasoning per task | [5.2](../README.md#52-eval-driven-model-selection), Self-check 2; practice §5.2, homework exercise 1 (lineups in [Claude 01 §1.7](../../../anthropic-claude/01-claude-api-fundamentals/README.md#17-model-selection-basics) and [OpenAI 01 §1.7](../../../openai-codex/01-responses-api-fundamentals/README.md#17-model-selection-and-reasoning-effort)) | Primary |
| `ROLE/ARCH/6` | Provider-agnostic and multi-model architecture | [5.3](../README.md#53-multi-model-designs-routing-cascades-advisors-and-orchestrators), [5.4](../README.md#54-provider-agnostic-design-and-lock-in), Self-check 3; practice §5.4 (built end to end in [capstone 03](../../capstones/03-extraction-pipeline-at-scale/README.md#architecture)) | Primary |
| `ROLE/COST/4` | Model routing, cascading and tiering | [5.3](../README.md#53-multi-model-designs-routing-cascades-advisors-and-orchestrators); practice §5.3, homework exercise 4 (taught with cost math in [OpenAI 07 §7.11](../../../openai-codex/07-batch-and-cost/README.md#711-model-routing-and-cascades)) | Supporting |
| `ACAD/partner-basecamp/3` | Partner Basecamp pre-work: understanding foundation models | [5.5](../README.md#55-just-enough-ml-how-models-learn-and-how-to-measure-them) (pretraining, post-training, training cutoff and context window, where customization sits), [5.2](../README.md#52-eval-driven-model-selection) | Primary |
| `CCAR-F/APPX/OUT/1` | Fine-tuning Claude or training custom models (out of scope for the CCAR-F exam) | [5.6](../README.md#56-fine-tuning-methods-and-parameter-efficient-tuning-lora)–[5.8](../README.md#58-the-fine-tuning-lifecycle-hosting-and-total-cost), taught for the job, not the exam | Primary |
| `OAI/tracks/ai-app-development/23` | Three performance levers: prompt, context or RAG, model or fine-tuning | [5.1](../README.md#51-the-customization-ladder-knowledge-vs-behavior) (ladder) | Supporting |
| `OAI/bootcamp/api-builder/30` | Choose a model and an optimization from eval results | [5.2](../README.md#52-eval-driven-model-selection) (`pick_config`) | Supporting |
| `OAI/tracks/model-optimization/1` | Choose the right optimization lever for the goal | [5.1](../README.md#51-the-customization-ladder-knowledge-vs-behavior), [5.6](../README.md#56-fine-tuning-methods-and-parameter-efficient-tuning-lora) (OpenAI job API in planned `openai-codex/16-models-migration-and-model-optimization`) | Supporting |
| `OAI/api/optimize-ai-app-performance/16` | Smaller fine-tuned or distilled models | [5.6](../README.md#56-fine-tuning-methods-and-parameter-efficient-tuning-lora) (distillation row); the hands-on steps are planned for `openai-codex/16-models-migration-and-model-optimization` | Supporting |

## More self-check questions

**1. (Knowledge vs behavior)** A telecom's support bot gives correct plan prices (they come from a pricing tool) but writes long, chatty answers, while the brand guide asks for three short sentences. Prompt changes helped a little: about 70% of answers now follow the guide on a 200-item eval. What is the next step?

- A) Fine-tune on the price list so the prices are built in
- B) Rewrite the instruction with the exact rule and add 3–5 examples of on-guide answers, then re-run the eval; consider SFT only if a well-built prompt still cannot hold the format at the volume and price needed
- C) Move every request to the largest model at maximum effort
- D) Remove the pricing tool and let the model answer from memory to save tokens

<details><summary>Answer</summary>

**B.** This is a behavior problem (length and tone), so the next rung is better instructions and examples, measured on the eval; SFT is the rung after that. A fixes nothing that is broken (prices are already right) and treats facts as training data. C is a costly guess with no evidence. D breaks the part that works.
</details>

**2. (Fine-tuning lifecycle)** A SaaS vendor wants each of its 40 enterprise customers to get answers in that customer's house style, with one shared open-weight base model it hosts itself. What design fits best?

- A) One full fine-tune per customer, each deployed on its own GPU
- B) One LoRA adapter per customer on the shared base, each versioned with its data hash and test score, loaded per request by tenant
- C) Put all 40 style guides into one huge system prompt for every request
- D) Train one model on all customers' data mixed together

<details><summary>Answer</summary>

**B.** Adapters are small, so 40 of them sit next to one base model and swap per tenant, and each one is versioned and evaluated separately. A multiplies storage and hosting by 40. C wastes tokens and mixes styles. D blends the styles the customers want to keep separate and mixes their data.
</details>

**3. (Fine-tuning methods)** Reviewers can always say which of two meeting summaries they prefer, but they cannot write a single "correct" summary. You have 2,000 such judgments. Which method fits, if fine-tuning is justified at all?

- A) Supervised fine-tuning on the preferred summaries only
- B) Preference tuning (DPO) on prompt + preferred + rejected summary triples
- C) Reinforcement fine-tuning with an exact-match grader
- D) Distillation from the largest model

<details><summary>Answer</summary>

**B.** The data is preferences between two answers, which is exactly what DPO trains on. A throws away the information in the rejected answers. C needs a grader that can score a summary, and exact match cannot. D copies a teacher's outputs, which does not use the reviewers' judgments.
</details>

**4. (Multi-model design)** A proposal adds a Fable 5.1 "advisor" to a coding agent that runs on Opus 5.5 at high effort. On 50 tasks it scores 1 point higher than Opus 5.5 alone at about twice the cost per attempt. What should you check before approving it?

- A) Nothing: any quality gain is worth it
- B) Whether the gain is outside run-to-run noise, how often the advisor is actually consulted, and how it compares with Opus 5.5 alone at a higher effort or with Fable 5.1 alone, at the same spend
- C) Whether Fable 5.1 has a larger context window
- D) Whether the advisor can be run in a batch

<details><summary>Answer</summary>

**B.** A pairing has to beat the single-model score-vs-spend curve, and a 1-point gain on 50 tasks can be noise. A ignores the doubled cost. C and D do not decide whether the pairing pays off.
</details>

**5. (Staying current)** A client's intent classifier runs on Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`). It is November 6, 2026. What should the architect do this week?

- A) Nothing until Anthropic sends a final reminder
- B) Wait for the model to stop responding, then switch to whatever is newest
- C) Treat it as urgent: the model is deprecated and retires on November 30, 2026. Run the client's eval on `claude-sonnet-5-5` (and a cheaper candidate), fix any request settings the newer model rejects, and move production in stages with a tested rollback before that date
- D) Pin the dated snapshot ID, which keeps it working after retirement

<details><summary>Answer</summary>

**C.** Requests to a retired model fail, and the retirement is 24 days away, so the move needs an eval, any request-setting fixes and a staged rollout now. A and B leave the client exposed to an outage. D is wrong: a pinned snapshot is exactly what retires.
</details>

## Share your progress

```text
Chapter 05 of the applied AI architect track: model strategy and customization.

3 takeaways:
1. Fine-tuning shapes behavior, not knowledge. Facts that change belong in retrieval.
2. Pick models on the client's own eval: cost per successful task, not price per token.
   Sweep effort before you switch models.
3. Portability lives in what you own: versioned prompts, schemas and the eval suite.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#AIArchitecture #LLM #FineTuning #LearningInPublic
```
