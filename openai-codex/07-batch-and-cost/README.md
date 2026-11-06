# Chapter 07 — Batch API and Cost Optimization

> **Claude counterpart:** [Chapter 7 — Message Batches API](../../anthropic-claude/07-message-batches/README.md) · **Academy course(s):** Optimize AI Application Performance (API pathway) · API Builder Bootcamp: Production & Optimization session · **Est. time:** 6–8 hours (reading + 2 notebooks) · **Status:** [ ] not started

Once a prototype works, the customer asks what it will cost at volume and how fast it will be. Cost on OpenAI comes from four choices: how many requests, how many tokens, which model and which processing tier. Your job is to match each workload to the cheapest option that meets its deadline, and to put a number on it: cost per request, per workload and per successful task.

## What you'll learn

- The cost formula and the lever that moves each term.
- The Batch API lifecycle: JSONL file, `custom_id`, upload, create, poll, download output and error files.
- How to classify failed lines and resubmit only what failed, and how to plan a deadline.
- When to use Standard, `background`, Flex, Batch, Fast or Ultrafast (`service_tier`).
- Prompt caching on GPT-6: stable prefix first, explicit breakpoints, 1.25× writes and 0.1× reads.
- Rate limits, retries by error code, model routing, and production account setup.

## Prerequisites

- [00 — Prerequisites](../../00-prerequisites/README.md), [Chapter 01](../01-responses-api-fundamentals/README.md) (`usage`, `background`, `reasoning.effort`) and [Chapter 02](../02-function-calling-and-structured-outputs/README.md) (strict JSON Schemas).
- [Chapter 06 — Prompt engineering and evals](../06-prompt-engineering-and-evals/README.md): the eval harness proves a cheaper model or tier did not cost you quality.
- Snippets assume `client = OpenAI()` and `MODEL = "gpt-6-luna"`, the cheapest GPT-6 model and the right default for high-volume extraction.

---

## Concepts

### 7.1 The cost levers

OpenAI's [cost-optimization guide](https://developers.openai.com/api/docs/guides/cost-optimization) boils down to two moves: use fewer tokens, or pay less per token. For one request:

```text
cost = ( uncached_input × P_in
       + cached_input   × P_in × read_multiplier  # 0.1 (0.05 on gpt-6.1-sol)
       + cache_write    × P_in × 1.25             # 30m lifetime; 2.5 for 12h (GPT-5.6+)
       + output_tokens  × P_out )                 # INCLUDES reasoning tokens
       × tier_multiplier       # Batch/Flex 0.5, Std 1, Fast 2, Ultrafast 6
       × region_multiplier     # 1.1 for regional processing on newer models
       + tool fees             # e.g. web search, file search calls
```

| Lever | What it changes | Where |
|---|---|---|
| Fewer requests | Combine steps, skip the LLM where code will do | 7.11 |
| Fewer input and output tokens | Trimmed context, `max_output_tokens`, lower `reasoning.effort` | 7.10, 7.11 |
| Cheaper repeated input | Prompt caching | 7.7 |
| Cheaper per token | Batch or Flex (50% off) | 7.2–7.6 |
| Cheaper model | Luna instead of Sol or Astra, or a cascade | 7.11 |
| Faster, not cheaper | Fast / Ultrafast, streaming, cache prewarming | 7.6, 7.7 |

