# Chapter 10 — Error Handling in Multi-agent Systems

> **Exam domain(s):** Domain 5 — Context Management & Reliability (**15%**, task 5.3 error propagation) · Domain 2 — Tool Design & MCP Integration (**18%**, task 2.2 structured error responses) · also supports Domain 1 — Agentic Architecture & Orchestration (**27%**, task 1.2: the coordinator owns error handling)

A multi-agent system fails quietly. One subagent times out, another returns an empty list, and the coordinator still writes a confident report on top of the gaps. As an architect you design the **error contract** between layers: what a tool tells the agent, what a subagent tells the coordinator, and what the final report tells the reader.

## What you'll learn

- Place a failure in the right layer, and tell integration problems from model-output problems.
- Classify errors as **transient**, **validation**, **business** or **permission**, with a matching `retryable` flag.
- Tell an **access failure** from a **valid empty result**.
- Return structured tool errors and a structured **subagent result envelope** the coordinator can act on.
- Recover locally with bounded retries, isolate subagents, and set timeouts and budgets.
- Write a final report with **coverage annotations** that show where the gaps are.

## Prerequisites

- [Chapter 2 — Tool Use](../02-tool-use/README.md) (`tool_result` with `is_error`), [Chapter 3 — Agent SDK](../03-agent-sdk/README.md) (subagents, `max_turns`, hooks), [Chapter 4 — Model Context Protocol](../04-model-context-protocol/README.md) (MCP `isError`).
- [Chapter 8 — Task Decomposition](../08-task-decomposition/README.md) defines what "coverage" means; [Chapter 9 — Escalation and Human-in-the-Loop](../09-escalation-human-in-the-loop/README.md) is where unresolvable errors go.

## Concepts

### 10.1 Where failures happen in a multi-agent system *(expanded beyond the guide)*

Before you handle an error, find **which layer owns it**. Each layer recovers what it can and passes a clear signal upward. The coordinator owns the final error handling and routing.

| Layer | Typical failures | Handles it first | Passes upward |
|---|---|---|---|
| 1. Claude API | `429`, `529`, `5xx`, timeouts, `400` | SDK retries, then your code | A classified exception (10.2) |
| 2. Tool | Backend timeout, bad arguments, policy block, zero matches | The tool itself | A structured `isError` / `is_error` result (10.4) |
| 3. Subagent | Source still down after retries, turn or budget cap | The subagent (10.5) | A result envelope (10.6) |
| 4. Coordinator | Several subagents partly failed | Its recovery policy | Retry modified, delegate, accept partial, escalate |
| 5. Synthesis | Mixed-quality inputs | The synthesis step | A report with coverage annotations (10.9) |

**Isolate the origin before you fix anything** (the Developer exam calls this "problem origin isolation between the integration layer and model output"):

| Symptom | Origin | Fix belongs in |
|---|---|---|
| HTTP error, exception, `stop_reason` `max_tokens` or `refusal` | Integration layer | Code, configuration, request parameters |
| Well-formed answer that is wrong or invented, tools succeeded | Model output | Prompts, decomposition, validation, review |
| Well-formed answer built on a timeout or 403 shown as "empty" | Error contract | This chapter (10.3 to 10.7) |

> **Exam trap:** If every subagent **succeeded** and the report still misses whole topics, the cause is the coordinator's **task decomposition**, not error handling. Error handling can only report gaps in work that was assigned. See [Chapter 8](../08-task-decomposition/README.md).

### 10.2 Error categories and the retryable flag

| Category | Examples | `retryable` | Right response |
|---|---|---|---|
| **Transient** | Timeout, `503`/`529`, connection reset, rate limit | `true` | Bounded retries with backoff and jitter |
| **Validation** | Wrong date format, missing field, syntax error | `false` *as sent* | Fix the input, then call again |
| **Business** | Refund above policy limit, order already shipped | `false` | Explain in plain language, offer an alternative |
| **Permission** | `403`, expired token, missing scope | `false` | Escalate or request access |

The flag answers one question: will the *same* request have a reasonable chance of succeeding later? Its job is to stop wasted retries. A **valid empty result** is not an error at all (10.3). MCP itself defines only the `isError` boolean on a tool result. Category and retry fields are **your** convention inside the content (the exam guide spells the flag both `isRetryable` and `retriable`: pick one).

