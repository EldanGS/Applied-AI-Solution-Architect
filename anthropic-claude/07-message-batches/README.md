# Chapter 7 — Message Batches API

> **Exam domain(s):** Domain 4 — Prompt Engineering & Structured Output (**20%**, task 4.5 batch processing; builds on 4.4 retry loops) · Domain 5 — Context Management & Reliability (**15%**, failure handling and recovery around 5.3, review routing from 5.5) · also CCDV-F Domain 2.3 (batch API use, realtime vs batch) and Domain 5.4 (cost and token management)
> **Est. time:** 4–6 hours (reading + 2 notebooks) · **Status:** [ ] not started

Most enterprise LLM work is not chat. It is piles: contracts to extract, tickets to classify, eval suites to run. The Message Batches API halves the price of every token in exchange for giving up latency guarantees. The architect decides which workloads can wait, plans the schedule so the 24-hour bound still meets the SLA, and builds the code that correlates, validates and resubmits results.

## What you'll learn

- The core facts: 50% discount, up to 24 hours with no latency SLA, 100,000 requests or 256 MB per batch, results kept for 29 days.
- How to choose batch or synchronous from a workload's latency tolerance, and what a batch request cannot do (run your client tools mid-request).
- How to design `custom_id`, track a batch to `ended`, triage results and resubmit **only** the failures.
- How to plan a submission cadence for an SLA and build a cost model with caching and model choice.
- The operational limits: rate limits, retention, ZDR and HIPAA, cloud platforms.

## Prerequisites

- [00 — Prerequisites](../../00-prerequisites/README.md) (`.env` with `ANTHROPIC_API_KEY`), [Chapter 1 — Claude API Fundamentals](../01-claude-api-fundamentals/README.md) (`stop_reason`, usage fields).
- [Chapter 2 — Tool Use](../02-tool-use/README.md) (client vs server tools, `pause_turn`) and [Chapter 6 — Prompt Engineering](../06-prompt-engineering/README.md) (validation and retry-with-feedback).

## Concepts

### 7.1 What the Message Batches API is

You send a list of ordinary Messages API requests. Each is a pair: a `custom_id` you choose and a `params` object with exactly what you would pass to `client.messages.create()`. Requests run asynchronously and independently, and you get one result file when the batch ends.

| Property | Value |
|---|---|
| Price | **50% of standard prices** for all usage, cache writes and reads included |
| Processing time | Most batches finish in under 1 hour. **Up to 24 hours. No latency SLA.** Requests not run by then come back `expired` (not billed) |
| Size limit | **100,000 requests or 256 MB**, whichever comes first |
| `custom_id` | 1–64 characters, `^[a-zA-Z0-9_-]{1,64}$`, unique within the batch |
| Result order | **Not guaranteed.** Match by `custom_id`, never by position |
| Retention | **29 days after `created_at`**, in the Workspace that created it |
| SDK methods | `client.messages.batches.create`, `retrieve`, `list`, `results`, `cancel`, `delete` |

```python
import os, anthropic
from dotenv import load_dotenv
from anthropic.types.message_create_params import (
    MessageCreateParamsNonStreaming,
)
from anthropic.types.messages.batch_create_params import Request

load_dotenv()                                  # loads ANTHROPIC_API_KEY
client = anthropic.Anthropic()                 # never hardcode the key
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
docs = {"inv-00001": "Invoice text ...", "inv-00002": "Invoice text ..."}

batch = client.messages.batches.create(requests=[
    Request(custom_id=doc_id, params=MessageCreateParamsNonStreaming(
        model=MODEL, max_tokens=1024,
        system="Extract the invoice fields as JSON.",
        messages=[{"role": "user", "content": text}],
    ))
    for doc_id, text in docs.items()
])
print(batch.id, batch.processing_status)   # msgbatch_..., "in_progress"
```

> **Exam trap:** "Up to 24 hours" is a **ceiling, not a promise**. Your design must work when a batch takes 23 hours. A failed request does not fail the batch, and `errored`, `canceled` and `expired` requests are **not billed**.

### 7.2 Batch vs synchronous: matching the API to latency requirements

The deciding question is not "how many requests?" but **"is anyone (a person or a pipeline stage) blocked waiting for this answer?"** If yes, use the synchronous Messages API. If the result is consumed later on a schedule, batch it. When work must stay synchronous, cut cost with prompt caching, a smaller model (Haiku 5.5, the current small tier), lower `effort` and tight `max_tokens`.

