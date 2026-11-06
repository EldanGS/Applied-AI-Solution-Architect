# Chapter 6 — Prompt Engineering and Evals

> **Claude counterpart:** [Chapter 6 — Prompt Engineering: Advanced Techniques](../../anthropic-claude/06-prompt-engineering/README.md) · **Academy course:** Evaluate AI Applications (API pathway, 70 min) · **Est. time:** 9–11 hours (reading + notebooks) · **Status:** [ ] not started

A prompt is a contract with a non-deterministic component. An eval is the test suite that tells you whether the contract still holds after you change the prompt, the model, the reasoning effort or the schema. On OpenAI, reusable prompt objects and the Evals platform both shut down on 2026-11-30, so prompts and evals now live in your repository, go through code review and run in CI. Your job is to pick the lever that fixes the root cause and prove the fix with a measurement instead of a vibe.

## What you'll learn

- Use `instructions` vs `developer` messages, and resend `instructions` when you chain with `previous_response_id`.
- Prompt GPT-6 reasoning models outcome-first, and tune `reasoning.effort` and `text.verbosity` instead of shouting.
- Apply few-shot examples, explicit criteria and prompt chaining, and know when each is the right fix.
- Build a validate → retry-with-feedback loop with `client.responses.parse` and keep prompts as versioned code.
- Build an eval harness and regression gate, migrate legacy Evals to Promptfoo, calibrate an LLM judge, and add moderation.

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md) (`.env` with `OPENAI_API_KEY`) · [Chapter 01 — Responses API fundamentals](../01-responses-api-fundamentals/README.md) (`instructions`, `status`, `previous_response_id`) · [Chapter 02 — Function calling and Structured Outputs](../02-function-calling-and-structured-outputs/README.md) (strict schemas, `responses.parse`). The Claude counterpart, [Chapter 6 — Prompt Engineering](../../anthropic-claude/06-prompt-engineering/README.md), covers the shared techniques in more depth.

## Concepts

Diagnose the failure first. Rules ignored on later turns → resend instructions (6.1). Too long everywhere → `text.verbosity` (6.2). Format varies → few-shot (6.3). Flags the wrong things → explicit criteria (6.4). Depth varies across many inputs → chaining (6.5). Valid JSON, wrong values → validate and retry (6.6). Source contradicts itself → self-correction fields (6.7). Not sure the fix helped → eval harness and gate (6.9, 6.10). Fails for unknown reasons → error analysis (6.12). Code can't parse the output → strongest output constraint (6.13).

> **Note: changed on the OpenAI platform in 2026.** (1) `v1/prompts` (the `prompt={"id": "pmpt_..."}` parameter) shuts down on **2026-11-30**; keep prompts in code (6.8). (2) The Evals platform (dashboard and API) was deprecated on 2026-06-03, has been **read-only since 2026-10-31** and shuts down on **2026-11-30**. The graders are part of the same transition. OpenAI's suggested migration path is **Promptfoo**. Do not start new work on the Evals API (6.9, 6.10). (3) GPT-6 prompting is outcome-first: clear success criteria beat step-by-step scripts, and "think step by step" is unnecessary for reasoning models (6.2).

Snippets omit imports and use `client = OpenAI()` and `MODEL`, default `gpt-6-luna` ($0.10 / $0.50 per million input / output tokens at time of writing). For an LLM judge, OpenAI's evaluation guide suggests starting on `gpt-6-astra`.

### 6.1 Instructions, roles and message formatting

You can send developer guidance two ways. The `instructions` parameter takes priority over `input` and applies **only to the current request**. A `developer`-role message is an item in `input`, so it stays in the conversation if you keep that history. `developer` messages outrank `user` messages. `"role": "system"` is still valid and also outranks `user`; this repo uses `developer` so one grep finds every rule.

```python
RULES = "You are a terse release-notes writer. Answer in one sentence."
ASK = "What changed in v2.3? Added SSO, fixed CSV export."
r1 = client.responses.create(model=MODEL, instructions=RULES, input=ASK)
r2 = client.responses.create(model=MODEL, input=[
    {"role": "developer", "content": RULES},
    {"role": "user", "content": ASK}])
```