The same taxonomy applies to Claude API calls. The Python SDK already retries connection errors, timeouts, `408`, `409`, `429` and `5xx` **twice by default** (`max_retries=2`) with exponential backoff, and honors `retry-after`. The default timeout is **10 minutes** per request. Network failures raise `APIConnectionError` (including `APITimeoutError`). HTTP errors raise `APIStatusError` subclasses (`RateLimitError`, `OverloadedError`, `PermissionDeniedError` and so on), each with `status_code`, `type` and `request_id`.

| HTTP status / `error.type` | Category | Retry? |
|---|---|---|
| `400 invalid_request_error`, `404`, `413` | Validation | No: fix the request |
| `401 authentication_error`, `403 permission_error` | Permission | No |
| `402 billing_error` | Business | No: alert a human |
| `409 conflict_error` | Transient-ish | After re-reading state |
| `429 rate_limit_error` | Transient | Yes, honor `retry-after` |
| `500 api_error`, `504 timeout_error`, `529 overloaded_error` | Transient | Yes, with backoff |

Two special cases. A usage tier's monthly spend-cap `429` has **no** `retry-after` and carries `error.details.error_code: "enforced_spend_limit_reached"`: treat it as business and stop. Check the code, not the missing header: ordinary 429s can also arrive without `retry-after`, and they stay transient. A spend limit you set yourself returns `400 invalid_request_error` with a message starting "You have reached your specified API usage limits" (or "specified workspace API usage limits"): that is business too, not a request to fix. An `error` event mid-stream arrives as an `APIStatusError` whose `status_code` is `200`: classify it by `err.type`.

> **Exam trap:** `529 overloaded_error` means the API is busy for everyone; `429 rate_limit_error` means your organization hit a limit. Both are transient, and both are fixed by backing off, not by retrying faster.

### 10.3 Access failure vs valid empty result

| | Access failure | Valid empty result |
|---|---|---|
| What happened | Source unreachable or refused (timeout, 503, 403) | Source answered: nothing matches |
| Is it information? | No. You know **nothing** | Yes. "No patents match" is a **finding** |
| Correct report | A failure with category, attempts, `retryable` | A success with an empty list |
| If you confuse them | "No patents exist" while the database was down | Pointless retries and false alarms |

This is the most tested distinction in the chapter. Example: a court-records search returns 6 rulings, a regulator's register returns no entries, and a news API times out. That is three different outcomes: success, valid empty, access failure.

**Suspicious empties** look like success: `200 OK` with an empty list while a shard is down, or a stale index. Resolve them in the tool or subagent with a canary query, health metadata or a broader query. If you still cannot vouch for the emptiness, say so. Give each outcome its own status (`SearchOutcome.status` is `ok`, `empty` or `failed`), never an overloaded empty list:

```python
async def search_source(source, query, backend, canary_query=None):
    """Query one source and say precisely what happened."""
    out = dict(source=source, query=query)
    try:
        hits = await backend(source, query)
    except TimeoutError:
        return SearchOutcome(**out, status="failed", error="timeout after 10s")
    if hits:
        return SearchOutcome(**out, status="ok", hits=hits)
    # Empty: resolve it HERE. Is the source answering, or degraded?
    if canary_query is not None:
        try:
            canary = await backend(source, canary_query)  # always matches
        except TimeoutError:
            canary = []
        if not canary:
            return SearchOutcome(**out, status="failed",
                                 error="empty, and the canary query too")
    return SearchOutcome(**out, status="empty")
```

> **Exam trap:** "Catch the timeout and return an empty result marked as success" is **silent suppression**, the most dangerous wrong answer. The opposite mistake, reporting "0 results" as a failure, causes pointless retries.

### 10.4 Structured error responses from tools

The tool is the first place a failure is understood. It must describe the failure so the agent can act on it. MCP uses `isError: true` on the tool result; the Messages API uses `is_error: true` on the `tool_result` block. Tool execution errors (API failures, bad input, business rules) belong in that result so the model can self-correct; only unknown tools, malformed requests and server errors are JSON-RPC protocol errors. Put the details in `content`: an `errorCategory`, an `isRetryable` flag, a `message` with the cause and next step, and for business errors a `customerMessage` that is safe to show an end user.

