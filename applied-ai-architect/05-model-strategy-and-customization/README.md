# Chapter 05 — Model strategy and customization trade-offs

> **Serves:** OpenAI Academy Scope AI Solutions, Build with RAG and Optimize AI Application Performance; the OpenAI AI application development track; the model-choice side of CCAR-P solution design · **Role areas:** ARCH, TUNE, COMM · **Est. time:** 5–7 hours (reading + 2 notebooks) · **Status:** [ ] not started · **Facts checked:** 2026-11-06

Customers ask an architect three model questions in almost every engagement: *which model should we use, should we fine-tune, and how do we avoid getting locked in?* This chapter gives you a repeatable way to answer all three with evidence instead of opinion. You start from the cheapest change that could fix the problem, measure every option on the customer's own eval set, and only pay for model training when the numbers say it is worth it. Everything here is vendor-neutral; where Claude and OpenAI differ, the chapter says how.

## What you'll learn

- Pick the right lever for a failure: **prompt, context (RAG), tools, model and effort, or fine-tuning**, and explain why fine-tuning does not teach facts.
- Choose a model and effort level from **eval results**, using cost per successful task and a latency budget.
- Decide when a **multi-model design** (routing, cascade, advisor, orchestrator) beats one model at a lower effort.
- Keep a design **provider-agnostic** where it pays, and name what lock-in remains.
- Use just enough **ML**: data splits, leakage, overfitting, precision and recall.
- Judge a **fine-tuning proposal**: SFT vs preference tuning, LoRA, data preparation, lifecycle, hosting and total cost.
- Run a **release radar** that turns new models and deprecations into dated recommendations.

## Prerequisites

