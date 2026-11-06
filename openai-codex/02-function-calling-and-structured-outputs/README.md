# Chapter 2 — Function Calling and Structured Outputs

> **Claude counterpart:** [Chapter 2 — Tools and `tool_use`](../../anthropic-claude/02-tool-use/README.md) (and the structured-output parts of [Chapter 6](../../anthropic-claude/06-prompt-engineering/README.md)) · **Academy course(s):** Design and Build Agentic Systems (API pathway) · **Est. time:** 5–7 hours (reading + notebooks) · **Status:** [ ] not started

Function calling lets a model act on your systems (CRMs, order databases, payment APIs). Structured Outputs lets it return data your code can trust. Both use the same engine (constrained decoding against a JSON Schema). The architect question is simple: the API guarantees that arguments and outputs match a schema, but it can't guarantee that a refund is allowed or a total adds up. Your code adds that.

## What you'll learn

- The Responses API round trip: `function_call` item → your code runs it → `function_call_output` item, matched by `call_id`
- When to write a function tool and when to use a built-in tool
- The flat Responses tool shape, and strict-mode rules (every field required, optional means nullable)
- `tool_choice` (including `allowed_tools`), `parallel_tool_calls`, and a bounded loop with errors as data
- Typed output with `text.format` and `responses.parse()`, plus refusal and truncation handling
- Syntax guarantees (the schema) vs semantic validation (your code)

## Prerequisites

[00-prerequisites](../../00-prerequisites/README.md) and [Chapter 1 — Responses API fundamentals](../01-responses-api-fundamentals/README.md) (output items, `status` / `incomplete_details`, `previous_response_id`). Optional: [Claude Chapter 2 — Tools and `tool_use`](../../anthropic-claude/02-tool-use/README.md). Snippets assume `client = OpenAI()` and `MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")`, as in the notebooks. Names such as `SUPPORT_TOOLS` and `SUPPORT_INSTRUCTIONS` come from `01_practice.ipynb`. The snippets are short versions of the notebook helpers: the notebook versions take `client` as an argument and return more detail, and the notebook's `extract_with_retry` uses `create()` + `read_structured()` where 2.8 shows the `parse()` variant.

## Concepts

### 2.1 The function-calling round trip

The model never runs your code. It returns a **`function_call` output item** (a name plus JSON arguments). Your application decides whether to run it, runs it, and sends the result back as a **`function_call_output` input item**. The two are linked by `call_id`.

These details trip people up:

- `arguments` is a **JSON-encoded string**. Call `json.loads(item.arguments)` first.
- There are **two IDs**: `id` (`fc_...`, the item) and `call_id` (`call_...`, the link). Return results with `call_id`.
- Reasoning models return **reasoning items** with the calls, and they must be passed back. The simple way is to append the whole `response.output` to your input list.
- Chat Completions uses `tool_calls` and `{"role": "tool"}` messages. In Responses, calls and outputs are separate **items**. Mixing the two shapes is the most common migration bug.

```python
input_list = [{"role": "user", "content": "Where is order A-1001?"}]
response = client.responses.create(model=MODEL, tools=tools, input=input_list)

input_list += response.output          # keep EVERY output item
for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)
        result = call_function(item.name, args)  # your dispatcher
        input_list.append({
            "type": "function_call_output",
            "call_id": item.call_id,   # not item.id
            "output": json.dumps(result),  # usually a string
        })

response = client.responses.create(model=MODEL, tools=tools, input=input_list)
print(response.output_text)
```

> **Exam trap:** "The model called the refund API" is never literally true. The model *requested* a call, and your code made it. Approval gates, permission checks and rate limits belong in your code.

#### Function tools vs built-in tools

Function tools share the `tools` array with **built-in** tools (web search, file search, remote MCP, shell, computer use and more). What matters for your loop is **who executes the call**:

| Kind | Examples (`type`) | Who executes | What your loop does |
|---|---|---|---|
| **Function tool** | `function`, `custom` | Your application | Run it and return an output with the same `call_id` |
| **Hosted built-in tool** | `web_search`, `file_search`, `image_generation` | OpenAI | Nothing: the call item and its result come back in the same response |
| **Remote MCP** | `mcp` | A remote MCP server, called by OpenAI | Usually nothing, except approvals |
| **Client-executed built-in** | `computer`, local `shell`, `apply_patch` | Your application, with a fixed schema | Run it in your sandbox and return the matching `*_output` item |

**Rule: use a built-in tool when one exists.** Don't write `search_web()` when `web_search` exists. Write a function when the capability is **yours** (your CRM, your refund API), or when a hosted tool can't meet a requirement. When you mix them, execute **only** `function_call` items. [Chapter 4](../04-built-in-tools-and-mcp/README.md) covers the built-in tools.

### 2.2 Defining function tools: Responses vs Chat Completions shape

A Responses function tool has `type: "function"`, a `name` (letters, digits, `_` and `-`, at most 64 characters), a `description`, a JSON Schema `parameters` object and `strict`. Chat Completions nests the same fields under a `function` key. Responses puts them at the top level.

```python
# Chat Completions (still supported; Responses recommended for new work): nested
chat_tool = {"type": "function",
             "function": {"name": "lookup_order", "description": "...",
                          "strict": True, "parameters": {...}}}

# Responses API: flat
responses_tool = {"type": "function", "name": "lookup_order",
                  "description": "...", "strict": True, "parameters": {...}}
```

> **Gotcha:** `openai.pydantic_function_tool(MyModel)` returns the **Chat Completions** (nested) shape. `client.responses.parse(tools=[...])` converts it, but `client.responses.create(tools=[...])` expects the flat shape. Flatten it first.

OpenAI's best practices: the **description** is the model's main signal for choosing a tool, so say what it does, each parameter's format, and when *not* to use it. Use **enums and object structure** to make invalid states impossible. **Offload work to code**: if your app already knows the `order_id`, inject it. Keep the initial tool set **small** (the docs suggest fewer than 20 functions); definitions are billed as input tokens.

> **Exam trap:** When the agent picks the wrong tool, the first fix is to **rewrite and differentiate the descriptions** (and the `instructions`). A routing classifier or fine-tuning comes later.

### 2.3 Strict mode schema rules

`strict: true` makes arguments reliably follow the schema. OpenAI recommends always enabling it. It has two hard requirements:

1. `additionalProperties` must be `false` on **every** object.
2. **Every** field in `properties` must be listed in `required`. To make a field "optional", keep it required and add `null` to its type:

```python
"parameters": {
    "type": "object",
    "properties": {
        "email":       {"type": ["string", "null"]},
        "customer_id": {"type": ["string", "null"]},
    },
    "required": ["email", "customer_id"],  # both listed, both nullable
    "additionalProperties": False,
}
```

> **Exam trap:** Claude strict tools allow optional parameters. OpenAI strict mode rejects any property missing from `required`. The OpenAI pattern is **required + nullable**.

**If you omit `strict`:** in Responses the API *tries* to normalize your schema to strict mode, and if it can't, it silently falls back to best effort (the tool shows `strict: false`). In Chat Completions, tools are non-strict by default. With `strict: true` and a bad schema, both APIs reject the request. So set `strict: true` explicitly, and a bad schema fails at development time.

**Schema subset.** Supported: `anyOf` inside properties, `$defs` / `$ref`, recursion, `pattern`, `format` (`date-time`, `email`, `uuid` and others), `minimum` / `maximum` / `multipleOf`, `minItems` / `maxItems`. Not supported: `anyOf` at the root (the root must be an object), `allOf`, `not`, `if`/`then`/`else`. Fine-tuned models support fewer keywords. The docs contradict themselves on `minLength` / `maxLength`, so check lengths in code (2.8). With **Pydantic**, the SDK generates a strict schema for you: every field goes into `required`, `Optional[...]` becomes `anyOf [..., null]`, and `additionalProperties: false` is added. A default value does **not** make a field optional.

### 2.4 `tool_choice` and `parallel_tool_calls`