| Workload | API | Reasoning |
|---|---|---|
| Pre-merge check that blocks merging (official sample) | **Synchronous** | Someone waits on every run, and a batch may take 24 hours |
| Support-chat reply, fraud flag on a live payment | **Synchronous** | A customer or a transaction is on hold |
| Tech-debt report read at the next morning's stand-up (official sample) | **Batch** | Consumed hours later, on a schedule |
| 10,000 non-urgent documents overnight, cost-driven | **Batch** | The textbook case (CCDV-F sample question) |
| Nightly CRM enrichment, quarterly contract re-classification | **Batch** | Nobody is waiting; the data is read next day or later |
| Eval suite of 5,000 cases before a model upgrade | **Batch** | Throughput and cost matter, not latency |

> **Exam trap:** "Move *both* workflows to batch and fall back to synchronous if a batch takes too long" is wrong for a blocking check: the developer still waits for the timeout, and you pay for both paths. "Keep both synchronous to avoid ordering problems" is wrong too: `custom_id` solves ordering.

> **Exam trap (vocabulary):** Three things share the word "batch" and are not this API: (1) Claude Code has **no `--batch` flag** (non-interactive CI runs use `claude -p`, see [Chapter 5](../05-claude-code/README.md)); (2) the Academy "**batch tool**" is a tool-design pattern (one tool that accepts a list of calls) and runs synchronously; (3) "batching findings back to the coordinator" in multi-agent questions is about orchestration.

### 7.3 What can and cannot be batched

Almost any Messages request can go in a batch: vision and PDFs, system prompts, multi-turn histories you build in advance, thinking and `effort`, structured outputs, prompt caching, and tool definitions, including **all server tools** (web search, web fetch, code execution, MCP connector, advisor, tool search).

Four parameters are rejected: `stream: true`, `speed` (fast mode), `max_tokens: 0` (cache pre-warming) and the beta `fallbacks` (comes back as a per-item `errored` result). Validation is asynchronous, so lint these out before you submit.

**The tool-calling limitation.** Each batch request produces exactly one response, with no connection back to your app. If Claude calls a **client tool** (a function *your* code runs, such as `read_file`), the request just ends with `stop_reason: "tool_use"`. Every round trip needs a *new* request, with another wait of up to 24 hours. Server tools are different. Anthropic runs them, so their loop runs **inside** the batch. If it hits the iteration limit, the result has `stop_reason: "pause_turn"`, and you continue in a follow-up request.

> **Exam trap:** If the workflow depends on Claude calling *your* tool and then carrying on with the answer, a batch breaks it: nothing in the batch can run your code and hand the result back within the same request. Tool definitions are allowed, and results are still matched by `custom_id`; the missing piece is the round trip. Fix: keep it synchronous, or gather the context first, put it in the prompt, then batch a single-turn analysis.

### 7.4 Designing `custom_id`

`custom_id` is the only link between a result and its source. Results come back in any order, so treat it as a primary key. It lets you link each result to its document, find exactly which ones failed, and resubmit only those.

| Do | Avoid | Why |
|---|---|---|
| Derive it from your record key (`inv-2026-000417`) | List position (`req-17`) | Results are unordered; the list changes on resubmission |
| Keep a ledger: `custom_id → source, hash, attempt, batch_id, status` | Encoding everything into the ID | 64 characters run out; the ledger is your audit trail |
| Add a chunk suffix when you split a document (`-c2`) | Reusing the parent ID | Chunks must be re-assembled per parent |
| Hash long or sensitive keys; keep the same ID across retries | Raw paths, emails, a new random ID per attempt | Illegal characters, PII; one item = one key |

> **Exam trap:** Any answer that resubmits the whole batch, or re-runs "the last N requests", ignores `custom_id`.

### 7.5 Tracking a batch: polling, streaming results, cancel and delete

**Poll** `retrieve()` until `processing_status == "ended"` (`in_progress` → optional `canceling` → `ended`). Back off on long batches, because status calls count against the batch rate limit.

**Persist the batch ID first.** If your code crashes after `create()` without saving the ID, a restart submits the work again and you pay twice. Save `batch_id` with its `custom_id` list, and resume polling on restart.

```python
import json, pathlib, time

STATE = pathlib.Path("batch_state.json")

def submit_once(requests: list[Request]) -> str:   # never submits twice
    if STATE.exists():
        return json.loads(STATE.read_text())["batch_id"]
    batch = client.messages.batches.create(requests=requests)
    STATE.write_text(json.dumps({
        "batch_id": batch.id,
        "custom_ids": [r["custom_id"] for r in requests],
    }))
    return batch.id

def wait_until_ended(batch_id: str, delay: float = 30, max_delay: float = 600):
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            return batch                      # request_counts are now final
        time.sleep(delay)
        delay = min(delay * 2, max_delay)
```