[Claude 01 §1.7](../../anthropic-claude/01-claude-api-fundamentals/README.md#17-model-selection-basics) or [OpenAI 01 §1.7](../../openai-codex/01-responses-api-fundamentals/README.md#17-model-selection-and-reasoning-effort) (model lineups, effort) · [OpenAI 06 §6.12](../../openai-codex/06-prompt-engineering-and-evals/README.md#612-error-analysis-judge-calibration-and-accuracy-targets) or [Claude 06 §6.9](../../anthropic-claude/06-prompt-engineering/README.md#69-matching-the-strategy-to-the-task-and-iterating-expanded-beyond-the-guide) (prompting first, error analysis) · [Claude 08 §8.6](../../anthropic-claude/08-task-decomposition/README.md#86-the-workflow-pattern-catalog) (routing) · [OpenAI 07 §7.11](../../openai-codex/07-batch-and-cost/README.md#711-model-routing-and-cascades) (cascades). No ML background needed.

## Concepts

Snippets are plain Python. The notebooks run every one of them offline; the few live cells call `claude-sonnet-5-5`, `claude-haiku-4-5` or `gpt-6-luna` and are marked.

### 5.1 The customization ladder: knowledge vs behavior

Every "the model isn't good enough" complaint is one of two problems:

- **Knowledge:** the model does not have the facts (your price list, this week's policy, a customer's contract). Fix it by putting the facts **in the context**: retrieval (RAG), a tool call, or the document itself.
- **Behavior:** the model has what it needs but does the task the wrong way (wrong format, tone, label set, or reasoning steps). Fix it with **instructions and examples** first, then a stronger model or higher effort, and only then by training.

Climb the ladder one rung at a time, cheapest first, and measure after each rung:

| Rung | What changes | Fixes | Cost to change | Undo |
|---|---|---|---|---|
| 1. Prompt | Instructions, criteria, few-shot examples, output schema | Format, tone, label definitions, steps | Minutes | Edit text |
| 2. Context | Retrieval, tools, attached documents | Missing, private or fresh facts | Days | Re-index |
| 3. Model and effort | Tier, `effort` / `reasoning.effort`, routing | Capability ceiling, cost, latency | Hours (re-run evals) | Config change |
| 4. Fine-tuning | Model weights | Behavior that prompts cannot hold at the volume or price you need | Weeks, plus data | Retrain or roll back |

**Fine-tuning changes behavior, not knowledge.** Training on a product catalog makes the model *sound* like your catalog. It does not reliably recall the right price, and every price change makes the weights stale. Facts that change belong behind retrieval. The rungs also **stack**: OpenAI's accuracy guide describes production systems that use RAG for context *and* fine-tuning for consistent behavior, with fine-tuning used partly to replace long instructions and few-shot blocks with training examples.

**Where you are today.** The Claude API does not offer fine-tuning (Anthropic's glossary says to ask your Anthropic contact). Claude fine-tuning was offered only through Amazon Bedrock, for Claude 3 Haiku. OpenAI is winding down self-serve fine-tuning (dates in 5.8). So for most new projects, rungs 1–3 are the whole ladder, and the architect's job is to prove they are enough.

> **Exam trap:** "The assistant quotes old prices, so fine-tune it on the new price list" is wrong. That is a knowledge problem. Retrieval with a refreshed index fixes it, and keeps fixing it after the next price change.

### 5.2 Eval-driven model selection

Pick the model the same way you would pick a database: against requirements, with a benchmark you ran yourself.

1. **Write the bar first.** A pass rate on a labeled eval set of 20–100 real examples (more for rare classes), a p95 latency budget, and a cost ceiling. See [chapter 08](../README.md#chapter-plan) (planned) for building eval sets.
2. **Pick a starting point.** Anthropic's guide offers two: *capability-first* (start with Claude Opus 5.5, then lower effort or step down) for complex work, and *efficiency-first* (start with the smallest model, step up only on a measured gap) for high-volume, simple tasks. OpenAI gives the same advice for GPT-6 (Luna for well-scoped extraction, Sol for complex work).
3. **Sweep effort before switching models.** Anthropic's guide calls effort often a better lever than a model change, and OpenAI's advice also steps down effort before the model. A stronger model at low effort can beat a weaker one at high effort.
4. **Choose on cost per *successful* task**, not price per token. A cheap model that fails 20% of the time pays for retries, escalations or human review.
5. **Check the non-functional fit:** context length, modalities, tool and structured-output support, data residency, the platform the customer buys through, and the **retirement date** (5.9).

```python
@dataclass
class Run:                 # one model config scored on the whole eval set
    config: str            # e.g. "claude-sonnet-5-5 effort=low"
    passed: int
    total: int
    cost_usd: float        # summed from each response's usage
    p95_ms: float

def pick_config(runs: list[Run], bar=0.90, p95_budget_ms=4000):
    ok = [r for r in runs
          if r.passed / r.total >= bar and r.p95_ms <= p95_budget_ms]
    if not ok:
        return None        # nothing clears the bar: go back to rungs 1-2
    return min(ok, key=lambda r: r.cost_usd / r.passed)
```

`None` is a result, not a bug: when nothing clears the bar, look at the failures (5.1) before reaching for a bigger model.

> **Exam trap:** "Use the biggest model at maximum effort to be safe" and "pick the largest context window" are wrong. Measure, then choose the cheapest configuration that clears the bar.

### 5.3 Multi-model designs: routing, cascades, advisors and orchestrators

One model for everything is the baseline. A multi-model design must **beat that baseline at its best effort setting**, not just beat the expensive model at its default.

| Pattern | How it works | Pays off when | Watch out for |
|---|---|---|---|
| **Static routing** | Each step or task type gets the cheapest model that passes *its* eval | Steps differ a lot in difficulty | One eval per step |
| **Classifier routing** | A small model labels the request; code dispatches | Inputs fall into distinct groups ([Claude 08 §8.6](../../anthropic-claude/08-task-decomposition/README.md#86-the-workflow-pattern-catalog)) | Router errors; always keep an "other" route |
| **Cascade** | Cheap model first; a code gate (schema, business rules) escalates failures | Most items are easy and failures are **detectable** | Valid-looking wrong answers never escalate |
| **Advisor** | A smaller model runs the loop and consults a frontier model on hard turns | Long serial work that is hard in a few places | Adds prompt tokens on every call; helps only if consulted |
| **Orchestrator** | A frontier model plans and delegates bulk work to cheaper workers | Work fans out or is larger than one context | Coordination cost; loses on one dependent chain |

Anthropic's measurements on the 5.5 models make the point: Opus 5.5 orchestrating Sonnet 5.5 workers matched Opus 5.5 alone on a defect search too big for one context, for about a third less cost; but an advisor added to Haiku 5.5 or Sonnet 5.5 on a science benchmark was never consulted and only added cost. Measure the pairing on your workload.

```python
def cascade(item, cheap, strong, is_valid):
    first = cheap(item)
    if is_valid(first):            # schema + business rules, in code
        return first, "cheap"
    return strong(item), "escalated"

# expected cost per item = c_cheap + escalation_rate * c_strong
# 0.0004 + 0.08 * 0.0060 = $0.00088 vs $0.0060 all-strong (6.8x cheaper)
```

A cascade is only as good as its gate. If the cheap model produces well-formed but wrong answers, nothing escalates them, so check the cascade's **accuracy**, not just its cost, on the eval set.

### 5.4 Provider-agnostic design and lock-in

"No lock-in" is not free, and total portability is not the goal. The goal is that **switching or mixing vendors is a measured, bounded change**. Put a thin adapter around the one thing every vendor does (send a prompt, get text, usage and a stop signal back) and keep everything else in shared code: prompts as versioned files, schemas, validation, routing, and the eval suite.

```python
@dataclass
class Reply:
    text: str
    input_tokens: int
    output_tokens: int
    truncated: bool

class ClaudeChat:
    def __init__(self, client, model): self.c, self.m = client, model
    def complete(self, system: str, user: str, max_tokens=1024) -> Reply:
        r = self.c.messages.create(
            model=self.m, max_tokens=max_tokens, system=system,
            messages=[{"role": "user", "content": user}])
        text = "".join(b.text for b in r.content if b.type == "text")
        return Reply(text, r.usage.input_tokens, r.usage.output_tokens,
                     r.stop_reason == "max_tokens")

class OpenAIChat:
    def __init__(self, client, model): self.c, self.m = client, model
    def complete(self, system: str, user: str, max_tokens=1024) -> Reply:
        r = self.c.responses.create(
            model=self.m, instructions=system, input=user,
            max_output_tokens=max_tokens, store=False)
        return Reply(r.output_text, r.usage.input_tokens,
                     r.usage.output_tokens, r.status == "incomplete")
```

What stays vendor-specific, from least to most lock-in:

| Layer | Portability | Keep it portable by |
|---|---|---|
| Plain text calls | High | The adapter above |
| Prompts | Medium: each model family needs its own tuning | One prompt file per model, each with its own eval score |
| Tool and structured-output schemas | Medium | One JSON Schema in your code, translated per vendor |
| Caching, batch, effort settings | Low: different APIs and prices | Configure per adapter; compare cost per successful task |
| Hosted tools (file search, code execution, MCP connectors) | Low | Use them knowingly, or wrap your own tool |
| Fine-tuned weights | None: they live on one platform and one base model | Keep the **training data and eval** portable instead |

Your most portable asset is the **eval suite**: with it, a vendor switch is a re-run and a diff, not a rewrite. For a full two-adapter build see [capstone 03](../capstones/03-extraction-pipeline-at-scale/README.md#architecture); a central LLM gateway (auth, routing, budgets) is planned for chapter 13.

### 5.5 Just enough ML: how models learn and how to measure them

**How a foundation model gets its behavior.** *Pretraining* on a huge text corpus teaches next-token prediction and broad knowledge, frozen at a training cutoff. *Post-training* (instruction tuning and learning from human or AI preferences) turns that into an assistant that follows instructions. Your customizations sit on top: prompts and context at run time, fine-tuning as a small extra round of post-training. That is why fine-tuning shifts style and habits more easily than it adds facts. Two limits follow for design: the model knows only its training data up to the cutoff plus what you put in the **context window** (its working memory for one request), and because it predicts likely text, it can state a wrong fact fluently. So current facts go in the context, and outputs get checked.

The ML vocabulary you need to review a proposal:

| Term | What it means for you |
|---|---|
| Supervised / unsupervised / reinforcement | Learn from labeled input→output pairs / find structure without labels (clustering, embeddings) / learn from a reward or a preference |
| Train / validation / test split | Train on one part, tune choices on the second, report once on the third. Your **eval set is the test set**: never train on it |
| Leakage | Test items that are near-copies of training items (same customer, same thread, same template) inflate scores. Split **by group**, not by row |
| Overfitting | Training loss keeps falling while validation loss rises: the model memorizes. Stop early, add data, lower epochs |
| Precision / recall / F1 | Of what you flagged, how much was right / of what was there, how much you found / their harmonic mean. Pick by the cost of each error |
| Baseline | The score of today's prompt-only system. A fine-tune that does not beat it on the same test set is not an improvement |
| Class imbalance | 2% fraud makes "never fraud" 98% accurate. Report per-class recall |

```python
def split_by_group(rows, key, test_pct=20):
    """Every row of one group lands on the same side, so no leakage."""
    def bucket(g):          # stable across runs and machines
        return int(hashlib.sha256(g.encode()).hexdigest(), 16) % 100
    test_groups = {r[key] for r in rows if bucket(r[key]) < test_pct}
    train = [r for r in rows if r[key] not in test_groups]
    test = [r for r in rows if r[key] in test_groups]
    return train, test
```

### 5.6 Fine-tuning methods and parameter-efficient tuning (LoRA)

| Method | Training data | Use it for | Not for |
|---|---|---|---|
| **Supervised fine-tuning (SFT)** | Input → ideal output pairs ("show, don't tell") | A fixed format, label set or tone held at scale; shorter prompts; a smaller model doing a narrow task | New or changing facts |
| **Preference tuning (DPO)** | Input + preferred answer + rejected answer | Subjective quality: tone, what a summary should focus on | Tasks with one correct answer (SFT is simpler) |
| **Reinforcement fine-tuning (RFT)** | Inputs + a grader that scores answers | Reasoning models on tasks with checkable answers | Tasks you cannot grade reliably |
| **Distillation** | A strong model's outputs used as SFT data for a small model | Cutting cost and latency once the strong model's output is good | Raising quality above the teacher |

**Full fine-tuning vs parameter-efficient fine-tuning (PEFT).** Full fine-tuning updates every weight, which means a full model copy per variant. **LoRA**, the most common PEFT method, freezes the base weights and learns a small low-rank update for selected weight matrices: instead of changing a `d_in × d_out` matrix, it trains two thin matrices of shapes `d_in × r` and `r × d_out`, with rank `r` often 8–64. **QLoRA** does the same on a quantized (compressed) base model to fit on smaller GPUs.

```python
def lora_params(d_in: int, d_out: int, rank: int) -> int:
    return rank * (d_in + d_out)     # A: d_in x r,  B: r x d_out

full = 4096 * 4096                   # one projection matrix
lora = lora_params(4096, 4096, rank=16)
print(f"{lora:,} vs {full:,} = {lora / full:.2%}")
# 131,072 vs 16,777,216 = 0.78%
```

Architecturally this matters because adapters are **small files you can version, swap and serve per tenant** on one shared base model. You only get that option with **open-weight models** you host (or a cloud service that hosts adapters for you). Hosted vendor fine-tuning gives you a model ID, not the weights.

### 5.7 Training data: curation, formats and governance

Data quality decides a fine-tune's outcome far more than hyperparameters. OpenAI's accuracy guide suggests starting with about 50 high-quality examples, evaluating, and growing only if the remaining errors are behavior errors.

1. **Source** from real traffic that matches production: same input format, and if production uses RAG, the retrieved context inside each example.
2. **Label** with a written guideline. Have two people label a sample and measure agreement; low agreement means the task definition is unclear, not that you need more data.
3. **Clean:** remove exact and near duplicates, broken or empty turns, and examples that contradict the guideline.
4. **Protect:** scrub or tokenize PII and secrets, check you have the right to use the data for training, and record retention.
5. **Split by group** (5.5) and freeze the test set before training starts.
6. **Document** in a data card: source, date range, label guideline version, known gaps, licence or consent basis, and the file's hash.

Formats are JSONL, one example per line. SFT uses a chat transcript whose last assistant message is the target; OpenAI's DPO format adds a preferred and a non-preferred final answer to a single-turn input:

```text
{"messages": [{"role": "system", "content": "Label the ticket."},
  {"role": "user", "content": "Charged twice"},
  {"role": "assistant", "content": "billing"}]}
{"input": {"messages": [{"role": "user", "content": "Summarize: ..."}]},
 "preferred_output": [{"role": "assistant", "content": "Key risk: ..."}],
 "non_preferred_output": [{"role": "assistant", "content": "It's a doc."}]}
```

Each record is one physical line in the real file (wrapped here to fit). The practice notebook validates these rules before anything is uploaded.

### 5.8 The fine-tuning lifecycle, hosting and total cost

The vendor-neutral lifecycle, whatever the platform:

1. **Baseline:** best prompt-and-context system, scored on the frozen test set.
2. **Data:** curate, split and document (5.7).
3. **Method and base:** SFT, DPO or RFT; hosted vendor tuning or open-weight + LoRA.
4. **Train:** watch validation loss; stop when it turns up.
5. **Evaluate:** the same test set as the baseline, plus a **regression set** of general tasks the model must not get worse at, plus safety checks.
6. **Ship:** behind a flag, staged rollout, rollback to the baseline ready (planned chapter 09).
7. **Operate:** version every artifact, monitor drift, and plan the re-tune when the base model retires.

```python
@dataclass(frozen=True)
class TunedModel:
    name: str                  # "ticket-triage-sft-v3"
    base_model: str            # the exact snapshot it was trained from
    method: str                # "sft" | "dpo" | "lora-sft" ...
    data_sha256: str           # hash of the training file
    test_set: str              # e.g. "triage-test-2026-10"
    score: float               # on test_set
    baseline_score: float      # prompt-only system, same test_set
    base_retires: str | None   # re-tune or migrate before this date
```

**Total cost of ownership** is more than the training bill: data labeling, training runs, evaluation, hosting (a dedicated endpoint or GPU for open-weight models), monitoring, and **re-tuning every time the base model is retired**. A fine-tune pays off when it lets you serve a cheaper model or a much shorter prompt at high volume and still clear the bar. Compare monthly savings with the one-off and recurring costs before you start.

**Platform status (checked 2026-11-06):**

| Platform | Status | What it means |
|---|---|---|
| Claude API | No fine-tuning | Customize with prompts, retrieval, tools, skills and model choice |
| Claude on Amazon Bedrock | Fine-tuning was offered for Claude 3 Haiku only | Check Bedrock's customization pages before promising it |
| OpenAI self-serve fine-tuning | Closed to orgs that never fine-tuned (2026-05-07); closed to orgs with no fine-tuned-model inference in 60 days (2026-07-02); no new jobs for anyone from 2027-01-06 | Existing fine-tuned models keep serving until their base model is deprecated |
| Open-weight models | Full control with PEFT/LoRA | You own hosting, scaling, security and upgrades |

> **Exam trap:** For a new organization in late 2026, "fine-tune a GPT model on OpenAI" is not an available option. The answer is prompting, retrieval and model choice, or open-weight tuning if the case truly needs it.

### 5.9 Staying current: a release radar

Models change faster than projects. Turn that into a routine, not a surprise:

- **Watch** the vendor pages that matter: models overview, deprecations, pricing and release notes for every model in production.
- **Know the commitments.** Anthropic gives at least 60 days' notice before retiring a public model and lists "not sooner than" dates; OpenAI lists shutdown dates on its deprecations page.
- **Trigger** an eval run on every relevant event: a new model in a tier you use, a deprecation, a price change, or an API change.
- **Recommend** in writing within a fixed time (say two weeks): eval results, cost per successful task, migration effort, risk, and a date.

Real signals on 2026-11-06: Claude Haiku 5.5 (`claude-haiku-5-5`) is now listed as the current Haiku model, while Haiku 4.5's "not sooner than" date (2026-10-15) has passed, so a deprecation could now arrive with 60 days' notice. Claude Sonnet 4.5 retires on **2026-11-30**. Claude API version `2026-10-21` removed `temperature`, `top_p` and `top_k` (they return a 400). Each is a radar item with an owner.

```python
def radar(in_use: dict, today: date, window_days=90) -> list[str]:
    """in_use: model -> (status, retire_date or None, committed_until)."""
    alerts = []
    for model, (status, retires, committed) in in_use.items():
        if status == "deprecated":
            alerts.append(f"{model}: deprecated, retires {retires}")
        elif committed and committed <= today:
            alerts.append(f"{model}: commitment passed; ready a successor")
        elif committed and (committed - today).days <= window_days:
            alerts.append(f"{model}: commitment ends {committed}")
    return alerts
```

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Offline, one section per concept (5.1–5.9): diagnose failures to a lever, pick a model config from eval runs, simulate a cascade, run one eval through Claude and OpenAI adapters on mocked SDK clients, split data without leakage, count LoRA parameters, validate a training file, compare fine-tune TCO, and run a release radar. Mini-project: a model-strategy decision record. Optional live cells are marked |
| [`02_homework.ipynb`](02_homework.ipynb) | 8-question scenario quiz (hashed answer key), 5 auto-checked offline exercises, an architecture scenario with a rubric, and a scorecard (pass mark 72%) |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Model lacks facts, or facts change | Retrieval or tools (context) | Fine-tuning |
| Wrong format, tone or labels | Clearer instructions, examples, schema | A bigger model |
| Quality short of the bar | Error analysis, then effort sweep, then next model up | Max effort everywhere |
| Several configs clear the bar | Lowest cost per successful task within the latency budget | Lowest price per token |
| Most items easy, failures detectable in code | Cascade with a validation gate | All traffic on the strong model |
| Work fans out or exceeds one context | Orchestrator with cheaper workers, if it beats one model at lower effort | Multi-agent by default |
| "Avoid lock-in" | Thin adapter, versioned prompts, portable evals | A lowest-common-denominator wrapper that bans vendor features |
| Prompts cannot hold a behavior at your volume or price | SFT (or DPO for subjective preferences), with a frozen test set | Fine-tuning before rungs 1–3 |
| Many tenants need their own behavior | LoRA adapters on one open-weight base | One full fine-tune per tenant |
| A new model or a deprecation lands | Re-run the eval, recommend in writing with a date | Switching on the announcement |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Fine-tuning for facts.** Training on documents that change instead of retrieving them.
- **Choosing by reputation.** Picking a model from a leaderboard or a blog post instead of the customer's eval set.
- **Price per token, not per success.** Ignoring retries, escalations and human review caused by a cheaper model's failures.
- **Pairing without a baseline.** Adding a router, advisor or orchestrator without comparing it with one model at a lower effort.
- **Leaky splits.** Splitting by row so the same customer or template appears in train and test, then trusting a 97% score.
- **No regression set.** Shipping a fine-tune that wins its task and quietly loses general skills.
- **Forgetting the base model's lifecycle.** A fine-tune dies with its base model, and the re-tune was never budgeted.

## Self-check

**1. (Knowledge vs behavior)** An insurer's claims assistant answers coverage questions. Policies change every quarter, and agents report it quotes last quarter's deductible amounts. The vendor proposes fine-tuning the model on all current policy documents every quarter. What do you recommend?

- A) Fine-tune quarterly as proposed, because the model will then know the current policies
- B) Retrieve the relevant policy sections at question time from an index refreshed when policies change, and ask the model to answer only from them
- C) Switch to the most capable model, which has more knowledge built in
- D) Add "always use the latest deductible amounts" to the system prompt

<details><summary>Answer</summary>

**B.** Deductibles are facts that change, so they belong in the context through retrieval, with the index refreshed on every policy change. A is the "fine-tuning teaches facts" misconception: weights recall facts unreliably and go stale on the next change, and the Claude API offers no fine-tuning anyway. C does not know the insurer's private, current policies either. D asks for facts the model does not have.
</details>

**2. (Model selection)** On a 120-item eval for invoice field extraction (bar: 95% pass, p95 under 3 s), the team's results are: Opus 5.5 at medium effort 98% at $0.019 per item; Sonnet 5.5 at low effort 96% at $0.006; Haiku 4.5 91% at $0.003. The tech lead wants Opus 5.5 "for headroom". What do you recommend?

- A) Opus 5.5, because the highest score gives the most headroom
- B) Haiku 4.5, because it is the cheapest per item
- C) Sonnet 5.5 at low effort: it clears both bars at the lowest cost per successful item; keep the eval as a regression gate and re-run it on any model or prompt change
- D) Run all three in a majority vote to be safe

