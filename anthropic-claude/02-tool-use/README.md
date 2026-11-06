# Chapter 2 — Tools and `tool_use`

> **Exam domain(s):** Domain 2 — Tool Design & MCP Integration (**18%**, tasks 2.1 and 2.3; previews 2.2 error responses, taught in Chapters 4 and 10) · Domain 4 — Prompt Engineering & Structured Output (**20%**, task 4.3; previews 4.4 retry with feedback, taught in Chapter 6) · also supports Domain 1 — Agentic Architecture & Orchestration (**27%**, the agent loop) · Claude Certified Developer – Foundations: Tool Implementation (domain 8.1) and tool-use loops
> **Est. time:** 7–9 hours (reading + notebooks) · **Status:** [ ] not started

Tool use is where Claude stops only writing text and starts acting on real systems. Every agent later in this repo is a loop of tool calls. Your job as an architect is to decide where reliability comes from: the model (good descriptions), the API (strict schemas) or your own code (validation, retries, approval gates).

## What you'll learn

- The client-tool round trip: `tool_use` → your code runs the tool → `tool_result` → final answer
- How to write tool descriptions that steer Claude to the right tool, and how to scope toolsets by role
- `tool_choice` modes, and which current models reject forced tool use
- Schema design for extraction, `strict: true`, `output_config.format` and `messages.parse()`
- Syntax errors (the schema prevents them) vs. semantic errors (your code catches them)
- A correct `stop_reason` loop, and how client, Anthropic-schema and server tools differ

## Prerequisites

[00-prerequisites](../../00-prerequisites/README.md) and [Chapter 1 — Claude API fundamentals](../01-claude-api-fundamentals/README.md) (request shape, roles, `stop_reason`, `max_tokens`). Put `ANTHROPIC_API_KEY` in `.env`, never in code. Snippets assume `client = anthropic.Anthropic()` and `MODEL = "claude-sonnet-5-5"`, as in the notebooks.

## Concepts

### 2.1 What is `tool_use`

Tool use (also called *function calling*) lets Claude ask your application to run a function. **The model never executes anything itself.** It writes a request (tool name plus JSON arguments). Your code decides whether to run it, runs it and sends the result back. The round trip: you send `messages` + `tools` → Claude returns `stop_reason: "tool_use"` with a `tool_use {id, name, input}` block → your code runs the tool → you send the full assistant content plus a `tool_result {tool_use_id, content}` → Claude answers with `stop_reason: "end_turn"`.

**Client tools** run in your application (your functions, and Anthropic-schema tools such as `bash`). **Server tools** run on Anthropic's infrastructure (`web_search`, `code_execution`), and their results arrive in the same response. See [2.7](#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide).

> **Exam trap:** "Claude called the refund API" is never literally true. Claude *requested* a call and your code made it. Approval gates, permission checks and rate limits belong in **your** code, not in the prompt.

### 2.2 Tool definition

A tool needs a `name` (matching `^[a-zA-Z0-9_-]{1,128}$`) and an `input_schema` (JSON Schema). The `description` is optional in the API but essential: **it is the main signal Claude uses to choose a tool.** Optional `input_examples` must validate against the schema. Optional `strict: true` guarantees valid arguments (2.4).

```python
get_customer = {
    "name": "get_customer",
    "description": (
        "Identity check for the support flow: call it before lookup_order "
        "or process_refund whenever the customer is not verified yet. "
        "Takes exactly one of email (user@domain.com) or customer_id (an "
        "integer such as 48213). Returns name, email, account status and "
        "the customer's order IDs, but not order details. For an order's "
        "status, items or price, do NOT use it; call lookup_order instead."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "email": {"type": "string",
                      "description": "Customer email, e.g. jane@example.com"},
            "customer_id": {"type": "integer",
                            "description": "Numeric customer ID, e.g. 48213"},
        },
        "required": [],
    },
    "input_examples": [{"email": "jane@example.com"}, {"customer_id": 48213}],
}
```

