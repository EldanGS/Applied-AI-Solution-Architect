# Chapter 1 — Responses API Fundamentals: How You Talk to GPT Models

> **Claude counterpart:** [Chapter 1 — Claude API Fundamentals](../../anthropic-claude/01-claude-api-fundamentals/README.md) · **Academy course(s):** Scope AI Solutions (API pathway) · **Est. time:** 5–7 hours (reading + notebooks) · **Status:** [ ] not started

Everything else in the OpenAI path (function calling, the Agents SDK, built-in tools, MCP, Codex) sits on one HTTP call: `POST /v1/responses`. Compared with Claude, the real differences are **server-side state** (the API can remember the conversation for you), **no single `stop_reason` field** (you read `status`, `incomplete_details` and the output item types), and a **reasoning-effort scale with model-specific values**. Who owns the conversation state is an architecture decision: it touches retention, compliance (Zero Data Retention), portability and cost.

## What you'll learn

- Build a valid Responses API request and read the typed `output` list safely
- Use `instructions` vs `developer` messages, and handle every `status` and `incomplete_details.reason`
- Choose between stateless history, `previous_response_id` and the Conversations API, with their retention and billing consequences
- Stream a response, run one in background mode, and know when webhooks fit
- Count tokens, read `usage`, estimate cost, and pick a model and `reasoning.effort` from evals
- Move a Playground prototype into versioned code, and test outputs that vary between runs

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md) (Python 3.11+, venv, `.env` with `OPENAI_API_KEY` and optionally `OPENAI_MODEL`) and the [OpenAI path overview](../README.md). Optional: [Claude Chapter 1](../../anthropic-claude/01-claude-api-fundamentals/README.md). Shared setup for every snippet (`gpt-6-luna` keeps each notebook well under a cent):

```python
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()                                   # reads OPENAI_API_KEY from .env
client = OpenAI()                               # key from the environment
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna") # cheapest GPT-6 model
RULES = "You are a concise travel assistant. Answer in at most three sentences."
```

## Concepts

### 1.1 Anatomy of a Responses API request

All text generation, tool use, structured output and built-in tools go through `POST /v1/responses` (`client.responses.create`). Features are *parameters on this endpoint*, not separate APIs. The reply is a `Response` whose `output` is a **list of typed items** (`reasoning`, `message`, `function_call`, ...), not a string.

```python
response = client.responses.create(
    model=MODEL,
    instructions="You are a concise assistant for a cloud architecture team.",
    input="In two sentences, what is an API gateway?",  # one user message
    reasoning={"effort": "low"},     # how much the model thinks (see 1.7)
    max_output_tokens=2000,          # ALL generated tokens, reasoning included
)
for item in response.output:         # reasoning, message, function_call, ...
    if item.type == "message":
        for part in item.content:
            if part.type == "output_text":
                print(part.text)
            elif part.type == "refusal":
                print("Refused:", part.refusal)
```