<details><summary>Answer</summary>

**C.** Sonnet 5.5 at low effort clears the quality and latency bars at about a third of Opus's cost per successful item. "Headroom" is not a requirement unless it is in the bar. A pays for quality nobody asked for. B fails the bar (91% < 95%), and its failures would cost more in review than it saves. D triples cost without a measured need.
</details>

**3. (Provider-agnostic design)** A CIO says: "No vendor lock-in. Write a wrapper so we only use features both vendors have, and never use caching, batch or hosted tools." What is the best response?

- A) Agree: the lowest-common-denominator wrapper guarantees portability
- B) Disagree and pick one vendor for everything; portability is not worth any effort
- C) Fine-tune on one vendor to lock in the best quality
- D) Keep a thin adapter for calls, keep prompts, schemas and the eval suite in your own code, and use vendor features such as caching or batch inside each adapter where they pay for themselves, so a switch is a re-run of the eval rather than a rewrite

<details><summary>Answer</summary>

**D.** Portability comes from owning the parts that are expensive to rebuild (prompts, schemas, evals, routing) and keeping vendor plumbing behind a small interface. A throws away large cost savings (caching, batch) for a theoretical benefit. B ignores a real risk that a cheap adapter reduces. C increases lock-in the most: fine-tuned weights cannot move between platforms.
</details>