**What a strong description contains:** (1) what it does and returns, including what it does *not* return; (2) input formats with example values; (3) when to use it vs. similar tools; (4) edge cases and constraints. Aim for at least 3–4 sentences. **Tool-set design rules:**
- **No overlap.** `analyze_content` and `analyze_document`, both described as "analyzes … and extracts key information", get mixed up. Rename and re-scope one (`extract_web_results`: "processes results from web search and URLs").
- **Split vague tools** into narrow contracts: `analyze_document` becomes `extract_data_points`, `summarize_content` and `verify_claim_against_source`. Consolidate instead when tools are variations of one contract (one `github_pr` tool with an `action` parameter).
- **Replace generic tools with constrained ones.** A `load_document` tool that accepts only allowed hosts and file types replaces a generic `fetch_url`. The constraint lives in code, so it holds when the model is wrong.
- **Keep each agent's toolset small and scoped to its role.** An agent with 18 tools selects less reliably than one with 4–5. Agents also misuse tools outside their role: a synthesis agent with web search starts doing its own research. Give each subagent only its role's tools (a `ROLE_TOOLS` map from role to tool names). When a role often needs one simple thing from another role, add one scoped cross-role tool: the synthesizer gets only `verify_fact`, which checks one claim against the gathered sources. Route anything more complex back through the coordinator.
- **Check the system prompt too.** "Whenever the user mentions their *account*, look up the customer first" sends "Which *account* was order ORD-5001 billed to?" to `get_customer`. Rewrite keyword rules as conditions on intent, or remove them.

> **Exam trap:** When the agent picks the wrong tool, the **first** fix is to rewrite or differentiate the descriptions. Classifiers, merged tools or many few-shot examples are heavier and usually wrong as a first step. Targeted few-shot examples (4–6 ambiguous cases, each with the reason) are the right *second* step.

### 2.3 The `tool_choice` parameter

`tool_choice` controls **whether** Claude must call a tool and **which** one. With `any` or `tool`, Claude writes no text before the `tool_use` block. `"disable_parallel_tool_use": true` inside `tool_choice` allows at most one call (`auto`) or exactly one (`any`/`tool`). With manual extended thinking (`thinking: {"type": "enabled", ...}`), `any` and `tool` return an error.

| Value | Behavior | Typical use |
|---|---|---|
| `{"type": "auto"}` | Claude decides: tool call or text. Default with `tools` | Assistants and agents |
| `{"type": "any"}` | Claude **must** call one of the tools; it picks which | Several extraction schemas, document type unknown |
| `{"type": "tool", "name": "..."}` | Claude **must** call this tool | Forcing a pipeline's first step |
| `{"type": "none"}` | No tool calls. Default without `tools` | Keep definitions cached, forbid calls this turn |

> **Note: changed since the guide.** **Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1 reject forced tool use**: `any` and `tool` return **HTTP 400**. Use `auto` + `strict: true` + a prompt instruction and **check in code** that the call happened, or use structured outputs (2.4) when you only need JSON. Claude Haiku 5.5, Claude Haiku 4.5, Claude Opus 5, Claude Sonnet 5, Claude Fable 5 and older models still accept `any` and `tool`, but a forced call skips thinking. The exam still tests the `auto` / `any` / forced semantics.

**Force the first step, then continue in follow-up turns.** Forcing fixes only step 1. On a model that supports it (the practice notebook uses `claude-haiku-4-5`; set `CLAUDE_FORCED_TOOL_MODEL=claude-haiku-5-5` in `.env` if Haiku 4.5 is retired), send `tool_choice={"type": "tool", "name": "extract_metadata"}`. Append the assistant content and the `tool_result`, then call again with `tool_choice={"type": "auto"}` so Claude picks the enrichment tools that fit the metadata. On the default model, the notebook's `require_tool_call()` gets the same result with `auto` + strict tools: it returns the expected tool's input, raises on a different tool, `refusal` or `max_tokens`, and otherwise asks "Please call the X tool now." and retries.

> **Exam trap:** `auto` does **not** guarantee a tool call. The guarantee comes from forced `tool_choice` (on supporting models) or from code that checks for the call.

### 2.4 JSON schemas for structured output

An "extraction tool" whose `input_schema` *is* your output format is the classic way to get structured data. There are three mechanisms:

