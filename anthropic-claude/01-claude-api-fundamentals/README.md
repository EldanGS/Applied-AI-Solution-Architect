# Chapter 1 — Claude API Fundamentals: How You Talk to the Model

> **Exam domain(s):** CCDV-F D2.3 (Messages, invoking Claude through third-party vendors) and D5.1–5.2 (tokens, context windows, sampling, non-determinism, effort, SDKs that wrap REST APIs) are the primary targets. For CCA-F this chapter is background for Domains 1, 4 and 5; their task statements are taught in [Chapter 3](../03-agent-sdk/README.md), [Chapter 6](../06-prompt-engineering/README.md) and [Chapter 11](../11-context-management/README.md) · **Est. time:** 6–8 hours (reading + notebooks) · **Status:** [ ] not started

> **Also maps to:** the Messages API lessons of several Anthropic Academy courses. The full mapping is in [Certification coverage](coverage/README.md#certification-coverage).

Every topic later in this repo (tool use, the Agent SDK, MCP, Claude Code) is built on one HTTP call: `POST /v1/messages`. The API is **stateless**, so your application owns the conversation state, and with it latency, cost and memory. Most "the bot forgot", "the agent never stopped" and "the bill doubled" incidents come from a wrong assumption at this layer.

## What you'll learn

- Build a valid Messages API request and read the typed response safely
- Run a multi-turn chat on a stateless API by resending history
- Handle all seven `stop_reason` values
- Use the system prompt for persistent behavior without creating unintended tool associations
- Reason about the context window, sampling, non-determinism, tokens and cost
- Choose a model and effort level by evals, and call Claude through the SDK, raw REST or a cloud platform

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md) (Python 3.11+, venv, `.env` with `ANTHROPIC_API_KEY`) and the [Claude path overview](../README.md). Shared setup for every snippet:

```python
import anthropic
from dotenv import load_dotenv

load_dotenv()                       # reads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic()      # key from the environment, never hardcoded
MODEL = "claude-sonnet-5-5"
```

## Concepts

### 1.1 Anatomy of a Messages API request

All interaction with Claude goes through one endpoint, `POST /v1/messages`. Tools and structured output are *parameters on this endpoint*, not separate APIs. The response `content` is a **list of typed blocks** (`text`, `thinking`, `tool_use`, ...), not a string.

```python
response = client.messages.create(
    model=MODEL,             # required: which model answers
    max_tokens=16000,        # required: output ceiling, thinking included
    system="You are a concise assistant for a cloud architecture team.",
    messages=[               # required: the conversation so far
        {"role": "user",
         "content": "In two sentences, what is an API gateway?"},
    ],
)
print(response.stop_reason)   # why generation stopped (see 1.3)
for block in response.content:
    if block.type == "text":
        print(block.text)
```

