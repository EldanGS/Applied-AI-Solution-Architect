# Chapter 10 — Error Handling in Multi-agent Systems

> **Claude counterpart:** [Chapter 10 — Error Handling in Multi-agent Systems](../../anthropic-claude/10-multi-agent-error-handling/README.md) · **Academy course(s):** Design and Build Agentic Systems (API pathway, ~110 min course) and Optimize AI Application Performance (API pathway) · **Est. time:** 5–7 hours (reading + 2 notebooks) · **Status:** [ ] not started

A multi-agent system fails in pieces: one worker times out, another hits a paywalled source, a third finds nothing, and the API throws a `429`. The architect question is: when one part fails, does the system still deliver an honest, useful answer? That works only if every failure reaches the coordinator as **structured data**. This chapter takes the vendor-neutral patterns from the Claude chapter and wires them to the OpenAI platform.

## What you'll learn

- Sort failures into transient, validation, business and permission, and tell a valid empty result from an access failure
- Read `openai` errors by `error.code`, not status alone, and know the client already retried twice
- Turn Agents SDK exceptions and tool errors into data (`run_data`, `error_handlers`, `failure_error_function`)
- Return a structured `WorkerResult` with partial results, recover locally first, and let the coordinator decide
- Compute coverage annotations in code, debug with traces, and read terminal statuses of long-running work

## Prerequisites

[00-prerequisites](../../00-prerequisites/README.md), [Chapter 02](../02-function-calling-and-structured-outputs/README.md) (errors as data, refusals, `incomplete`), [Chapter 03](../03-agents-sdk-and-agents-api/README.md) (`Runner`, agents-as-tools, guardrails, tracing) and [Chapter 09](../09-escalation-human-in-the-loop/README.md) (escalation). Optional: the [Claude counterpart](../../anthropic-claude/10-multi-agent-error-handling/README.md). Snippets assume `import openai`, `client = OpenAI()` and `MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")`, plus `json`, `Literal`, `BaseModel` and the `agents` imports from the first cell of `01_practice`; 10.3 uses top-level `await`, so run it in a notebook. Verified against `openai` 3.24 and `openai-agents` 0.23.1.

## Concepts

The chapter is one flow: classify the failure where it happens (10.1–10.4), recover locally if you can (10.6), propagate a structured result if you can't (10.5), and let the coordinator decide (10.7) and annotate coverage (10.8).

### 10.1 Error categories on the OpenAI platform

The categories match the Claude side. What changes is where the signal comes from.

| Category | Examples on OpenAI | Retryable? | Right response |
|---|---|---|---|
| **Transient** | `APITimeoutError`, `APIConnectionError`, `429 slow_down`, `500`, `503 server_is_overloaded`, `ToolTimeoutError`, `ModelTimeoutError` | Yes, bounded | Back off (honor `Retry-After`), retry a few times, then report |
| **Validation** | `400 BadRequestError` (`exc.param` names the field), `422`, `ModelBehaviorError` | Not as-is | Fix the input once, then retry; otherwise report |
| **Business** | Refund over the limit, `credit_balance_exhausted`, spend/usage-limit codes | No | Explain, offer an alternative, or route to the owner |
| **Permission** | `401`, `403`, a paywalled source | No | Escalate (Chapter 09) |
| **Valid empty** (not an error) | A search that ran and found 0 matches | n/a | Report success with an empty result, and say so |

**Policy blocks** (guardrail tripwires, `ModelRefusalError`, `misalignment_policy_violation`) follow one rule in this chapter: never retry or rephrase them. In a `WorkerResult` they are `failure_type="policy_blocked"`, and the coordinator routes them to review.

Two traps hide here:

1. **Status code is not category.** The same `429` can mean "slow down" or "no credits left". Check both the HTTP status and `error.code`, and never retry errors that need someone to act.
2. **Empty is not failed, and failed is not empty.** A timeout reported as `[]` makes the coordinator write "no evidence found". This is **silent suppression**: the output looks complete and is wrong. A status field must separate "searched, found nothing" from "could not search".

### 10.2 OpenAI client errors, retries and timeouts

All HTTP and connection errors inherit from `openai.APIError` (itself an `openai.OpenAIError`). `APIConnectionError` (and its subclass `APITimeoutError`) means no HTTP response. `APIStatusError` has one subclass per status (`RateLimitError` 429, `InternalServerError` ≥500, ...) and carries `status_code`, `request_id`, `code` and `param`.