| Mechanism | How | What it guarantees |
|---|---|---|
| Plain tool `input_schema` | Tool without `strict` | Usually close, **not guaranteed** (`"2"` for `2`, missing field) |
| **Strict tool use** | `"strict": true` on the tool | `input` always validates against the schema |
| **JSON outputs** | `output_config={"format": {"type": "json_schema", "schema": ...}}` or `client.messages.parse(output_format=PydanticModel)` | Valid JSON matching the schema; `parse()` returns a validated object in `.parsed_output` |

> **Note: changed since the guide.** The guarantee now comes from **strict mode** or **structured outputs**, both grammar-constrained. The old `output_format` request parameter is deprecated in favor of `output_config.format`; `messages.parse(output_format=...)` takes a Python type (a Pydantic model is recommended; any type `pydantic.TypeAdapter` accepts works), not a schema dict, so pass a raw JSON schema as `output_config={"format": {...}}`. Final-turn prefill returns a 400 on Claude 4.6 and later, so the old prefill trick for JSON no longer works.

**Schema design principles:**
1. **Required vs. optional.** Require a field only if the source *always* has it. A required field that is missing pushes the model to **invent** a value. **Exam trap:** "make every field required so the output is complete" causes fabrication.
2. **Nullable fields.** Use `"type": ["string", "null"]` (`Optional[str]` in Pydantic). Required + nullable: the key is always there, and `null` means "not in the source".
3. **Enums with `"other"` + a detail field** keep data you didn't anticipate.
4. **An `"unclear"` enum value** beats a confident wrong category and gives a signal for human review.
5. **Field descriptions** are prompts too: units, formats, normalization ("ISO 8601 date").
6. **Normalization rules in the prompt, next to the strict schema.** A schema can't say "write `03/04/26` from a UK supplier as `2026-04-03`". A `NORMALIZATION_RULES` prompt does: dates to ISO 8601; money to integer cents ("1.299,00 EUR" -> 129900); missing values to null, never guess.

```python
classify_ticket = {
    "name": "record_ticket_classification",
    "description": "Record the classification of one support ticket. "
                   "Call exactly once per ticket.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "enum": [
                "bug", "billing", "account", "unclear", "other"]},
            "category_detail": {"type": ["string", "null"]},  # other/unclear
            "severity": {"type": "string",
                         "enum": ["p1", "p2", "p3", "p4"]},
            "customer_email": {"type": ["string", "null"]},
        },
        "required": ["category", "category_detail",
                     "severity", "customer_email"],
        "additionalProperties": False,
    },
}
```

**Flexible extraction.** For attributes you can't list in advance, an open object (`"additionalProperties": true`) works only on a non-strict tool. A key/value list (an array of `{name, value, unit}` objects) works with `strict: true`; rebuild the dict in code.

**Strict-mode limits:** `additionalProperties: false` on every object. No recursive schemas, `minimum` / `maximum` / `multipleOf`, `minLength` / `maxLength`, complex types inside `enum` or external `$ref`. At most 20 strict tools per request, 24 optional parameters and 16 union parameters (`anyOf`, `["string", "null"]`), summed across all strict schemas and the output schema. A new schema adds compile latency; the grammar is cached for 24 hours after its last use. `parse()` strips numeric constraints and validates them client-side; with a raw strict schema, enforce ranges in your code. The same contract works as a Pydantic model with `messages.parse()`. Enum letter-casing is not guaranteed, so the notebook lowercases values with a `BeforeValidator` before the `Literal` check.

### 2.5 Syntax vs. semantic errors

| Error type | Examples | What prevents or catches it |
|---|---|---|
| **Syntax** | Invalid JSON, `"2"` vs `2`, missing key, value outside the enum | `strict: true` or `output_config.format`. Exceptions: `max_tokens` truncation, `refusal`, enum casing. Check `stop_reason` first |
| **Semantic** | Line items don't add up, value in the wrong field, invented ID | **Your code**: business-rule checks, retry with specific feedback, human review |