**Stream results.** `client.messages.batches.results(batch_id)` streams the `.jsonl` file one result at a time. Before `ended`, it raises because `results_url` is still `null`. **Cancel** moves the batch to `canceling`. Finished requests keep their results; unsent ones become `canceled` (not billed). **Delete** works only after processing has ended.

> **Exam trap:** While a batch is `in_progress`, `request_counts.succeeded` stays **0**. The outcome counters fill in only when the whole batch ends, so "zero succeeded after 40 minutes" is not a failure.

### 7.6 Result types and resubmitting only the failures

Every request ends as one of four `result.type` values. Only `succeeded` is billed. `errored` carries `result.error`: fix an `invalid_request_error` before resending, and resend server errors as is. `canceled` and `expired` never ran: resubmit them, synchronously if the deadline is close. **"Succeeded" is not "usable"**, so check every succeeded result:

| Situation | Detect with | Action |
|---|---|---|
| Refused | `stop_reason == "refusal"` | Fallback model or review; count refusals as their own metric |
| Truncated or context full | `stop_reason` is `max_tokens` or `model_context_window_exceeded` | Raise `max_tokens`, or chunk the input |
| Unfinished turn | `pause_turn` or `tool_use` | Continue in a follow-up, or redesign (7.3) |
| Schema-invalid output | Pydantic validation fails | Resubmit with the validation error ([Chapter 6](../06-prompt-engineering/README.md)) |
| Information absent from the source | Your own checks | Return `null` and route to human review; a retry cannot help |

```python
from pydantic import BaseModel, ValidationError

class Invoice(BaseModel):
    vendor: str
    invoice_number: str | None
    total: float | None

def triage(batch_id: str) -> dict[str, list]:
    b = {"ok": [], "retry_as_is": [], "fix_then_retry": [],
         "fallback_model": [], "continue_turn": [], "human": []}
    for item in client.messages.batches.results(batch_id):
        cid, r = item.custom_id, item.result
        if r.type == "succeeded":
            msg, stop = r.message, r.message.stop_reason
            if stop == "refusal":
                b["fallback_model"].append((cid, stop))
            elif stop in ("max_tokens", "model_context_window_exceeded"):
                b["fix_then_retry"].append((cid, stop))
            elif stop == "pause_turn":        # server-tool loop paused
                b["continue_turn"].append((cid, stop))
            elif stop != "end_turn":          # tool_use (client tool), ...
                b["human"].append((cid, stop))
            else:
                text = "".join(x.text for x in msg.content if x.type == "text")
                try:
                    b["ok"].append((cid, Invoice.model_validate_json(text)))
                except ValidationError as e:
                    b["fix_then_retry"].append((cid, str(e)))
        else:                                 # errored, canceled, expired
            fix = (r.type == "errored"
                   and r.error.error.type == "invalid_request_error")
            b["fix_then_retry" if fix else "retry_as_is"].append((cid, r.type))
    return b
```

**Resubmit with modifications.** The exam case: 100 documents, 95 succeed, 5 fail because they exceed the context window. Find the 5 by `custom_id`, split each into chunks (`inv-000417-c0`, `-c1`), and submit a **new batch with only those requests**. The 95 are never reprocessed. Cap attempts at 2–3; each batch retry can add another 24 hours (7.8).

### 7.7 Pre-flight: refine on a sample before the big run

Each request's `params` are validated asynchronously, so a malformed request shows up as `errored` only when the whole batch ends. A bad prompt is worse: it "succeeds" and you pay for 50,000 bad extractions. Before a large run:

1. **Dry-run the request shape** with one synchronous `client.messages.create(**params)` call.
2. **Refine the prompt on a representative sample** (20–100 documents covering every type) until first-pass success is high.
3. **Count tokens** with `client.messages.count_tokens(...)` and chunk oversized documents **before** you submit.
4. **Estimate cost** from the sample's `usage` (7.9).

An 85% first-pass rate on 50,000 documents leaves 7,500 resubmissions that need another batch cycle (up to 24 h more); raising it to 98% on a 50-document sample costs cents.

> **Exam trap:** To "maximize first-pass success and reduce resubmission cost", the answer is **prompt refinement on a sample set first**. Not "submit everything and fix failures", and not "use a bigger model".

