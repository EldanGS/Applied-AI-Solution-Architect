# Chapter 1 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

IDs come from this repo's requirement checklists: OpenAI Academy courses, bootcamps and developer tracks (`OAI/...`) and the role competency matrix (`ROLE/...`). Items marked **[INFERRED]** in the checklist are likely curriculum, not confirmed course content, because the Academy course internals are behind sign-in.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/bootcamp/api-builder/2` | API Foundations: core API building blocks | [1.1](../README.md#11-anatomy-of-a-responses-api-request)–[1.6](../README.md#16-context-window-tokens-and-cost) (request, items and roles, status, state, streaming and background, tokens and cost); practice notebook and mini-project | Primary |
| `OAI/tracks/building-agents/3` | Reasoning vs non-reasoning models: chain of thought, effort, latency and cost | [1.7](../README.md#17-model-selection-and-reasoning-effort) ("Reasoning vs non-reasoning models", effort levers), [1.3](../README.md#13-status-and-incomplete_details-why-generation-stopped) (reasoning eats `max_output_tokens`), [1.6](../README.md#16-context-window-tokens-and-cost) (reasoning billed as output); practice effort sweep | Primary |
| `OAI/api/design-build-agentic-systems/21` [INFERRED] | Reasoning vs non-reasoning and effort; a fast model for conversation that delegates demanding work to the flagship | [1.7](../README.md#17-model-selection-and-reasoning-effort) ("Fast front, flagship behind"), [cheat-sheet](../README.md#cheat-sheet), More self-check questions 6; practice delegation router | Primary |
| `OAI/tracks/ai-app-development/11` | Prototype in the Playground, then move the code into the app | [1.9](../README.md#19-playground-to-code-sampling-and-non-determinism) ("Prototype in the Playground, then move to code"); practice request builder | Primary |
| `OAI/bootcamp/api-builder/3` | API Foundations: model selection | [1.7](../README.md#17-model-selection-and-reasoning-effort) (lineup, levers, eval-driven selection process) | Supporting |
| `OAI/tracks/building-agents/4` | Start with the flagship, use smaller models for latency, conversational model delegates heavy tasks | [1.7](../README.md#17-model-selection-and-reasoning-effort) ("Selection process", "Fast front, flagship behind") | Supporting |
| `ROLE/BUILD/5` | Work fluently with model APIs and SDKs | [1.1](../README.md#11-anatomy-of-a-responses-api-request)–[1.8](../README.md#18-chat-completions-the-legacy-contrast), practice notebook and homework exercises | Supporting |
| `ROLE/ARCH/3` | Model selection and trade-off reasoning | [1.7](../README.md#17-model-selection-and-reasoning-effort), [cheat-sheet](../README.md#cheat-sheet), More self-check questions 4, More self-check questions 6 | Supporting |
| `ROLE/BUILD/3` | Rapid prototyping, POCs and pilots | [1.9](../README.md#19-playground-to-code-sampling-and-non-determinism) (Playground to versioned code, eval before shipping) | Supporting |

## More self-check questions

**Q1.** A product manager says: "Switching to `previous_response_id` will cut our input token bill, because we no longer resend the history." What is the accurate response?

- A) Correct: chained context is free
- B) Correct, but only with `store=True`
- C) Incorrect: all earlier input tokens in the chain are still billed as input; use prompt caching and compaction to reduce cost
- D) Incorrect: `previous_response_id` doubles the bill because responses are stored twice

<details><summary>Answer</summary>

**C.** OpenAI states that even with `previous_response_id`, all previous input tokens in the chain are billed as input. Savings come from cached-input pricing on a stable prefix and from making the context smaller.
</details>

**Q2.** An analysis job on `gpt-6-astra` at `xhigh` effort runs for several minutes, and your API gateway kills idle HTTP connections after 60 seconds. Users see random failures. What should you do?

- A) Retry failed requests up to five times
- B) Use `background=True` and poll `responses.retrieve` (or subscribe to the `response.completed` webhook)
- C) Lower `max_output_tokens` to 1,000 so the job finishes faster
- D) Switch to Chat Completions, which has longer timeouts

<details><summary>Answer</summary>

**B.** Background mode is designed for long-running reasoning: the job runs server-side and you poll or receive a webhook. A re-runs and re-bills the job, C risks `incomplete` output, and D does not address the transport problem (and Chat Completions loses Responses features).
</details>

**Q3.** A support bot calls `responses.create` and shows `output_text` to the user whenever `status` is `completed`. One response has `status: "completed"` and these output items: `reasoning`, a `message` with `phase: "commentary"` ("Let me look up that order."), and a `function_call` to `get_order`. The user sees "Let me look up that order." and nothing else. What should the code do with this response?

- A) Nothing different: `completed` means the answer is final, so show the text
- B) Run `get_order`, send its result as a `function_call_output` with the same `call_id` (replaying the earlier output items unchanged), and ask for the next response
- C) Retry the request with a larger `max_output_tokens`, because the answer was cut off
- D) Drop the `commentary` message before replaying the items, because only the `function_call` matters

<details><summary>Answer</summary>