The client has `max_retries=2` by default (up to 3 attempts). It retries connection errors, timeouts, `408`, `409`, `429` and every `≥500`, with exponential backoff from 0.5 s capped at 8 s, and honors `Retry-After` up to 120 s (a longer `Retry-After` means no retry: the error reaches you immediately). The default timeout is 600 s read/write and 5 s connect. Override per call with `client.with_options(max_retries=0, timeout=20)`. So by the time your code sees a `RateLimitError`, it was already retried twice, billing errors included. Your layer must read `exc.code` and stop. `ErrorInfo` is a small dataclass with `category`, `retryable` and `detail`.

```python
NON_RETRYABLE_429 = {"credit_balance_exhausted",
                     "organization_spend_limit_exceeded",
                     "project_spend_limit_exceeded",
                     "organization_usage_limit_exceeded"}

def classify_openai_error(exc: Exception) -> ErrorInfo:  # after retries
    if isinstance(exc, openai.APITimeoutError):  # before APIConnectionError
        return ErrorInfo("transient", True, "timeout")
    if isinstance(exc, openai.APIConnectionError):
        return ErrorInfo("transient", True, "connection")
    if isinstance(exc, openai.RateLimitError):
        if exc.code in NON_RETRYABLE_429:     # billing / quota: a human acts
            return ErrorInfo("business", False, exc.code)
        return ErrorInfo("transient", True, exc.code or "rate_limited")
    if isinstance(exc, openai.InternalServerError):  # 500, 503, ...
        return ErrorInfo("transient", True, f"{exc.status_code} {exc.code}")
    if isinstance(exc, (openai.AuthenticationError,
                        openai.PermissionDeniedError)):
        return ErrorInfo("permission", False, exc.code or str(exc.status_code))
    if isinstance(exc, (openai.BadRequestError, openai.NotFoundError,
                        openai.UnprocessableEntityError)):
        return ErrorInfo("validation", False, f"{exc.param}: {exc.message}")
    return ErrorInfo("unknown", False, type(exc).__name__)
```

- **Nested retries multiply.** Client (3 attempts) × an app decorator (3) × a worker re-run (2) = up to 18 calls for one step. Pick **one layer that owns retries** per failure type and set the others to zero or a known small number.
- **`429 slow_down` measures traffic growth**, not your RPM/TPM limit. Fanning out 50 workers on a cold project triggers it, so cap concurrency (an `asyncio.Semaphore`) instead of retrying harder.
- **Log `exc.request_id`** on every `APIStatusError`. Support asks for it. Connection errors and timeouts have none, so use `getattr(exc, "request_id", None)`.

### 10.3 Agents SDK exceptions and run-level handlers

Every Agents SDK exception inherits from `agents.AgentsException`. When the runner fails mid-run it fills **`run_data`** (check for `None`): the `input`, the `new_items` produced before the failure, the `raw_responses` and the `last_agent`. That is your source of partial results.

| Exception | When | Category |
|---|---|---|
| `MaxTurnsExceeded` | More than `max_turns` model calls (default 10) | Usually a design problem: salvage `run_data.new_items` |
| `ModelBehaviorError` | Unknown tool, malformed JSON, invalid structured output | Validation |
| `ModelRefusalError` | The model refused (`.refusal` holds the text) | Policy block: don't retry blindly |
| `ModelTimeoutError`, `ToolTimeoutError` | A model call or tool exceeded its timeout | Transient. Not Python's `TimeoutError`, so `except TimeoutError` misses them |
| The four guardrail tripwires (`Input`, `Output`, `ToolInput`, `ToolOutput`) | A guardrail tripped | Policy block: never retry the same input |

`openai.APIError` subclasses escape `Runner.run` unwrapped after all retries; classify them as in 10.2. Run-level controls change what happens before an exception escapes:

```python
from agents import (Agent, ModelRetrySettings, ModelSettings, RunConfig,
                    RunErrorHandlerResult, Runner, retry_policies)

def not_billing(ctx) -> bool:                # ctx is a RetryPolicyContext
    return ctx.normalized.error_code not in NON_RETRYABLE_429

settings = ModelSettings(
    timeout=60,                              # per attempt: ModelTimeoutError
    retry=ModelRetrySettings(                # opt-in runner-managed retries
        max_retries=2,
        policy=retry_policies.all(           # every policy must agree...
            retry_policies.any(retry_policies.provider_suggested(),
                               retry_policies.network_error()),
            not_billing)))                   # ...so the billing veto wins
worker = Agent(name="Music researcher", model=MODEL, model_settings=settings)

def on_max_turns(data) -> RunErrorHandlerResult:
    return RunErrorHandlerResult(include_in_history=False, final_output=(
        '{"status": "partial_failure", "failure_type": "max_turns"}'))

result = await Runner.run(
    worker, task, max_turns=6,
    error_handlers={"max_turns": on_max_turns},
    run_config=RunConfig(tool_not_found_behavior="return_error_to_model"))
```

- **`error_handlers`** turns `max_turns`, `model_refusal` and `invalid_final_output` into a controlled final output instead of an exception. With a typed `output_type` (like `WorkerResult` in 10.5), the handler must return a full `WorkerResult` built from `data.run_data.new_items`, or the run raises `UserError`. It replaces the `except MaxTurnsExceeded` path of 10.5, so pick one of the two per worker.
- **`ModelSettings(retry=...)` is opt-in.** The runner coordinates with the client so layers add instead of multiply. Against a server that always answers `503`: no `retry` gives 3 requests, `max_retries=2` gives 5, `max_retries=0` gives 1.
- **Retry policies don't know about billing.** `provider_suggested()` and `http_status([429])` are status-based, so they would retry `credit_balance_exhausted`. Hence the `not_billing` veto. The veto stops runner retries only: the first attempt still includes the client's 2 retries (3 requests for a billing `429`) unless the model's client is built with `max_retries=0` or the server sends `x-should-retry: false`.
- **`tool_not_found_behavior="return_error_to_model"`** sends "Tool 'x' not found." back to the model instead of raising `ModelBehaviorError`.
- Raising `max_turns` to 100 is not a fix. Hitting it means the loop isn't converging: salvage, report and fix the cause.

### 10.4 Tool errors as data

`function_call_output` has **no error flag**. The model learns a tool failed only from the text in `output`. In the Agents SDK, the runner writes that text using the tool's **`failure_error_function`**. Not set, it returns a fixed `An error occurred while running the tool. Please try again.` and the run continues. Your own `(ctx, error) -> str` function's string becomes the tool output. `None` makes the run fail with `UserError` (with `run_data`).

The default is safe (no leaked exception text) but generic: no category, no retry hint, and "Please try again" even when retrying can't help. Write your own:

```python
class ToolFailure(Exception):           # raise for anticipated failures
    def __init__(self, category, message, retryable, suggestion=None):
        super().__init__(message)
        self.category, self.retryable = category, retryable
        self.suggestion = suggestion

def tool_error_as_data(ctx, error: Exception) -> str:
    if isinstance(error, ToolFailure):
        p = {"category": error.category, "retryable": error.retryable,
             "message": str(error), "suggestion": error.suggestion}
    elif isinstance(error, (TimeoutError, ToolTimeoutError)):
        p = {"category": "transient", "retryable": True,
             "message": "Upstream search timed out.",
             "suggestion": "Retry once with a narrower query."}
    else:                               # unexpected: don't leak internals
        p = {"category": "unknown", "retryable": False,
             "message": type(error).__name__, "suggestion": "Do not retry."}
    return json.dumps({"status": "error", **p})

@function_tool(failure_error_function=tool_error_as_data, timeout=20,
               timeout_error_function=tool_error_as_data)
async def search_archive(query: str, topic: str) -> str:
    hits = await archive_client.search(query, topic)  # may raise
    return json.dumps({"status": "ok", "results": hits,  # empty is success
                       "note": "searched, 0 matches" if not hits else None})
```

- **Successes and failures use different `status` values**, and an empty success says it searched. That one field prevents silent suppression.
- **Timeouts.** `timeout=` with the default `timeout_behavior="error_as_result"` returns the plain text `Tool 'name' timed out after N seconds.` to the model, with no `status` field, because SDK timeouts skip `failure_error_function`. Pass `timeout_error_function=` (as above) so they also return the structured envelope; it receives a `ToolTimeoutError`. `"raise_exception"` raises `ToolTimeoutError`. `timeout` works only on **async** tools; on a sync function the decorator raises `ValueError`.
- **Side-effecting tools need idempotency.** If `issue_refund` timed out, you don't know whether the refund happened. Pass an idempotency key, or check state before retrying.
- The formatter's output is model-visible: no secrets, hostnames or raw SQL. Put the full exception in logs and the trace.

