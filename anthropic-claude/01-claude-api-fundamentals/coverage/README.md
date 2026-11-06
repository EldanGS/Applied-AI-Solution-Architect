# Chapter 1 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Requirement IDs come from the repo's requirements checklist, built from the official exam guides (v1.0, July 2026) and the Anthropic Academy course pages. "Primary" means this chapter is the main place the item is taught; "Supporting" means the chapter teaches the content but the item itself is completed or examined elsewhere. Academy lessons appear in several courses with the same title (for example "System prompts" in the Claude API, Amazon Bedrock and Google Cloud courses); each one is listed.

| Requirement ID | What it asks (short) | Where in this chapter | Depth |
|---|---|---|---|
| `CCDV-F/D2/2.3/K1` | Claude API mechanics: messages | [1.1](../README.md#11-anatomy-of-a-messages-api-request), [1.2](../README.md#12-message-roles-alternation-and-stateless-conversations), [1.3](../README.md#13-stop_reason-why-the-model-stopped); practice 1.1–1.3; homework Ex 1–4 | Primary |
| `CCDV-F/D2/2.3/K7` | Invoking Claude through third-party vendors | [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) (platform table, feature parity, exam trap); practice 1.8; homework Ex 7, Q12; More self-check questions 6 | Primary |
| `CCDV-F/D5/5.1/S1` | LLM fundamentals: tokens, context windows, sampling, non-determinism, model options (effort, thinking) | [1.5](../README.md#15-the-context-window), [Sampling and non-determinism](../README.md#sampling-and-non-determinism), [1.6](../README.md#16-tokens-counting-before-measuring-after), [1.7](../README.md#17-model-selection-basics), thinking row in [1.1](../README.md#11-anatomy-of-a-messages-api-request). Next-token generation: [00 §2.9](../../../00-prerequisites/README.md#29-next-token-generation); zero/one/multi-shot prompting: [Chapter 6](../../06-prompt-engineering/README.md) | Primary |
| `CCDV-F/D5/5.1/K1` | Tokens | [1.6](../README.md#16-tokens-counting-before-measuring-after) (`count_tokens`, `usage`, tokenizer change); practice 1.6; homework Ex 5–6 | Primary |
| `CCDV-F/D5/5.1/K2` | Context windows | [1.5](../README.md#15-the-context-window) (what fills it, overflow, lost in the middle); practice 1.5; homework Ex 6 | Primary |
| `CCDV-F/D5/5.1/K3` | Sampling | [Sampling and non-determinism](../README.md#sampling-and-non-determinism) (temperature, top-p, top-k, current-model rules); practice 1.5 sampling simulator; homework Q11 | Primary |
| `CCDV-F/D5/5.1/K4` | Non-determinism | [Sampling and non-determinism](../README.md#sampling-and-non-determinism) (why runs differ, eval consequences); practice 1.5 "one run vs. several runs"; [Self-check](../README.md#self-check) Q4; homework Q11 | Primary |
| `CCDV-F/D5/5.1/K9` | Model option: effort levels | [1.7](../README.md#17-model-selection-basics) (levels, per-model defaults, effort vs. model tier); practice 1.7 eval; homework Ex 1 | Primary |
| `CCDV-F/D5/5.2/K1` | Integrating with SDKs that wrap REST APIs | [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) (SDK vs. raw REST, sync vs. async); practice 1.8 (captured SDK request vs. raw `httpx2`, retries, async fan-out) | Primary |
| `ACAD/claude-certified-developer-foundations/LO1` | How Claude works at the level that affects engineering: tokens, context budget, sampling and non-determinism, model tiers, SDK vs. REST | [1.5](../README.md#15-the-context-window), [Sampling and non-determinism](../README.md#sampling-and-non-determinism), [1.6](../README.md#16-tokens-counting-before-measuring-after), [1.7](../README.md#17-model-selection-basics), [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) | Primary |
| `ACAD/claude-certified-developer-foundations/1` | Complete the prep module "MSO Foundations" | Whole chapter covers the module's objective (see `.../1/LO1`); completing the Academy module itself is done on the Academy site | Supporting |
| `ACAD/claude-certified-developer-foundations/1/LO1` | Tokens, the context window as a fixed budget, why sampling varies outputs, non-determinism for testing and evals | [1.5](../README.md#15-the-context-window), [Sampling and non-determinism](../README.md#sampling-and-non-determinism), [1.6](../README.md#16-tokens-counting-before-measuring-after); practice 1.5–1.6 | Primary |
| `ACAD/claude-platform-101/1` | What is the Claude Platform? | [1.1](../README.md#11-anatomy-of-a-messages-api-request) (one endpoint, features as parameters), [1.7](../README.md#17-model-selection-basics) (model lineup, Models API), [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) (SDKs and platforms) | Primary |
| `ACAD/claude-platform-101/2` | Your first API call | [Prerequisites](../README.md#prerequisites) setup snippet, [1.1](../README.md#11-anatomy-of-a-messages-api-request); practice 1.1 | Primary |
| `ACAD/claude-with-the-anthropic-api/LO1` | Set up and authenticate, API key management, request configuration | [Prerequisites](../README.md#prerequisites) (`.env`, never hardcode), [1.1](../README.md#11-anatomy-of-a-messages-api-request) (fields, typed errors), [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) (credential resolution, per-platform auth); key creation in [00 Step 4](../../../00-prerequisites/README.md#step-4--get-an-anthropic-api-key) | Primary |
| `ACAD/claude-with-the-anthropic-api/LO2` | Single and multi-turn conversations with proper message formatting and context handling | [1.2](../README.md#12-message-roles-alternation-and-stateless-conversations), [1.5](../README.md#15-the-context-window) (hybrid history); practice 1.2 `StatelessChat`, mini-project `ChatSession` | Primary |
| `ACAD/claude-with-the-anthropic-api/LO3` | System prompts; control behavior with temperature, streaming and structured output formats | [1.4](../README.md#14-the-system-prompt), [Sampling and non-determinism](../README.md#sampling-and-non-determinism) (temperature), `stream` row in [1.1](../README.md#11-anatomy-of-a-messages-api-request) and SDK streaming helper in [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms). Structured outputs in depth: [Chapter 6](../../06-prompt-engineering/README.md) | Primary |
| `ACAD/claude-with-the-anthropic-api/3` | Accessing the API | [1.1](../README.md#11-anatomy-of-a-messages-api-request), [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) | Primary |
| `ACAD/claude-with-the-anthropic-api/4` | Getting an API key | [Prerequisites](../README.md#prerequisites) (load from `.env`), [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) (how the SDK finds credentials); step-by-step key creation in [00 Step 4](../../../00-prerequisites/README.md#step-4--get-an-anthropic-api-key) | Supporting |
| `ACAD/claude-with-the-anthropic-api/5` | Making a request | [1.1](../README.md#11-anatomy-of-a-messages-api-request); practice 1.1; homework Ex 1 | Primary |
| `ACAD/claude-with-the-anthropic-api/6` | Multi-turn conversations | [1.2](../README.md#12-message-roles-alternation-and-stateless-conversations); practice 1.2 | Primary |
| `ACAD/claude-with-the-anthropic-api/7` | Chat exercise | Practice 1.2 (`StatelessChat`) and the mini-project (`ChatSession`) | Primary |
| `ACAD/claude-with-the-anthropic-api/8` | System prompts | [1.4](../README.md#14-the-system-prompt); More self-check questions 7–8 | Primary |
| `ACAD/claude-with-the-anthropic-api/9` | System prompts exercise | Practice 1.4 (prompt linter, A/B tool-choice test, drift experiment) | Primary |
| `ACAD/claude-with-the-anthropic-api/10` | Temperature | [Sampling and non-determinism](../README.md#sampling-and-non-determinism); practice 1.5 sampling simulator | Primary |
| `ACAD/claude-with-the-anthropic-api/15` | Quiz on accessing Claude with the API | [Self-check](../README.md#self-check) Q1–Q4, [More self-check questions](#more-self-check-questions) 1–8 and homework Part A (12 questions); the Academy quiz itself is taken on the Academy site | Supporting |
| `ACAD/claude-in-amazon-bedrock/4` | Making a request (Bedrock course) | [1.1](../README.md#11-anatomy-of-a-messages-api-request); Bedrock client and model IDs in [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms); practice 1.8 (offline Bedrock request) | Primary |
| `ACAD/claude-in-amazon-bedrock/5` | Multi-turn conversations | [1.2](../README.md#12-message-roles-alternation-and-stateless-conversations) (identical on Bedrock) | Primary |
| `ACAD/claude-in-amazon-bedrock/6` | Chat bot exercise | Practice 1.2 `StatelessChat` and the mini-project; swap in the Bedrock client from practice 1.8 | Primary |
| `ACAD/claude-in-amazon-bedrock/7` | System prompts | [1.4](../README.md#14-the-system-prompt); More self-check questions 7–8 | Primary |
| `ACAD/claude-in-amazon-bedrock/8` | System prompt exercise | Practice 1.4 | Primary |
| `ACAD/claude-in-amazon-bedrock/9` | Temperature | [Sampling and non-determinism](../README.md#sampling-and-non-determinism) | Primary |
| `ACAD/claude-in-amazon-bedrock/11` | Controlling model output | `max_tokens`, `stop_sequences` ([1.1](../README.md#11-anatomy-of-a-messages-api-request), [1.3](../README.md#13-stop_reason-why-the-model-stopped)), prefill and why it is gone ([1.2](../README.md#12-message-roles-alternation-and-stateless-conversations)), effort ([1.7](../README.md#17-model-selection-basics)); practice 1.2–1.3 | Primary |
| `ACAD/claude-in-amazon-bedrock/14` | Quiz on working with the API | [Self-check](../README.md#self-check), [More self-check questions](#more-self-check-questions) and homework Part A; the Academy quiz itself is taken on the Academy site | Supporting |
| `ACAD/claude-with-google-vertex/LO2` | Multi-turn conversations with proper message handling and context management | [1.2](../README.md#12-message-roles-alternation-and-stateless-conversations), [1.5](../README.md#15-the-context-window); Vertex client in [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms) | Primary |
| `ACAD/claude-with-google-vertex/5` | Making a request (Vertex course) | [1.1](../README.md#11-anatomy-of-a-messages-api-request); Vertex client, URL and `anthropic_version` in [1.8](../README.md#18-access-paths-sdks-raw-rest-async-clients-and-cloud-platforms); practice 1.8 (offline Vertex request) | Primary |
| `ACAD/claude-with-google-vertex/6` | Multi-turn conversations | [1.2](../README.md#12-message-roles-alternation-and-stateless-conversations) | Primary |
| `ACAD/claude-with-google-vertex/7` | Chat exercise | Practice 1.2 `StatelessChat` and the mini-project; swap in the Vertex client from practice 1.8 | Primary |
| `ACAD/claude-with-google-vertex/8` | System prompts | [1.4](../README.md#14-the-system-prompt); More self-check questions 7–8 | Primary |
| `ACAD/claude-with-google-vertex/9` | System prompts exercise | Practice 1.4 | Primary |
| `ACAD/claude-with-google-vertex/10` | Temperature | [Sampling and non-determinism](../README.md#sampling-and-non-determinism) | Primary |
| `ACAD/claude-with-google-vertex/13` | Controlling model output | `max_tokens`, `stop_sequences`, prefill, effort ([1.1](../README.md#11-anatomy-of-a-messages-api-request), [1.2](../README.md#12-message-roles-alternation-and-stateless-conversations), [1.3](../README.md#13-stop_reason-why-the-model-stopped), [1.7](../README.md#17-model-selection-basics)) | Primary |
| `ACAD/claude-with-google-vertex/16` | Quiz on accessing Claude with the API | [Self-check](../README.md#self-check), [More self-check questions](#more-self-check-questions) and homework Part A; the Academy quiz itself is taken on the Academy site | Supporting |

## More self-check questions

**Q1.** A shop assistant's system prompt says *"Check stock before every answer."* Its `check_stock` tool now runs on 70% of turns, including "How long does delivery to Almaty take?" and "Can I return opened items?". The team wants fewer wasted tool calls without losing correct stock answers. Which change targets the cause?

- A) Set `tool_choice` to `{"type": "none"}` for every request
- B) Rewrite the rule so it names the situation: check stock before promising a specific item, size or quantity
- C) Add "only use tools when needed" to the `check_stock` description and keep the system rule as it is
- D) Cache the stock results so repeated calls are cheaper

<details><summary>Answer</summary>

**B.** The unconditional rule ties every turn to the tool. Stating when it applies removes the over-use while stock questions still trigger the call. A blocks the tool even when it is needed. C leaves the stronger system-prompt rule in place, so it keeps winning. D makes the wasted calls cheaper but does not remove them.
</details>

**Q2.** A research chat on Sonnet 5.5 resends a 20K-token system prompt and tool list that never change, plus a history that has grown to 300K tokens. The team has two goals: lower the bill, and keep every request under its own 400K-token budget as the chat continues. Which statement is correct?

- A) Prompt caching on the system prompt and tools meets both goals, because cached tokens no longer count toward the context window
- B) Prompt caching lowers the cost of the stable prefix but frees no space; to stay under the budget, shrink the history itself (case facts + summary of old turns + recent turns verbatim, or server-side compaction)
- C) Moving the history into the system prompt meets both goals, because the system prompt is outside the context window
- D) The Message Batches API meets both goals: it is 50% cheaper and allows longer histories

<details><summary>Answer</summary>

**B.** Cached tokens are cheaper to read but still sit in the window, so caching helps only the cost goal. Only removing or condensing tokens helps the size goal. A mixes the two up. C is false: the system prompt is part of the window. D cuts the price of each request, but a batch request has the same context window, and a chat needs real-time answers anyway.
</details>

**Q3.** Before you route a large contract to a model, you need to know whether it fits and roughly what it costs. Which approach is most accurate?

- A) Estimate with `tiktoken`, because tokenizers are similar across vendors
- B) Divide the character count by 4
- C) Call `messages.count_tokens` with the same model, system prompt, tools and messages you will send
- D) Send the request and read `usage`; if it fails, split the document

<details><summary>Answer</summary>

**C.** Token counts are model-specific (current models use a newer tokenizer), and the counting endpoint is free and accepts the same inputs as `messages.create`. A and B are inaccurate. D wastes money and time and gives no answer in advance.
</details>

**Q4.** You migrate a working extractor from Claude Haiku 4.5 to Claude Sonnet 5.5. Every request now fails with HTTP 400. The code ends `messages` with `{"role": "assistant", "content": "{"}` to force JSON output. What is the right fix?

- A) Change the prefill to `"Here is the JSON:"`
- B) Remove the prefill and use structured outputs (`output_config.format`) or clear system-prompt format instructions
- C) Set `temperature=0` so the output is deterministic
- D) Move the prefill into the system prompt as `{"role": "assistant"}`

<details><summary>Answer</summary>

**B.** Final-turn assistant prefill is not supported on Opus 4.6 / Sonnet 4.6 and later models, so any prefill returns 400 (A). Structured outputs guarantee the shape. Non-default `temperature` values are themselves rejected on the newest models (C), and D is not valid API usage.
</details>

**Q5.** You must classify 2 million short support tickets per day into 6 categories, with a p95 latency target under 2 seconds. How should you choose the model?

- A) Use Claude Fable 5.1 because accuracy matters most
- B) Build a labeled eval set, measure Haiku 5.5 and Sonnet 5.5 (at low effort), and pick the cheapest configuration that meets the accuracy and latency targets
- C) Use the model with the largest context window
- D) Use Opus 5.5 because it is Anthropic's recommended default

<details><summary>Answer</summary>

**B.** Model choice should be evidence-based and measured as cost per completed task at the required quality. A and D skip measurement and are likely far more expensive than needed at this volume. C is irrelevant for short inputs.
</details>

**Q6.** A bank's security team requires that all Claude traffic stays inside its AWS account boundary with IAM-based access, so the team moves a working Claude API integration to Amazon Bedrock. The integration uses Sonnet 5.5 with structured outputs, reads model limits from the Models API at startup, and runs nightly jobs on the Message Batches API. Which plan is correct?

- A) Keep `anthropic.Anthropic()` and the model ID `claude-sonnet-5-5`; only change the API key
- B) Use `AnthropicBedrockMantle` with the model ID `anthropic.claude-sonnet-5-5`, keep structured outputs, and redesign the parts that rely on endpoints Claude in Amazon Bedrock does not offer (the Models API and Message Batches), for example with model limits kept in configuration and concurrent real-time calls
- C) Rewrite the integration against a different, AWS-specific request format, because Bedrock does not use the Messages API shape
- D) Use `AnthropicVertex`, because every cloud platform exposes the same features

<details><summary>Answer</summary>

**B.** Claude in Amazon Bedrock serves the same Messages API body through its own client class and endpoint, with `anthropic.`-prefixed model IDs and AWS credentials. Its feature set is a subset: structured outputs work there, but as of November 2026 it has no Message Batches API and no Models API. A sends traffic to Anthropic's endpoint, outside the AWS boundary. C is wrong because the body is the same Messages API. D picks the wrong platform, and feature sets differ across platforms anyway. (If the requirement were only AWS billing and IAM rather than the AWS security boundary, Claude Platform on AWS, which Anthropic operates with first-party feature parity, would be the alternative to evaluate.)
</details>

**Q7.** A museum-guide app on Sonnet 5.5 has two kinds of instruction. Standing rules (friendly docent, under 100 words, end by suggesting one nearby exhibit) apply to every visit. Live notices such as *"Gallery 3 closes in 10 minutes"* arrive from the backend in the middle of a chat. The app uses prompt caching. Where should each go?

- A) Standing rules in the top-level `system` field, unchanged on every request; each notice as a mid-conversation `system` message right after the latest user turn
- B) Both in the top-level `system` field, editing it each time a notice arrives
- C) Standing rules in the first user message; notices in `metadata.user_id`
- D) Standing rules in each tool description; notices as extra `assistant` turns

<details><summary>Answer</summary>

**A.** Standing rules are operator instructions and belong in a stable `system` field, which also caches well ([1.4](../README.md#14-the-system-prompt)). A mid-conversation `system` message gives a notice operator authority without touching the cached prefix ([1.2](../README.md#12-message-roles-alternation-and-stateless-conversations)). B works but changes the prefix on every notice, so everything from the system prompt onward has to be cached again. C gives the rules only user-level authority, and `metadata.user_id` is an opaque user ID the model never reads. D misuses tool descriptions, and an `assistant` turn is the model's own voice, not an instruction.
</details>

**Q8.** A cooking-coach app's system prompt sets a persona ("Chef Ama"), requires metric units and says to ask about the user's skill level before giving a recipe. The system prompt is sent unchanged on every request. After about eight exchanges, roughly 3,000 tokens in all, replies turn generic, switch to cups and ounces, and drop the persona. What is the most likely cause, and the best fix?

- A) The system prompt only applies to the first turn; send it again
- B) The growing run of the assistant's own earlier replies pulls behavior toward them and dilutes the system prompt; keep the persona rules concrete (a short example or two) and restate the critical ones at breakpoints, for example in a short mid-conversation `system` message where supported
- C) The context window is filling up; move to a model with a larger window
- D) Raise `temperature` so the persona comes through more strongly

<details><summary>Answer</summary>

**B.** This is instruction drift, and it can happen in a short chat: as assistant turns pile up, the model increasingly follows the pattern of its own replies rather than the system prompt ([1.4](../README.md#14-the-system-prompt), "Instruction drift"). Concrete examples and short reminders at breakpoints counter it. A is false: the app already resends the system prompt on every request. C cannot be the cause at 3,000 tokens. D does not target the cause, and the newest models (Opus 5.5, Sonnet 5.5) reject a non-default `temperature` anyway.
</details>

## Share your progress

```text
Day 1 of my AI Solution Architect journey: the Claude Messages API.

3 takeaways:
1. The API is stateless: your app resends the whole conversation, so cost grows every turn.
2. stop_reason is the real control signal, and there are now 7 values, not 4.
3. A 1M-token window is not a strategy. Curate the context; don't stuff it.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #Anthropic #AIArchitecture #LLM #BuildInPublic
```