A schema guarantees **shape**, never **truth**: "we switched to strict schemas, so extraction is now correct" is a classic wrong answer. Below, `InvoiceExtraction` is a Pydantic model with `line_items` (each with `amount_cents`) and `stated_total_cents`; `semantic_errors()` compares the sum of the line amounts with `stated_total_cents`, and the loop sends the specific error back. Retries help with format slips, misplaced values and arithmetic. They do **not** help when the information is not in the source: they only produce more confident fabrication, so return `null` or escalate. Compute totals in code; a mismatch may be a real error in the source, which you flag, not hide.

```python
import pydantic

def extract_with_retry(document: str, max_retries: int = 2):
    messages = [{"role": "user",
                 "content": f"Extract the invoice data:\n\n{document}"}]
    for attempt in range(max_retries + 1):
        try:
            response = client.messages.parse(
                model=MODEL, max_tokens=2048, messages=messages,
                output_format=InvoiceExtraction)
        except pydantic.ValidationError as exc:  # truncated/refused reply
            raise ValueError("Unparseable, route to human review") from exc
        if (response.stop_reason in ("refusal", "max_tokens")
                or response.parsed_output is None):  # no text block
            raise ValueError("No valid extraction, route to human review")
        invoice = response.parsed_output
        errors = semantic_errors(invoice)
        if not errors:
            return invoice
        messages += [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": "Validation failed:\n- "
                + "\n- ".join(errors) + "\nCorrect only the affected fields."
                + " If a value is truly not in the document, use null."},
        ]
    raise ValueError(f"Still inconsistent, route to human review: {errors}")
```

### 2.6 The client-side tool loop and `tool_result` rules *(expanded beyond the guide)*

Every agent is this loop: **call the API → check `stop_reason` → run the tools → append the results → repeat.** The Python SDK's beta **Tool Runner** (`@beta_tool` + `client.beta.messages.tool_runner(...)`) runs it for you; write it by hand once so you know what it automates.

| `stop_reason` | Loop action |
|---|---|
| `tool_use` | Run the client tools, append results, call again |
| `end_turn` | Exit and return the answer |
| `max_tokens` | Don't run a truncated call; retry with a higher `max_tokens` |
| `pause_turn` | Server tool hit its iteration limit; resend the assistant content as-is |
| `refusal` | Stop; never run tools from that turn |

```python
def run_agent(user_text, tools, handlers, max_turns=10):
    messages = [{"role": "user", "content": user_text}]
    for _ in range(max_turns):                  # always bound the loop
        response = client.messages.create(
            model=MODEL, max_tokens=4096, tools=tools, messages=messages)
        # Append the FULL content (text, thinking and tool_use blocks)
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":  # end_turn, max_tokens, ...
            return response
        results = []                            # one result per tool_use
        for block in response.content:
            if block.type != "tool_use":
                continue
            result = {"type": "tool_result", "tool_use_id": block.id}
            try:
                output = handlers[block.name](**block.input)
                result["content"] = json.dumps(output)
            except Exception as exc:            # unknown tool, bad input
                result["content"] = (f"{type(exc).__name__}: {exc}. "
                                     "Check the arguments and try again.")
                result["is_error"] = True
            results.append(result)
        messages.append({"role": "user", "content": results})  # ONE message
    raise RuntimeError("Agent exceeded max_turns")
```

**Formatting rules (breaking them returns a 400):** a `tool_result` comes **immediately** after the assistant message with its `tool_use`. In that user message, `tool_result` blocks come **first** (prefer sending only results). Every `tool_use` gets a matching `tool_result`; a failed call gets `is_error: true`. **Behavior rule:** put all parallel results in **one** user message. Splitting them is not a 400, but it is the most common reason Claude stops making parallel calls. **Single call or parallel calls?** Parallel calls suit **independent** work (three order lookups). Use one call per turn when a call depends on another's result or side effects need a fixed order: set `disable_parallel_tool_use: true`, or add "Only batch tool calls that are independent of each other" to the system prompt.

**Thinking blocks in the loop.** With thinking on, pass `thinking` blocks back complete and unmodified. Appending the whole `response.content` does this. **Errors as information.** Write `is_error` messages that help recovery ("customer_id must be numeric"). Retry **transient** failures (timeouts) with backoff inside the tool; return **validation** errors right away with details. Keep untrusted content (web pages, emails) inside `tool_result` blocks, and enforce preconditions for irreversible actions in code.