> **Exam trap:** With `previous_response_id`, `instructions` from previous turns **are not in the context**. Resend `instructions` on every request, or put the rules in a `developer` message that stays in the stored history.

**Formatting.** Use Markdown sections for structure and XML tags for data. A developer message usually has **Identity**, **Instructions**, **Examples** and **Context** (last). Context here means trusted data you control, such as account facts; untrusted or per-document text goes in the user turn (6.13). **Static first, dynamic last:** caching matches the start of the rendered context, so keep repeated content identical and first. Untrusted text (uploads, web pages, tool output) goes in the `user` turn, wrapped in tags such as `<document>`. Role priority helps against injection but is not a guarantee; test it with adversarial eval cases.

### 6.2 Prompting reasoning models

All current GPT-6 models are reasoning models. Their hidden reasoning tokens are billed as output and count against `max_output_tokens`. Give the goal, constraints, **success criteria**, an output contract and **stop rules** (when to answer, ask, abstain or retry). Avoid scripting every step, "think step by step", repeated rules, and ALWAYS / NEVER / MUST except for true invariants. OpenAI's GPT-5.6 guide reports leaner prompts improved internal coding-agent evals by roughly 10–15% while cutting tokens by 41–66% (directional). Its migration workflow: switch the model, keep the current effort, run evals, remove one group of instructions at a time, re-run evals.

| Model | Supported `reasoning.effort` | Default |
|---|---|---|
| `gpt-6-astra` | `low`, `medium`, `high`, `xhigh`, `max` (`none` returns 400) | Not stated in the docs: always send it |
| `gpt-6.1-sol` | `low`, `medium`, `high`, `xhigh`, `max` | `medium` |
| `gpt-6-luna` | `none` (no reasoning, lowest latency), `low`, `medium`, `high`, `xhigh`, `max` | `medium` |

Effort is "a tuning knob, not the primary way to recover quality": check for a missing success criterion first, then test one level up. **Reasoning mode** (`reasoning={"mode": "pro"}`) is independent of effort and costs more tokens and latency; change mode and effort one at a time, only when an eval shows a gain. **Verbosity** (`text={"verbosity": "low"}`, default `medium`) sets the product-wide level of detail; put task-specific length in the prompt. Keep `max_output_tokens` generous, because it covers reasoning plus visible text.

> **Gotcha:** With effort other than `none`, remove `temperature`, `top_p` and `top_logprobs` (unsupported). Hitting `max_output_tokens` gives `status == "incomplete"`, possibly with no text, and you still pay for the reasoning.

Raw reasoning is never returned: request `reasoning={"summary": "auto"}`, and ask for **fields** (a short `rationale`) instead of a printed chain of thought. GPT-6 Astra asks clarifying questions more often than earlier models; if you need autonomy, state the authorization boundary once. The **interview pattern** (ask up to N questions whose answers would change the design) surfaces design decisions; it does not replace tests or examples.

### 6.3 Few-shot examples

A few diverse input → output examples steer format and decisions. Put them in the developer message, each in XML tags with an `id`, for example `<product_review id="example-1">…</product_review>` followed by `<assistant_response id="example-1">Positive</assistant_response>`. On reasoning models, start **zero-shot**, add examples for a measured problem only, and keep them **aligned with the instructions**. Examples that change nothing are only cost. Few-shot pays off most for **ambiguous decisions** (show the decision and its rationale), **output format** (one complete item), **acceptable vs problematic** (`PO# KE-2026-03` is a PO number; `Net 30` is a payment term, not one), **source layouts** (line items in a table vs in running text) and **fuzzy values** (`approx. 2 hrs` → `{"hours": 2, "precision": "approximate"}`). Vary the examples, show `null` for an absent field, and pair them with **normalization rules** (ISO 8601 dates, unknown values `null`).

> **Exam trap:** For wrong **tool selection**, fix tool names and descriptions first ([Chapter 2](../02-function-calling-and-structured-outputs/README.md)). For a format that still varies, use 3–5 examples of the exact format (or Structured Outputs), not adjectives, a bigger model or higher effort.