| Field | Required | What it does |
|---|---|---|
| `model` | yes | Model ID. Drives quality, latency, price and limits. Pin it in config, not in code. |
| `max_tokens` | yes | A ceiling, not a target. On current models **thinking tokens count against it**, so values that are too low truncate answers. |
| `messages` | yes | Ordered `user` / `assistant` turns. Must contain the **full** history you want the model to see. |
| `system` | no | Operator instructions: role, rules, output format |
| `tools`, `tool_choice` | no | Tool definitions ([Chapter 2](../02-tool-use/README.md)) |
| `stop_sequences` | no | Custom strings that end generation; produces `stop_reason: "stop_sequence"` |
| `output_config` | no | `effort` ([1.7](#17-model-selection-basics)) and `format` for structured outputs ([Chapter 6](../06-prompt-engineering/README.md)) |
| `thinking` | no | Adaptive thinking runs by default on Sonnet 5.5, Opus 5.5 and Fable 5.1. `{"type": "disabled"}` and `budget_tokens` return 400 on all three, so lower `effort` instead. On Sonnet 5.5, `{"type": "between_tools"}` turns off up-front thinking (only at effort `low`, `medium` or `high`). Haiku 5.5 is adaptive by default too, but accepts `{"type": "disabled"}` at effort `high` or below. Legacy Haiku 4.5 still uses `{"type": "enabled", "budget_tokens": N}`. |
| `stream` | no | Server-sent events instead of one JSON body. Use it for long outputs or a large `max_tokens` to avoid HTTP timeouts. |

> **Exam trap:** `response.content[0].text` is a bug. With thinking on by default, the first block can be a `thinking` block, which has no `.text`. Always filter by `block.type`.

**Errors are not stop reasons.** A failed request returns an HTTP error (`400`, `401`, `429`, `500`, `529`). A successful one returns 200 with a `stop_reason`. The Python SDK retries connection errors, 408, 409, 429 and 5xx twice by default. Catch typed exceptions such as `anthropic.RateLimitError`; do not string-match messages.

### 1.2 Message roles, alternation and stateless conversations

`messages` alternates `user` and `assistant` turns and starts with `user`. Two `user` messages in a row are merged into one turn. There is no `"tool"` role: a tool result is a `tool_result` block inside a `user` message, linked by `tool_use_id`. `"content": "Hi"` is shorthand for `[{"type": "text", "text": "Hi"}]`.

**The API is stateless by default.** Claude keeps no memory between calls, and a request has no session ID. To continue a conversation you resend **every** earlier turn, so input tokens, cost and latency grow with each turn. (The Message threads beta can hold a conversation for a few minutes so later requests send only new messages, but it is best-effort: your app still keeps the full history and replays it when the thread expires.) If the bot forgets what the user said, check what your app sends in `messages`.

```python
SYSTEM = "You are a friendly travel assistant. Keep answers under 80 words."
history: list[dict] = []

def chat(user_text: str) -> str:
    history.append({"role": "user", "content": user_text})
    resp = client.messages.create(
        model=MODEL, max_tokens=16000, system=SYSTEM, messages=history,
    )
    history.append({"role": "assistant", "content": resp.content})  # all blocks
    return "".join(b.text for b in resp.content if b.type == "text")

chat("I love hiking and I'm vegetarian.")
chat("Suggest a weekend trip near Almaty.")   # works only because of `history`
```

**Mid-conversation `system` messages (model-gated).** On Opus 5.5, Opus 5, Opus 4.8, Sonnet 5.5, Haiku 5.5 and Fable 5 / 5.1 you can append `{"role": "system", "content": "..."}` inside `messages`, for example for a backend event. This keeps the cached prefix intact. It must follow a `user` turn (or an `assistant` turn ending in a server tool result), must be the last message or be followed directly by an `assistant` turn, cannot be `messages[0]`, and cannot sit between a `tool_use` and its `tool_result`; otherwise you get a 400. Haiku 4.5, Sonnet 5 and older models reject it with a 400. Never put untrusted text in a system message: it gains operator authority.

**Prefill is gone on current models.** On Opus 4.6 / Sonnet 4.6 and every later model, ending `messages` with a partial `assistant` turn (for example `"{"`) returns **400**. Use structured outputs (`output_config.format`) or system-prompt instructions instead. Haiku 4.5 still accepts prefill. Earlier assistant turns, such as few-shot examples, are fine.

### 1.3 `stop_reason`: why the model stopped

Every successful response carries `stop_reason`. It is the **only reliable control signal**. Never parse the model's prose ("I'm done!") to decide what to do next. An agent loop continues while `stop_reason == "tool_use"` and stops on `end_turn`; a fixed iteration cap is only a safety net. The current API has **seven** values.

| `stop_reason` | Meaning | What your code should do |
|---|---|---|
| `end_turn` | The model finished naturally | Return the answer, end the loop |
| `tool_use` | The model requests client tool calls | Run **every** `tool_use` block, send all `tool_result` blocks in one `user` message, call again |
| `max_tokens` | Output hit `max_tokens` and is **truncated** | Raise `max_tokens`, stream, or continue. Never run a half-written `tool_use`. |
| `stop_sequence` | One of your `stop_sequences` was generated | Read `response.stop_sequence`, apply app logic |
| `pause_turn` | A **server-side** tool loop hit its iteration limit | Send the assistant turn back unchanged and call again |
| `refusal` | The model or a safety classifier declined | Check before reading `content`; `stop_details.category` says why. Explain or fall back. |
| `model_context_window_exceeded` | Generation filled the **context window** | Treat as truncated. Shrink the input; raising `max_tokens` does nothing. |

```python
def handle(resp) -> str | None:
    match resp.stop_reason:
        case "end_turn":
            return "".join(b.text for b in resp.content if b.type == "text")
        case "tool_use":
            raise NotImplementedError("Run tools and loop (Chapter 2)")
        case "pause_turn":
            raise NotImplementedError("Resend history + this turn unchanged")
        case "max_tokens":
            raise RuntimeError("Output truncated: raise max_tokens or stream")
        case "model_context_window_exceeded":
            raise RuntimeError("Context window full: shrink the input")
        case "stop_sequence":
            print("Stopped on", repr(resp.stop_sequence))
            return "".join(b.text for b in resp.content if b.type == "text")
        case "refusal":
            cat = resp.stop_details.category if resp.stop_details else None
            print("Refused, category:", cat)
            return None
        case other:
            raise ValueError(f"Unknown stop_reason: {other}")  # future-proof
```

`stop_details` is set **only** for `refusal` and can still hold `null` fields, so branch on `stop_reason`. On the Claude API and Claude Models on Google Cloud (Anthropic managed) you can opt in to a server-side retry on a fallback model (beta `server-side-fallback-2026-07-01`, `fallbacks="default"`); on other platforms use the SDK's client-side fallback middleware.

### 1.4 The system prompt

The top-level `system` field carries **operator-level** instructions for the whole conversation: role, scope, rules, tone and format. You resend it on every request; keep it stable so prompt caching works. The task and per-request data go in the `user` turn. Keep standing rules out of the user turns: user content carries less authority than `system`, and a rule stated once early in the chat is easy to lose.

```python
SYSTEM = """You are the support assistant for Acme Cloud.
<scope>Billing, plans and invoices only.</scope>
<style>Friendly, direct, max 120 words, no marketing language.</style>
<rules>
- Look up the customer only when the question is about their specific
  account or invoice.
- Never promise refunds; explain the refund policy and offer escalation.
</rules>"""
```

**Unintended tool associations.** The system prompt also shapes which tools the model reaches for. In a shop assistant, *"Check stock before every answer"* leads to a `check_stock` call when the user only asks about delivery times or returns. Scope rules to the situation: "before you promise a specific item or quantity, check stock". If a tool is over-used although its description is clear, check the system-prompt wording first.

**Instruction drift.** In long chats, behavior can slide toward the model's own earlier replies. Use concrete examples instead of long abstract rules, tag critical constraints clearly, re-inject short reminders (a mid-conversation `system` message where supported), and validate outputs as a last resort.

### 1.5 The context window

The context window is the model's working memory for **one request**. The system prompt, tool definitions, every message (tool results, images, documents) and this turn's output, **including thinking**, all count. On Opus 4.5+, Sonnet 4.6+ and Fable 5 / 5.1, thinking blocks from earlier turns are kept and count as input.

Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5 have a 1M-token window and 128K max output (sync API); legacy Haiku 4.5 has 200K and 64K. On Claude 4.5 and newer, a request whose input + `max_tokens` exceeds the window is accepted and stops with `model_context_window_exceeded` when the window is actually full; if the input alone is over the limit, you get `400 "prompt is too long"`. A bigger window does not mean better answers: as context grows, recall degrades (*context rot*). "Switch to a bigger context window" is usually an exam distractor. Curate what goes in instead:

1. **Trim what you append.** Tool results are resent on every later turn. Keep only the fields the task needs before you add a result to the history.
2. **Protect exact values.** Summaries and compaction round numbers and dates. Keep IDs, amounts and deadlines in a structured **"case facts"** block that is never summarized, next to a summary of old turns and the recent turns verbatim (hybrid history).
3. **Mind the position.** Recall is weakest for details in the middle of a long input. Put long documents first, the question last, and restate key facts near the end.

Other mitigations: prompt caching (cheaper reuse, but it does **not** free space), server-side compaction ([Chapter 11](../11-context-management/README.md)), subagents ([Chapter 3](../03-agent-sdk/README.md)) and retrieval.

#### Sampling and non-determinism

The model computes a probability for every possible next token, **samples** one, appends it and repeats ([00 §2.9](../../00-prerequisites/README.md#29-next-token-generation)). Sampling parameters reshape that distribution:

| Parameter | What it does | On Sonnet 5.5, Opus 5.5 and Fable 5.1 |
|---|---|---|
| `temperature` (0.0–1.0, default 1.0) | Low = more predictable, high = more varied | Not supported: non-default values return 400 |
| `top_p` | Keeps the smallest set of likely tokens summing to `p` | Not supported: the default is 0.99; any other value (including 1), or `top_p` sent together with `temperature`, returns 400 |
| `top_k` | Keeps only the `k` most likely tokens | Not supported: non-default values return 400 |

The same rules apply to Haiku 5.5. Haiku 4.5 and models 4.6 and older still accept them, but only on API version `2023-06-01`, which this repo's SDK 1.x sends. SDK 1.x has no keyword arguments for them, so pass them via `extra_body={"temperature": 0.2}`. On API version `2026-10-21` (SDK 2.x), any of the three returns 400 on every model. Steer output with the prompt, `effort` and structured outputs.

**Identical requests return different answers**, because tokens are sampled and adaptive thinking varies. Even `temperature` of `0.0` was never fully deterministic. For tests and evals:

- Test properties, not strings (it parses, matches the schema, has the right label). Structured outputs make the shape deterministic.
- Run 3–5 samples per example and report a **pass rate**.
- Pin model ID, prompt version, `effort` and tools, and log the `request_id`. If the product needs the same answer every time, store and reuse it.

> **Exam trap:** "Set `temperature=0` so tests are deterministic" is wrong twice: current models reject it, and it never guaranteed identical output.

### 1.6 Tokens: counting before, measuring after

Tokens are the unit for limits, rate limits and billing. Before sending, `messages.count_tokens` takes the same inputs as `messages.create` and returns an estimate; it is **free** (with its own rate limit). It rejects server tools, the MCP connector and `url`/`file` image or document sources, so send those as base64 or read `usage` afterwards. After sending, read `response.usage`.

```python
count = client.messages.count_tokens(
    model=MODEL,               # counts are model-specific
    system=SYSTEM,
    messages=history + [
        {"role": "user", "content": open("contract.txt").read()},
    ],
)
print(count.input_tokens)

u = response.usage
PRICE = {"claude-sonnet-5-5": (2.00, 10.00)}   # USD per 1M tokens (in, out)
inp, out = PRICE[MODEL]
# Uncached input + output only; cache writes/reads are priced differently
cost = u.input_tokens / 1e6 * inp + u.output_tokens / 1e6 * out
print(f"${cost:.5f}")
```

Don't use `tiktoken` or "characters ÷ 4" for Claude. Claude 4.7 and later use a newer tokenizer: about 30% more tokens for the same text than earlier models such as Haiku 4.5, so recount when you change model generation. Thinking tokens are billed as **output** and are part of `max_tokens`. A 50-turn chat re-bills earlier turns as input on every call.

### 1.7 Model selection basics

| Model | API ID | Best for | Input / Output per 1M | Context |
|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | Hardest reasoning, long-horizon agentic work | $10 / $50 | 1M |
| Claude Opus 5.5 | `claude-opus-5-5` | Long-running agentic coding and knowledge work; suggested starting point | $4 / $20 | 1M |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | Balance of speed and intelligence for everyday production | $2 / $10 | 1M |
| Claude Haiku 5.5 | `claude-haiku-5-5` | High-volume, latency-sensitive tasks: classification, extraction, routing | $0.10 / $0.50 (prompts up to 100K tokens; $0.50 / $2.50 above) | 1M |

Claude Haiku 4.5 (`claude-haiku-4-5-20251001`, $1 / $5, 200K) is now a legacy model.

Three levers interact:

1. **Model tier:** the capability ceiling and the price. Batch requests are 50% off ([Chapter 7](../07-message-batches/README.md)).
2. **Effort** (`output_config={"effort": "low" | "medium" | "high" | "xhigh" | "max"}`): how much the model thinks and spends. Defaults: Fable 5.1 `high`, Sonnet 5.5 `high`, Opus 5.5 and Haiku 5.5 `medium`. Legacy Haiku 4.5 does not support effort. A stronger model at lower effort can beat a weaker model at high effort, so measure both.
3. **Architecture:** a cheap model for routing, a stronger one for synthesis.

```python
resp = client.messages.create(
    model=MODEL,
    max_tokens=2000,
    output_config={"effort": "low"},   # cheap and fast for a simple label
    system="Classify the ticket as billing, technical or other. "
           "Reply with one word.",
    messages=[{"role": "user",
               "content": "My invoice shows two charges for September."}],
)
```

Choose with evidence: build an eval set of 20–100 real examples, start from Sonnet 5.5 or Opus 5.5, step down (lower effort, then a cheaper model) while it still passes, and compare **cost per completed task**. Check lifecycle too: the current models are committed until at least September 2027 (Haiku 5.5: October 2027), while legacy Haiku 4.5 was committed only until October 15, 2026, so it can now be deprecated at any time; watch the [deprecations page](https://platform.claude.com/docs/en/about-claude/model-deprecations). Read limits at runtime with `client.models.retrieve(MODEL)` (`max_input_tokens`, `max_tokens`) instead of hardcoding them.

> **Exam trap:** "Use the biggest model to be safe" and "pick the largest context window" are wrong. Measure, then choose the cheapest configuration that meets the bar.

### 1.8 Access paths: SDKs, raw REST, async clients and cloud platforms

**SDK vs raw REST.** The SDKs (Python, TypeScript, Java, Go, C#, PHP, Ruby) wrap one `POST https://api.anthropic.com/v1/messages`; the JSON body is exactly your keyword arguments. The Python SDK 1.x this repo installs sends `x-api-key`, `anthropic-version: 2023-06-01` and `content-type: application/json`. The current API version is `2026-10-21`: SDK 2.x sends it, passes the key as `Authorization: Bearer <key>`, and the sampling parameters are removed. The SDK also finds credentials (`ANTHROPIC_API_KEY`, then `ANTHROPIC_AUTH_TOKEN`, then a login profile), retries with backoff, raises typed exceptions and offers helpers such as `messages.stream()` with `get_final_message()`. With raw HTTP you build all of that yourself. Prefer the SDK; use `base_url=` to route through a gateway.

**Sync vs async.** `anthropic.AsyncAnthropic()` has the same methods, but you `await` them. Use it to keep many requests in flight, with a semaphore to stay under rate limits. Async does not make one request faster or cheaper.

```python
import asyncio

aclient = anthropic.AsyncAnthropic()
limit = asyncio.Semaphore(8)                  # at most 8 requests in flight

async def summarize(doc: str) -> str:
    async with limit:
        resp = await aclient.messages.create(
            model=MODEL, max_tokens=2000,
            messages=[{"role": "user",
                       "content": f"Summarize in one sentence:\n{doc}"}],
        )
    return "".join(b.text for b in resp.content if b.type == "text")

docs = ["First incident report ...", "Second incident report ..."]
# In a notebook; use asyncio.run(...) in a script
summaries = await asyncio.gather(*(summarize(d) for d in docs))
```

**Cloud platforms.** Each has its own client class; after that you call `client.messages.create(...)` as before.

| Platform | Python client | Sonnet 5.5 model ID | Auth |
|---|---|---|---|
| Claude API | `Anthropic()` | `claude-sonnet-5-5` | Anthropic API key |
| Claude Platform on AWS (Anthropic-operated) | `AnthropicAWS()` | `claude-sonnet-5-5` | AWS IAM, AWS Marketplace billing |
| Amazon Bedrock (AWS-operated) | `AnthropicBedrockMantle(aws_region=...)` | `anthropic.claude-sonnet-5-5` | AWS IAM or Bedrock bearer token |
| Google Cloud, Anthropic managed | `AnthropicGoogleCloud()` (SDK client in beta) | `claude-sonnet-5-5` | Google Cloud credentials only; the Claude API run by Anthropic |
| Google Cloud, Google managed (Vertex AI) | `AnthropicVertex(project_id=..., region="global")` | `claude-sonnet-5-5` (dated: `claude-haiku-4-5@20251001`) | Application Default Credentials; the model goes in the URL (`.../models/claude-sonnet-5-5:rawPredict`) and the body carries `"anthropic_version": "vertex-2023-10-16"` |
| Microsoft Foundry | `AnthropicFoundry(api_key=..., resource=...)` | Your deployment name | Azure API key or Entra ID |

Feature parity differs (as of November 2026):

| Feature | Claude API | Bedrock | Google Cloud (Google managed) | Foundry |
|---|---|---|---|---|
| Messages, caching, thinking, effort, token counting, structured outputs | ✓ | ✓ | ✓ | ✓ |
| URL image/document sources, Files API | ✓ | ✗ | ✗ | ✓ (no Files API on Azure-hosted deployments) |
| Message Batches API, Models API | ✓ | ✗ | ✗ | ✗ |
| Server-side `fallbacks` (beta) | ✓ | ✗ | ✗ | ✗ |

Keep a per-platform model map and limits in configuration. Claude Platform on AWS and Google Cloud (Anthropic managed) are the Claude API run by Anthropic, so they follow the Claude API column (with a few documented exceptions); Bedrock and Vertex AI are run by the cloud provider with their own feature subsets. **Exam trap:** "Move to Bedrock and keep the code unchanged" is wrong: client class, model ID, credentials and features change. "Rewrite for the provider's own API" is also wrong: the body is the same Messages API.

## Lesson code

Video-lesson code: [../../presentations/01-api-fundamentals/code/](../../presentations/01-api-fundamentals/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`00_session_demo.ipynb`](00_session_demo.ipynb) | Walk through one call, typed replies, stop reasons, history, tokens, cost, effort, non-determinism, streaming and async |
| [`01_practice.ipynb`](01_practice.ipynb) | One section per concept 1.1–1.8, then build `ChatSession`, a chat helper that handles every `stop_reason` and reports cost |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: 12-question quiz, 7 auto-checked coding exercises, an architecture scenario and a scorecard |

## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| The bot forgets facts from earlier turns | Resend full history (or a curated version) every call | Bigger context window or a "session" feature | The API is stateless |
| Should an agent loop continue? | `tool_use` → continue, `end_turn` → stop | Parsing text or fixed iteration counts | `stop_reason` is the reliable signal |
| Cut off with `max_tokens` | Raise `max_tokens` / stream / continue | Shrinking the prompt | Only the output budget ran out |
| Cut off with `model_context_window_exceeded` | Trim, summarize, compact or split the input | Raising `max_tokens` | The whole window is full |
| Persona, tone and rules for every turn | Top-level `system` prompt | First user message | Operator authority, caches well |
| Token count before a big request | `messages.count_tokens` with the target model | `tiktoken` or chars/4 | Model-specific tokenizer; free |
| High-volume simple classification | Smallest model / lowest effort that passes your eval | The largest model | Cost per completed task |
| Guaranteed JSON shape on current models | Structured outputs (`output_config.format`) | Assistant prefill | Prefill returns 400 on 4.6+ models |
| Evals vary on identical inputs | Several runs, property checks, pass rates | `temperature=0` | Variation is by design; non-default `temperature` is rejected |
| Data, IAM and billing must stay in a cloud | The platform's client class + a per-platform model map | First-party client with copied IDs | IDs, auth and features differ |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- Reading `response.content[0].text` blindly. Filter blocks by `type`.
- Appending only the reply text to history. Append `resp.content` so `tool_use` / `thinking` blocks survive.
- Ignoring `stop_reason`, or running tools from a truncated `max_tokens` turn.
- Lowballing `max_tokens`: with adaptive thinking, 512 tokens can go entirely to thinking. Use around 16K non-streaming.
- Absolute, keyword-driven system-prompt rules ("ALWAYS call X"). They cause over-triggering.
- Copying old snippets: prefill, `temperature`, `budget_tokens` and inline `system` messages behave differently across model generations.

## Self-check

**Q1.** After each reply, your app stores `{"role": "assistant", "content": text_of(resp)}` in the history. Plain chat works. The first time the model calls a tool, the follow-up request that carries the `tool_result` fails with HTTP 400. What is the fix?

- A) Send the tool output in a separate message with `role: "tool"`
- B) Append the assistant's full `resp.content` list (with its `tool_use` and `thinking` blocks), not only its text
- C) Put a `session_id` in `metadata` so the API can find the earlier tool call
- D) Raise `max_tokens` so the tool call fits in the reply

<details><summary>Answer</summary>

**B.** Every `tool_result` must point, by `tool_use_id`, to a `tool_use` block in the assistant turn just before it. Storing only the text throws that block away (and the thinking blocks with it), so the API rejects the request. A: there is no `tool` role; results go in a `user` turn. C: the API does not look up earlier requests; it reads only what you send. D: truncation would show up as `stop_reason: "max_tokens"`, not as a 400 on the next request.
</details>

**Q2.** Your agent loop runs tools whenever a reply contains a `tool_use` block, and otherwise returns the reply text. In the logs, a few tool calls arrive with cut-off arguments, and a few answers end mid-sentence. All of those responses have `stop_reason: "max_tokens"`. What change fixes the loop?

- A) Wrap tool execution in `try/except` and send any parse error back as a `tool_result`
- B) Branch on `stop_reason` first: run tools only on `tool_use`, return only on `end_turn`, and on `max_tokens` never run the tool call; raise `max_tokens` (or stream) and retry
- C) Lower `effort` so the model writes shorter tool arguments
- D) Add `"}"` to `stop_sequences` so the tool JSON always closes