**4. (Fine-tuning data)** A team fine-tuned an open-weight model with LoRA to label support tickets. It scored 97% on their test set, but 79% in production. The 20,000 examples were shuffled and split 80/20 by row; many customers send several near-identical tickets. What is the most likely cause, and the fix?

- A) The LoRA rank was too low; retrain at a higher rank
- B) Leakage: near-duplicate tickets from the same customers sit in both train and test. Re-split by customer, freeze a test set drawn from recent production traffic, and re-score both the fine-tune and the prompt-only baseline on it
- C) Production traffic is noisier; add more epochs so the model memorizes better
- D) The base model is too small; switch to full fine-tuning

<details><summary>Answer</summary>

**B.** A row-level split put copies of training tickets into the test set, so the 97% measured memorization. Splitting by customer and testing on recent traffic gives an honest number, and the baseline tells you whether the fine-tune helps at all. A and D change capacity without fixing the measurement. C makes overfitting worse.
</details>

## Official documentation

- [Choosing the right model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) (Claude): criteria, capability-first vs efficiency-first, effort before model
- [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence) (Claude): advisor and orchestrator strategies, with measurements
- [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) (Claude): lifecycle states, retirement dates, notice period
- [Glossary: fine-tuning](https://platform.claude.com/docs/en/about-claude/glossary) (Claude): what fine-tuning is and its status on the Claude API
- [Model optimization](https://developers.openai.com/api/docs/guides/model-optimization) (OpenAI): evals, prompting, SFT and DPO, the wind-down notice
- [Optimizing LLM accuracy](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) (OpenAI): context vs behavior, when RAG and fine-tuning stack, data practices
- [Deprecations](https://developers.openai.com/api/docs/deprecations) (OpenAI): fine-tuning and model shutdown dates
- [LoRA conceptual guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora) (Hugging Face PEFT): low-rank adapters on open-weight models

[← Chapter 04 — Solution architecture patterns](../04-solution-architecture-patterns/README.md) | [↑ Applied AI Architect track](../README.md) | [Chapter 06 — RAG pipelines →](../06-rag-pipelines/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