Standard prices per 1M tokens (input / output) are $0.10 / $0.50 for `gpt-6-luna`, $2.00 / $10.00 for `gpt-6.1-sol` and $10.00 / $50.00 for `gpt-6-astra` ([pricing page](https://developers.openai.com/api/docs/pricing)). Requests over 272K input tokens cost 2× on input and cache rates and 1.5× on output. **Reasoning tokens are billed as output**, and output is 5× the input price, so check `usage.output_tokens_details.reasoning_tokens` before you blame prompt length.

### 7.2 Batch API: the lifecycle

The Batch API runs a file of requests asynchronously: **50% off**, a **separate rate-limit pool** (it does not use your per-model RPM/TPM), and completion **within 24 hours**. It supports `/v1/responses` and the other main endpoints, and all three GPT-6 models. A nightly batch therefore does not cause daytime `429`s on synchronous traffic. Statuses: `validating` → `in_progress` → `finalizing` → `completed`. A rejected file ends in `failed`, a batch that runs out of time in `expired`, and `batches.cancel()` goes through `cancelling` to `cancelled`.

Each JSONL line holds a unique `custom_id`, `method`, `url` and a `body`. A batch line is raw JSON (`responses.parse(text_format=...)` does not exist here), so write the strict schema yourself (every property `required`, `additionalProperties: false`) and validate the output with Pydantic after download.

```python
def batch_line(custom_id: str, document: str) -> dict:
    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/responses",
        "body": {
            "model": MODEL,                  # ONE model per input file
            "instructions": INSTRUCTIONS,    # identical on every line
            "input": f"<document>\n{document}\n</document>",  # varies, last
            "text": {"format": {"type": "json_schema", "name": "invoice",
                                "schema": INVOICE_SCHEMA, "strict": True}},
        },
    }
```

Then run the lifecycle:

1. **Upload:** `client.files.create(file=f, purpose="batch")`.
2. **Create:** `client.batches.create(input_file_id=..., endpoint="/v1/responses", completion_window="24h")`. The `endpoint` must match the `url` on every line, and `"24h"` is the only supported window.
3. **Wait:** poll `client.batches.retrieve(batch.id)` every few minutes, or subscribe to the `batch.completed`, `batch.failed`, `batch.expired` and `batch.cancelled` [webhooks](https://developers.openai.com/api/docs/guides/webhooks).
4. **Download:** a finished batch has an `output_file_id` (successes) and an `error_file_id` (failures), both JSONL with the `custom_id`; read them with `client.files.content(file_id).text`.

**Limits to design around:** 50,000 requests and 200 MB per file, 2,000 batch creations per hour, one model per file, and a per-tier queue of pending prompt tokens per model. Output files are deleted 30 days after completion by default (`output_expires_after`: 1 h to 30 days), so copy results to your own store.

### 7.3 Designing `custom_id`s and the input file

Output line order **may not match** input order. `custom_id` is your only join key, so design it like a primary key:

- **Business key plus prompt version**, for example `inv-000123__invoice-v3`, so a v3 retry is never mistaken for a v2 result. **Deterministic:** no timestamps or UUIDs.
- **Reserve the separator** (`("a__b", "c")` collides with `("a", "b__c")`), and use `[A-Za-z0-9_-]` with no PII: portable to Claude's `^[a-zA-Z0-9_-]{1,64}$`, and IDs end up in logs.

Keep a **manifest** per batch: `batch_id`, `input_file_id`, model, prompt version and the submitted `custom_id`s. Write it as soon as `batches.create` returns, before polling, so a crash cannot lose a running, billable batch. Afterwards compute `missing = submitted − (seen in output ∪ seen in errors)`. Lint the file before upload: one model per file, one endpoint per batch. Put the stable part (instructions, schema) first and identical on every line, and the document last. On GPT-6 that is necessary but not sufficient for caching; see [7.7](#77-prompt-caching).

### 7.4 Reading results and handling failures

An error-file line has either a top-level `error` (for example `"code": "batch_expired"`) or a `response` whose `status_code` is not 200. There are five failure layers:

| Layer | How it shows up | Resubmit? |
|---|---|---|
| Batch failed validation | `batch.status == "failed"`, details in `batch.errors` | Fix the file, create a new batch |
| Request expired | `error.code == "batch_expired"` | **Yes, as-is** (or via Flex/Standard if the deadline is close) |
| Transient server error | `429` or `5xx` `status_code` | **Yes, as-is**, unless it is a billing, spend or quota code: then **stop and alert** ([7.9](#79-retries-and-backoff)) |
| Invalid request | `4xx` (for example, input exceeds the context window) | **No.** Fix it first (split, shorten) |
| Failure on a 200 | `body.status == "incomplete"`, refusal, JSON that fails validation | Raise the limit, retry with feedback, or human review |

```python
def classify(line: dict) -> tuple[str, Invoice | None]:  # Invoice: Pydantic
    if line.get("error"):
        return line["error"].get("code") or "error", None  # "batch_expired"
    response = line.get("response") or {}
    status_code = response.get("status_code")
    if status_code != 200:  # is_billing_error(): the 7.9 billing codes
        err = (response.get("body") or {}).get("error") or {}
        if is_billing_error(err.get("code"), err.get("type")):
            return f"billing:{err.get('code') or err.get('type')}", None
        return f"http_{status_code}", None
    body = response["body"]
    if body.get("status") != "completed":
        reason = (body.get("incomplete_details") or {}).get("reason")
        return f"incomplete:{reason}", None
    try:  # output_text() joins the output_text parts of the raw body
        invoice = Invoice.model_validate_json(output_text(body))
    except ValidationError:
        return "invalid_output", None
    return "ok", invoice
```

**Resubmit only what failed.** Rebuild the retry JSONL from the manifest, keep the same `custom_id`s, and include only `batch_expired`, `429` and `5xx` lines. Billing codes go to a human; everything else is fixed first. Re-running the whole batch after 2% failures doubles the cost of the 98% that succeeded. In an expired batch you pay for the requests that did complete. Failed-line billing is not documented, so reconcile with the batch `usage` and the Costs API. `client.batches.cancel(batch_id)` stops a batch with a prompt bug; in-flight requests drain for up to 10 minutes.

### 7.5 SLA planning and choosing sync, background, Flex or Batch

Batch promises "within 24 hours", so plan with the worst case: `latest_submit = deadline − 24 h − retry_path_time − safety_buffer`. With a 30-hour deadline, 30 − 24 = 6 hours is the latest submit time with **zero** time for retries. A retry batch adds another 24 hours; a Flex or Standard retry path adds its own time. For a continuous stream, submit in rolling windows.

| Option | How you call it | Price | Result arrives | Good for |
|---|---|---|---|---|
| Standard | `responses.create(...)` | 1× | Seconds | Users waiting |
| `background=True` | Poll `responses.retrieve` or webhook | 1× | Minutes | Long runs that would time out a connection |
| Flex | `service_tier="flex"` | 0.5× | Slower; sometimes `429` | Evals, enrichment; sync API |
| Batch API | JSONL + `batches.create` | 0.5× | Within 24 h | Bulk offline jobs |
| Fast | `service_tier="fast"` | 2× | Up to 2.5× faster | Latency is the product |
| Ultrafast | `service_tier="ultrafast"` on `gpt-6-astra` or `gpt-6.1-sol` | 6× | Fastest | Latency-critical Astra/Sol agents |

A pre-merge check or a live support reply must be synchronous; a nightly report belongs in Batch. `background` is not a discount: it is Standard pricing with an async call pattern.

### 7.6 Service tiers: `service_tier`

`service_tier` is a request parameter on Responses and Chat Completions:

- Omitted / `"auto"`: the project's configured tier (`"default"` unless changed; if the project is set to Fast, these bill as Fast).
- `"default"`: Standard. `"flex"`: batch prices, slower, occasionally unavailable.
- `"fast"` / `"priority"`: Fast mode (renamed from Priority processing on 2026-07-30).
- `"ultrafast"`: broadly available for `gpt-6-astra` and `gpt-6.1-sol`, with its own separate rate limits.
- `"scale"`: purchased Scale Tier on eligible earlier models; Reserved Tier for GPT-5.6 and later.

**Log `response.service_tier`.** It reports the tier that actually served the request. If Fast traffic ramps too fast, some requests run and bill at Standard and come back as `"default"`. **Allowed service tiers per project:** A disallowed tier fails with `400` `invalid_request_error`, `error.param == "service_tier"`. Use it as a guardrail (a bulk-job project can disallow `priority`), and never retry it: it is a configuration error.

**Flex.** Use a longer timeout (OpenAI's example is 15 minutes; the SDK default is 10). When Flex lacks capacity it returns `429 Resource Unavailable`, and you are **not charged**. Back off on Flex, or fall back to Standard with `service_tier="default"` set **explicitly**, so a project set to Fast does not bill the fallback at 2×. Don't back off on billing `429`s. The practice notebook's `create_flex_with_fallback` bounds the whole call by a deadline and honors `Retry-After`. **Fast** shares the Standard rate limit. With EU data residency it works on `gpt-6-luna` and `gpt-6.1-sol`, but not on `gpt-6-astra` (or `gpt-6-sol`). Don't run ETL in Fast mode.

### 7.7 Prompt caching

Prompt caching reuses work for an **identical prompt prefix**: tools, developer instructions, `text.format` schema and history, in order. It is on by default. Any change before a breakpoint (a timestamp, reordered tools, a different `reasoning.effort`) breaks the match.

| GPT-6 rule (GPT-5.6 and later) | Value |
|---|---|
| Minimum cacheable prefix | 1,024 tokens |
| Write / read | 1.25× (30m) or 2.5× (12h) / 0.1× the input rate (read **0.05×** on `gpt-6.1-sol`) |
| Lifetime | `prompt_cache_options.ttl`: `"30m"` (default) or `"12h"`; `prompt_cache_breakpoint.ttl` overrides it per breakpoint. openai 3.24 type hints still list only `"30m"` |
| Breakpoints | Implicit (default): one at the end of the latest eligible message. Explicit: `prompt_cache_breakpoint: {"mode": "explicit"}`; up to four cache writes per request |
| Explicit-only mode | `prompt_cache_options={"mode": "explicit"}`: content after your last breakpoint is plain input, no write |
| `prompt_cache_key` | Separates cache accounting per tenant |

One write plus nine reuses costs 2.15× the plain input price instead of 10×. A prefix written but **never reused** costs 25% more than not caching.

**Why a shared prefix is not always cached.** In implicit mode the breakpoint sits at the end of the user message, so request 1 writes *rules + document A* and request 2 cannot match it. Put an explicit breakpoint after the static content. Top-level `instructions` **cannot** hold one, so use a `developer` block:

```python
response = client.responses.create(
    model=MODEL,
    prompt_cache_options={"mode": "explicit"},  # document is never written
    prompt_cache_key="invoices:tenant-042",     # per-tenant accounting
    input=[
        {"role": "developer", "content": [{
            "type": "input_text",
            "text": STATIC_RULES,                # well over 1,024 tokens
            "prompt_cache_breakpoint": {"mode": "explicit"},
        }]},
        {"role": "user", "content": f"<document>\n{document}\n</document>"},
    ],
)
details = response.usage.input_tokens_details
print(details.cached_tokens, details.cache_write_tokens)
```

Keep tools stable (`tool_choice="none"` instead of removing them), append history instead of rewriting it, and pad a 900-token prefix with useful content past 1,024. `prompt_cache_options={"prewarm": True}` writes a prefix without generating output (billed at the write rate), for example at app startup. On GPT-5.5 and earlier there is no explicit mode or write charge, and lifetime is set with `prompt_cache_retention`.

### 7.8 Rate limits, usage tiers and spend controls

Rate limits apply per organization and project, per model, in **RPM** and **TPM**. Your usage tier upgrades automatically as total credit purchases grow (rate-limits guide, checked 2026-11-06):

| Tier | Qualification | Monthly usage limit | `gpt-6-luna` RPM / TPM | Astra, Sol, Terra RPM / TPM |
|---|---|---|---|---|
| Free | Allowed geography | $100 | Not listed | Not listed |
| Build | $5 in credit purchases | $500 | 5,000 / 2,000,000 | 5,000 / 1,000,000 |
| Launch | $100 in credit purchases | $5,000 | 10,000 / 10,000,000 | 10,000 / 4,000,000 |
| Grow | $500 in credit purchases | $200,000 | 30,000 / 180,000,000 | 15,000 / 40,000,000 |

Astra, Sol and Terra share a lower limit than Luna. For capacity planning, the TPM estimate uses your output cap, so a 32,000-token `max_output_tokens` consumes far more budget than it uses; size the cap from observed `usage`. **Cached tokens count toward TPM**: caching cuts cost, not rate-limit usage. Log the `x-ratelimit-*` headers and `Retry-After` (via `client.responses.with_raw_response.create(...)`). A `429` with `error.code == "slow_down"` means traffic grew too fast: above 1M TPM, ramp at most 50% every 15 minutes.

**Spend controls.** A spend alert only notifies. A hard spend limit makes requests fail with `429` `organization_spend_limit_exceeded` or `project_spend_limit_exceeded`; OpenAI's tier limit returns `organization_usage_limit_exceeded`. Enforcement is not instant. Separate staging and production projects (7.12) so a runaway test cannot exhaust production's budget.

### 7.9 Retries and backoff

Not every `429` is a rate limit. Classify by HTTP status and `error.code`:

| Signal | Action |
|---|---|
| `429` rate limit, `slow_down`, `503` `server_is_overloaded` | Honor `Retry-After`, else exponential backoff with jitter; slow down on `slow_down` |
| `500`, `408`, connection error | Retry with backoff; make the operation idempotent |
| `429` billing: `insufficient_quota` type, `credit_balance_exhausted`, `*_spend_limit_exceeded`, `organization_usage_limit_exceeded` | **Do not retry.** Alert a human |
| `400` (bad param, context too long, invalid `service_tier`) | Fix the request or project settings |
| Validation failure on a `200` | Retry **with feedback** (chapter 06), not backoff |

The Python SDK already retries connection errors, `408`, `409`, `429` and `>=500` **twice by default**, honoring `Retry-After` up to 120 s (a longer requested wait is not retried; it raises at once). It never reads `error.code` (it only obeys an `x-should-retry` header), so a billing `429` can be retried too. **If you write your own loop, set `max_retries=0` on that client**, or each attempt becomes up to three requests. A production version also bounds the total time: each attempt's timeout is the time left. `retry_action()` (practice 7.9) classifies status plus `error.code`; `server_delay()` reads `Retry-After`.

```python
import random, time
from openai import APIConnectionError, APIStatusError

def call_with_backoff(max_attempts: int = 5, **kwargs):
    api = client.with_options(max_retries=0)  # SDK retries off: we own it
    for attempt in range(max_attempts):
        try:
            return api.responses.create(**kwargs)
        except APIStatusError as err:
            action = retry_action(err.status_code, err.code, err_type=err.type)
            if action not in ("backoff", "reduce_rate"):  # billing, auth, 400
                raise
            delay = max(server_delay(err.response.headers) or 0.0,
                        2 ** attempt)  # Retry-After is a minimum
        except APIConnectionError:     # includes APITimeoutError
            delay = 2 ** attempt
        if attempt < max_attempts - 1:  # no pointless wait after the last try
            time.sleep(delay + random.uniform(0, 1))  # jitter: no lockstep
    raise RuntimeError("retry budget exhausted; defer the request")
```

### 7.10 Cost modeling per request and per workload

**Per request**, read `response.usage` (or each `body.usage` in a batch output file) and apply the 7.1 formula:

```python
PRICES = {  # USD per 1M tokens, Standard, 30m writes. Re-check the pricing page.
    "gpt-6-luna":  {"input": 0.10,  "cached": 0.01, "write": 0.125, "output": 0.50},
    "gpt-6.1-sol": {"input": 2.00,  "cached": 0.10, "write": 2.50,  "output": 10.00},
    "gpt-6-astra": {"input": 10.00, "cached": 1.00, "write": 12.50, "output": 50.00},
}
TIER_MULTIPLIER = {"default": 1.0, "flex": 0.5, "batch": 0.5, "fast": 2.0,
                   "priority": 2.0, "ultrafast": 6.0}

def request_cost(model: str, usage, tier: str = "default") -> float:
    p, d = PRICES[model], usage.input_tokens_details
    plain = usage.input_tokens - d.cached_tokens - d.cache_write_tokens
    dollars = (plain * p["input"] + d.cached_tokens * p["cached"]
               + d.cache_write_tokens * p["write"]
               + usage.output_tokens * p["output"]) / 1_000_000
    return dollars * TIER_MULTIPLIER[tier]
```

**Per workload**, multiply by volume and add retries, escalations, tool calls and eval runs. Example: invoice extraction, 2,000 input tokens (1,200 a cached prefix), 400 output tokens. Per request (Standard, cache hit) that is $0.000292 on `gpt-6-luna`, $0.005720 on `gpt-6.1-sol` and $0.029200 on `gpt-6-astra`. For 100,000 requests: $29.20 / $572.00 / $2,920.00 on Standard, and $14.60 / $286.00 / $1,460.00 on Batch.

Model choice moves cost **100×**, the tier **2×**, and caching moved Luna from $0.000400 to $0.000292 (27%). Optimize in that order, and check quality. **Report cost per successful task:** if Luna passes validation 92% of the time and failures go to a human at $0.50 each, the review queue dominates the cost.

**Monitor.** Log model, served `service_tier`, token counts, latency, prompt version and cost per request. Reconcile daily with the **Costs API** (`client.admin.organization.usage.costs(...)`, which needs an Admin key). Before a large batch, count a sample's tokens with `client.responses.input_tokens.count(...)` on the same payload you will send.

### 7.11 Model routing and cascades

OpenAI's deployment checklist: "Choose the model that performs well on representative tasks rather than routing every request to the most capable model." `gpt-6-luna` is the most efficient (extraction, classification, routing). `gpt-6.1-sol` gives near-Astra performance at lower cost (complex extraction, most agent work). `gpt-6-astra` is the most capable (hardest reasoning, coding, LLM judges). Routing patterns, cheapest first:

1. **Static routing by task type:** each step gets the cheapest model that passes its eval.
2. **Routing by size or features:** count tokens first; send long or multimodal inputs to the model whose eval covers them.
3. **Cascade:** run Luna; if the output fails schema or business-rule validation, re-run on Sol. With an 8% escalation rate, `0.000292 + 0.08 × 0.00572 ≈ $0.00075` per document, about **7.6× cheaper** than all-Sol.
4. **Effort before model:** try one `reasoning.effort` level up on the same model first. Reasoning tokens are output tokens, so measure it. Luna accepts `none` … `max`; Sol and Astra start at `low` (no `none`).

A cascade without an eval is a guess: if Luna produces valid but wrong values, nothing escalates them. Gate the change with the chapter 06 eval harness. Distilling into a smaller fine-tuned model is not taught here: self-serve fine-tuning is closed to new organizations and ends for existing customers on 2027-01-06.

### 7.12 Production readiness: setting up the account

The controls in 7.6–7.10 only work if the organization is set up for production ([production best practices](https://developers.openai.com/api/docs/guides/production-best-practices), [spend limits](https://developers.openai.com/api/docs/guides/spend-limits)):

| Area | What to set up |
|---|---|
| Roles | **Readers** make requests; **owners** also manage billing and members. Without the org header (`OPENAI_ORG_ID`), the default organization is billed |
| Projects | Separate **staging** and **production** projects, each with its own rate and spend limits |
| Allowed service tiers | A batch project should not allow `priority`/`fast`, so a wrong tier fails with `400` |
| API keys | From env vars or a secret manager; set an **expiration date** and rotate (create, deploy, verify, revoke) |
| Spend, cost, scaling, compliance | **Spend alerts** below **hard spend limits**; per-request cost log; daily Costs API reconciliation with an Admin key outside app code; horizontal scaling, rate-limit-aware queues; data retention (`store`, ZDR); Fast with EU data residency is not available on `gpt-6-astra` (or `gpt-6-sol`) |

If a staging load test hits the hard spend limit and production goes down, the fix is not a higher limit. Put staging in its **own project** so a test can only stop itself.

---

## Lesson code

Video-lesson code: [../../presentations/07-batches-and-cost/code/](../../presentations/07-batches-and-cost/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Work through 7.1–7.12 offline against a fake batch server behind the real SDK, then build a batch extraction pipeline with resubmission and a cost report |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: 11-question quiz, 6 coding exercises, an architecture scenario and a scorecard (pass mark 72%) |

## Cheat-sheet

| Situation | Choose | Why |
|---|---|---|
| 400,000 records to score by next week | Batch API, chunked to ≤ 50,000 lines | 50% off and a separate rate-limit pool |
| Developer waiting on a pre-merge check | Standard (streaming) | Someone is blocked: it needs seconds, not a 24-hour window |
| Eval runs that should finish within hours | Flex with backoff and a Standard fallback | Batch price, synchronous API |
| 3% of batch lines failed | Classify, then resubmit only retryable `custom_id`s | Pay only for what failed |
| Same 3,000-token instructions on every request | Stable prefix first, explicit breakpoint after it | Writes 1.25×, reads 0.1× |
| `429` with `insufficient_quota` / spend-limit code | Stop and alert | Retrying cannot fix billing |
| "Use Astra for everything to be safe" | Cheapest model that passes the eval, plus a cascade | 100× price spread between Luna and Astra |
| Bulk-job project must never pay Fast rates | Disallow `priority`/`fast` in its allowed service tiers | A wrong tier fails with a `400` |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Joining batch results by line order.** Join by `custom_id`.
- **Treating `status_code == 200` as success.** A 200 can carry `status: "incomplete"`, a refusal or invalid JSON.
- **Re-running the whole batch** after a few failures, or resubmitting invalid requests unchanged.
- **Planning SLAs on the typical completion time** instead of the 24-hour worst case plus a retry path.
- **Treating every `429` the same:** backing off on a billing error, or hammering through `slow_down`.
- **Routing to a cheaper model without an eval**, or reporting cost per request instead of cost per successful task.

## Self-check

**1.** A team builds a nightly batch of 30,000 invoice extractions. They store results by enumerating the output file and matching line *n* to input document *n*. Some mornings the numbers are attached to the wrong vendors. What is the fix?

- A) Sort the output file by `id` before matching
- B) Join on a deterministic `custom_id` derived from the document ID and prompt version, and keep a manifest of submitted IDs
- C) Submit 30,000 one-line batches so order cannot change
- D) Switch to `background=True` so results come back in order

<details><summary>Answer</summary>

**B.** The guide states that output order may not match input order and tells you to use `custom_id`. A: `batch_req_...` IDs are not your join key. C hits the 2,000-batches-per-hour creation limit and loses the batch's purpose. D is a different feature at full price.
</details>

**2.** A data-enrichment job must finish within about 4 hours, is not user-facing, and the team wants the lowest price without managing files. Which option fits best?

- A) Batch API
- B) Flex (`service_tier="flex"`) with a longer timeout, exponential backoff on `429`, and a fallback to Standard when the deadline gets close
- C) Fast mode
- D) `background=True` on Standard

<details><summary>Answer</summary>

**B.** Flex is priced at batch rates but stays a synchronous call, and a `429 Resource Unavailable` is not charged. A has a 24-hour window, which does not fit a 4-hour deadline. C costs 2×. D is full price.
</details>

**3.** An extraction service on `gpt-6.1-sol` sends a 3,000-token rule block followed by a different document each time, in implicit caching mode. `cached_tokens` is always 0, but `cache_write_tokens` is high. Why, and what fixes it?

- A) Caching is off by default; enable it with `prompt_cache_key`
- B) The implicit breakpoint sits after the document, so each request writes a prefix nobody reuses. Put the rules in a `developer` `input_text` block with an explicit `prompt_cache_breakpoint`, and consider `prompt_cache_options={"mode": "explicit"}`
- C) Move the rules into `instructions` and add the breakpoint there
- D) Set `prompt_cache_retention="24h"`