### 6.4 Explicit criteria and rubrics

Replace adjectives ("be conservative") with a **flag-only-if list and a do-not-flag list**, and give the reason behind each rule. Keep categories as data (a `CATEGORIES` dict with an `enabled` flag and a `flag_if` rule each) so you can switch off a noisy one. OpenAI's GPT-5.6 prompt guidance notes that "GPT-5-class models follow prompt contracts closely", so check criteria for contradictions as well as gaps. A **severity rubric** gives a definition and an example per level: for an invoice pipeline, critical = money moves wrongly (a misread total is auto-approved and paid); high = data exposure (a bank account number written to logs); medium = wrong but caught downstream (a date left as `Jan 9, 2026`); low = cosmetic (a typo in a line-item description). A criterion you can state is one you can grade (6.9).

> **Exam trap:** When one category's false positives make developers ignore **every** finding, temporarily disable that category (`"enabled": False`) and fix its criterion. "Be stricter" lowers recall everywhere. A self-rated 1–10 confidence is not a calibrated gate; at most it is a triage hint for a human.

### 6.5 Prompt chaining

A **prompt chain** is a fixed sequence of focused calls where code owns the flow: one call per file for local issues (can run in parallel), then one integration call for cross-file issues. It fixes attention dilution and makes each step testable.

```python
LOCAL = "Review ONE file. Report only issues visible inside this file."
INTEGRATION = "You get per-file findings. Report ONLY cross-file issues."

def call(instructions: str, text: str) -> str:
    r = client.responses.create(model=MODEL, reasoning={"effort": "low"},
                                instructions=instructions, input=text)
    if r.status != "completed":
        raise RuntimeError(f"step failed: {r.status} {r.incomplete_details}")
    return r.output_text

files = {"auth.py": "...", "db.py": "..."}
local = {p: call(LOCAL, f'<file path="{p}">\n{src}\n</file>')
         for p, src in files.items()}
bundle = "\n".join(f'<findings file="{p}">\n{f}\n</findings>'
                   for p, f in local.items())
report = call(INTEGRATION, bundle)
```

Keep a chain when you need to inspect intermediate outputs, run steps in parallel, use different models or efforts per step, or evaluate each step on its own. Use **dynamic decomposition** (an agent loop, [Chapter 3](../03-agents-sdk-and-agents-api/README.md)) only when the next step depends on what the last one found. A 1M-token window does not fix attention quality when one pass reviews many files (attention dilution).

### 6.6 Validation and retry-with-feedback