**B.** `completed` only means the model finished its turn, and here the turn ends with a tool request. The `commentary` message is a preamble, not the final answer ([1.2](../README.md#12-input-items-roles-and-instructions), [1.3](../README.md#13-status-and-incomplete_details-why-generation-stopped)); Chapter 2 builds the full loop. A shows the preamble as if it were the answer. C fixes a problem that isn't there: the status would be `incomplete` if the budget had run out. D breaks the replay rule from 1.2: replay output items unchanged (the SDK notes that dropping `phase` from assistant messages can degrade performance).
</details>

**Q4.** You must classify 2 million short tickets per day with p95 latency under 2 seconds. Which approach is best?

- A) `gpt-6-astra` at `max` effort, because accuracy matters
- B) Build a labeled eval and compare `gpt-6-luna` at `none`/`low` effort with `gpt-6.1-sol` at `low`; pick the cheapest configuration that meets accuracy and latency
- C) The model with the largest context window
- D) Chat Completions with `temperature=0` on `gpt-6-astra`

<details><summary>Answer</summary>

**B.** Model choice should be measured as cost per successful task at the required quality and latency. A is far too slow and expensive for this volume, C is irrelevant for short inputs, and D uses the legacy API plus a sampling parameter that OpenAI says to remove from GPT-6 requests whenever reasoning effort is not `none`.
</details>

**Q5.** A prompt for routing tickets passed every example the team tried in the Playground. In CI, the same eval example sometimes passes and sometimes fails on `gpt-6.1-sol` at `medium` effort. A developer proposes adding `temperature=0`. What should you do instead?

- A) Add `temperature=0` and `top_p=0` together to force determinism
- B) Add a `seed` to the request so the runs repeat
- C) Run each eval example several times, report a pass rate, check properties (the right label, valid schema) rather than exact strings, and use Structured Outputs for the shape
- D) Keep the Playground result as the reference, because it was reviewed by hand

<details><summary>Answer</summary>

**C.** Output is non-deterministic, and with reasoning on GPT-6 models `temperature` and `top_p` are unsupported (OpenAI says to remove them when effort is not `none`), so A fails on this model and would not guarantee identical output anyway. B: `responses.create` has no `seed` parameter. D confuses a few manual tries with evidence.
</details>

**Q6.** A travel chat app runs every turn on `gpt-6-astra` at `high` effort. Users complain that small talk feels slow, but about 5% of turns ask for a full multi-city itinerary that needs real planning. Which design follows OpenAI's guidance?

- A) Keep Astra on every turn and lower `max_output_tokens`
- B) Put a fast model (for example Luna at `none` or `low`) in front for the conversation, and let it delegate the planning requests to Astra; confirm both choices with evals
- C) Switch every turn to Luna at `max` effort
- D) Use Chat Completions for small talk and Responses for planning

<details><summary>Answer</summary>

**B.** OpenAI's Building Agents track recommends a fast conversational model that delegates demanding tasks to the flagship. Most turns become fast and cheap, and you pay for flagship reasoning only where it matters. A risks `incomplete` answers without fixing latency, C makes small talk slow again, and D changes the API rather than the model choice.
</details>

**Q7.** A bank's support chat uses the Conversations API so that any server can pick up a thread. The base persona comes from code as `instructions` on every request. Halfway through one thread, an operator tool adds a new rule for that customer only: "Do not offer a fee refund; escalate instead." The rule must still apply on later turns, whichever server handles them. Where should the app put it?

- A) Add it to the conversation as a `developer` message item, and keep sending the base persona as `instructions`
- B) Send it once in `instructions` on the next request; the conversation saves it for later turns
- C) Store it in the conversation's `metadata`
- D) Send it with `previous_response_id` pointing at the operator's response, alongside `conversation`

<details><summary>Answer</summary>

**A.** A `developer` message is an input item, so the conversation stores it, and later turns see it with developer-level authority ([1.2](../README.md#12-input-items-roles-and-instructions)). B fails because `instructions` are not input items: the conversation does not keep them, so the rule disappears on the turn after. C is key-value data for your own tracking and queries; the model never reads it. D is rejected by the API, because `previous_response_id` and `conversation` cannot be combined.
</details>

**Q8.** A chained chat on `gpt-6-luna` runs at `low` effort. One turn asks for a careful root-cause analysis; the follow-ups after it are routine again. You want more reasoning for that one turn without breaking the cached prompt prefix. What do you do?

- A) Add "think step by step and be thorough" to `instructions` for that turn
- B) Add a `configuration_update` item with effort `high` before that user message, and one with effort `low` before the next routine message; keep the request-level `reasoning.effort` at `low`
- C) Add the same `configuration_update` items, and also turn on `truncation="auto"` so the chain stays short
- D) Set `text.verbosity` to `high` for that turn

<details><summary>Answer</summary>

**B.** A `configuration_update` item changes effort from that point on, until another update replaces it, and the request-level setting stays the same, so the cached prefix is kept ([1.7](../README.md#17-model-selection-and-reasoning-effort)). A edits the start of the prompt, which breaks the cached prefix, and wording is not the effort lever. C breaks a documented rule: don't combine configuration updates with automatic truncation or automatic compaction. D changes how long the answer is, not how much the model reasons.
</details>

## Share your progress

```text
OpenAI branch, chapter 1: the Responses API.

3 takeaways:
1. State is a design choice: resend history, chain with previous_response_id, or use a Conversation. Each has different retention rules.
2. There is no stop_reason. Check status + incomplete_details, and never trust output[0].
3. max_output_tokens includes reasoning. Set it too low and you pay for an empty answer.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#OpenAI #AIArchitecture #LLM #BuildInPublic
```