`tool_choice` controls **whether** the model must call a tool and **which** ones it may call.

| Value (Responses API) | Behavior | Typical use |
|---|---|---|
| `"auto"` (default) | Call zero, one or several functions | Assistants and agents |
| `"required"` | Call **one or more**; the model picks | You must get a tool call |
| `{"type": "function", "name": "lookup_order"}` | Call **exactly this** function | Forcing a pipeline step |
| `{"type": "allowed_tools", "mode": "auto" \| "required", "tools": [...]}` | Restrict this turn to a **subset** of `tools` | Per-turn permissions |
| `"none"` | Don't call tools | A pure text turn |

`allowed_tools` exists for prompt caching. Tool definitions are part of the prompt prefix. Changing the `tools` array changes the prefix; changing only `tool_choice` doesn't. Use `mode: "required"` only when the turn's input always fits a tool (for example, the email is already known). A conversational agent that may need to ask the user first should use `mode: "auto"`, as the notebook does.

```python
# Not verified yet, email already given: read-only tools, at least one call
response = client.responses.create(
    model=MODEL, input=input_list,
    tools=SUPPORT_TOOLS,  # the three tool dicts: a stable list
    tool_choice={"type": "allowed_tools", "mode": "required",
                 "tools": [{"type": "function", "name": "get_customer"},
                           {"type": "function", "name": "lookup_order"}]},
)
```

**Parallel calls.** The model may return several `function_call` items in one turn. Setting the **top-level** `parallel_tool_calls: false` ensures **zero or one** call per turn. (Claude puts `disable_parallel_tool_use` inside `tool_choice`.)

> **Exam trap:** `auto` does **not** guarantee a call. If the process requires a tool to run, use `required`, a forced function, or code that checks for the call. A sentence in the prompt is not a guarantee.

### 2.5 The client-side loop, and errors in tool outputs

There is **no `stop_reason`** in the Responses API. The loop reads the output items and `status`. `function_call` items mean: run them, append one output per `call_id`, call again. No calls means the model is done. `status == "incomplete"` means don't execute half-written calls. A `refusal` part means stop and never act on that turn (2.7), even though the turn is `completed`. Never end the loop by matching text such as "done"; `max_turns` is only a safety net.

```python
def run_agent(user_text: str, tools: list[dict], handlers: dict,
              max_turns: int = 8) -> str:
    input_list: list = [{"role": "user", "content": user_text}]
    for _ in range(max_turns):                 # your own bound
        response = client.responses.create(
            model=MODEL, instructions=SUPPORT_INSTRUCTIONS,
            tools=tools, input=input_list,
        )
        if response.status != "completed":
            raise RuntimeError(f"Response {response.status}")
        refusal = find_refusal(response)       # a refusal is "completed"
        if refusal is not None:
            return f"[refused] {refusal}"
        input_list += response.output          # replay ALL items
        calls = [i for i in response.output if i.type == "function_call"]
        if not calls:                          # no calls -> final answer
            return response.output_text
        for call in calls:                     # one output per call_id
            input_list.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": execute_tool(call, handlers),  # always a string
            })
    raise RuntimeError("Agent exceeded max_turns")
```