<details><summary>Answer</summary>

**B.** In implicit mode the breakpoint is at the end of the latest user message, so the reusable prefix ends inside it. A: caching is on by default; the key only separates accounting on GPT-6. C: `instructions` cannot hold an explicit breakpoint. D applies to models before GPT-5.6; GPT-6 uses `prompt_cache_options.ttl`.
</details>

**4.** Overnight, a job starts returning `429` errors with `error.code == "project_spend_limit_exceeded"`. The retry wrapper backs off and retries for hours. What is wrong?

- A) Nothing; exponential backoff is the documented fix for every `429`
- B) A spend-limit `429` needs a human to raise the limit (or wait for the monthly reset); the handler should stop and alert, and only retry rate-limit, `slow_down` and overload conditions
- C) The job should switch to `service_tier="fast"` to bypass the limit
- D) Move the traffic to another project in the same organization without telling anyone

<details><summary>Answer</summary>

**B.** OpenAI's error guide: retrying billing, spend or quota errors won't restore access. A misreads the guidance. C still bills the same project. D bypasses a control someone set on purpose.
</details>

## Official documentation

- [Batch API](https://developers.openai.com/api/docs/guides/batch): JSONL format, endpoints, statuses, output and error files, limits, expiration
- [Flex processing](https://developers.openai.com/api/docs/guides/flex-processing): `service_tier="flex"`, timeouts, `429 Resource Unavailable`
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching): implicit and explicit modes, pricing multipliers, lifetime, keys, break-even
- [Rate limits](https://developers.openai.com/api/docs/guides/rate-limits): usage tiers, headers, `slow_down`, backoff · [Error codes](https://developers.openai.com/api/docs/guides/error-codes)
- [Pricing](https://developers.openai.com/api/docs/pricing): Standard, Batch, Flex, Fast and Ultrafast tables
- [Cost optimization](https://developers.openai.com/api/docs/guides/cost-optimization) · [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)

---

[← Chapter 06 — Prompt Engineering and Evals](../06-prompt-engineering-and-evals/README.md) | [↑ OpenAI path](../README.md) | [Chapter 08 — Task Decomposition and Orchestration →](../08-task-decomposition-and-orchestration/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
