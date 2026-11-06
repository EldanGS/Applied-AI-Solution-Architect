# Chapter 3 — Agents SDK and the Agents API: Building Agentic Systems on OpenAI

> **Claude counterpart:** [Chapter 3 — Claude Agent SDK](../../anthropic-claude/03-agent-sdk/README.md) · **Academy course:** Design and Build Agentic Systems (API pathway) · **Est. time:** 8–10 hours (reading + 2 notebooks) · **Status:** [ ] not started

On OpenAI you can run an agent three ways: your own loop on the Responses API, the **Agents SDK** (a library that runs the loop inside your service), or the **Agents API** (a managed Codex harness that OpenAI runs, currently a beta API). After that choice come three design questions: **who owns the reply** (handoff or agent-as-tool), **which rules must hold every time** (guardrails and approvals in code), and **where conversation state lives**. Each answer trades control against effort and has data-retention and cost consequences a client will ask about.

## What you'll learn

- Choose between the Responses API, the Agents SDK, and the Agents API for a workload
- Define agents with `Agent`, run them with `Runner`, write function tools, and keep app state in the local run context
- Choose between **handoffs** (the specialist takes over) and **agents-as-tools** (the manager keeps control)
- Put guardrails and `needs_approval` where they actually run, pick one state strategy, and test routing, ownership, and safety against the trace

## Prerequisites

- [Chapter 1 — Responses API Fundamentals](../01-responses-api-fundamentals/README.md) and [Chapter 2 — Function Calling and Structured Outputs](../02-function-calling-and-structured-outputs/README.md)
- [00 — Prerequisites](../../00-prerequisites/README.md): Python 3.11+, `async`/`await`, `.env` handling
- Install: `pip install openai openai-agents python-dotenv` (the package is `openai-agents`, the import name is `agents`; 0.23.1 at the time of writing). In Jupyter use top-level `await Runner.run(...)`; `asyncio.run` and `Runner.run_sync` fail there

## Concepts

### 3.1 Choosing a runtime: Responses API, Agents SDK, or Agents API

**What counts as an agent.** OpenAI's [Building agents](https://developers.openai.com/tracks/building-agents) track defines an agent by **instructions** (what it should do), **guardrails** (what it should not do) and **tools** (what it can do), and it acts on the user's behalf. A chatbot that only answers questions is not an agent. Every OpenAI agent stack uses four platform primitives: **models**, **tools** (hosted tools, your functions, MCP), **state and memory**, and **orchestration** (the loop, handoffs, guardrails, tracing). The three runtimes differ in **where the loop runs** and **who keeps the state**.