**Errors are data.** `function_call_output` has **no `is_error` flag** (unlike Claude's `tool_result`). The output is usually a string in a format you design (it can also be a list of image or file content items). A good convention is JSON that says what went wrong, whether a retry makes sense, and what to do next, for example `{"error": "timeout", "retryable": true, "message": "..."}`. In the notebook, `execute_tool` never raises: unknown tools, bad JSON, timeouts, permission and validation errors all become outputs. `find_refusal` (also in the notebook) returns the text of a `refusal` content part, or `None`.

Rules for the loop:

- **One `function_call_output` for every `call_id`**, including failed calls. With parallel calls, append **all** outputs before the next request.
- **Server-side state is an option:** send `previous_response_id` plus only the new outputs. Resend `instructions` and `tools` every time.
- **Bound the loop yourself.** `max_tool_calls` limits **built-in** tools only, not your functions.
- **Retry transient failures inside the tool.** Send validation errors straight back.

**Async function tools** (`"async": true`) let the model keep working while you return the result later on the same `call_id`. The latest-model guide introduces it with GPT-6; check that your model supports it.

### 2.6 Structured Outputs: `text.format` and `responses.parse()`

Structured Outputs makes the model's **final answer** match your JSON Schema. The docs' rule: to connect the model to your tools or data, use **function calling**; to structure its response, use **`text.format`** with `json_schema`.

The raw form is `text={"format": {"type": "json_schema", "name": ..., "strict": True, "schema": ...}}`, then `json.loads(response.output_text)`. The SDK form with Pydantic gives one source of truth for schema and validation:

```python
from typing import Literal, Optional
from pydantic import BaseModel

class TicketClassification(BaseModel):
    category: Literal["billing", "shipping", "account", "unclear", "other"]
    category_detail: Optional[str]   # required key, value may be None
    order_id: Optional[str]

response = client.responses.parse(
    model=MODEL,
    input="Classify this support ticket: "
          "'I was charged twice for order A-1001.'",
    text_format=TicketClassification,
)
ticket = response.output_parsed      # an instance, or None (refusal etc.)
```

**JSON mode** (`"type": "json_object"`) guarantees valid JSON only, with **no** schema adherence. `json_schema` with `strict: true` guarantees both, and `parse()` adds a parsed object in `output_parsed`.

> **Gotcha:** Chat Completions uses `response_format`. Responses uses `text.format`, with `name` and `schema` directly inside `format`. Sending `response_format` to Responses is a common migration error.

Schema design: use **required + nullable** for information that may be absent ("null if the ticket has no order ID"); add `"other"` and `"unclear"` to enums; write field descriptions as prompts (units, formats). The model "will always try to adhere to the provided schema", which can cause hallucinations on unrelated input, so give it a way out.

### 2.7 Refusals and incomplete responses

A schema can't stop a **safety refusal** or a **cut-off** response. Check both before you trust parsed data.

- **Refusal:** the message has a content part of type `refusal` instead of `output_text`. `status` is still `"completed"`, so checking `status` alone is not enough.
- **Incomplete:** on `max_output_tokens` or the content filter, `status` is `"incomplete"` and `incomplete_details.reason` says why. The JSON may be truncated.

```python
def read_structured(response) -> dict:
    if response.status != "completed":           # never parse a partial
        d = response.incomplete_details
        reason = d.reason if d else None
        raise RuntimeError(f"Response {response.status} ({reason})")
    for item in response.output:
        if item.type != "message" or item.phase not in (None, "final_answer"):
            continue                    # skip reasoning, calls, preambles
        for part in item.content:
            if part.type == "refusal":
                return {"refused": True, "reason": part.refusal}
            if part.type == "output_text":
                return {"refused": False, "data": json.loads(part.text)}
    raise RuntimeError("No final-answer message in output")
```

Only `final_answer` (or phase-less) message text is your result. `response.output_text` joins the text of **every** message, preambles included. With `parse()`, `output_parsed` is `None` on a refusal. A truncated payload makes `parse()` itself raise `pydantic.ValidationError`, so catch it (as in 2.8).

> **Exam trap:** "We use Structured Outputs, so `json.loads(response.output_text)` can never fail" is wrong. Refusals and truncated responses are the documented exceptions.

### 2.8 Syntax vs semantic validation

| Error type | Examples | What catches it |
|---|---|---|
| **Syntax** | Invalid JSON, wrong type, missing key, value outside the enum | Strict functions and `text.format` **eliminate** these (except 2.7 cases) |
| **Semantic** | Line items don't add up, an invented order ID, a refund larger than the order | **Your code**: validators, cross-field checks, lookups, retry with feedback, human review |

The docs say it directly: "Structured Outputs can still contain mistakes." A schema guarantees **shape**, never **truth**. In the notebook, `semantic_errors()` sums line items in integer cents and compares them with the stated total (`InvoiceExtraction` has `invoice_number`, `line_items` and a nullable `stated_total_usd`). On a mismatch, retry with the specific error:

```python
from pydantic import ValidationError

def extract_with_retry(document: str, max_retries: int = 2):
    input_list = [{"role": "user",
                   "content": f"Extract the invoice data:\n\n{document}"}]
    for _ in range(max_retries + 1):
        try:
            response = client.responses.parse(
                model=MODEL, input=input_list,
                text_format=InvoiceExtraction)
        except ValidationError as exc:     # truncated JSON raises here
            raise ValueError("Unparseable; route to human review") from exc
        invoice = response.output_parsed
        if response.status != "completed" or invoice is None:
            raise ValueError("Incomplete or refused; route to human review")
        if invoice.stated_total_usd is None:  # a retry can't fix that
            raise ValueError("No total printed; route to human review")
        errors = semantic_errors(invoice)
        if not errors:
            return invoice
        # the previous attempt as plain text: replaying parse() items would also send their `parsed` field
        input_list.append({"role": "assistant", "content": response.output_text})
        input_list.append({"role": "user", "content":
            "Validation failed:\n- " + "\n- ".join(errors)
            + "\nCorrect only the affected fields. Don't invent values."})
    raise ValueError(f"Still inconsistent; human review: {errors}")
```

- **Retries help** with values in the wrong field, arithmetic and format slips. They **don't help** when the information isn't in the source: return `null` or escalate.
- **Extract the stated total and compute the sum in code.** Don't ask the model to "make the totals match".
- **The same applies to tool arguments.** A strict `process_refund` call can still name another customer's order or exceed the refundable amount. Check ownership, status and limits in the handler, and make it idempotent.

## Lesson code

Code from the video lesson: [../../presentations/02-function-calling/code/](../../presentations/02-function-calling/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run 2.1–2.8 mostly offline on fake `Response` objects, then build a customer-support agent loop with `allowed_tools` phase gating and refund rules in code |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 offline exercises with auto-checks, an airline architecture scenario and a scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>
## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| New integration | Responses API function tools | Chat Completions functions | Recommended for new work; GPT-6 Astra, GPT-6.1 Sol and GPT-6.1 Terra need Responses for tool calling |
| Model picks the wrong tool | Rewrite and differentiate descriptions and `instructions` | Routing classifier, fine-tuning | Descriptions are the selection mechanism |
| You only need JSON back, no action taken | `text.format` / `responses.parse(text_format=...)` | A fake "extraction function" with forced `tool_choice` | Purpose-built for the final answer |
| Arguments must always type-check | `strict: true` (explicitly) | Omitting `strict` | Responses may fall back to non-strict silently |
| A field may be absent | Required + nullable + "null if absent" | Leaving it out of `required` | Strict mode rejects it, and a forced value invites fabrication |
| Different permissions per phase | `tool_choice: allowed_tools` | Rebuilding the `tools` list each turn | Stable prefix for prompt caching; same security effect |
| Must get some tool call | `tool_choice: "required"` | `auto` + prompt wording | `auto` may answer in prose |
| Calls have ordering dependencies or side effects | `parallel_tool_calls: false`, plus preconditions in each handler | Default parallel calls | One call per turn; enforce the order in code |
| Irreversible action (refund) | Code-level preconditions in the handler | Warnings in the description | Probabilistic compliance isn't enough |
| Extraction is well-formed but numbers disagree | Semantic validation + retry with the specific error | "Be careful" prompt, bigger model only | Schemas can't express cross-field rules |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **Returning the output with `item.id` instead of `item.call_id`**, or treating `arguments` as a dict.
- **Appending only the text or only the function calls** to history and dropping reasoning items.
- **Passing Chat Completions-shaped tools** (including `pydantic_function_tool()` output) to `responses.create`, or using `response_format` instead of `text.format`.
- **Leaving optional fields out of `required`** in a strict schema, or assuming that omitting `strict` gives you strict mode.
- **Raising out of the loop when a tool fails**, dropping that call, or returning generic error strings.
- **Parsing without checking `status` and refusals**, or treating strict mode as a correctness guarantee.

## Self-check

**Q1. (Strict schemas)** A strict `get_customer` tool has `properties` `email` and `customer_id`, with `"required": ["email"]` because callers send one or the other. The request is rejected. What is the correct fix?

- A) Remove `strict: true` and validate in code
- B) Add `customer_id` to `required` and make both fields nullable (`["string", "null"]`), describing that one of them may be null
- C) Add `"additionalProperties": true` so the schema is more flexible
- D) Split the tool into `get_customer_by_email` and `get_customer_by_id`