```python
import json
def tool_error_result(tool_use_id, category, retryable, message, **extra):
    """A tool_result block the model can reason about."""
    payload = {"errorCategory": category, "isRetryable": retryable,
               "message": message, **extra}
    return {"type": "tool_result", "tool_use_id": tool_use_id,
            "is_error": True, "content": json.dumps(payload)}

# Business-rule violation: not retryable, with customer-safe wording.
tool_error_result(
    "toolu_01", "business", False,
    "Refund of $820 exceeds the $500 self-service limit.",
    customerMessage="I can't approve a refund this large myself, "
                    "but I can pass it to a supervisor today.",
    alternatives=["escalate_to_human", "offer store credit up to $500"],
)
```

A uniform `"Operation failed"` forces the agent to guess: it retries a validation error, gives up on a timeout, or tells the user something false. "No match" is a successful result with an empty payload. For the MCP server side, see [Chapter 4, section 4.4](../04-model-context-protocol/README.md#44-the-iserror-flag-and-structured-errors).

> **Exam trap:** For business-rule violations the answer has **two** parts: `retryable: false` **and** a customer-friendly explanation.

### 10.5 Local recovery before propagation

**Handle each error at the lowest level that can resolve it.** Retry transient errors locally. Fix the input once for validation errors. Propagate business and permission errors immediately. Propagate whatever is left, with what you tried and your partial results.

```python
import asyncio, random

# ToolFailure: an exception that carries .category and .retryable
async def with_local_retry(op, *, max_attempts=3,
                           base_delay=0.5, max_delay=8.0):
    """Retry ONLY retryable failures, with capped backoff and jitter.
    Returns (result, attempts). Re-raises everything else."""
    for attempt in range(1, max_attempts + 1):
        try:
            return await op(), attempt
        except ToolFailure as err:
            if not err.retryable or attempt == max_attempts:
                err.attempts = attempt   # evidence for the envelope
                raise
            delay = min(base_delay * 2 ** (attempt - 1), max_delay)
            # jitter avoids synchronized retry storms
            await asyncio.sleep(delay * random.uniform(0.5, 1.0))
```

1. **Bound it.** One or two retries for a transient error is normal. **Never retry non-retryable errors:** a corrupted PDF stays corrupted.
2. **Change something before a validation retry.** Re-sending the same request is not recovery.
3. **Retry at one layer.** SDK × subagent × coordinator retries can produce 3 × 3 × 3 = 27 calls per task. That is **retry amplification**. Higher layers should change approach, not repeat.
4. **Make writes idempotent** (idempotency keys or a state check) before you retry them.
5. **Record what you tried**, so the propagated error is useful (10.6).

> **Exam trap:** When a subagent hands every failure to the coordinator, the fix is to sort failures by whether a retry can help: the subagent absorbs the ones a short retry fixes, and passes the rest up at once with what failed, what it tried and what it kept. Inside one tool the rule is the same: let the tool absorb retryable noise, and fail fast on input it can't accept, naming the bad field.

### 10.6 The structured subagent result

When a subagent cannot resolve a failure, its report decides whether the coordinator can recover. A generic status ("search unavailable") throws away what the subagent learned. The envelope needs: status, failure type, attempted queries, partial results, alternatives and coverage impact. The field names are a convention; the exam tests the content. `status` is one of `success`, `empty`, `partial` or `failed`.

```json
{
  "subagent": "web_search", "topic": "film", "status": "partial",
  "failure_type": "timeout", "error_category": "transient",
  "retryable": true, "attempts": 3,
  "attempted": ["generative AI in film visual effects 2025"],
  "findings": [{"claim": "Two studios report AI-assisted rotoscoping",
                "source_url": "https://example.org/vfx", "relevance": 0.7}],
  "alternatives": ["Narrower query: 'AI rotoscoping VFX studios'"],
  "coverage_impact": "Film: effects on VFX jobs not covered"
}
```

The notebook defines it as a Pydantic model, `SubagentResult`, that rejects contradictions (a `failed` result with no `failure_type`). The coordinator's recovery policy becomes an explicit decision:

- `success` or `empty`: accept. "No results" is a valid finding.
- Permission failure: escalate. A retry cannot grant access.
- Retryable or validation failure, retries left, an alternative exists: retry with the **modified** query. Never retry business failures.
- Partial: accept what survived and annotate the rest.
- A backup source exists: delegate. Otherwise continue and annotate the gap.

In the Agent SDK a subagent returns **only its final message** to the coordinator (see [Chapter 3](../03-agent-sdk/README.md#34-the-subagent-tool-agent-formerly-task)). Put the envelope format in the subagent's prompt and validate it before you trust it.

> **Exam trap:** For "a web-search subagent times out; how should it report?", the answer is **failure type, the query attempted, partial results and alternatives**. The distractors: a generic status, an empty success, and an exception that ends the workflow.

### 10.7 Error-handling anti-patterns

| Anti-pattern | Do this instead |
|---|---|
| **Generic status** ("Operation failed") | Category, retry flag, attempts, partial results, alternatives |
| **Silent suppression** (failure as empty success) | Separate "no results" from "could not search" (10.3) |
| **Abort the whole workflow** on one failure | Continue with partial results, annotate the gap |
| **Unbounded retries, or retrying non-retryable errors** | 1–2 bounded retries for transient errors only |
| **Stacked retries at every layer** | One layer retries; higher layers change approach |
| **Success status with errors in metadata** | Make failure part of the status |
| **A dedicated "error-handling agent"** | Local recovery in the subagent, structured propagation |
| **Coordinator pre-validates everything** | Let the specialist handle and report its own failures |
| **Hiding gaps in the synthesis** | Coverage annotations (10.9) |

> **Exam trap:** Silent suppression and aborting the workflow are **both** wrong. One hides the failure, the other overreacts. Keep going, keep what you have, make the gap visible.

### 10.8 Timeouts, budgets and graceful degradation *(expanded beyond the guide)*

Set limits at every level, or local recovery can eat the whole budget:

- **Per API call:** `AsyncAnthropic(timeout=..., max_retries=...)`.
- **Per subagent:** `asyncio.timeout(seconds)`; in the Agent SDK, `AgentDefinition(maxTurns=...)`.
- **Per run:** a deadline and a shared retry budget; in the Agent SDK, `ClaudeAgentOptions(max_turns=..., max_budget_usd=...)`. Subagent spend counts toward the budget.

**Isolate subagents.** `asyncio.TaskGroup` cancels all siblings when one task raises, and default `asyncio.gather` loses the other results. Wrap each subagent so it **always returns an envelope**, then `asyncio.gather` the wrapped coroutines:

```python
async def run_isolated(name, topic, work, deadline_s) -> SubagentResult:
    """Run one subagent so its failure can never take down its siblings."""
    fail = dict(subagent=name, topic=topic, status="failed",
                coverage_impact=f"{topic}: not covered")
    try:
        async with asyncio.timeout(deadline_s):   # retries included
            return await work()
    except TimeoutError:
        return SubagentResult(**fail, failure_type="timeout",
                              error_category="transient", retryable=True,
                              message=f"no answer within {deadline_s}s")
    except Exception as exc:          # a bug: isolate it anyway
        return SubagentResult(**fail, failure_type="internal_error",
                              error_category=None, retryable=False,
                              message=f"{type(exc).__name__}: {exc}")
```

**Agent SDK results.** When a cap is hit, `ResultMessage.subtype` is `error_max_turns` or `error_max_budget_usd`, with `is_error=True`. A run ended by an API failure says `subtype="success"` but `is_error=True` and `terminal_reason="api_error"`, so check `is_error` first. A single-shot `query()` raises `ResultError` after yielding the error result; catch it and turn it into a failed envelope. On error subtypes `result` is absent, so recover partial work from what you persisted (10.10). This applies when each subagent is its own `query()`. A subagent defined with `AgentDefinition(maxTurns=...)` and run through the Agent tool yields no `ResultMessage`: a `maxTurns` hit comes back to the parent as Agent tool output marked partial.

**Task budgets (beta, Messages API only; Claude Code and the Agent SDK don't support them)** give the model an advisory token budget for a whole loop (`output_config={"task_budget": {"type": "tokens", "total": 64000}}`, beta header `task-budgets-2026-03-13`), so it wraps up instead of being cut off. `max_tokens` stays the hard limit. **Circuit breaker.** After N consecutive failures, stop calling a source for a cool-down and fail fast with `failure_type="unavailable"`. The coordinator uses the other sources and annotates the gap.

> **Exam trap:** `max_turns`, `max_budget_usd` and task budgets are **guardrails**, not completion signals. Hitting one is a failure to report.

### 10.9 Coverage annotations in the final synthesis

Graceful degradation only works if the reader can see it. **Coverage annotations** mark each section as well-supported or partial, and say why a gap exists. **Compute them in code from the envelopes**, not from the model's impression:

```python
def coverage_label(results: list[SubagentResult]) -> str:
    statuses = {r.status for r in results}
    if statuses <= {"success", "empty"}:
        return "FULL"          # every source answered (0 results counts)
    if statuses & {"success", "empty", "partial"}:
        return "PARTIAL"
    return "NONE"
```

Compare against the **plan**: a planned subagent that never ran also turns FULL into PARTIAL. Then give the synthesis step a coverage table like this one, with rules: one section per topic, headings such as "Games (PARTIAL COVERAGE: web_search: timeout)", findings only from the results with sources, and never "no evidence exists" for a source that failed. Claim-level provenance is the subject of [Chapter 12](../12-provenance/README.md).

| Topic | Coverage | Answered | Gaps |
|---|---|---|---|
| Film | FULL | web_search (7), documents (3) | - |
| Games | PARTIAL | documents (2) | web_search: timeout |
| Architecture | FULL | web_search (0 results), documents (4) | - |

> **Exam trap:** When some sources timed out, the best synthesis strategy is **coverage annotations**. Not "hide the gaps", not "fail the task", and not "block until retries finish".

### 10.10 Observing and debugging failures *(expanded beyond the guide)*

You cannot improve an error contract you cannot see. Log at least:

- Every subagent envelope (status, failure type, attempts).
- `request_id` of failed API calls (`APIStatusError.request_id`).
- `ResultMessage.subtype`, `is_error`, `terminal_reason`, `api_error_status` and `total_cost_usd` from the Agent SDK.
- Tool failures, through the Agent SDK `PostToolUseFailure` hook (`tool_name`, `error`, `agent_type`). It fires for tools that started and then failed, not for calls rejected before running. It can also return `additionalContext` with a recovery hint ("if this was a timeout, retry once with a narrower query; otherwise report it in your final JSON"), so the model gets the rule when it needs it.
- The coverage table of each run.

**Resume instead of restart.** Persist each envelope as it arrives (a manifest of completed topics), so a crashed coordinator re-runs only the missing topics. See [Chapter 11](../11-context-management/README.md).

**Read failures as data.** Cluster envelopes by `failure_type` and source. More `timeout` on one source is an operations problem. More `invalid_input` points to a prompt or tool-description fix.

## Lesson code

Video-lesson code: [../../presentations/10-multi-agent-error-handling/code/](../../presentations/10-multi-agent-error-handling/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Work through 10.1–10.10 offline (scripted client, simulated sources), then build the mini-project: a research coordinator that degrades gracefully and writes a report with coverage annotations |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 auto-checked coding exercises, an architecture scenario and a scorecard |

Run them from the repo root venv (see [../../00-prerequisites/README.md](../../00-prerequisites/README.md)).

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| A subagent's search times out | Failure type, attempted query, partial results, alternatives | Generic status; empty success; aborting |
| A source returns zero matches | Success with an empty list | `isError`, or a retry |
| Transient failure inside a subagent | 1–2 local retries with backoff, then propagate | Escalating every hiccup; unlimited retries |
| One tool sees retryable failures and bad input | The tool absorbs retryable noise; fails fast on bad input, naming the field | The same backoff for every failure |
| Business-rule violation | `retryable: false` + customer-friendly text | Retrying; raw internal errors |
| Permission or expired credentials | Non-retryable error; escalate | Retry, or report as empty |
| Retries at SDK, subagent and coordinator | One layer retries; others change approach | Stacked retries |
| Parallel independent subagents | Each wrapped to return an envelope, own deadline | Raw `TaskGroup` / default `gather` |
| Some sources failed, synthesis must run | Coverage annotations computed in code | Hiding gaps; failing the task |
| Long run with a cost ceiling | Agent SDK: `max_budget_usd` / `max_turns`; Messages API loop: task budget + `max_tokens` | No limits |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- Returning "Operation failed" instead of a category, retry flag and message.
- Converting timeouts into empty results "so the pipeline doesn't break".
- Flagging "no results" as an error.
- Letting one failure abort everything (an uncaught exception in a `TaskGroup`).
- Retrying without reading the category, or retrying at every layer.
- Checking only `subtype == "success"` on an Agent SDK result.

## Self-check

**Q1. (Multi-agent research system)** While researching a broad topic, the patent-search subagent times out after its local retries. How should it report this to the coordinator?

- A) Return `{"status": "error", "message": "patent search unavailable"}`
- B) Return an empty list of patents with a success status so the report can still be produced
- C) Return the failure type (timeout), the queries it tried, any results retrieved before the timeout and suggested alternatives (a narrower query, another patent source)
- D) Raise the timeout to the top-level handler so the run stops and can be restarted cleanly

<details><summary>Answer</summary>

**C.** Structured context lets the coordinator choose between retrying with a modified query, delegating, accepting partial results or annotating the gap. A is a generic status that hides the context. B is silent suppression: the report would claim there are no relevant patents. D throws away every other subagent's completed work because of one source.
</details>

**Q2. (Multi-agent research system)** A regulatory-filings subagent searches an index that is rebuilt every night. During the rebuild the index answers `200 OK` with an empty hit list for every query. Overnight runs report "no filings mention the merger"; daytime runs of the same question find 4 filings. What is the best fix?

- A) Treat every empty result as a failure and retry it three times
- B) Before reporting an empty result, have the subagent check the source: run a canary query that always matches (or read the index's health or freshness data), report `empty` only if the check passes, and otherwise report a retryable access failure
- C) Schedule every research run for daytime
- D) Tell the synthesis model to be skeptical of empty results