> **Exam trap:** The loop ends on `stop_reason == "end_turn"`, not when the text says "done". Keep `max_turns` as a safety net only.

### 2.7 Client tools, Anthropic-schema tools and server tools *(beyond the guide)*

| Execution model | Examples | Who runs it | What your harness does |
|---|---|---|---|
| **User-defined client tool** | `get_customer`, `lookup_order` | Your app | Dispatch by name, return a `tool_result` |
| **Anthropic-schema client tool** | `bash`, `str_replace_based_edit_tool`, `memory`, computer and browser toolsets | Your app, in a sandbox | Implement the published schema, return a `tool_result` |
| **Server tool** | `web_search`, `web_fetch`, `code_execution`, tool search | Anthropic | Enable it, pass result blocks back unchanged, handle `pause_turn`. **Never** send a `tool_result` |

#### The harness dispatch table

A harness is a loop plus a map from each `tool_use` identity to code. Dispatch on the (`toolset_name`, `name`) pair, because toolset members share names such as `screenshot`. Server blocks stay in history but are never dispatched.

```python
HANDLERS = {
    ("", "lookup_order"): lookup_order,                    # user-defined
    ("", "str_replace_based_edit_tool"): run_text_editor,  # Anthropic-schema
    ("computer", "screenshot"): take_screenshot,           # toolset member
    ("computer", "left_click"): left_click,
}
def dispatch(response) -> list[dict]:
    results = []
    for block in response.content:
        if block.type != "tool_use": continue  # server_tool_use, thinking
        key = (block.toolset_name or "", block.name)
        result = {"type": "tool_result", "tool_use_id": block.id}
        if block.toolset_name:  # member results echo the toolset name
            result["toolset_name"] = block.toolset_name
        handler = HANDLERS.get(key)
        if handler is None:
            results.append({**result, "is_error": True,
                            "content": f"Unknown tool {key}"})
            continue
        try:
            results.append({**result, "content": handler(**block.input)})
        except Exception as exc:
            results.append({**result, "is_error": True,
                            "content": f"{type(exc).__name__}: {exc}"})
    return results
```

#### Server tools: what changes in the loop

- **No `tool_result`.** A `server_tool_use` block (id `srvtoolu_…`) is followed by its result block, such as `web_search_tool_result`, in the same turn.
- **`pause_turn`.** The server loop hit its limit (default 10). Resend the paused assistant content as-is, with the same `tools` and no "continue" message.
- **Mixed turns.** If Claude calls a server tool and a client tool together, the response ends with `tool_use` and the server call has no result yet. Send only your `tool_result` blocks and keep the same `tools` array, or the resume fails with a 400.
- **Errors arrive inside a 200** as an error object (`max_uses_exceeded`, `too_many_requests`). Pass results back unchanged, including `encrypted_content`.
- **Cost and control.** Web search costs **$10 per 1,000 searches** plus result tokens. Enable it with `tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}]`; `max_uses` caps searches per turn (resumed requests and failed searches count too), and `allowed_domains` / `blocked_domains` restrict sources. On Claude 4.6+ models prefer `web_search_20260318` (dynamic filtering, which runs code execution for you). Google-managed Google Cloud (Vertex AI) and Azure-hosted Microsoft Foundry offer only the basic `web_search_20250305`.

#### Anthropic-schema client tools in brief

Prefer these over a home-made `run_shell` or `edit_file`: Claude was trained on those exact schemas and calls them more reliably. The security boundary is still yours.
- **Text editor** (`text_editor_20250728`, name `str_replace_based_edit_tool`): `view`, `str_replace`, `create`, `insert`. Keep paths inside an allowed root and require `old_str` to match **exactly one** location.
- **Bash** (`bash_20250124`): you run commands in a sandboxed, persistent shell. Security is entirely yours.
- **Computer use** (`computer_toolset_20260801`, generally available on the Claude API and Google Cloud): 17 member tools (`screenshot`, `left_click`, `type`, `zoom`) with `"toolset_name": "computer"`. Run a **batch action** in order, stop at the first failure, return a result for every block. Adds about 4,500 input tokens per request. Use a minimal-privilege VM and human confirmation for consequential actions.