<details><summary>Answer</summary>

**B.** The presence of a block is not a control signal; `stop_reason` is. A `max_tokens` turn is truncated, so its last block may be half-written. A treats the symptom, and a cut-off call that still parses could run with the wrong arguments. C may make truncation rarer but leaves the loop wrong. D would end generation at the first `}`, with `stop_reason: "stop_sequence"`, and break nested JSON.
</details>

**Q3.** A pipeline streams a 950K-token set of filings to Sonnet 5.5 with `max_tokens=64000` and asks for a summary. The response ends mid-sentence with `stop_reason: "model_context_window_exceeded"`. What should you do?

- A) Increase `max_tokens` to 128000
- B) Retry the same request with a longer HTTP timeout
- C) Reduce the input (split the filings into chunks, summarize each, then synthesize) so input plus output fits in the window
- D) Lower the effort level so thinking uses fewer tokens, and resend unchanged

<details><summary>Answer</summary>

**C.** The whole context window, not the output budget, is exhausted. A larger `max_tokens` (A) cannot help, and a longer timeout (B) changes transport, not capacity. (Streaming is already required here: the Python SDK refuses non-streaming requests whose `max_tokens` is large enough to risk a 10-minute HTTP timeout.) Lower effort (D) might squeeze one answer through, but it leaves the design fragile and lowers summary quality. The input needs to shrink.
</details>