### 10.5 Structured worker results with partial results

A tool error tells the **worker**. A **worker result** tells the **coordinator**. Make it a Pydantic `output_type` (`Finding` has `title` and `source`), and wrap every run so the coordinator **always** gets one. The fields carry the structured error context that the Claude Certified Architect – Foundations exam guide lists (failure type, attempted query, partial results, alternative approaches); the exact field names are this course's design:

```python
class WorkerResult(BaseModel):      # strict-schema friendly: all required
    topic: str
    status: Literal["success", "partial_failure", "failure"]
    failure_type: Literal["timeout", "rate_limited", "validation",
                          "permission", "policy_blocked", "max_turns",
                          "unknown"] | None
    retryable: bool
    attempted_query: str
    findings: list[Finding]             # partial results survive a failure
    alternative_approaches: list[str]   # what the coordinator could try
    coverage_impact: str | None         # "Not covered: licensed sales data"

async def run_worker(agent, topic: str, task: str) -> WorkerResult:
    try:
        result = await Runner.run(agent, task, max_turns=6)
        return result.final_output_as(WorkerResult)
    except MaxTurnsExceeded as exc:     # failed() salvages run_data.new_items
        return failed(topic, task, "max_turns", False,
                      "Worker stopped at its turn limit.", exc)
    except (ModelTimeoutError, ToolTimeoutError) as exc:
        return failed(topic, task, "timeout", True, "Timed out.", exc)
    # tripwires, ModelRefusalError -> "policy_blocked"; and so on
```

`failed()` builds a `WorkerResult` from the tool outputs in `exc.run_data.new_items`: `partial_failure` if any findings survived, else `failure`. The full wrapper also maps `ModelBehaviorError` to `validation` and `openai.APIError` through 10.2, with `401`/`403` as `failure_type="permission"` so the coordinator escalates a revoked key. When one worker hits several failures, report the **most actionable** one (policy and permission first), not the first that happened. How failures reach the coordinator in each wiring pattern:

| Pattern | What the coordinator sees | Watch out for |
|---|---|---|
| **Code orchestration** (`asyncio.gather` over `run_worker`) | Always a `WorkerResult` | `asyncio.TaskGroup` **cancels the healthy workers** when one raises. Use `gather(..., return_exceptions=True)` or per-task wrappers |
| **Agents as tools** (`worker.as_tool(...)`) | The worker's final output as the manager's tool output | If the nested run raises, the manager gets the generic default. Pass `failure_error_function=` to `as_tool` too, and an async `custom_output_extractor` that returns `model_dump_json()` |
| **Hosted multi-agent** (Responses API beta, Agents API) | Coordination items and the root's final answer | Less control. Don't assume the answer reports gaps; ask the root for a per-subtask status |

### 10.6 Local recovery before propagation

Recover where the knowledge is. The tool knows whether a timeout is worth retrying, the worker knows whether a narrower query exists, and only the coordinator knows whether the answer can live without a section.

| Layer | Owns | Budget (example) |
|---|---|---|
| `openai` client | Transport and `429`/`5xx` retries for one call | `max_retries=2`, or `0` if a higher layer owns it |
| Tool | One quick retry of an idempotent read; a `timeout` | 1 retry, 20 s |
| Worker | Retry a transient tool error once with a changed query | 1 retry per search |
| Coordinator | Re-dispatch with a changed task, reroute, accept partial, or escalate | 1 re-dispatch per topic, per-worker and total deadlines |

A deadline covers the whole budget, not one attempt. Cut each attempt off when time runs out (`async with asyncio.timeout_at(deadline):`), don't start a backoff that would cross the deadline, and re-raise so `failure_error_function` reports it. Around the `openai` client, pass the remaining time as the per-attempt timeout (`with_options(max_retries=0, timeout=remaining)`), because the default read timeout is 600 s. The rule: **1–2 local retries for transient errors, zero for everything else, then propagate with context.** A coordinator retry should change the approach, not repeat what the worker exhausted. During a sustained outage, a **circuit breaker** fails fast for a cool-down, then goes **half-open** and admits exactly one probe; the probe's result closes or re-opens it. A retry is a new request: check what already happened before you repeat side effects (10.10).