#### The "batch tool" pattern (legacy)

Some Academy courses teach a **batch tool**: a meta-tool whose input is a list of `{"name", "arguments"}` calls that your harness fans out. Current models emit several `tool_use` blocks natively, so prefer native parallel calls. Each keeps its own schema, `strict: true` and `tool_result`.

#### Tool-set construction checklist

1. **Few tools per agent** (4–5). For large catalogs, use `defer_loading: true` plus a tool search tool.
2. **Distinct, namespaced names** (`crm_get_customer`); consolidate variations, split different contracts.
3. **Detailed descriptions** (3–4+ sentences) plus `input_examples` for complex inputs.
4. **`strict: true`** on action tools, with `additionalProperties: false`.
5. **High-signal results**: only the fields the next step needs.
6. **The right execution model**: server tool when Anthropic can host it, Anthropic-schema tool for shell and files, your own tool for your systems.
7. **Parallel-friendly design**: independent reads together, ordered side effects one at a time.

## Lesson code

Code from the video lesson: [../../presentations/02-function-calling/code/](../../presentations/02-function-calling/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run 2.1–2.7 offline and live, then build a customer-support agent with strict tools, a bounded loop and refund rules in code |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 7 offline coding exercises, an architecture scenario and a scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>
## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Agent keeps picking the wrong one of two similar tools | Rewrite / rename tools to remove overlap | Routing classifier, merging tools | Descriptions are the selection mechanism; fix the root cause cheaply first |
| You only need JSON back, no action is taken | `output_config.format` / `messages.parse()` | A fake "extraction tool" with forced `tool_choice` | Purpose-built, guaranteed schema, and works on models that reject forced tool use |
| Document type unknown, several extraction schemas | `tool_choice: any` (supporting models) or `auto` + strict + call check | Plain `auto` with no check | `auto` may answer in prose; you need a guaranteed structured result |
| A pipeline step must always run first (e.g. `extract_metadata`) | Forced `tool_choice: tool`, or a deterministic code step | Prompt instruction "always call X first" | Ordering is a business rule, so enforce it in code or the API, not in prose |
| A field may be absent from the source | Nullable (or optional) field + "return null if absent" | Required field | Required fields cause fabrication |
| Category set is not truly closed | Enum + `"other"` + `detail` string (+ `"unclear"`) | Closed enum | Keeps unexpected data and gives an honest low-confidence signal |
| Extraction is well-formed but numbers disagree | Semantic validation + retry with the specific error | Bigger model, "be careful" prompt | Schemas can't express business rules; targeted feedback fixes most slips |
| Irreversible action (refund, delete) | Code-level precondition (token binding, approval gate) | Prompt rules / tool-description warnings | Probabilistic compliance is not acceptable for destructive actions |
| Synthesis agent keeps doing its own web research | Remove web search from its toolset; add a scoped `verify_fact` tool; route new research through the coordinator | Prompt rule "don't search" | Tools outside a role's specialty get misused; scoping is enforced, prompts are not |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **One-line or near-identical tool descriptions**, or giving one agent every tool.
- **Appending only the assistant's text** instead of the full `response.content`. The `tool_use` blocks are lost and the next request fails.
- **Breaking the `tool_result` rules**: text before the results, a message in between, parallel results in separate messages, or a dropped failed call instead of `is_error: true`.
- **Ending the loop by parsing text** instead of checking `stop_reason`, or running truncated calls after `max_tokens`.
- **Treating `strict: true` as a correctness guarantee**, or making every field required "for completeness".
- **Trying to answer server tools**: a `tool_result` for `server_tool_use`, or a "continue" message after `pause_turn`.

## Self-check

**Q1. (Customer support agent)** Your agent often calls `get_customer` when the user asks about an order, even though `lookup_order` would answer it. Both tools have one-line descriptions that look alike. What should you do first?

- A) Add 15 few-shot examples of correct tool choices to the system prompt, covering both order and customer questions
- B) Add a small routing classifier in front of the agent that picks the tool before Claude sees the request
- C) Expand both descriptions with what each returns, input formats, examples and explicit "use when / don't use when" boundaries
- D) Merge both tools into one `customer_lookup` tool that returns the profile and every order in one call