<details><summary>Answer</summary>

**B.** OpenAI strict mode requires every property to be listed in `required` and `additionalProperties: false`. Optional values are expressed as a union with `null`. A gives up the guarantee. C breaks the other strict requirement. D can work, but it doubles the tool surface to avoid a one-line schema fix, so it isn't the correct first fix.
</details>

**Q2. (Agent loop)** A teammate's loop sends results back as `{"type": "function_call_output", "call_id": item.id, "output": ...}` and only appends `function_call` items (not reasoning items) to the history. Responses become erratic or fail. Which pair of fixes is correct?

- A) Use `item.call_id`, and append every item in `response.output` to the input list
- B) Use `item.id`, and append only the final message text
- C) Send each result in its own request, and switch to Chat Completions
- D) Set `parallel_tool_calls: false`, and remove `instructions`

<details><summary>Answer</summary>

**A.** Outputs are matched by `call_id`, not the item `id`. Reasoning items returned with tool calls must be passed back, and the simplest correct approach is to replay the whole `output` array. B repeats both bugs. C and D don't address the cause.
</details>

**Q3. (Structured Outputs)** You call `client.responses.parse(text_format=Invoice)` and then do `response.output_parsed.total`. In production this sometimes raises `AttributeError: 'NoneType' object has no attribute 'total'`, although `response.status == "completed"`. What is the most likely cause, and the fix?