### 10.7 Coordinator decisions and the anti-patterns

The coordinator makes one decision per topic. Make the rules explicit, in code or instructions:

| Worker result | Coordinator decision |
|---|---|
| `success`, findings present | Use them |
| `success`, no findings | Report "searched, no matching records" (full coverage) |
| `partial_failure`, `retryable=True` | Re-dispatch once with an `alternative_approaches` entry (narrower query, other source); if still partial, annotate |
| `failure`, `permission` or `policy_blocked` | Don't retry or rephrase. Annotate the gap; escalate access (Chapter 09) or route to review |
| `rate_limited`, non-retryable (billing) | Stop new work for the whole workflow; alert the owner |
| Too many gaps | Return a clearly marked partial report, or ask the user whether to continue |

Two ordering rules keep this honest. First, **check workflow-wide stop conditions** (billing) across all results before starting new work. Second, **merging a re-dispatch must not erase failures**: keep findings from both attempts and recompute status from both.

The anti-patterns, with their fixes: **silent suppression** (distinct status for "empty" vs "could not search"), **generic errors** (a custom `failure_error_function`), **killing the whole workflow** (a per-worker wrapper instead of `TaskGroup`), **infinite or multiplied retries** (one owning layer, bounded attempts, a deadline), **retrying the non-retryable** (classify first; retry only transient) and **blind replay of side effects** (idempotency keys; continue only unfinished work).

### 10.8 Coverage annotations in the final synthesis

The final report must say which parts are complete. Compute the coverage map **in code** from the `WorkerResult`s. Don't ask the model to judge its own coverage: it will smooth over a gap.

```python
LABEL = {"success": "FULL COVERAGE", "partial_failure": "PARTIAL COVERAGE",
         "failure": "NOT COVERED"}

def render_report(title: str, results: list[WorkerResult]) -> str:
    lines = [f"## {title}", ""]
    for r in results:
        label = LABEL[r.status] + (f": {r.failure_type}"
                                   if r.failure_type else "")
        if r.status == "success" and not r.findings:
            label += "; searched, no matching records"
        lines.append(f"### {r.topic.replace('_', ' ').title()} ({label})")
        lines += [f"- {f.title} ({f.source})" for f in r.findings] \
            or ["- No findings."]
        if r.coverage_impact:
            lines.append(f"> Coverage note: {r.coverage_impact}")
        lines.append("")
    gaps = [r.topic for r in results if r.status != "success"]
    done = len(results) - len(gaps)
    lines.append(f"**Coverage:** {done}/{len(results)} sections complete"
                 + (f"; gaps: {', '.join(gaps)}" if gaps else ""))
    return "\n".join(lines)
```

For the sample results in `01_practice` this prints sections like `### Writing (PARTIAL COVERAGE: timeout)` and `### Music (FULL COVERAGE; searched, no matching records)`, and ends with `**Coverage:** 2/3 sections complete; gaps: writing`. If a model writes the prose, give it the code-computed map, and add an output guardrail that fails when a section claims full coverage but its worker reported `partial_failure`.

### 10.9 Tracing for debugging failures

The Agents SDK traces every run by default. For failures:

- **Handled tool errors are recorded on the function span** as `"Error running tool (non-fatal)"` with the tool name and error. The run succeeded; the trace still shows the failure. With a custom formatter and sensitive data on (the default), the span holds the raw exception text. With the SDK's default formatter, or with `RunConfig(trace_include_sensitive_data=False)`, the error text is redacted.
- **Add your own spans for worker outcomes.** Wrap each worker in `custom_span(f"worker:{topic}")` and call `span.set_error({"message": ..., "data": {...}})` when it returns `partial_failure` or `failure`. Group the coordinator and all workers in one `trace(..., group_id=report_id)`.
- **Keep the request IDs**: `exc.request_id` on `APIStatusError`s (timeouts and connection errors have none: `getattr(exc, "request_id", None)`), `response._request_id` on successes.
- **Sensitive data.** Spans contain prompts and tool data by default. Turn that off for regulated data. Tracing is unavailable under Zero Data Retention.