### 7.8 SLA planning and submission cadence

Processing has an upper bound (24 h) but no lower-bound guarantee, so plan for the worst case:

```text
worst-case latency = W (window: longest wait before submission)
                   + P (batch processing, plan for 24 h)
                   + B (buffer: polling, validation, retries)
```

Choose a window `W ≤ SLA − P − B`. **The exam example: 30-hour SLA.** 30 − 24 leaves 6 hours of slack. Submitting every 6 hours leaves **zero** buffer. Submitting every **4 hours** keeps a 2-hour buffer: 4 + 24 + 2 = 30.

| Rule | Reason |
|---|---|
| For a fixed deadline, submit no later than `deadline − 24 h − B` | Same arithmetic, with `W = 0` |
| Retries inside the SLA go **synchronous** | A second batch cycle can add another 24 h |
| Batch-priced retries need an SLA of `W + 24 + 24 + B` | Otherwise retries break the SLA |
| Plan for `expired` items | Under heavy demand some requests do not run within 24 h |

> **Exam trap:** "Most batches finish within an hour, so 1-hour windows with a 2-hour SLA are fine" fails whenever a batch is slow. Compute guarantees from the 24-hour bound.

### 7.9 Cost modeling: batch discount, prompt caching and model choice

Batch prices are half of standard prices (per million tokens, Claude API, October 2026):

| Model | Standard in / out | **Batch in / out** | Cache read, batch | Min. cacheable prefix |
|---|---|---|---|---|
| Claude Sonnet 5.5 | $2 / $10 | **$1 / $5** | $0.05 | 512 tokens |
| Claude Haiku 5.5 (prompts up to 100K tokens; higher above) | $0.10 / $0.50 | **$0.05 / $0.25** | $0.005 | 512 tokens |
| Claude Haiku 4.5 (legacy) | $1 / $5 | **$0.50 / $2.50** | $0.05 | 4,096 tokens |
| Claude Opus 5.5 | $4 / $20 | **$2 / $10** | $0.10 | 512 tokens |
| Claude Fable 5.1 | $10 / $50 | **$5 / $25** | $0.125 | 512 tokens |

**Prompt caching stacks with the batch discount** (they are complementary, not alternatives). Cache multipliers (write 1.25× for 5 minutes or 2× for 1 hour; read 0.1× base input on most models, 0.05× on Sonnet 5.5 and Opus 5.5, 0.025× on Fable 5.1) apply on top of the batch price. Batch cache hits are **best-effort** (typically 30% to 98%). To raise them:

1. Put an **identical** shared prefix (system prompt, schema, few-shot examples) first in every request, with the same explicit `cache_control` breakpoint on the last shared block, for example `{"type": "ephemeral", "ttl": "1h"}`. Automatic caching would put the breakpoint on the varying document, so nothing is shared.
2. Prefer the **1-hour TTL**, and submit the requests that share a prefix together, so they run while the entry is still warm.
3. Check the minimum: a prefix shorter than the model's minimum is silently not cached.

**Worked example (illustrative).** 10,000 documents, each a 3,000-token shared prefix plus a 2,000-token document, with 500 output tokens.

| Option | Input | Output | Total |
|---|---|---|---|
| Sonnet 5.5, synchronous, no caching | 50M × $2 = $100 | 5M × $10 = $50 | **$150** |
| Sonnet 5.5, batch | 50M × $1 = $50 | 5M × $5 = $25 | **$75** |
| Sonnet 5.5, batch + 5-min caching at 70% hits | prefix: 21M read × $0.05 + 9M write × $1.25 = $12.30; documents: 20M × $1 = $20 | $25 | **≈ $57** |
| Haiku 5.5, batch (if the sample shows quality holds) | 50M × $0.05 = $2.50 | 5M × $0.25 = $1.25 | **$3.75** |
| Haiku 4.5 (legacy), batch + "caching" | 50M × $0.50 = $25 (prefix below its 4,096 minimum, so nothing is cached) | $12.50 | **$37.50** |

**Track actual spend.** Sum `message.usage` from every succeeded result, multiply by batch prices, and report cost per document.

> **Exam scope.** CCAR-F lists "rate limiting, quotas, or API pricing calculations" as **out of scope** (`CCAR-F/APPX/OUT/11`). It tests the 50% discount, the 24-hour window and the batch-vs-sync decision. The cost tables here and the rate-limit table in 7.11 are for the job and for CCDV-F.

### 7.10 Extended output (beta) on batches