Structured Outputs fix **syntax**, not **semantics**: "Structured Outputs can still contain mistakes." `client.responses.parse(..., text_format=Model)` turns a Pydantic model into a strict schema and fills `response.output_parsed`. Check first: `status == "incomplete"` means cut off (truncated JSON can make `parse()` raise `ValidationError`), so never use partial output; a `refusal` content part (in the message's `content`) leaves `output_parsed` as `None`, so log it and don't retry blindly. Then validate meaning in code (`Invoice` is the strict Pydantic schema with `line_items` and `total`; `INSTRUCTIONS` holds the extraction rules):

```python
class ValidatedInvoice(Invoice):          # semantics: business rules in code
    @model_validator(mode="after")
    def total_matches_items(self):
        items = round(sum(i.amount for i in self.line_items), 2)
        if abs(items - self.total) > 0.01:
            raise ValueError(f"total is {self.total} but items sum to {items}")
        return self

def extract_invoice(document: str, max_attempts: int = 3):
    prompt = f"<document>\n{document}\n</document>"
    for attempt in range(max_attempts):
        r = client.responses.parse(model=MODEL, instructions=INSTRUCTIONS,
                                   input=prompt, text_format=Invoice)
        if r.status != "completed" or r.output_parsed is None:
            raise RuntimeError(f"incomplete or refused: {r.status}")
        draft = r.output_parsed
        try:
            return ValidatedInvoice.model_validate(draft.model_dump())
        except ValidationError as err:
            errors = "\n".join(f"- {e['msg']}" for e in err.errors())
            prompt = (f"<document>\n{document}\n</document>\n"
                      f"<previous_extraction>\n{draft.model_dump_json()}\n"
                      f"</previous_extraction>\n<validation_errors>\n{errors}"
                      "\n</validation_errors>\nReturn a corrected extraction.")
    return None                                # route to human review
```

**Schema rules on OpenAI.** Strict mode enforces `pattern`, `format` (`date`, `email`, …), `minimum` / `maximum` and `minItems` / `maxItems`, so `Field(pattern=r"^[A-Z]{3}$")` enforces a currency code at decode time. Every field must be `required` (use `T | None` for optional), and keys come out in schema order. Cross-field rules stay in your validator. **Don't force invention:** nullable fields for values the source may lack, enums with `"other"` (plus `category_detail`) and `"unclear"`, and a "not for me" path such as `is_invoice: bool`. For tool-step output, a forced function with `strict: true` also works ([Chapter 2](../02-function-calling-and-structured-outputs/README.md#24-tool_choice-and-parallel_tool_calls)).

> **Exam trap:** The retry must contain the **original document, the previous extraction and the specific error**. Do not retry when the value is not in the document: return `null` and route to review. Exponential backoff is for 429 / 5xx / timeouts, not validation failures.

### 6.7 Self-correction

Design outputs so inconsistencies become **visible to code**. Extract `stated_total` as printed, recompute the sum of the line items in Python, and route a mismatch to `human_review`: arithmetic belongs to code, and a model-reported `conflict_detected` is not trusted alone. Record a `detected_pattern` on findings so you can group dismissed ones and fix the noisy criterion. Run review as a **fresh request** (no `previous_response_id` from the draft), with explicit criteria and a structured verdict.

### 6.8 Prompts as versioned code

"Treat prompts as application code." With `v1/prompts` shutting down on 2026-11-30, move prompt content into source code, replace prompt variables with **typed function arguments**, pass the result through `instructions` and `input`, and version with git, PR review and evals. Keep static content first to preserve caching. Log the version and hash with every request to join production traces to eval results, and give prompt PRs an owner, a review rule and an eval run.

```python
# Before (stops working 2026-11-30): prompt={"id": "pmpt_123", ...}
# After: prompts/invoice.py, a named, versioned builder
PROMPT_VERSION = "invoice-extract@2"

def build_invoice_request(document: str, *, today: str) -> dict:
    instructions = ("# Instructions\n* Dates ISO 8601. Currency ISO 4217. "
                    "Use null for absent values.\n"
                    f"* Resolve relative dates against {today}.")
    sha = hashlib.sha256(instructions.encode()).hexdigest()[:12]
    return {
        "instructions": instructions,
        "input": f"<document>\n{document}\n</document>",
        "metadata": {"prompt_version": PROMPT_VERSION, "prompt_sha": sha},
    }
```

### 6.9 Building your own eval harness

OpenAI's evaluation guide has five steps: **define the objective → collect a dataset → define metrics → run and compare → evaluate continuously**. Its anti-patterns: generic metrics only, datasets unlike production, "vibe-based" evals, and automated scores never calibrated against humans. Grader types: **exact / normalized match** (normalize first, or you grade formatting), **schema / rule checks** (passing says nothing about truth), **LLM-as-judge with a rubric** (position and verbosity bias), and **human review** (ground truth and judge calibration).

| Task shape | Eval approach |
|---|---|
| Right answer exists (classification, extraction, tool choice) | Exact or normalized match, order-insensitive set match for lists, numeric tolerance, function-call accuracy |
| Output can be executed | Run it: SQL returns the expected rows, code passes tests |
| No single right answer (summaries, replies) | Rubric-based grading by an LLM judge or humans, against a rubric or reference answer |
| High stakes, or the judge is new | Humans first, then a judge calibrated against them (6.12) |

A judge runs in one of three modes: **pairwise** (pick the better of two; swap the order to cancel position bias), **single-answer** grading against a rubric, or **reference-guided** grading against a gold answer. Prefer pass/fail or pairwise over open scales, control for length, and let the judge reason before it scores. The rubric here passes an extraction only if every non-null value appears in the document; for human grading, use a "show rather than tell" scorecard and consensus votes.

```python
class Verdict(BaseModel):
    rationale: str                    # generated first: reason before scoring
    verdict: Literal["pass", "fail"]

def judge(document: str, extraction_json: str,
          judge_model: str = "gpt-6-astra") -> Verdict:
    r = client.responses.parse(
        model=judge_model, reasoning={"effort": "low"},
        instructions=JUDGE_RUBRIC, text_format=Verdict,
        input=f"<document>\n{document}\n</document>\n"
              f"<extraction>\n{extraction_json}\n</extraction>")
    if r.status != "completed" or r.output_parsed is None:   # 6.6 checks
        raise RuntimeError(f"judge incomplete or refused: {r.status}")
    return r.output_parsed
```

**Evals per architecture:** a single-turn call needs instruction-following and functional-correctness evals; a workflow adds them **per step**; an agent adds **tool selection** and **argument precision**; multi-agent adds **handoff accuracy**. For agents, grade the **trace** (model calls, tool calls, guardrails, handoffs), not only the final answer. **Datasets** mix production logs, expert-written and synthetic cases, with edge and adversarial inputs: typos, mixed languages, several intents, user-vs-developer conflicts and jailbreak attempts. A judge you have not compared with human labels is an unvalidated metric.

### 6.10 Regression testing and Promptfoo

An eval becomes a **regression test** when it runs on every change and can block it. Compare the **baseline** (production) with a **candidate** on the same dataset and settings. Fail if the mean drops below a floor or if **any critical case** that passed now fails, even when the average improves. Compare the **set of cases** too, so a dropped case cannot pass silently.

```python
def regression_gate(baseline: dict[str, float], candidate: dict[str, float],
                    critical: set[str], min_mean: float = 0.9):
    case_ids = set(baseline) | set(candidate) | set(critical)
    # A case that did not run scores 0.0: a dropped case is a regression.
    regressions = sorted(cid for cid in case_ids
                         if candidate.get(cid, 0.0) < baseline.get(cid, 0.0))
    if not candidate or not case_ids:
        return False, regressions              # an empty run never passes
    mean = sum(candidate.get(cid, 0.0) for cid in case_ids) / len(case_ids)
    missing_critical = set(critical) - set(candidate)
    ok = (mean >= min_mean and not missing_critical
          and not any(cid in critical for cid in regressions))
    return ok, regressions
```

Change one thing at a time and pin model snapshots. Then: gate in CI → **staged rollout** behind a flag → production signals per version (feedback, escalations, judge on sampled traffic, latency, cost) → full rollout or rollback, with new failures added as cases. Tag requests with the prompt version so signals split by version and **traffic segment**; an average can hide a regression in one language or tier.

**Promptfoo** is the documented migration path from Evals: an open-source CLI for evaluating and red-teaming AI apps, configured next to your code. Criteria become **assertions** (`is-json`, `javascript`, `llm-rubric`), datasets become **tests with vars**, prompt versions become `prompts`. Use the provider `openai:responses:gpt-6-luna`, pin the judge with `defaultTest.options.provider` (or `llm-rubric` uses Promptfoo's default grader), and run `promptfoo eval -c promptfooconfig.yaml --no-cache`. Promptfoo is a Node.js tool; this repo does not install or run it.

**Reading a legacy Evals API eval** (to migrate it, not to build on it):

| Evals API piece | In your harness | In Promptfoo |
|---|---|---|
| `client.evals.create(data_source_config=...)` with an `item_schema` | Dataset row type | `tests[].vars` |
| `testing_criteria`: the list of graders | Grader functions | `assert` entries |
| `string_check` (`{{ sample.output_text }}` eq `{{ item.correct_label }}`) | Normalized exact match | `equals`, `contains`, `regex` |
| `text_similarity`, `score_model`, `python` graders | Similarity, LLM judge, code check | `similar`, `llm-rubric`, `python` |
| `client.evals.runs.create(...)`; results `status`, `result_counts`, `report_url` | `run_eval(...)`, report, gate | `promptfoo eval`, `promptfoo view`, CI exit code |

`{{ item.<field> }}` is a test-row value; `{{ sample.output_text }}` is the model output. Migrate the dataset and criteria, re-validate the judge (6.12), and treat the first new run as a fresh baseline.

### 6.11 Moderation and safety basics

**Moderation** with `client.moderations.create(model="omni-moderation-latest", input=...)` is **free** and returns `flagged`, `categories` and `category_scores`; screen input before you spend tokens and output before you show it. **Inline moderation** (`moderation={"model": "omni-moderation-latest"}` on `responses.create`) returns scores for both sides, and **you** decide what to show. A **`safety_identifier`** is a stable, hashed per-user ID, so misuse is attributed to one user, not your organization. Add **adversarial cases** (injection, jailbreaks) to the eval set, **human review** for high-stakes outputs, and **constrained input and output** (length limits, capped tokens).

```python
def safety_id(email: str) -> str:            # never send the raw email
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()

mod = client.moderations.create(model="omni-moderation-latest", input=user_text)
if not mod.results[0].flagged:   # flagged: block or review per YOUR policy
    client.responses.create(model=MODEL, input=user_text,
                            safety_identifier=safety_id(user_email))
```

Treat scores as **signals for your policy**, not automatic verdicts. Inline moderation does not cover tool names, descriptions or schemas. On GPT-6 Astra agent workflows, a `403` with `misalignment_policy_violation` means stop dispatching actions and do **not** auto-retry.

### 6.12 Error analysis, judge calibration and accuracy targets

OpenAI's evaluation-flywheel cookbook loops **Analyze → Measure → Improve**. Its dashboard steps belong to the Evals transition; the method does not.

1. **Error analysis.** Read about 50 failing traces and label each error specifically (**open coding**), then group the labels into a few categories and count them (**axial coding**). Each category becomes a grader and a dataset slice.
2. **Structured synthetic data.** Define dimensions (channel × intent × persona), generate cases for tuples such as `(chat, cancel_order, first-time customer)`, add perturbations (typos, slang, mixed languages), and have a human review each case.
3. **Align the judge.** Eval sets are imbalanced, so an always-pass judge can score high accuracy. Measure **TPR** (failures caught) and **TNR** (passes passed) against human labels, with about **20%** of labels as few-shot examples, **40%** validation and **40%** a held-out test run **once**. With 18 human passes and 2 failures, an always-pass judge has accuracy 0.9 and TPR 0.0: useless as a gate.
4. **Good enough is a business number.** In the "Optimizing LLM accuracy" example, a resolved case saves $20; failures are 95% wrong escalations ($40 each) and 5% churned customers ($1,000 each), so the expected failure cost is $88 and break-even is 88 / (20 + 88) ≈ 81.5%. Where one failure is very expensive, the AI assists and a human decides; design for graceful failure.
5. **Pull the right lever.** Start with prompt engineering and 20+ ground-truth questions. Inconsistent format, tone or reasoning (**behavior**) → prompt fixes. Missing or proprietary knowledge (**context**) → retrieval ([Chapter 4](../04-built-in-tools-and-mcp/README.md)). Still inconsistent after prompting → fine-tuning, which is being wound down: new jobs have been closed to organizations without prior fine-tuning since 2026-05-07 (and to those with no fine-tuned inference in the last 60 days since 2026-07-02), and existing customers lose job creation on 2027-01-06. Inference on existing fine-tuned models continues until the base model is deprecated.

> **Exam trap:** "The judge agrees 95% of the time" can come from a judge that never flags anything: ask for TPR on real failures, on a held-out split. "85% isn't 99%" is not a launch blocker by itself: compute the break-even point.

### 6.13 The prompt structure toolkit

**Delimiters:** Markdown sections tell the model what kind of text it reads, XML tags mark where content starts and ends, and instructions refer to tags by name. **Placement:** `instructions` / `developer` hold what is true on every request; the `user` turn holds this request's documents in tags. Per-request data in the developer prefix breaks caching and gives that data developer authority. There is **no stop-sequence parameter** on `responses.create` and **no prefill**, so mark the machine-readable part with a tag and parse defensively (code below the table).

| Output lever (strongest first) | What it guarantees | Watch out for |
|---|---|---|
| Structured Outputs (`json_schema`, `strict: true`, or `responses.parse`) | Matches your schema (not truth) | Check `status` and refusals; validate meaning (6.6) |
| JSON mode (`{"type": "json_object"}`) | Valid JSON, not your schema | Legacy; the word "JSON" must appear in the context |
| Output in named XML tags | Nothing, but a missing tag is easy to detect | "Tag not found" is a failure |
| `text.verbosity` / `max_output_tokens` | A default detail level / a ceiling on **reasoning plus output** | Neither is a length instruction |

```python
def read_label(response, allowed: set[str]) -> str:
    if response.status != "completed":
        raise ValueError(f"unusable response: status={response.status}")
    parts = [c for item in response.output if item.type == "message"
             for c in item.content]
    if any(c.type == "refusal" for c in parts):
        raise ValueError("model refused")
    text = "".join(c.text for c in parts if c.type == "output_text")
    match = re.search(r"<label>\s*(\w+)\s*</label>", text)
    if not match or match.group(1).lower() not in allowed:
        raise ValueError(f"no valid <label> in output: {text[:80]!r}")
    return match.group(1).lower()
```

**Few-shot cost.** Zero-shot is the baseline; one example tends to be copied; 3–5 diverse examples give the most consistency. Five 120-token examples on 50,000 calls a day add 30 million input tokens: about **$3 a day on `gpt-6-luna`**, **$300 on `gpt-6-astra`**. Put them in the cached developer prefix: on GPT-5.6+ a cache read costs 0.1× (0.05× on `gpt-6.1-sol`), a write 1.25×, and a prefix needs **1,024** visible input tokens. For single-turn calls, use `prompt_cache_options={"mode": "explicit"}` with a `prompt_cache_breakpoint`. **Chain-of-thought:** don't ask for it; add the missing criterion, test one effort level up, and ask for a `rationale` field before `verdict`.

---

## Lesson code

Video-lesson code: [../../presentations/06-prompt-engineering-and-evals/code/](../../presentations/06-prompt-engineering-and-evals/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run each technique 6.1–6.13, then build an invoice extraction pipeline and a mini eval harness that compares three prompt versions and blocks a critical regression (offline first, live last). |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: 12-question quiz, 7 auto-checked coding exercises, an architecture scenario and a scorecard (pass mark 72%). |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Rules disappear after turn 1 with `previous_response_id` | Resend `instructions` each request | Rewriting the rules louder |
| Answers too long across the product | `text.verbosity="low"` + task-specific length | "Be concise" in every prompt |
| Quality too low on a reasoning model | Add success criteria / stop rules, then one effort level up | Jumping to `xhigh` / `max` |
| Output format varies | 3–5 aligned few-shot examples or Structured Outputs | More adjectives |
| Valid JSON, wrong numbers | Validator + retry with document, previous output, exact error | Trusting the schema |
| Using saved prompt objects in production | Typed prompt builders in a `prompts/` module, in git | Re-saving prompt objects |
| Planning a new eval suite | Own harness or Promptfoo, in the repo, run in CI | OpenAI Evals API |
| Prompt v2 raises the average but breaks a critical case | Block the change and investigate | Shipping on the better mean |
| LLM judge shows 95% agreement | Check TPR on real failures on a held-out split | Trusting accuracy |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Relying on `instructions` to persist** across `previous_response_id` turns.
- **Porting prompts unchanged.** "Think step by step" and "CRITICAL: you MUST" can hurt GPT-6 reasoning models.
- **Sending `temperature` / `top_p` with reasoning on**, or raising effort before fixing a missing success criterion.
- **Using `max_output_tokens` as a length control.** Reasoning tokens count too.
- **Trusting `output_parsed` without checking `status` and refusals**, and blind retries without the error.
- **Gating only on the average score**, or trusting an uncalibrated LLM judge.

## Self-check

**1.** Your support bot chains turns with `previous_response_id`. On turn 1 it follows the tone and refund rules you pass in `instructions`; from turn 2 on, when your code sends only the new user message, it ignores them. What is the fix?

- A) Repeat the rules in capital letters inside the user message
- B) Resend `instructions` on every request (or move the rules into a `developer` message that stays in the stored conversation)
- C) Raise `reasoning.effort` to `high` so the model remembers earlier turns
- D) Switch to Chat Completions, which keeps system messages automatically