Each production failure you fix can become an eval case ([agent workflow evaluation](https://developers.openai.com/api/docs/guides/agent-evals), Chapter 06). On the **Agents API**, debugging starts from events: `agent.session.turn.failed`, `agent.session.failed` and `agent.session.environment.failed`. Include the request, session and turn IDs when you contact support.

### 10.10 Background mode and managed-runtime failure statuses

Long-running work doesn't raise in your process. It ends in a **terminal status** you must read. A background response (`client.responses.create(..., background=True)`) stays `queued` or `in_progress` while you poll `client.responses.retrieve(resp.id)`, until it ends `completed`, `failed`, `cancelled` or `incomplete`. Even `completed` needs a check for `refusal` content.

| Terminal status | Read, then do |
|---|---|
| `incomplete` | `incomplete_details.reason`. `max_output_tokens` is a budget: raise it or split the task. `content_filter` is policy: don't resubmit unchanged. Never trust partial JSON |
| `failed` | `error.code` and `error.message`. Classify like 10.1: bounded retry for `server_error` or `rate_limit_exceeded`, never for `invalid_prompt` or `misalignment_policy_violation` |
| `cancelled` | Usually intentional; check your own records |

Instead of polling, subscribe to webhooks (`response.completed`, `response.failed`, ...). Save what you need as soon as the response is terminal, because retention can be short.

**Agents API sessions** (beta): a failed **turn** (`error.code` such as `server_overloaded`, `context_length_exceeded`, `session_budget_exceeded`, `credit_balance_exhausted`) doesn't always mean the **session** failed, and `idle` means "ready for input", not success. OpenAI's recovery procedure: (1) check the outcome, since the turn may have completed; (2) check completed actions, such as files changed or tools called; (3) wait and limit retries, honoring `Retry-After`; (4) once the session is `idle`, send a follow-up that asks it to continue **only the unfinished work**.

## Lesson code

Code from the video lesson: [../../presentations/10-multi-agent-error-handling/code/](../../presentations/10-multi-agent-error-handling/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run 10.1–10.10 offline (mock transports and `agents.testing.ScriptedModel`), then build a research coordinator with three workers, injected failures and a coverage-annotated report; the last cell runs it live |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 offline exercises with auto-checks, a due-diligence architecture scenario and a scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>
## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| `429` reaches your code | Read `exc.code`: back off on `slow_down`; stop and alert on billing/quota codes | Retrying every `RateLimitError` | Same status, different categories |
| Several retry layers exist | One owning layer per failure type; others at 0 or a known small number | Retry decorators at every layer | Retries multiply |
| Tool fails | Custom `failure_error_function` with category, retryable, suggestion | SDK default generic message, or raising | The model and coordinator need to know what to do |
| Search finds nothing | `status: ok`, empty results, "searched, 0 matches" | Raising an error, or returning `[]` from an `except` | Empty is a finding; failure is a gap |
| One worker raises | Per-worker wrapper returning a `WorkerResult`; `gather(return_exceptions=True)` | `TaskGroup`, or letting the exception escape | Keep the healthy workers' results |
| Coordinator must synthesize | Agents-as-tools or code orchestration | Handoffs | After a handoff the coordinator is out of the loop |
| Worker hit `max_turns` | Salvage `run_data.new_items`, return `partial_failure`, fix the loop | Raising `max_turns` to 100 | It's a convergence problem |
| Permission or policy block | Annotate the gap and escalate | Retrying or rephrasing | Not retryable by definition |
| Final report | Coverage map computed in code + annotations per section | Asking the model whether it covered everything | Models smooth over gaps |
| Background job `failed` | Classify `error.code`; bounded retry only for transient codes | Resubmitting in a loop | `failed` covers transient and permanent causes |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **Returning `[]` (or `status: success`) when a search failed.** Silent suppression produces confident, wrong reports.
- **Treating "no results" as an error**, which triggers useless retries and "system is down" messages.
- **Letting `as_tool` failures reach the manager as the generic default message.**
- **Using a handoff when the coordinator must handle failures and synthesize.**
- **Leaking stack traces, hostnames or secrets** into model-visible error text.
- **Ignoring terminal statuses** (`failed`, `cancelled`, `incomplete`) on background responses, or treating Agents API `idle` as success.

## Self-check

**1.** A research coordinator gets `{"results": []}` from its music worker and writes "No significant AI impact on the music industry was found." Later you find the archive search timed out on every call. What is the root fix?

- A) Raise the worker's `max_turns` so it keeps trying
- B) Make the tool and worker report a distinct status for "could not search" (category, retryable, attempted query) versus "searched, 0 matches", and have the coordinator annotate the gap
- C) Tell the coordinator in its instructions to be skeptical of empty results
- D) Switch the coordinator to `gpt-6-astra`