The beta header `output-300k-2026-03-24` raises `max_tokens` to **300,000** on batch requests for Claude Opus 5.5, Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5.5, Sonnet 5, Sonnet 4.6 and Haiku 5.5. The synchronous limit stays at 128K. Send it with `client.beta.messages.batches.create(betas=["output-300k-2026-03-24"], ...)`. It works only on the Claude API and Claude Platform on AWS. One such generation can take over an hour, so leave room in the 24-hour window.

### 7.11 Operations: rate limits, retention, privacy and platforms

**Rate limits.** The Batches API has its own limits, shared across models, and does **not** consume your Messages API limits.

| Usage tier | Batch API RPM | Batch requests in processing queue | Requests per batch |
|---|---|---|---|
| Start | 1,000 | 200,000 | 100,000 |
| Build | 2,000 | 300,000 | 100,000 |
| Scale | 4,000 | 500,000 | 100,000 |

**Retention and privacy.** Batches and results are isolated to the **Workspace** that created them, and stored for up to **29 days after creation**. Delete earlier with `batches.delete()`.

- Batches are **not eligible for Zero Data Retention (ZDR)**, and the API does not block them under ZDR: using batches steps outside ZDR for that data.
- Batches are **not HIPAA-eligible**. Under HIPAA readiness the API returns a `400`, so PHI workloads stay synchronous.

**Cloud platforms.** `/v1/messages/batches` works on the Claude API, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed). It is **not supported** on Amazon Bedrock, Claude Models on Google Cloud (Google managed, formerly Vertex AI) or Microsoft Foundry. Use the cloud's own service instead: Bedrock **batch inference** (JSONL in S3; check your model is listed) or Google Cloud's **batch predictions** for Claude (Cloud Storage or BigQuery input). Foundry has **no batch option documented**, so use synchronous calls behind your own queue. Each service has its own format, limits and pricing, so put the batch client behind an interface.

### 7.12 Reliability around a batch pipeline (Domain 5)

The Batches API runs requests. Reliability comes from the code around it:

| Concern | Practice | Task |
|---|---|---|
| Crash recovery | Persist `batch_id` and `custom_id`s at submit (a manifest); resume polling on restart ([Chapter 11](../11-context-management/README.md)) | 5.4 |
| No silent loss, no full stop | Every `custom_id` ends in exactly one terminal state (accepted, human review, abandoned with reason). One errored request never blocks the rest | 5.3 |
| Structured failure records | Store failure type, what was attempted, partial results and next action, not just "failed" | 5.3 |
| "Not found" is not "failed" | A correct `null` for an absent field is a valid result, not a retry | 4.4 / 5.3 |
| Coverage reporting | 100 submitted → 95 accepted, 3 after resubmission, 2 in human review | 5.3 |
| Human review | Route low-confidence fields and refusals to reviewers; sample by document type ([Chapter 9](../09-escalation-human-in-the-loop/README.md)) | 5.5 |
| Idempotent sinks | Upsert results keyed by `custom_id` | ROLE/ARCH/5 |

> **Exam trap:** "97% of the batch succeeded" can hide a document type that fails 40% of the time. Report **by document type and field** before you reduce human review.

## Lesson code

Video-lesson code: [../../presentations/07-batches-and-cost/code/](../../presentations/07-batches-and-cost/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Work through 7.1–7.12 offline on a simulated Batches API (`FakeBatchAPI`), then build the mini-project: a 100-document extraction pipeline that resubmits only the failures |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 auto-checked coding exercises, a 50,000-contract architecture scenario and a scorecard |

## Cheat-sheet

| Situation | Choose | Why |
|---|---|---|
| A developer or pipeline stage is blocked on the answer | Synchronous Messages API | No latency SLA on batches |
| Scheduled, latency-tolerant bulk work | Message Batches API | 50% off every token, separate rate limits |
| Workflow needs your client tools mid-reasoning | Synchronous loop, or pre-fetch context then batch | A batch cannot run your tool and continue |
| 5 of 100 documents failed (too long) | Chunk those 5 and resubmit only them | No duplicate cost or records |
| Large run with an untested prompt | Refine on a 20–100 document sample first | Bad prompts "succeed" |
| 30 h SLA, 24 h processing | 4 h submission windows (2 h buffer) | Room for validation and sync retries |
| Retry must land inside a tight SLA | Synchronous retry | Another batch can add 24 h |
| Shared long prefix across the batch | Batch + prompt caching (identical prefix, 1-hour TTL) | Discounts stack |
| Customer requires ZDR or HIPAA | Synchronous API | Batches are neither ZDR- nor HIPAA-eligible |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Batching a blocking check** because it is cheaper, or adding a sync fallback to make it acceptable.
- **Matching results by position** instead of `custom_id`.
- **Treating `succeeded` as done** without checking `stop_reason` and validating the output.
- **Resubmitting the entire batch**, or resubmitting failures unchanged when the request itself caused them.
- **Not persisting the batch ID**, then double-submitting after a crash.
- **Planning the SLA from the typical one-hour completion** instead of the 24-hour bound.

## Self-check

**1.** A team runs two Claude workflows synchronously: a pre-merge check that blocks merging, and a tech-debt report generated overnight for the morning stand-up. A manager wants to move both to the Message Batches API for the 50% saving. What do you recommend?

- A) Move both to batches and poll for completion
- B) Move both to batches, with a fallback to synchronous calls if a batch takes too long
- C) Batch the overnight report only; keep the pre-merge check synchronous
- D) Keep both synchronous to avoid batch result-ordering problems