<details><summary>Answer</summary>

**B.** An empty list from a degraded source looks exactly like a real "0 results". Only a check at the source can tell them apart, and the subagent is the lowest level that can run it. A turns every genuine "nothing matches" into wasted retries and false alarms. C hides the problem for one schedule and one source. D asks the model to guess at a fact that code can check, and the model sees only the empty list.
</details>

**Q3. (Multi-agent research system)** A pricing subagent's `fetch_prices` tool calls a partner API that, at peak hours, answers about one call in five with HTTP `429` and `retry-after: 2`. Today the tool passes every 429 straight up as an error, the subagent reports `failed`, and the coordinator re-runs the whole subagent, which repeats all of its earlier calls. What is the most effective change?

- A) Inside the tool, wait the `retry-after` period and retry once or twice; if the 429s continue, return a structured, retryable error with the attempts made, so the subagent can report it
- B) Keep the design, but let the coordinator re-run the subagent up to five times
- C) Have the subagent return success with the prices it already has and leave the failed calls out
- D) Treat the 429 as a permission problem and send each one to a human

<details><summary>Answer</summary>

**A.** Handle an error at the lowest level that can resolve it. The tool knows the failure is transient and how long to wait, so a short, bounded retry there fixes most cases without repeating completed work. A persistent 429 still reaches the coordinator with context. B multiplies calls (retry amplification) and repeats work that already succeeded. C hides failed calls behind a success status. D misclassifies a transient error and wastes human time.
</details>