**Q4.** Your regression suite runs each of 40 extraction prompts once against Sonnet 5.5 and compares the output to a stored "golden" string. After a harmless prompt edit, 6 tests fail; rerunning the unchanged suite makes 4 different tests fail. A teammate proposes adding `temperature=0` to every request. What should you do?

- A) Add `temperature=0`, because it makes the model deterministic
- B) Switch to Haiku 4.5, which accepts `temperature=0`, so the goldens stay stable
- C) Assert on properties instead of exact strings (schema-valid, required fields correct), run each prompt several times, and track the pass rate per prompt and overall
- D) Increase `max_tokens`, because truncation is causing the differences

<details><summary>Answer</summary>

**C.** Sampling and adaptive thinking make identical requests produce different text, so exact-string goldens are flaky by design. Property checks plus several runs per example give a stable pass rate you can compare across prompt versions. A returns 400 on Sonnet 5.5 and never guaranteed identical output anyway. B changes the model to fit a broken test design, and Haiku is not fully deterministic at `temperature=0` either. D has no evidence behind it: truncation would show up as `stop_reason: "max_tokens"`.
</details>

## Official documentation

- [Messages API reference](https://platform.claude.com/docs/en/api/messages)
- [Stop reasons and fallback](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)
- [Models overview](https://platform.claude.com/docs/en/models/overview)
- [Features overview (platform availability)](https://platform.claude.com/docs/en/build-with-claude/overview)

**Source / credit:** the syllabus order follows the community study guide by paullarionov, [*Claude Certified Architect — Foundations: Study Guide*](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md), checked against the current Anthropic docs as of October 2026.

---

[← Claude path overview](../README.md) | [↑ Root README](../../README.md) | [Chapter 2 — Tool Use →](../02-tool-use/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