| Field | What it does | Architect note |
|---|---|---|
| `input` | A string (one `user` message) or a list of input items | Optional only when state comes from `previous_response_id` / `conversation` |
| `instructions` | A system/developer message for this request | **Not** carried over by `previous_response_id`; resend every turn |
| `max_output_tokens` | Optional ceiling on generated tokens, **reasoning included** | Too low gives `status: "incomplete"` with no visible text |
| `store` | Keep the response (30 days); **defaults to `true`** | `store=False` for stateless or ZDR flows ([1.4](#14-conversation-state-stateless-chained-or-durable)) |
| `previous_response_id` / `conversation` | Server-side conversation state | You cannot send both |

Other fields: `reasoning` ([1.7](#17-model-selection-and-reasoning-effort)), `stream` and `background` ([1.5](#15-streaming-background-mode-and-webhooks)), `truncation` (`disabled` by default, so an over-long input fails with 400; see [1.6](#16-context-window-tokens-and-cost)), and `temperature` / `top_p`, which you remove on GPT-6 whenever effort is not `none`. The response also carries `id`, `status` and `usage`.

`response.output_text` is an SDK helper that joins every `output_text` part and returns `""` when there are none. **Exam trap:** `response.output[0].content[0].text` is a bug. With a reasoning model the first item is often `reasoning` (on easy prompts at low effort it may be absent); with tools it may be a `function_call`. Use `output_text` or filter by `item.type`.

**Errors are not statuses.** A failed request returns an HTTP error (`400`, `401`, `429`, `5xx`, ...); an accepted one returns a `Response` with a `status`. The SDK retries connection errors, `408`, `409`, `429` and `5xx` twice by default (`max_retries`) and honors `Retry-After`. Catch typed exceptions (`openai.RateLimitError`, `openai.BadRequestError`). Quota `429`s (`insufficient_quota`) do not go away by retrying.

### 1.2 Input items, roles and instructions

`input` is a list of **items**, and a message is only one item type. Others are `reasoning` (opaque; replay it unchanged when you manage state) and `function_call` / `function_call_output`, linked by `call_id` (Chapter 2). Roles carry different authority: `developer` (and `system`) instructions take precedence over `user` instructions, and `assistant` messages are the model's own earlier output.

`instructions="Talk like a pirate."` and a `{"role": "developer", "content": "Talk like a pirate."}` input item are roughly equivalent for one request. They differ across turns. `instructions` apply to **this request only**: `previous_response_id` does not carry them over and the Conversations API does not store them, so resend them every turn. They suit stable app rules you control from code. A `developer` message is an input item, so it stays in the chained context and is stored in a conversation; use it for a transcript you replay exactly, or an operator update mid-chat. **Exam trap:** "After switching to `previous_response_id`, the bot stopped following our tone rules from turn 2 onward." The rules were sent as `instructions` on turn 1 only. Resend them on every request, or put them in a `developer` message that is part of the chain.

**Instruction drift.** Resending `instructions` keeps the rules in every request, but still include long transcripts in your evals: replies late in a long chat can wander from the rules.

**Prompts live in code.** Reusable prompt objects (`v1/prompts`, the `prompt` parameter) are deprecated and shut down on 2026-11-30. Keep prompt builders in your codebase. Assistant messages can carry `phase` (`"commentary"` or `"final_answer"`); replay output items unchanged so a preamble does not look like a final answer.

### 1.3 Status and incomplete_details: why generation stopped

Claude has one `stop_reason`. OpenAI splits it across **`response.status`** (did it finish?), **`incomplete_details.reason`** (if not, why?) and **the output item types** (did the model call a tool, refuse, or answer?).

| `status` | Meaning | What your code should do |
|---|---|---|
| `completed` | The model finished its turn | Run any `function_call` items (Chapter 2) or return the text |
| `incomplete` | Stopped early; see `incomplete_details.reason` | `max_output_tokens`: your ceiling **or the context window** was hit. Partial text is truncated; no text means the budget ran out **during reasoning**. Raise the limit (OpenAI suggests reserving at least 25,000 tokens when you start with reasoning models), lower effort, or shrink the input. `content_filter`: don't show the partial output. `steered` (WebSocket steering) and `max_messages`: log them |
| `failed` | `response.error` has `code` and `message` | Log `error.code`; retry only transient codes |
| `cancelled` / `queued` / `in_progress` | A background response was cancelled / is still running | Stop / keep polling or reading the stream |

```python
def handle(resp) -> str | None:
    match resp.status:
        case "completed":
            if any(i.type == "function_call" for i in resp.output):
                raise NotImplementedError("Run the tools and loop (Ch. 2)")
            refusals = [p.refusal for i in resp.output if i.type == "message"
                        for p in i.content if p.type == "refusal"]
            # on a refusal, return None and show a fallback
            return None if refusals else resp.output_text
        case "incomplete":
            reason = getattr(resp.incomplete_details, "reason", None)
            if reason == "max_output_tokens":
                if resp.output_text:
                    raise RuntimeError("Truncated: raise the budget")
                raise RuntimeError("Budget spent on reasoning: no output")
            raise RuntimeError(f"Incomplete: {reason}")
        case "failed":
            code = resp.error.code if resp.error else "unknown"
            raise RuntimeError(f"Failed: {code}")
        case "queued" | "in_progress":
            raise RuntimeError("Still running: poll responses.retrieve")
        case "cancelled":
            return None
        case other:
            raise ValueError(f"Unknown status: {other}")  # future-proofing
```

> **Exam trap:** "The model returned an empty string, but the request succeeded (HTTP 200)." `incomplete` + `max_output_tokens` + empty `output_text` means the whole budget went into reasoning. Raising `max_output_tokens` (or lowering effort) fixes it; rewording the prompt does not. For agent loops, keep looping while the latest response contains `function_call` items; checking for non-empty `output_text` is wrong, because the model can write a preamble **and** call a tool in one response.

### 1.4 Conversation state: stateless, chained or durable

Each call is independent, but there are three ways to continue a conversation. In all three, the context the model sees is **billed as input on every turn**.

| Pattern | How | What OpenAI stores | Best for |
|---|---|---|---|
| **Stateless** | Append `response.output` items and the next user message to a list; send it all with `store=False` | Nothing durable | ZDR/compliance, full control over trimming, portability |
| **Chained** | New input plus `previous_response_id=prev.id` | Each response, 30 days by default | Simplest multi-turn code; short sessions |
| **Durable** | `conversation=conv.id` on every call | The conversation and its items, **until you delete them** | Threads across sessions, devices or jobs |

```python
# 1) Stateless: your app owns the transcript
history = [{"role": "user", "content": "I'm vegetarian and I love hiking."}]
r1 = client.responses.create(model=MODEL, input=history, store=False)
history += r1.output    # keep EVERY output item, reasoning included
history.append({"role": "user", "content": "Suggest a weekend trip."})
r2 = client.responses.create(model=MODEL, input=history, store=False)
# 2) Chained: OpenAI keeps the previous response
r1 = client.responses.create(model=MODEL, instructions=RULES,
                             input="I'm vegetarian.")
r2 = client.responses.create(model=MODEL, instructions=RULES,  # resend!
                             previous_response_id=r1.id,
                             input="Suggest a trip.")
# 3) Durable: a conversation object
conv = client.conversations.create(metadata={"user": "u_123"})
client.responses.create(model=MODEL, instructions=RULES,
                        conversation=conv.id, input="I'm vegetarian.")
```

- `store` defaults to `true` (30 days). Conversation items have **no** 30-day TTL, and **deleting a conversation does not delete its items**: delete each item (`client.conversations.items.delete(item_id, conversation_id=...)`), then the conversation. Delete responses with `client.responses.delete(response_id)` if your retention policy requires it. Switching to `previous_response_id` moves conversation data into OpenAI storage, so check with whoever owns data retention.
- `previous_response_id` and `conversation` **cannot be combined**. `previous_response_id` needs a stored response: over plain HTTP, treat it plus `store=False` as unsupported (only WebSocket mode keeps a connection-local cache).
- After an `incomplete` or `failed` turn in a conversation, the docs do not say whether its items were added. Check `client.conversations.items.list(conv.id)` before you resend.
- With **Zero Data Retention**, `store` is always treated as `false` and the Conversations API is not ZDR-eligible. A ZDR design is stateless: replay every output item (reasoning items include `encrypted_content` when `store=False`) and use compaction.

> **Exam trap:** "The assistant forgets what the user said two turns ago." Causes: the app sends only the new message without `previous_response_id` or `conversation`; it chains from the wrong (older or failed) response ID; or it uses `store=False` and chains over HTTP. The fix is never a bigger context window.

### 1.5 Streaming, background mode and webhooks

**Streaming** (`stream=True`) sends **typed events** over server-sent events: `response.created`, `response.output_text.delta`, `response.completed`, `error`, plus `response.incomplete`, `response.failed` and others; the `completed` / `incomplete` / `failed` events carry the full `Response`. The SDK helper `client.responses.stream(...)` accumulates for you (`get_final_response()`). **Background mode** (`background=True`) returns at once with `status: "queued"` or `"in_progress"`; you poll `responses.retrieve(id)`, and `responses.cancel(id)` stops it. It exists for reasoning tasks that take minutes.

```python
stream = client.responses.create(model=MODEL, stream=True,
                                 input="Explain idempotency in 3 bullets.")
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
job = client.responses.create(model=MODEL, background=True,
                              input="Write a long migration plan.")
while job.status in {"queued", "in_progress"}:
    time.sleep(2)
    job = client.responses.retrieve(job.id)
print(job.status, job.output_text)
```

`background=True` + `stream=True` lets you resume a stream from each event's `sequence_number`. With `store=False` (or ZDR), background data is kept for roughly 10 minutes. **Webhooks:** subscribe to events such as `response.completed` instead of polling; verify signatures with `client.webhooks.unwrap(body, headers)`. **WebSocket mode** (`client.responses.connect()`) keeps one connection open for many fast tool round trips; OpenAI reports up to roughly 40% faster execution for rollouts with 20+ tool calls. Thousands of non-urgent requests go to the Batch API (50% off, within 24 h; [chapter 07](../07-batch-and-cost/README.md)).

**Exam trap:** "Long reasoning requests time out at the load balancer after 60 seconds." The fix is `background=True` with polling or a webhook, not a bigger timeout or a retry loop that restarts (and re-bills) the job.

### 1.6 Context window, tokens and cost

The **context window** is the most tokens one request can use: input, output and reasoning together. The current GPT-6 models (`gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`) list a 1,050,000-token context window, 922,000 max input and 128,000 max output. Instructions, tool definitions, every input item, images and files all count. Reasoning tokens are never shown, but they occupy the window and are **billed as output tokens**. **Before sending**, `client.responses.input_tokens.count(...)` takes the same input as `create` and counts formatting tokens a local tokenizer cannot see (use it, not `tiktoken` or chars ÷ 4, for anything with images, files, tools or schemas). It rejects generation-only options (`max_output_tokens`, `stream`, `store`, `background` raise `TypeError`). **After sending**, read `response.usage`.

```python
context = dict(model=MODEL, instructions=RULES,   # counts are model-specific
               input=history + [{"role": "user", "content": "..."}])
print(client.responses.input_tokens.count(**context).input_tokens)
response = client.responses.create(**context, max_output_tokens=2000)
u = response.usage
print(u.input_tokens, u.input_tokens_details.cached_tokens,
      u.input_tokens_details.cache_write_tokens)
print(u.output_tokens,
      u.output_tokens_details.reasoning_tokens)  # INSIDE output_tokens
```

| Rates per MTok (2026-11-06) | Input | Cached input | Cache writes | Output |
|---|---|---|---|---|
| `gpt-6-astra` | $10 | $1 | $12.50 | $50 |
| `gpt-6.1-sol` | $2 | $0.10 | $2.50 | $10 |
| `gpt-6.1-terra` | $1 | $0.05 | $1.25 | $5 |
| `gpt-6-luna` | $0.10 | $0.01 | $0.125 | $0.50 |

- **Cost** = uncached input × input rate + cached × cached rate + cache writes × write rate + output × output rate, where uncached = `input_tokens` − cached − writes.
- **Long prompts cost more.** Over 272K input tokens, the **whole request** is priced at 2x input and cache rates and 1.5x output.
- **Prompt caching is automatic.** Cached input is up to 95% cheaper; the minimum cacheable prefix is 1,024 tokens on the GPT-6 models. Keep stable content first.
- **Long conversations:** `truncation="auto"` silently drops the oldest items. Prefer compaction (`context_management=[{"type": "compaction", "compact_threshold": 200000}]` or `client.responses.compact(...)`), which is ZDR-friendly with `store=False`.
- **Exam trap:** "Use `previous_response_id` so we stop paying for the history." Wrong: the chain's earlier input tokens are still billed as input. Caching lowers the price of a stable prefix; compaction and trimming lower the size.

### 1.7 Model selection and reasoning effort

| Model | API ID | Positioning | Input / Output per MTok | `reasoning.effort` | Default |
|---|---|---|---|---|---|
| GPT-6 Astra | `gpt-6-astra` | Most capable | $10 / $50 | `low` … `max` (no `none` / `minimal`) | not stated; set it |
| GPT-6.1 Sol | `gpt-6.1-sol` | Near-Astra at lower cost | $2 / $10 | `low` … `max` (no `none` / `minimal`) | `medium` |
| GPT-6.1 Terra | `gpt-6.1-terra` | Fast; visual reasoning, computer use, writing | $1 / $5 | `none`, `low` … `max` | `medium` |
| GPT-6 Luna | `gpt-6-luna` | Most efficient, high volume | $0.10 / $0.50 | `none`, `low` … `max` | `medium` |

#### Reasoning vs non-reasoning models

A **reasoning model** works through the problem (a "chain of thought") before it answers. You never see it: it comes back as an opaque `reasoning` item, and its tokens are billed as output. Reasoning is more accurate on hard, multi-step work (planning, math, code, multi-tool workflows) at the cost of latency and tokens. A **non-reasoning model** answers straight away: faster, usually cheaper, weaker on multi-step problems. Every GPT-6 model reasons, so `reasoning.effort` decides how much. `none` fits latency-critical tasks such as voice, fast retrieval and classification. Prompting differs too, so re-run evals when you switch. (The earlier `gpt-6-sol`, $2 / $10, is still listed and supports `none`. Batch and Flex are 50% of standard rates; Fast mode costs 2x.)

**Fast front, flagship behind.** OpenAI's Building Agents track recommends a fast model that chats with the user and **delegates the demanding tasks** to the flagship. Most turns stay quick, and you pay flagship prices only where needed. A sketch (`FRONT_DESK_RULES` and `DELEGATE_TOOL` are placeholders; needs `import json`):

```python
def reply(user_text: str, history: list) -> str:
    fast = client.responses.create(
        model="gpt-6-luna", reasoning={"effort": "none"},
        instructions=FRONT_DESK_RULES, tools=[DELEGATE_TOOL], store=False,
        input=history + [{"role": "user", "content": user_text}],
    )
    calls = [i for i in fast.output if i.type == "function_call"]
    if not calls:
        return fast.output_text            # most turns: fast and cheap
    task = json.loads(calls[0].arguments)["task"]  # fast model asks for help
    deep = client.responses.create(
        model="gpt-6-astra", reasoning={"effort": "high"},
        input=task, background=True, store=False,  # long job: poll (1.5)
    )
    ...
```

The levers: **model tier**; **`reasoning.effort`** (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, but **each model supports a subset**, and an unsupported value returns HTTP 400; `low` for extraction, routing and classification, `medium` or `high` for diagnosis, planning and code, `xhigh` / `max` only when evals justify it); **`text.verbosity`** (`low` / `medium` / `high`) for answer length; and **`reasoning.mode`** (`standard` or `pro`) for the hardest tasks. To change effort mid-conversation without breaking the cached prefix (GPT-6, standard single-agent mode), add a `{"type": "configuration_update", "reasoning": {"effort": "high"}}` input item before the next user message and keep the request-level `reasoning.effort` unchanged. It can also lower effort for routine follow-ups; don't combine it with automatic compaction (`context_management`) or `truncation="auto"`. On GPT-6, when effort is not `none`, remove `temperature`, `top_p` and `top_logprobs`.

**Selection process.** Build an **eval set** of 20–100 real examples with a pass criterion. If cost and latency don't matter, OpenAI suggests defaulting to Astra; otherwise start where your task sits (for example Luna · Low for well-scoped extraction, Sol · Medium for complex technical work). Step down (lower effort, then a cheaper model) while the eval passes. Compare **cost per successful task**, and check lifecycle with `client.models.retrieve(id).shutdown_date`. **Exam trap:** "Use the biggest model and `max` effort to be safe" and "pick the largest context window" are wrong. Measure on representative data, then pick the cheapest model + effort that meets the quality and latency bar.

### 1.8 Chat Completions: the legacy contrast

Chat Completions (`POST /v1/chat/completions`) is still supported, but OpenAI recommends Responses for all new projects. The **Assistants API** was retired on 2026-08-26; its replacement is Responses + the Conversations API. To migrate a text-only chat, pass the same `messages` list as `input`: Responses accepts it as-is.

| Concept | Chat Completions | Responses |
|---|---|---|
| Input / output | `messages=[...]` / `choices[0].message.content` | `input` + `instructions` / `output` items, `output_text` |
| Why it stopped | `choices[0].finish_reason` (`stop`, `length`, `tool_calls`, ...) | `status` + `incomplete_details.reason` + item types |
| Limits and effort | `max_completion_tokens`, `reasoning_effort="low"` | `max_output_tokens`, `reasoning={"effort": "low"}` |
| Tool calling on GPT-6 | Astra, 6.1 Sol and 6.1 Terra: **not supported**; Sol and Luna: only with `reasoning_effort="none"` | Supported |

> **Exam trap:** "We migrated our GPT-6 Astra tool-calling bot from Chat Completions and it now fails." GPT-6 Astra, GPT-6.1 Sol and GPT-6.1 Terra require the Responses API for tool calling.

### 1.9 Playground to code, sampling and non-determinism

#### Prototype in the Playground, then move to code

OpenAI's AI Application Development track starts in the [Playground](https://platform.openai.com/chat/edit): test prompts and tools there, then move into your app once you know what output to expect. Its **Generate** button drafts prompts, functions and schemas; treat them as first drafts. In code, the model goes to config, the prompt to a versioned builder in your repo, effort and verbosity to request parameters, and "it looked right on three examples" to an eval set ([Chapter 6](../06-prompt-engineering-and-evals/README.md)). Don't wire the app to a saved prompt object: `v1/prompts` shuts down on November 30, 2026.

```python
# prompts/support_reply.py: the Playground prompt, now reviewed like code
SUPPORT_REPLY_V3 = ("You are a support assistant for {product}. "
                    "Answer in at most {max_sentences} sentences.")
def support_reply_request(question: str, *, product: str,
                          max_sentences: int = 3) -> dict:
    return dict(
        model=os.getenv("OPENAI_MODEL", "gpt-6-luna"),
        instructions=SUPPORT_REPLY_V3.format(
            product=product, max_sentences=max_sentences),
        input=question, text={"verbosity": "low"},
        reasoning={"effort": "low"},   # the effort that passed the eval
    )
```

#### Sampling and non-determinism

Each output token is **sampled** from a probability distribution ([00 — Prerequisites §2.9](../../00-prerequisites/README.md#29-next-token-generation)). `temperature` (0–2) makes output more focused (low) or more random (high); `top_p` keeps only the top probability mass. Change one, not both, and on GPT-6 remove both whenever effort is not `none`. There is no `seed` parameter on `responses.create`. With reasoning on, two runs can give different text, tool calls or labels: "the content generated from a model is non-deterministic." The same rules as [Claude Chapter 1](../../anthropic-claude/01-claude-api-fundamentals/README.md#sampling-and-non-determinism) apply: **test properties, not strings** (it parses, matches the schema, picks the right label); **sample several runs per example** (3–5 is a common start) and report a **pass rate**; make the shape deterministic with Structured Outputs ([Chapter 2](../02-function-calling-and-structured-outputs/README.md)); pin the model snapshot, prompt version and effort; log `response.id`.

**Exam trap:** "Set `temperature=0` so the GPT-6 tests are deterministic" is wrong twice: with reasoning on, OpenAI says to remove `temperature`, and a low temperature never promised identical output.

## Lesson code

Video-lesson code: [../../presentations/01-api-fundamentals/code/](../../presentations/01-api-fundamentals/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`00_session_demo.ipynb`](00_session_demo.ipynb) | Walk through one call, typed replies, `instructions`, status, the three state patterns, tokens, cost, effort, non-determinism, streaming and background mode |
| [`01_practice.ipynb`](01_practice.ipynb) | One section per concept 1.1–1.9 (including an effort sweep and a delegation router), then build `ChatSession`, a multi-turn helper with chain / conversation / stateless modes and a cost report |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: 12-question quiz, 5 auto-checked exercises plus 1 optional live one, a ZDR architecture scenario and a scorecard |

## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| ZDR or strict retention | Stateless history with `store=False`, replaying all output items; compaction | `previous_response_id` or Conversations | ZDR forces `store=false`; Conversations are not ZDR-eligible |
| Thread must survive across devices or sessions | Conversations API (delete its items, then the conversation) | Chaining response IDs | Durable object with no 30-day TTL |
| Cut the cost of long chats | Stable prefix for caching + compaction/trimming | "Switch to `previous_response_id`" | The chain is still billed as input |
| Empty answer, `status: "incomplete"` | Raise `max_output_tokens` or lower effort | Rewriting the prompt | Reasoning used the budget |
| Multi-minute job behind short timeouts | `background=True` + polling or a webhook | Longer timeouts or blind retries | Retries restart and re-bill the job |
| Token count before a big request | `responses.input_tokens.count` with the target model | `tiktoken` / chars ÷ 4 | Counts tools, images, files, formatting |
| High-volume simple classification | Luna at `low` (or `none`), checked by an eval | Astra at default effort | Cost per successful task |
| Chat product where a few turns need deep work | A fast model at the front that delegates to Astra | Astra on every turn | Flagship cost only where it pays off |
| Tests flake because outputs vary | Several runs, property checks, Structured Outputs | `temperature=0` | Output is non-deterministic |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Reading `output[0].content[0].text`.** Use `output_text` or filter by type.
- **Ignoring `status`.** `incomplete` responses arrive with HTTP 200.
- **A tiny `max_output_tokens` on a reasoning model.** It can run out during reasoning, and you still pay.
- **Sending `instructions` only on the first turn of a chain.** They are not carried over.
- **Chaining with `previous_response_id` while using `store=False`** over HTTP. Replay the history yourself.
- **Assuming `conversations.delete()` removes the transcript.** Delete the items explicitly.

## Self-check

**Q1.** A trip-planning bot on the Responses API is told "I'm flying out of Lisbon" and, on its very next turn, asks "Which city are you departing from?" Each request sends `input=user_message` and `instructions=RULES`, with default settings. What is the most likely cause?

- A) The 1.05M context window is full
- B) The requests send neither the earlier items, nor `previous_response_id`, nor a `conversation`, so each call is independent
- C) `store` defaults to `false`, so OpenAI discards the earlier turns
- D) `instructions` override the earlier user messages

<details><summary>Answer</summary>

**B.** Each call only sees its own input unless you replay history, chain with `previous_response_id`, or attach a `conversation`. A is impossible for a short chat. C is false: `store` defaults to `true`, but storing a response doesn't attach it to the next request. D is not how `instructions` work.
</details>

**Q2.** A request to `gpt-6-luna` with `max_output_tokens=200` returns HTTP 200, `status: "incomplete"`, `incomplete_details.reason: "max_output_tokens"`, and `output_text == ""`. What happened, and what is the best fix?

- A) A content filter removed the answer; rephrase the prompt
- B) The model spent the whole budget on reasoning tokens; raise `max_output_tokens` or lower `reasoning.effort`
- C) The input exceeded the context window; enable `truncation="auto"`
- D) The response is still running; poll `responses.retrieve`

