# Chapter 2 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

OpenAI has no public architect certification. This table maps the chapter to the OpenAI Academy courses, bootcamps and developer tracks this repo targets (`OAI/...` IDs) and to the solution-architect competency matrix (`ROLE/...` IDs). Items marked **[INFERRED]** are not stated on the course page itself (course internals are behind sign-in); they are mapped from the matching bootcamp session or developer track, so treat them as likely, not confirmed, curriculum.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/api/design-build-agentic-systems/16` **[INFERRED]** | The function-calling flow (define, model calls, you execute, return, model continues); compare with built-in tools and use one when it exists | [2.1](../README.md#21-the-function-calling-round-trip), [Function tools vs built-in tools](../README.md#function-tools-vs-built-in-tools), [2.5](../README.md#25-the-client-side-loop-and-errors-in-tool-outputs), Self-check Q2 and More self-check questions 5; `01_practice.ipynb` 2.1 and 2.5 | Primary |
| `OAI/api/design-build-agentic-systems/22` **[INFERRED]** | Use structured outputs (strict JSON schema) for any agent output the application consumes | [2.6](../README.md#26-structured-outputs-textformat-and-responsesparse), [2.7](../README.md#27-refusals-and-incomplete-responses), [cheat-sheet](../README.md#cheat-sheet); `01_practice.ipynb` 2.6–2.7 | Primary |
| `OAI/bootcamp/api-builder/5` | API Foundations: structured outputs | [2.6](../README.md#26-structured-outputs-textformat-and-responsesparse)–[2.8](../README.md#28-syntax-vs-semantic-validation); `01_practice.ipynb` 2.6–2.8; homework exercise 6 | Primary |
| `OAI/tracks/ai-app-development/9` | Structured outputs (strict JSON schema) and strict function-call schemas for reliable outputs | [2.3](../README.md#23-strict-mode-schema-rules), [2.6](../README.md#26-structured-outputs-textformat-and-responsesparse); `01_practice.ipynb` 2.3 (strict-schema linter); homework exercise 2 (`make_strict`) | Primary |
| `OAI/tracks/building-agents/6` | Function-calling flow: define, model calls, you execute, return result, model continues | [2.1](../README.md#21-the-function-calling-round-trip), [2.5](../README.md#25-the-client-side-loop-and-errors-in-tool-outputs); `01_practice.ipynb` 2.1, 2.5 and the mini-project | Primary |
| `OAI/tracks/building-agents/21` | Structured outputs for app-consumed output, and output guardrails for user-facing agents | [2.6](../README.md#26-structured-outputs-textformat-and-responsesparse) covers the structured-output half; output guardrails are in [Chapter 3](../../03-agents-sdk-and-agents-api/README.md) | Supporting |
| `ROLE/AGENT/2` | Tool / function-calling design: reliable tool schemas and descriptions, tool errors and the tool-result flow | [2.2](../README.md#22-defining-function-tools-responses-vs-chat-completions-shape)–[2.5](../README.md#25-the-client-side-loop-and-errors-in-tool-outputs); `01_practice.ipynb` mini-project; homework exercises 1–5 | Primary |
| `ROLE/PROMPT/3` | Structured outputs and schema enforcement, with validation and retry loops | [2.6](../README.md#26-structured-outputs-textformat-and-responsesparse)–[2.8](../README.md#28-syntax-vs-semantic-validation) (`extract_with_retry`); `01_practice.ipynb` 2.8; homework exercise 6 | Primary |

## More self-check questions

**Q1. (Migration)** You are reviewing a pull request that moves a Chat Completions tool loop to the Responses API. The tools are still built with `openai.pydantic_function_tool()` and passed unchanged to `client.responses.create()`. What must change before this can work?

- A) Nothing, because Responses doesn't support strict tools and ignores the extra fields
- B) The tools are in the nested Chat Completions shape; `responses.create()` expects `name`, `description`, `parameters` and `strict` at the top level, so flatten them (or call `responses.parse()`, which converts them)
- C) `tool_choice` must be set to `"required"` in Responses
- D) Pydantic models can't be used with the Responses API, so rewrite the schemas by hand

<details><summary>Answer</summary>

**B.** `pydantic_function_tool()` returns the Chat Completions shape (`{"type": "function", "function": {...}}`). The Responses function-tool type has `name`, `parameters` and `strict` at the top level. The SDK's `responses.parse()` converts the nested shape for you, but `responses.create()` sends your `tools` as they are, so flatten them first (homework exercise 1). A is wrong: Responses supports strict tools and even tries strict mode when `strict` is omitted. C has nothing to do with the tool shape. D is wrong: `responses.parse(text_format=...)` and converted tools work with Pydantic. (This answer relies on the documented shapes and the SDK source. The exact API error for a nested tool isn't documented, so the question asks what must change rather than what the error says.)
</details>

**Q2. (`tool_choice`)** Your support agent sends `get_customer`, `lookup_order` and `process_refund` on every turn to keep prompt caching effective. Before the customer is verified, the model must call a read-only tool and must not be able to call `process_refund`. Which request setting fits best?

- A) `tool_choice: "required"`, and a sentence in `instructions` saying not to refund yet
- B) Remove `process_refund` from `tools` until verification
- C) `tool_choice: {"type": "allowed_tools", "mode": "required", "tools": [get_customer, lookup_order references]}`
- D) `tool_choice: {"type": "function", "name": "get_customer"}` on every turn

<details><summary>Answer</summary>

**C.** `allowed_tools` restricts the callable subset for this turn without changing the `tools` list (so the cached prefix stays stable), and `mode: "required"` guarantees a call. A relies on the prompt for a security rule. B works functionally but changes the prefix every phase, which is exactly what `allowed_tools` is designed to avoid. D forces one tool even when `lookup_order` is the right one. (Keep a code-level check in the refund handler anyway.)
</details>

**Q3. (Errors)** `lookup_order` sometimes times out (succeeds on retry) and sometimes gets an unknown order ID (never succeeds). Both currently raise an exception that crashes the loop. What should you change?

- A) Catch nothing; let the caller retry the whole conversation
- B) Retry timeouts with backoff inside the tool; for unknown IDs return a `function_call_output` for that `call_id` with a clear JSON error (`"error": "not_found", "retryable": false`, and what to ask the user)
- C) Return an empty string as the output for both cases
- D) Set `is_error: true` on the `function_call_output`

<details><summary>Answer</summary>

**B.** The tool knows which failure happened, so deterministic retry belongs there. Non-retryable errors such as not_found go straight back as data the model can act on, and every `call_id` still gets an output. A wastes work and loses context. C gives the model nothing. D: `function_call_output` has no `is_error` field on OpenAI; that is Claude's `tool_result` field.
</details>

**Q4. (Model and API choice)** A team wants to keep Chat Completions and use `gpt-6.1-sol` with function calling for a new agent. What does the current guidance say?

- A) That works the same as on Responses
- B) GPT-6.1 Sol requires the Responses API for tool calling; use Responses for the new agent
- C) Function calling is only available on `gpt-6-astra`
- D) They must use JSON mode instead of tools

<details><summary>Answer</summary>

**B.** The GPT-6 guidance says GPT-6 Astra, GPT-6.1 Sol and GPT-6.1 Terra support Chat Completions but tool calling requires Responses. GPT-6 Sol and GPT-6 Luna support function calling in Chat Completions only with `reasoning_effort: "none"`. C and D are false.
</details>

**Q5. (Function vs built-in tool)** A support agent must answer questions from the company's uploaded policy PDFs and check the live status of orders in an internal database. A teammate proposes two functions, `search_policies(query)` (calling a home-grown vector index) and `lookup_order(order_id)`, and one loop that executes every tool-call item in `response.output`. What is the better design?

- A) Keep both functions; built-in tools are only for prototypes
- B) Use `file_search` (hosted) for the policy PDFs and a strict `lookup_order` function for the database; the loop executes only `function_call` items, because hosted calls have already run at OpenAI
- C) Use `web_search` for both, because it can reach any URL
- D) Use only `lookup_order`, and paste every policy PDF into `instructions`

<details><summary>Answer</summary>

**B.** Use a built-in tool when one exists (retrieval over uploaded files is `file_search`), and write a function only for capabilities that are yours (the order database). Hosted call items such as `file_search_call` come back already executed, so a loop that tries to "execute" every call item is wrong. A rebuilds a maintained capability for no gain, unless a requirement rules the hosted tool out. C can't reach an internal database. D wastes context and money on every turn and doesn't scale.
</details>

## Share your progress

```text
AI Solution Architect journey: OpenAI Chapter 2, function calling + Structured Outputs.

Same loop as Claude, different wiring.

3 takeaways:
1. arguments is a JSON string, and outputs go back by call_id (not id).
2. Strict mode = every field required. "Optional" means required + nullable.
3. A schema guarantees shape, not truth. Refusals, truncation and bad totals still need code.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#OpenAI #AIArchitecture #LLM #FunctionCalling #BuildInPublic
```