**Q4. (Multi-agent research system)** A report on AI in architecture firms has a section on design-software adoption. Its envelopes: the survey-database subagent searched and found 0 matching surveys (`status: "empty"`), and the vendor-filings subagent timed out after its retries (`status: "failed"`). The draft says: "No surveys or vendor filings report adoption of AI design software." How should the section be written?

- A) Keep the sentence: both sources were consulted, so it is accurate
- B) Drop the section, since neither source contributed findings
- C) Replace the sentence with "Data unavailable" for both sources
- D) Label the section PARTIAL and say two different things: the survey database has no matching surveys (a finding), and the vendor filings could not be searched (timeout), so nothing can be concluded from them

<details><summary>Answer</summary>

**D.** The two sources ended differently, so the report must say different things about them. "0 surveys" is information; a timeout is not. A turns a timeout into a false claim. B hides the gap and throws away a real finding. C turns a finding into a failure, so the reader loses the fact that no surveys exist.
</details>

## Official documentation

- [Claude API errors](https://platform.claude.com/docs/en/api/errors): HTTP status codes, error shapes, `request_id`, SDK retries
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls): `tool_result` with `is_error`
- [MCP specification: Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools): protocol errors vs tool execution errors (`isError`)
- [Agent SDK: Python reference](https://code.claude.com/docs/en/agent-sdk/python): `ResultMessage`, `ResultError`, `PostToolUseFailure`
- [How we built our multi-agent research system (Anthropic Engineering)](https://www.anthropic.com/engineering/multi-agent-research-system): errors compound, resuming, tracing
- Syllabus source: community study guide by paullarionov, [Chapter 10 and Domain 5.3](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-10-error-handling-in-multi-agent-systems), restructured and expanded here in my own words.

[← Chapter 9 — Escalation and Human-in-the-Loop](../09-escalation-human-in-the-loop/README.md) | [↑ Claude path overview](../README.md) | [Chapter 11 — Context Management in Production Systems →](../11-context-management/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