<details><summary>Answer</summary>

**C.** Batches have no latency SLA (up to 24 hours), which is fine for an overnight report and unacceptable for a blocking check. A blocks developers. B still makes developers wait for the timeout before the fallback runs, and pays for both paths. D cites a non-problem: `custom_id` handles ordering.
</details>

**2.** A nightly job scores 30,000 sales leads. For each lead, Claude may call `get_orders`, a function your service runs against the CRM, and then writes the score from the order history it gets back. Moving the job to the Message Batches API would halve the cost. What happens if you move it unchanged?

- A) It works as before: the batch runs `get_orders` for Claude and returns the finished score
- B) It is rejected: a batch holds at most 10,000 requests
- C) Requests that call `get_orders` stop with `stop_reason: "tool_use"`; only a new request carrying the order data can produce their score
- D) The scores cannot be matched to the leads, because results come back unordered

<details><summary>Answer</summary>

**C.** A batch request returns one response and has no channel back to your service, so it cannot run your function and continue. A confuses client tools with server tools (only Anthropic-run tools loop inside a batch). B is wrong: the limit is 100,000 requests or 256 MB. D is solved by `custom_id`. Fix: fetch each lead's order history first, put it in the prompt, then batch a single-turn scoring request.
</details>

**3.** You batch 100 invoices. 95 succeed. 5 come back `errored` with `invalid_request_error: prompt is too long`. What is the most efficient next step?

- A) Resubmit all 100 with a larger `max_tokens`
- B) Identify the 5 by `custom_id`, split each into chunks, and submit a new batch with only those chunk requests
- C) Resubmit the 5 unchanged, because errored requests are often transient
- D) Switch the whole pipeline to synchronous calls

<details><summary>Answer</summary>

**B.** Resubmit only the failures, with the modification that fixes the cause. A reprocesses 95 successes and changes the wrong parameter (`max_tokens` is the output cap; the problem is input size). C repeats a deterministic failure (`invalid_request_error` must be fixed before resending). D gives up the discount for no reason.
</details>

**4.** Documents arrive continuously and must be processed within 30 hours of arrival. You plan around the 24-hour batch processing bound and want time to validate results and synchronously retry failures. Which submission cadence fits?

- A) One batch every 24 hours
- B) One batch every 6 hours
- C) One batch every 4 hours
- D) One batch every 12 hours, since most batches finish within an hour

<details><summary>Answer</summary>

**C.** Worst case = window + 24 h + buffer. With 4-hour windows: 4 + 24 = 28 h, leaving 2 h for validation and synchronous retries. B uses all 6 hours of slack and leaves no buffer. A and D break the SLA in the worst case; "most batches are fast" is not a guarantee.
</details>

## Official documentation

- [Batch processing (Message Batches API guide)](https://platform.claude.com/docs/en/build-with-claude/batch-processing): limits, supported features, result types, caching, extended output, retention
- [Pricing: batch processing](https://platform.claude.com/docs/en/about-claude/pricing#batch-processing)
- [Rate limits: Message Batches API](https://platform.claude.com/docs/en/api/rate-limits#message-batches-api)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) (see the 1-hour cache duration and the batches FAQ)
- [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) (ZDR and HIPAA eligibility per feature)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) (`client.messages.batches`)

---

[← Chapter 6 — Prompt Engineering: Advanced Techniques](../06-prompt-engineering/README.md) | [↑ Claude path overview](../README.md) | [Chapter 8 — Task Decomposition Strategies →](../08-task-decomposition/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