<details><summary>Answer</summary>

**B.** The docs state that `instructions` from previous turns are not present in the context when you use `previous_response_id`. A mixes untrusted and trusted content and relies on shouting. C does not change what is in the context. D is a step back to the legacy API, and with Chat Completions you resend the whole history yourself anyway.
</details>

**2.** An invoice extractor uses `responses.parse` with a strict schema. In 5% of documents the total does not equal the sum of the line items. In another 3% the PO number is missing because it appears only in a separate contract you do not send. Which design is correct?

- A) Retry every failure up to 5 times with "please be more careful"
- B) For sum mismatches, retry with the document, the previous extraction and the exact discrepancy; for missing PO numbers return `null` and flag for review (or send the contract)
- C) Make `po_number` a required non-null string so the model must find it
- D) Lower `temperature` for more careful extraction

<details><summary>Answer</summary>

**B.** Retry-with-feedback works when the answer is in the document. It cannot find external information. A has no specific feedback. C forces the model to invent a value. D is not supported with reasoning on and does not address either cause.
</details>

**3.** Prompt v2 raises the average eval score from 0.86 to 0.91, but two cases tagged `critical` that passed on v1 now fail. The release is tomorrow. What should happen?

- A) Ship v2; the average improved
- B) Block v2 until the critical regressions are explained and fixed, then re-run the full suite
- C) Delete the two cases from the dataset because they are outliers
- D) Ship v2 and raise `reasoning.effort` to compensate