<details><summary>Answer</summary>

**B.** This is silent suppression: the failure was converted into an empty success before the coordinator saw it. No coordinator model can recover information that the result no longer contains (C, D). A treats a reporting problem as a loop problem.
</details>

**2.** Your pipeline wraps every model call in a decorator that retries `openai.RateLimitError` five times with backoff. Overnight, the organization's prepaid credits run out, and the logs show thousands of failed requests. What should change?

- A) Increase the backoff so the retries are slower
- B) Read `exc.code`: retry only rate-limit codes such as `slow_down`; treat `credit_balance_exhausted` and spend/usage-limit codes as non-retryable business errors that stop the workflow and alert an owner; and account for the client's own 2 retries in the budget
- C) Set `max_retries=0` on the client and keep the decorator
- D) Catch `RateLimitError` and return an empty result

<details><summary>Answer</summary>

**B.** The same `429` status covers temporary throttling and billing/quota errors. OpenAI's guidance is not to retry errors that need someone to act, and the client's status-based rules may already have retried each call twice before the decorator saw it. A and C still retry a billing error. D is silent suppression.
</details>

**3.** A tool raises `TimeoutError` inside an Agents SDK worker. The coordinator's trace shows the worker's tool output was "An error occurred while running the tool. Please try again.", and the worker retried five times with the same query. What is the best fix?

- A) Set `failure_error_function=None` so the run fails fast
- B) Pass a custom `failure_error_function` that returns a structured error (category `transient`, retryable, suggestion "retry once with a narrower query"), and tell the worker to retry transient errors at most once
- C) Increase the tool's `timeout` to 10 minutes
- D) Remove the tool and let the model answer from its own knowledge

<details><summary>Answer</summary>

**B.** The SDK default is a generic message with an unconditional "Please try again", so the model has no category and no limit. A turns a recoverable error into a run failure (`UserError`). C hides the latency problem. D invites fabrication.
</details>

**4.** Three researcher agents run in an `asyncio.TaskGroup`. When the literature worker raises `MaxTurnsExceeded`, the coordinator receives nothing, even though visual art and music were almost done. What should the design be?

- A) Run the workers sequentially so one failure can't affect the others
- B) Wrap each worker so it always returns a `WorkerResult` (salvaging `exc.run_data.new_items` on `MaxTurnsExceeded`), and gather with `return_exceptions=True` or per-task wrappers
- C) Set `max_turns=None` on every worker
- D) Use handoffs from the coordinator to each worker

<details><summary>Answer</summary>

**B.** `TaskGroup` cancels the remaining tasks when one raises, which is the "kill the whole workflow" anti-pattern. A gives up parallelism and still loses the failing section's partial work. C hides a non-converging loop. D removes the coordinator from the loop, so nothing synthesizes the results.
</details>

## Official documentation

- [Error codes](https://developers.openai.com/api/docs/guides/error-codes): API error codes (including the billing `429`s and `503 server_is_overloaded`), Python library error types, handling errors
- [Rate limits](https://developers.openai.com/api/docs/guides/rate-limits): `Retry-After`, `slow_down` vs `server_is_overloaded`, ramp rate, retrying with exponential backoff, nested-retry warning
- [Background mode](https://developers.openai.com/api/docs/guides/background): polling, cancelling, streaming resume, `store` and retention, limits
- [Agents SDK: Running agents](https://developers.openai.com/api/docs/guides/agents/running-agents): the loop, pauses vs failures
- [Agents SDK (Python): Tools](https://openai.github.io/openai-agents-python/tools/): `failure_error_function`, tool timeouts
- [Agents API: Errors and recovery](https://developers.openai.com/api/docs/guides/agents-api/errors): request, turn, session and environment errors; the recovery procedure

[← Chapter 09 — Escalation and Human-in-the-Loop](../09-escalation-human-in-the-loop/README.md) | [↑ OpenAI path](../README.md) | [Chapter 11 — Context Management in Production Systems →](../11-context-management/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