- A) A network error; add retries
- B) A refusal; look for a `refusal` content part in the message and handle it before using `output_parsed`
- C) The schema is too large; split it
- D) `max_output_tokens` was reached; raise it

<details><summary>Answer</summary>

**B.** A refusal comes back with `status: "completed"` and a `refusal` content part, so there is nothing to parse and `output_parsed` is `None`. D would show `status: "incomplete"`. A would raise an exception from the client, not return a response. C would be rejected at request time.
</details>

**Q4. (Validation)** After moving an invoice extractor to `text.format` with a strict schema, JSON errors drop to zero, but 4% of invoices have line items that don't add up to the stated total. What is the right next step?

- A) Nothing; strict mode guarantees correct values
- B) Add `minimum: 0` to every amount field
- C) Compute the sum in code, compare it with the extracted stated total, re-prompt with the specific discrepancy, and send cases that still fail to human review
- D) Switch to JSON mode for more flexibility

<details><summary>Answer</summary>

**C.** This is a semantic error. The schema guarantees shape, and the docs explicitly warn that Structured Outputs can still contain mistakes. B is supported on OpenAI but can't express "sum equals total". D removes the schema guarantee.
</details>

## Official documentation

- [Function calling](https://developers.openai.com/api/docs/guides/function-calling): definitions, `tool_choice`, `allowed_tools`, parallel calls, strict mode, streaming, custom tools
- [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs): `text.format`, `responses.parse`, refusals, supported schemas, JSON mode
- [Using tools](https://developers.openai.com/api/docs/guides/tools): function calling next to the built-in tools, remote MCP and tool search
- [Migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses): function definition and Structured Outputs differences, common migration errors
- [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state): replaying output items vs `previous_response_id`
- [Using GPT-6 (latest model guide)](https://developers.openai.com/api/docs/guides/latest-model): GPT-6 Astra, GPT-6.1 Sol and GPT-6.1 Terra need Responses for tool calling

[← Chapter 1 — Responses API Fundamentals](../01-responses-api-fundamentals/README.md) | [↑ OpenAI path](../README.md) | [Chapter 3 — Agents SDK and Agents API →](../03-agents-sdk-and-agents-api/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