<details><summary>Answer</summary>

**B.** A regression gate must check per-case results on critical cases, not only the mean. A and C hide a real regression. D changes a second variable without measuring it.
</details>

**4.** Your LLM judge agrees with human labels on 94% of 200 cases, so the team wants to gate releases on it. Humans marked 12 of the 200 outputs as failures, and the judge caught 1 of them. The judge prompt was tuned on the same 200 cases. What should the architect say?

- A) Ship the gate; 94% agreement is well above the usual 80% bar
- B) The judge is not ready: its TPR is about 8% (1 of 12 real failures), and the number comes from the tuning set. Improve the judge on a validation split, then report TPR and TNR once on a held-out test split
- C) Switch the judge to a 1–10 scale so it can express more nuance
- D) Average three judge runs to raise agreement above 95%

<details><summary>Answer</summary>

**B.** On an imbalanced set, an almost-always-pass judge scores high accuracy while missing the failures the gate exists to catch. The evaluation-flywheel cookbook measures TPR and TNR against human labels and keeps a held-out test split (about 40%) that the judge prompt was never tuned on. A trusts accuracy. C makes calibration harder. D averages the same blind spot.
</details>

## Official documentation

- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering): message roles, `instructions`, Markdown and XML formatting, few-shot, prompting reasoning models
- [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning): `reasoning.effort`, reasoning tokens, `max_output_tokens`, summaries
- [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs): `text.format`, `responses.parse`, refusals, supported schema keywords
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices): eval design, architectures, LLM-as-judge guidance
- [Moving from OpenAI Evals to Promptfoo](https://developers.openai.com/cookbook/examples/evaluation/moving-from-openai-evals-to-promptfoo)
- [Building resilient prompts using an evaluation flywheel](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel) (cookbook): open and axial coding, synthetic data, judge alignment with TPR/TNR. Its dashboard steps belong to the Evals transition; the method does not.

---

[← Chapter 05 — Codex](../05-codex/README.md) | [↑ OpenAI path](../README.md) | [Chapter 07 — Batch API and Cost Optimization →](../07-batch-and-cost/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