<details><summary>Answer</summary>

**B.** `max_output_tokens` includes reasoning tokens. An empty `output_text` with this reason means the budget ran out during reasoning. A would show `content_filter`, C would be a 400 error with the default `truncation="disabled"`, and D would show `queued` / `in_progress`.
</details>

**Q3.** You move a chat from manual history to `previous_response_id`. From turn 2 onward the assistant ignores the persona rules, which are passed in `instructions` on the first request only. What is the fix?

- A) Set `store=True` explicitly so the instructions are saved
- B) Resend `instructions` on every request
- C) Use `truncation="auto"` so the rules stay in context
- D) Raise `reasoning.effort` so the model remembers the rules

<details><summary>Answer</summary>

**B.** `instructions` apply only to the current request; when chaining with `previous_response_id`, earlier instructions are not carried over. A changes nothing (`store` already defaults to `true`, and a stored response still doesn't pass its `instructions` on), C is unrelated, D does not restore missing instructions.
</details>

**Q4.** A bank's compliance team requires Zero Data Retention. The team wants a multi-turn assistant on a reasoning model with good continuity. Which design fits?

- A) The Conversations API, deleting conversations after 30 days
- B) `previous_response_id` with `store=True`
- C) Stateless requests with `store=False`, replaying every output item (including encrypted reasoning items), plus compaction for long sessions
- D) Chat Completions with `n=2` so state is duplicated

<details><summary>Answer</summary>

**C.** Under ZDR, `store` is always treated as `false` and the Conversations API is not ZDR-eligible, so state must live in the app. Reasoning items carry `encrypted_content` when `store=False`, which preserves continuity without server-side storage. A and B rely on server storage; D is meaningless.
</details>

## Official documentation

- [Responses API reference: create](https://developers.openai.com/api/reference/resources/responses/methods/create)
- [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)
- [Background mode](https://developers.openai.com/api/docs/guides/background)
- [Reasoning models (effort, incomplete responses, persisted reasoning)](https://developers.openai.com/api/docs/guides/reasoning)
- [Counting tokens](https://developers.openai.com/api/docs/guides/token-counting)
- [Models](https://developers.openai.com/api/docs/models)

Facts checked against developers.openai.com and the `openai` 3.24 Python SDK on 2026-10-03; model lineup, prices and effort values re-checked on 2026-11-06 (the SDK's type hints don't list `gpt-6.1-terra` yet; any model string works).

---

[← OpenAI path overview](../README.md) | [↑ Root README](../../README.md) | [Chapter 2 — Function Calling and Structured Outputs →](../02-function-calling-and-structured-outputs/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