| | **Responses API** (build it yourself) | **Agents SDK** (`openai-agents`) | **Agents API** (beta, managed Codex harness) |
|---|---|---|---|
| Use for | Direct model calls, or a loop you write from scratch | Agents with custom tools and workflows inside your app | Long-running tasks where OpenAI manages the agent and saves its progress |
| Where the loop runs | Your code | The SDK, inside your process | OpenAI's service |
| Integration effort (per OpenAI's docs) | High | Medium | Low |

- **Responses API** for a single call (classification, extraction, one chat turn), or a loop so unusual that a framework gets in the way.
- **Agents SDK** when your app must own deployment, tools, storage, and approvals. It is built on the Responses API but not tied to OpenAI models: it routes `litellm/...` and `any-llm/...` model names to adapter providers, and you can plug in your own `ModelProvider`.
- **Agents API** when OpenAI should run the harness (sessions, compaction, recovery) and the agent may need a sandbox. Check its data controls first ([3.9](#39-the-managed-agents-api-beta)).

| OpenAI reference demo | Runtime | What to look at | Where in this chapter |
|---|---|---|---|
| [Customer service agents](https://github.com/openai/openai-cs-agents-demo) | Agents SDK | Triage that hands off to specialists, plus relevance and jailbreak input guardrails | [3.4](#34-handoffs-vs-agents-as-tools), [3.5](#35-guardrails-and-tripwires) |
| [Support agent with human in the loop](https://github.com/openai/openai-support-agent-demo) | Responses API | An AI agent suggests replies and tool calls; a human approves the sensitive ones | [3.6](#36-human-review-approvals-and-resumable-state) |
| [Testing agent](https://github.com/openai/openai-testing-agent-demo) | Responses API computer use + Playwright | A computer-use model follows a written test case | [Chapter 4](../04-built-in-tools-and-mcp/README.md) |

> **Gotcha:** "Agents SDK session", "Agents API session", "Responses conversation", and "sandbox" are four different resources. Name them precisely. Do not start new work on the retired Assistants API or the deprecated Agent Builder.

### 3.2 `Agent` and `Runner`: the SDK agent loop

An `Agent` is configuration: a model, instructions, and optional tools, handoffs, guardrails, and an output type. The `Runner` runs the loop.

```python
import os
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()                             # OPENAI_API_KEY from .env
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")

agent = Agent(
    name="Support assistant",             # shows up in traces
    instructions="Answer billing questions in two sentences or fewer.",
    model=MODEL,                          # set it explicitly
)
result = Runner.run_sync(agent, "Why was I charged twice this month?")
print(result.final_output, result.last_agent.name)   # answer, who wrote it
```

**The loop.** The runner calls the model, runs any tool calls, switches agent on a handoff, and calls the model again. The run ends when the model produces output of the agent's `output_type` (plain text by default) **and** makes no tool calls. You never parse the text for "done". `await Runner.run(...)` is the async default, `Runner.run_sync` is for plain scripts, and `Runner.run_streamed` streams events for a UI. `max_turns` defaults to **10** model calls. Exceeding it raises `MaxTurnsExceeded`: an error to investigate, not a success. `error_handlers` can return a controlled fallback.

> **Gotcha: set the model explicitly.** Without a model on the agent, in `RunConfig`, or in `OPENAI_DEFAULT_MODEL`, openai-agents 0.23.1 falls back to `gpt-5.6-luna`. OpenAI's SDK guide suggests starting with `gpt-6-astra` and moving to a smaller model when latency or cost matters; a common pattern is a cheap triage model plus a stronger specialist.

### 3.3 Function tools and local context

`@function_tool` turns a Python function into a tool. The name becomes the tool name, the docstring the description, and the type hints a **strict** JSON schema. Give each agent only the tools it needs.

```python
from agents import Agent, RunContextWrapper, function_tool

@function_tool
def lookup_invoice(ctx: RunContextWrapper[SupportContext],
                   invoice_id: str) -> str:
    """Return the status and amount of one invoice for the current customer."""
    return fake_db_lookup(ctx.context.customer_id, invoice_id)

billing_agent = Agent[SupportContext](
    name="Billing agent",
    instructions="Answer invoice questions. Always look the invoice up first.",
    tools=[lookup_invoice],
)
```

`SupportContext` is your own dataclass, passed as `Runner.run(..., context=SupportContext(customer_id="C-42"))`. The SDK injects `ctx`; it is not in the tool schema. In OpenAI's words: *conversation history is what the model sees; run context is what your code sees.* Other levers: `instructions=` as a function `(ctx, agent) -> str` (dynamic instructions), `output_type=MyPydanticModel` for a typed answer, and `is_enabled=` to hide a tool for some users. Every agent, tool, hook, and guardrail in one run must use the same context type, and the context is serialized into `RunState` when a run pauses for approval (3.6), so keep secrets out of it.

#### Knowledge and behavior: where RAG and fine-tuned models plug into an agent

OpenAI's [AI application development track](https://developers.openai.com/tracks/ai-application-development) pairs building agents with RAG and fine-tuning. Both plug into the same `Agent`:

- **Knowledge (RAG) enters through a tool:** the hosted `FileSearchTool(vector_store_ids=[...], filters=...)`, or your own retriever as a `@function_tool`. The hosted tool works only with OpenAI models through the Responses API, so a `litellm/...` agent needs a function tool. Put tenant and region filters in code, never in the prompt.
- **Behavior and format (fine-tuning) enter through `model=`:** `agent.clone(model="ft:<base-model>:<org>::<id>")` (a placeholder in OpenAI's ID format; use your own job's model ID). Instructions, tools, and guardrails stay the same.

**RAG has three steps.** *Data preparation:* clean, chunk, embed, and store documents. *Retrieval:* fetch the most relevant chunks, often with re-ranking. *Generation:* answer from those chunks. `FileSearchTool` hides all three; with your own retriever you own every step. **Fine-tuning changes behavior, not knowledge.** SFT targets tone, style, or format; DPO trains on preferred versus non-preferred answers; RFT targets reasoning models with nuanced goals. None reliably adds facts: outdated prices are fixed by retrieval and a refreshed index, not by fine-tuning on the new price list. OpenAI is also winding down its fine-tuning platform and no longer accepts new users (dates in the [OpenAI track README](../README.md#deprecated-and-retired-do-not-learn-these)).

### 3.4 Handoffs vs agents-as-tools

The Agents SDK has two multi-agent patterns. The question that separates them is **who owns the final, user-facing answer**.

| | **Handoff** | **Agent as tool** |
|---|---|---|
| Control | Moves to the specialist for the rest of the turn | Stays with the manager |
| What the specialist sees | The conversation history (unless you filter it) | Only the input the manager passes |
| Who writes the reply | The specialist | The manager, which synthesizes |
| How you write it | `handoffs=[refund_agent]` (tool `transfer_to_refund_agent`) | `tools=[policy_agent.as_tool(tool_name=..., tool_description=...)]` |
| `result.last_agent` | The specialist | The manager |
| Best for | Routing: triage, then billing or refunds | Bounded subtasks, or combining several specialists |

**Handoffs.** Each specialist's `handoff_description` is the routing signal, so keep them clear and non-overlapping. Wrap an agent in `handoff()` to customize it: `input_type` (structured data the model must supply), `input_filter` (trim the history the next agent sees), `on_handoff` (a callback, for example to open a ticket), and `is_enabled`. **Agents as tools:** by default `as_tool()` exposes one string parameter called `input` and returns the nested agent's final output. Use `parameters=` for structured input, `custom_output_extractor=` to shape what comes back, and `needs_approval=` to require review.

**You can combine them.** A triage agent can hand off to a specialist that calls other agents as tools. You can also orchestrate **in code**: run a classifier agent with a structured `output_type` and pick the next agent with an `if`, chain agents, or run independent agents with `asyncio.gather`. Code orchestration is cheaper and more predictable; model orchestration is more flexible. OpenAI's docs say to start with one agent and split only when a specialist needs different tools, a different approval policy or guardrail, a different model, or clearer routing in traces.

### 3.5 Guardrails and tripwires

Guardrails are automatic checks in your process. A failed check trips a **tripwire**, and the runner stops with an exception you catch.

| Guardrail | Attached to | Runs | On trip |
|---|---|---|---|
| Input (`@input_guardrail`) | `Agent.input_guardrails` or `RunConfig` | On the user input, **only for the first agent of the run** | `InputGuardrailTripwireTriggered` |
| Output (`@output_guardrail`) | `Agent.output_guardrails` or `RunConfig` | On the final output, **only for the agent that produces it** | `OutputGuardrailTripwireTriggered` |
| Tool input (`@tool_input_guardrail`) | `@function_tool(tool_input_guardrails=[...])` | Before **every** call of that function tool | `allow`, `reject_content`, or `raise_exception` |
| Tool output (`@tool_output_guardrail`) | `@function_tool(tool_output_guardrails=[...])` | After every call of that tool | `allow`, `reject_content`, or `raise_exception` |

```python
import json, math
from agents import ToolGuardrailFunctionOutput, tool_input_guardrail

REFUND_LIMIT_USD = 500

@tool_input_guardrail
def refund_limit(data) -> ToolGuardrailFunctionOutput:
    try:
        value = json.loads(data.context.tool_arguments or "{}").get("amount")
        amount = math.nan if isinstance(value, bool) else float(value)
    except (TypeError, ValueError, AttributeError):
        amount = math.nan
    # fail closed: NaN, inf, <= 0 and too-large amounts are all rejected
    if not (math.isfinite(amount) and 0 < amount <= REFUND_LIMIT_USD):
        return ToolGuardrailFunctionOutput.reject_content(  # tool never runs
            f"Refund NOT issued: amounts over ${REFUND_LIMIT_USD} "
            "(or invalid amounts) require human review. "
            "Tell the customer that; do not say it was escalated.")
    return ToolGuardrailFunctionOutput.allow()
# attach: @function_tool(tool_input_guardrails=[refund_limit])
```

Money checks must **fail closed**: every comparison with NaN is `False`, so `if amount > limit: reject` lets NaN through. `reject_content` only blocks the call; it does not escalate or notify anyone. Input and output guardrails return `GuardrailFunctionOutput(output_info=..., tripwire_triggered=...)` and can be plain Python or a small agent with a structured `output_type`.

**Which guardrails to build, and how strong.** OpenAI's track gives two reasons for input guardrails: so the agent can't be jailbroken, and so you don't pay for **irrelevant inputs**. The customer service demo runs a **relevance** and a **jailbreak** guardrail on its triage agent. Size them to the risk: a keyword check for a low-risk FAQ bot, a classifier agent for a public agent, plus tool guardrails and approvals for money or personal data. For outputs: **structured outputs** when your app consumes the result, **output guardrails** when the agent is user-facing.

- **Execution modes:** `run_in_parallel=True` (the default) starts the guardrail and the agent together, so the agent may already have spent tokens **and executed tools** when the tripwire fires. `run_in_parallel=False` finishes the guardrail first.
- **Workflow boundaries:** in triage → specialist, an input guardrail on the specialist never runs, and an output guardrail on triage never runs if triage hands off. Tool guardrails run wherever the guarded function tool lives, but not on handoffs or hosted tools.
- **So:** input guardrails on the entry agent, output guardrails on **every agent that can produce the final answer** (or once in `RunConfig.output_guardrails`, which runs on whichever agent answers), side-effect checks **on the tool**.

> **Exam trap:** "Refunds over $500 must never be issued without a human." A sentence in the instructions is probabilistic. A tool guardrail, a check inside the tool, or an approval is deterministic.

### 3.6 Human review: approvals and resumable state

A guardrail decides automatically. **Human review** pauses the run until a person approves or rejects a sensitive tool call.

```python
import math
from agents import Agent, Runner, function_tool

async def over_200(_ctx, params: dict, _call_id: str) -> bool:
    amount = params.get("amount")                   # per-call policy
    ok = isinstance(amount, (int, float)) and math.isfinite(amount)
    return not (ok and amount <= 200)               # NaN/missing -> ask a human

@function_tool(needs_approval=over_200)    # or needs_approval=True
async def issue_refund(order_id: str, amount: int | float) -> str:
    """Issue a refund for an order."""
    return f"Refunded ${amount:.2f} on {order_id}"

refund_agent = Agent(name="Refund agent", instructions="...",
                     tools=[issue_refund])
result = await Runner.run(refund_agent, "Refund $300 for order A-19")
while result.interruptions:                # paused: not the answer yet
    state = result.to_state()
    for item in result.interruptions:      # ToolApprovalItem
        if reviewer_approves(item.name, item.arguments):   # your UI
            state.approve(item)
        else:
            state.reject(
                item, rejection_message="A supervisor declined this refund.")
    result = await Runner.run(refund_agent, state)   # resume SAME run
```

**An approval is a paused run, not a new turn.** Resume from `state` with the original top-level agent. Store `state.to_string()` for long reviews and rebuild with `await RunState.from_string(agent, s)`. Tool input guardrails normally run **after** approval; `RunConfig(tool_execution=ToolExecutionConfig(pre_approval_tool_input_guardrails=True))` checks policy first. The SDK fails closed around a callable `needs_approval`: if validation changes the arguments (for example a JSON `40` becoming `40.0` for an `amount: float`, or a filled-in default) or can't parse them, it skips your callable and requires manual approval. So type money as `int | float`, and make the callable itself fail closed on bad values. **A serialized `RunState` is not authenticated.** Keep it server-side, authorize the reviewer on your server, and never accept a state blob from a browser.

### 3.7 Conversation state and sessions

The runner is stateless between calls unless you choose a strategy. OpenAI lists four and says to **pick one per conversation**:

| Strategy | State lives in | Next turn you pass |
|---|---|---|
| `result.to_input_list()` | Your app | Full history + new message |
| `session=SQLiteSession("customer_C-42", "conversations.db")` | Your storage, managed by the SDK | The same session + new message |
| `conversation_id=` | OpenAI Conversations API | The same ID + only the new message |
| `previous_response_id=result.last_response_id` | OpenAI Responses API | The last response ID + only the new message |

> **Gotcha:** a session cannot be combined with `conversation_id`, `previous_response_id` or `auto_previous_response_id`; the SDK raises `UserError` if you try. Output guardrails (on the agent or in `RunConfig`) also can't be combined with `conversation_id` / `previous_response_id` on the Responses model, because rejected output can't be removed from server history; use `to_input_list()` or a session when you need output guardrails. `SQLiteSession` without a path is in-memory and per process, so a multi-worker deployment needs a shared backend (Redis, SQLAlchemy, MongoDB) or server-side state.
>
> **Architect note:** after a handoff, pass the specialist (`result.last_agent`) as the starting agent of the next turn if it should stay in control; otherwise every turn starts at triage again. Server-side state means OpenAI stores the conversation; a SQL or Redis session keeps it in your infrastructure.

### 3.8 Tracing and lifecycle hooks

**Tracing is on by default.** Every `Runner.run` is wrapped in a trace with spans for each agent, model generation, function tool call, guardrail, and handoff. View them in the [Traces dashboard](https://platform.openai.com/traces); `with trace("Refund workflow"):` groups several runs into one trace. Tracing is **unavailable for organizations under a Zero Data Retention (ZDR) policy**, and by default spans can contain prompts and tool data.

| Control | Effect |
|---|---|
| `OPENAI_AGENTS_DISABLE_TRACING=1` or `RunConfig(tracing_disabled=True)` | Disable for the process or for one run |
| `RunConfig(trace_include_sensitive_data=False)` | Keep model and tool inputs/outputs out of spans |
| `add_trace_processor(...)` / `set_trace_processors([...])` | Send spans to your own stack, or replace the default exporter |

**Lifecycle hooks** observe a run: `RunHooks` (`Runner.run(..., hooks=...)`) sees the whole run across handoffs, `AgentHooks` (`Agent(hooks=...)`) one agent. Callbacks such as `on_handoff` and `on_tool_start` suit audit logs and metrics. Hooks return nothing: to **block** something, use a guardrail or an approval.

<a id="39-the-managed-agents-api-public-beta"></a>

### 3.9 The managed Agents API (beta)

The Agents API gives your app the **Codex harness as a managed API**. OpenAI runs the loop, keeps the session, compacts context, recovers from interruptions, and optionally provisions a sandbox. You call `client.beta.agents.sessions.create(agent={...}, environment={"type": "none"}, input=...)`; requests carry the `OpenAI-Beta: agents=v1` header. Your function tools run in your app: the session emits `agent.session.requires_action` on the stream (the webhook is `agent.session.action_required`), you run the function and return a `tool_result`. **Pricing:** model usage, OpenAI tools, and hosted sandboxes at standard rates, with no separate Agents API charge listed; check the [pricing page](https://developers.openai.com/api/docs/pricing) because beta pricing can change.

| Concept | Meaning |
|---|---|
| **Agent** | Model, instructions, tools, MCP servers; inline, or saved and reused by `agent_id` |
| **Environment** | `none`, `openai_hosted`, or `self_hosted` (your compute connects an executor) |
| **Session** | A durable instance of an agent. A message to an idle session starts a **turn**; one during a turn **steers** it |
| **Events and items** | Events are live progress (the stream has turn events; webhooks carry only session-level ones); items are the saved messages and tool calls |

> **Gotcha: `idle` is not success.** `agent.session.idle` means the session is ready for more input. Check the turn outcome: on a stream, `agent.session.turn.completed`, `turn.failed` or `turn.cancelled`; with webhooks, retrieve the turn after `agent.session.idle` (`sessions.turns.retrieve` / `list`) and read its `status`. Then check the tool results: a completed turn can contain failed tool calls.
>
> **Gotcha: data controls.** The Agents API currently supports data residency **only in the United States** and does **not** support Zero Data Retention, even with a self-hosted sandbox. A ZDR or EU-residency requirement points back to the Agents SDK or the Responses API. Sandboxes return in [Chapter 4](../04-built-in-tools-and-mcp/README.md); the Codex harness is [Chapter 5](../05-codex/README.md).

### 3.10 Testing agent decisions and handoffs

The Academy course *Design and Build Agentic Systems* frames testing as three steps.

**1. Write the requirements first, as data.**

| Requirement type | Question it answers | Example for the support desk |
|---|---|---|
| **Outcome** | Who must own the reply, and what must it contain? | A refund request ends with the Refund agent |
| **Safety** | What must never happen, and which control must fire? | `issue_refund` never runs for an invoice question; an off-topic input is blocked by an input guardrail |
| **Ownership** | How many times may control move, and from where? | At most one handoff, and only from the triage agent |

**2. Keep one owner at every handoff.** At any moment exactly one agent owns the conversation, and ownership moves only along edges you intended. Give specialists no `handoffs` of their own unless needed, keep `handoff_description`s non-overlapping, and start the next turn from `result.last_agent` if the specialist should keep ownership ([3.7](#37-conversation-state-and-sessions)).

**3. Test decisions against the trace, not only the final text.** Tracing ([3.8](#38-tracing-and-lifecycle-hooks)) records `agent`, `handoff` (`from_agent`, `to_agent`), `function`, and `guardrail` (`name`, `triggered`) spans. Register your own trace processor and assert on them:

```python
from agents import Runner, TracingProcessor, set_trace_processors

class TraceRecorder(TracingProcessor):
    def __init__(self): self.spans = []
    def on_span_end(self, span):
        d = span.span_data
        self.spans.append({"type": d.type, **(d.export() or {})})
    def on_trace_start(self, trace): pass
    def on_trace_end(self, trace): pass
    def on_span_start(self, span): pass
    def shutdown(self): pass
    def force_flush(self): pass

recorder = TraceRecorder()
set_trace_processors([recorder])   # in tests: nothing leaves the machine

async def test_refund_request_is_owned_by_refund_agent():
    recorder.spans.clear()
    r = await Runner.run(triage_agent, "I want my money back for order A-17")
    handoffs = [(s["from_agent"], s["to_agent"])
                for s in recorder.spans if s["type"] == "handoff"]
    tools = [s["name"] for s in recorder.spans if s["type"] == "function"]
    assert r.last_agent.name == "Refund agent"               # outcome
    assert handoffs == [("Triage agent", "Refund agent")]    # ownership
    assert "lookup_invoice" not in tools                     # safety
```

For a guardrail case, send an off-topic input, catch `InputGuardrailTripwireTriggered`, and assert a `guardrail` span with your guardrail's `name` and `triggered` true. Test **offline first**: a scripted stand-in model (the notebooks' `ScriptedModel`) tests the wiring deterministically in CI. **Then live, with repetition:** run each case several times on the real model and track the pass rate per requirement (graded evals are [Chapter 6](../06-prompt-engineering-and-evals/README.md)). In openai-agents 0.23.1, tool guardrails create no spans; read `result.tool_input_guardrail_results` and `result.tool_output_guardrail_results`.

> **Exam trap:** "The refund test passes because the final reply came from the Refund agent." That checks the outcome but not ownership or safety. Assert on the handoff and function spans too.

## Lesson code

Video-lesson code: [../../presentations/03-agent-sdk/code/openai_lesson4.py](../../presentations/03-agent-sdk/code/openai_lesson4.py)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Work through 3.1–3.10 offline with a scripted model, then build a triage desk with billing and refund specialists, guardrails, approvals, an audit hook, and a session |
| [`02_homework.ipynb`](02_homework.ipynb) | 10 quiz questions, 6 auto-graded exercises plus 1 optional live one, and an architecture scenario |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| One-shot extraction, classification, or a single chat turn | Responses API (+ Structured Outputs) | Agents SDK |
| Agent with your own tools, storage, and approval UI | Agents SDK | Agents API |
| Long-running, file- or shell-heavy task with managed sessions and a sandbox | Agents API (beta) | Hand-rolled loop + your own sandbox |
| ZDR or non-US data residency is a hard requirement | Agents SDK or Responses with your own storage | Agents API |
| Specialist should answer the user directly | Handoff | Agent as tool |
| Manager must combine several specialists into one answer | Agents as tools | Handoffs |
| Rule with financial, legal, or safety impact on a tool | Tool input guardrail or a check inside the tool | Instructions |
| Action needs a human decision | `needs_approval` + `interruptions` + `RunState` | A "please confirm" chat message |
| Output must never contain card numbers, whoever answers | Output guardrail on **every** agent that can produce the final output, or once in `RunConfig.output_guardrails` | One guardrail on the triage agent |
| Agent must answer from documents that change | Retrieval tool: `FileSearchTool` or your own `search_kb` | Fine-tuning on the documents |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Text-based completion detection**, or treating `max_turns` as "done". `MaxTurnsExceeded` is an error.
- **Relying on the SDK's default model.** In 0.23.1 the fallback is `gpt-5.6-luna`. Set `model` yourself.
- **Handoffs when the manager must synthesize**, or agents-as-tools when the specialist should own the conversation.
- **Input guardrail on a specialist** reached by handoff (it never runs), or **output guardrail only on triage** (it never runs once triage hands off).
- **Business rules only in `instructions`** (refund limits, identity checks). They will be skipped in some fraction of runs.
- **Resuming an approval as a new user message**, or trusting a `RunState` blob from the client.

## Self-check

**Q1.** A support app routes every message through a triage agent. For refund questions, the refund specialist should talk to the customer directly for the rest of the turn. Which pattern fits?

- A) `refund_agent.as_tool()` on the triage agent
- B) `handoffs=[refund_agent]` on the triage agent
- C) A tool input guardrail that redirects refund questions
- D) A second `Runner.run` call started from a lifecycle hook

<details><summary>Answer</summary>

**B.** A handoff moves ownership to the specialist, which then produces the final output (`result.last_agent` is the refund agent). A keeps the triage agent in control and makes it rewrite the answer. C and D misuse guardrails and hooks, which validate and observe; they don't route.
</details>

**Q2.** A research manager calls three specialists (pricing, competitors, regulations) and must merge their findings into one report. Which design is correct?

- A) Triage agent with handoffs to all three
- B) Manager agent with the three specialists exposed via `Agent.as_tool()`
- C) Chain three handoffs: pricing → competitors → regulations
- D) One agent with all three specialists' instructions concatenated

<details><summary>Answer</summary>

**B.** Agents as tools keep the manager in control so it can synthesize. With handoffs (A, C) control leaves the manager, so nothing merges the results. D loses the separation of tools and prompts that justified specialists in the first place.
</details>

**Q3.** You attached an input guardrail that blocks prompt-injection attempts to the **billing** agent. Billing is only reached through a handoff from triage. Logs show the guardrail never runs. Why, and what is the fix?

- A) Guardrails only run in streaming mode; switch to `run_streamed`
- B) Input guardrails run only for the first agent of a run; attach it to the triage agent (or `RunConfig.input_guardrails`)
- C) `run_in_parallel` must be `True`
- D) Handoffs disable all guardrails; use agents-as-tools

<details><summary>Answer</summary>

**B.** Input guardrails run on the user input for the first agent only. A and C are false. D is false: output guardrails still run on the final agent and tool guardrails still run on guarded function tools.
</details>

**Q4.** Refunds above $500 must never be issued without a human. After instruction changes, 3% of runs still issue large refunds. What should you do?

- A) Add few-shot examples of refusing large refunds
- B) Add `needs_approval` (or a tool input guardrail) on `issue_refund` that pauses or rejects calls above $500
- C) Add an output guardrail on the triage agent
- D) Lower `max_turns` so the agent has fewer chances to call the tool

<details><summary>Answer</summary>

**B.** A deterministic check on the tool that creates the side effect. A is still probabilistic. C runs on the wrong agent and after the money has moved. D does not stop a single bad call.
</details>

## Official documentation

- [Agents overview: compare the Agents API, Agents SDK, and Responses API](https://developers.openai.com/api/docs/guides/agents)
- [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents/sdk)
- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [Python SDK reference site](https://openai.github.io/openai-agents-python/)
- [Agents API (beta) overview](https://developers.openai.com/api/docs/guides/agents-api/overview)
- [Deprecations](https://developers.openai.com/api/docs/deprecations)

[← Chapter 2 — Function Calling and Structured Outputs](../02-function-calling-and-structured-outputs/README.md) | [↑ OpenAI path](../README.md) | [Chapter 4 — Built-in Tools and MCP →](../04-built-in-tools-and-mcp/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