<details><summary>Answer</summary>

**C.** Descriptions are the model's main tool-selection signal, so improving them is the cheapest fix with the biggest effect, and it targets the root cause. A adds tokens without fixing the cause (and untargeted examples are weak). B is over-engineering for a first step. D removes a useful separation and costs more effort than the problem justifies.
</details>

**Q2. (Structured data extraction)** In 30% of invoices there is no PO number. Your schema marks `po_number` as a required string, and reviewers find realistic-looking but invented PO numbers. What change fixes this most directly?

- A) Add "never make up data; copy the PO number exactly as printed" to the system prompt
- B) Retry extraction up to three times whenever a PO number fails a lookup in the purchasing database
- C) Switch the extraction tool to `strict: true` so the schema is always enforced
- D) Make `po_number` nullable (`["string", "null"]`), describe it as "null if not printed on the invoice", and treat `null` as a valid result

<details><summary>Answer</summary>

**D.** A required field for data that is often missing pushes the model to fabricate a value. A nullable field gives it an honest way to say "not present". A is a weak prompt-level patch. B cannot help, because retries can't create information that isn't in the source. C enforces shape (a string is still a string), and strict mode is what *forces* a value into a required field, so it doesn't stop the fabrication.
</details>

**Q3. (Structured data extraction)** You moved your extractor to a strict schema. JSON parse errors went to zero, but 5% of invoices still have line items that don't add up to the total. What is the right next step?

- A) Nothing in the pipeline. Strict mode guarantees correct values, so the 5% must be errors in the source documents; report them to the suppliers
- B) Add code that compares computed vs. stated totals; on a mismatch, re-prompt with the document, the previous extraction and the specific discrepancy, and send cases that still fail to human review
- C) Add `minimum`/`maximum` constraints on every amount in the strict schema so out-of-range line items can no longer be produced
- D) Switch to a larger model and lower the temperature so the arithmetic in each extraction is done more carefully

<details><summary>Answer</summary>

**B.** This is a semantic error. Schemas guarantee syntax and structure, not business rules. Validation plus retry with *specific* feedback fixes most slips, and human review covers the rest (including genuine errors in the source). A misreads what strict mode guarantees. C isn't supported in strict schemas and wouldn't express "sum equals total" anyway. D doesn't address the missing validation layer (and current models reject custom sampling parameters).
</details>

**Q4. (Agent loop)** A developer's loop sends the tool results back like this: `[{"type": "text", "text": "Here are the results"}, {"type": "tool_result", ...}]`, and the request fails with a 400. Another teammate suggests ending the loop when the reply contains the word "done". Which pair of fixes is correct?

- A) Put `tool_result` blocks first (text after them, if any), and end the loop when `stop_reason == "end_turn"`
- B) Send each `tool_result` in its own user message, and end the loop after 5 iterations
- C) Put the text in the system prompt, and end the loop when the response has no `tool_use` text
- D) Move the tool results into the assistant message, and end on "done"

<details><summary>Answer</summary>

**A.** In the user message that answers a `tool_use`, the `tool_result` blocks must come first. `stop_reason` is the structured signal for loop control. B breaks parallel-call batching, and a fixed iteration count is only a safety net. C and D misuse roles and rely on fragile text parsing.
</details>

## Official documentation

- [Tool use with Claude: overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools): descriptions, `input_examples`, `tool_choice` and forced-tool-use restrictions
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls): `tool_result` format, ordering rules, `is_error`
- [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): `output_config.format`, JSON Schema limitations
- [Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools): `server_tool_use`, `pause_turn`, mixed server and client turns
- Syllabus source: [Claude Certified Architect study guide, Chapter 2](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-2-tools-and-tool_use) by paullarionov (community guide, restructured and expanded here)

[← Chapter 1 — Claude API Fundamentals](../01-claude-api-fundamentals/README.md) | [↑ Claude path overview](../README.md) | [Chapter 3 — Agent SDK →](../03-agent-sdk/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
