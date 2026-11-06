# Chapter 9 — Escalation and Human-in-the-Loop

> **Claude counterpart:** [Chapter 9 — Escalation and Human-in-the-Loop](../../anthropic-claude/09-escalation-human-in-the-loop/README.md) · **Academy course(s):** Design and Build Agentic Systems (API pathway, 110 min), Scope AI Solutions (API pathway, 30 min) · **Est. time:** 6–8 hours (reading + 2 notebooks) · **Status:** [ ] not started

Every agent that touches money, accounts or customer commitments needs a defined way to stop and hand control to a person. This chapter answers four design questions: **when** the agent should stop, **who** enforces the stop (the prompt, a guardrail, or code), **how** a paused run survives a review that takes hours, and **what** the human receives. The concepts match the Claude chapter; the new material is how to build them with the Responses API and the Agents SDK.

## What you'll learn

- Which escalation triggers work (explicit request, policy gap, failure threshold, high-risk action, ambiguous identity), and why sentiment and self-reported confidence don't.
- How to escalate with a strict `escalate_to_human` tool, `StopAtTools` and `error_handlers` for `max_turns`.
- Where each rule belongs: instructions, input/output guardrails, tool input guardrails, human approval, or a check in the tool.
- How to gate a tool with `needs_approval` (or MCP `require_approval`), pause on `result.interruptions`, store the `RunState` on the server and resume the same run.
- How to build a self-contained handoff, calibrate a confidence threshold on labeled data, and audit with stratified sampling.

## Prerequisites

- [00 — Prerequisites](../../00-prerequisites/README.md) (Python env, `.env` with `OPENAI_API_KEY`) and the previous chapter, [Chapter 08 — Task decomposition and orchestration](../08-task-decomposition-and-orchestration/README.md).
- [Chapter 03 — Agents SDK and Agents API](../03-agents-sdk-and-agents-api/README.md) (guardrail basics 3.5, first look at approvals 3.6), [Chapter 02 — Function calling and Structured Outputs](../02-function-calling-and-structured-outputs/README.md), [Chapter 04 — Built-in tools and MCP](../04-built-in-tools-and-mcp/README.md), [Chapter 06 — Prompt engineering and evals](../06-prompt-engineering-and-evals/README.md).

## Concepts

A request either stays with the agent, is blocked by a deterministic rule, pauses for a human decision, or is handed to a human with a summary. Afterwards a sample of the automated work goes to human audit. Snippets assume `import json`, `import os`, `from agents import Agent, Runner` and `MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")`. API names were checked against `openai-agents` 0.23.1 and `openai` 3.24; re-check them against the [human-in-the-loop docs](https://openai.github.io/openai-agents-python/human_in_the_loop/) when you upgrade. The notebooks run offline on `agents.testing.ScriptedModel`.

### 9.1 When to escalate

Escalation rules should be **observable conditions** that code or a clear instruction can check, not feelings:

| Trigger | Example | What the agent does | Who enforces it |
|---|---|---|---|
| **Explicit request for a human** | "Get me a manager." | Escalate immediately | Instruction + `escalate_to_human`; optionally a blocking input guardrail (9.3) |
| **Policy gap** | "Another shop offers free next-day delivery. Give me that too." | Escalate. Don't invent policy | Instruction listing what the policy covers |
| **Failure threshold** | Intent unclear after 2 clarifying questions; `max_turns` reached | Escalate after bounded attempts | Counters in code; `error_handlers` (9.2) |
| **High-risk action** | Refund above $100, cancellation, payment | Pause for approval or block | `needs_approval`, tool guardrail, check in the tool (9.3, 9.4) |
| **Ambiguous identity** | Customer search returns 3 matches | Ask for another identifier. Never guess; escalate with `identity_ambiguous` only if the customer can't provide one | Tool returns all matches; instruction says "ask, don't pick" |

OpenAI's [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) names two primary triggers: **exceeding failure thresholds** and **high-risk actions** that are "sensitive, irreversible, or have high stakes". It also suggests a **risk rating per tool** (low, medium, high) based on read vs write access, reversibility, permissions and financial impact. Put that rating in the solution plan, before anyone writes a prompt. For example: `lookup_order` is low (ownership check in the tool), `issue_refund` up to $100 is medium (policy gate, 9.3), above $100 is high (gate + human approval, 9.4), and above $500 is blocked for the agent (the gate rejects; the agent must escalate).

**Weak triggers.** Sentiment fails because mood doesn't track case complexity. "This is ridiculous, I'm so frustrated!" is **not** a request for a human: acknowledge it, offer a concrete fix, and escalate if the customer then asks for a person. "I want to talk to a human" **is**: escalate on that turn. Self-reported confidence ("rate 1–10") fails because the number is not calibrated (9.8). A custom-trained escalation classifier as the first step is over-engineering: start with explicit rules and log every escalation.

**Conflicting user statements.** If two earlier statements pull in opposite directions ("cheapest option" in one turn, "it must arrive by Friday" in another, and only express shipping arrives in time), say so and ask which one wins. Don't average them or pick one silently.

**Don't over-ask.** Ask first when a wrong guess is costly: identity, money, or an action you can't undo. For a low-risk, reversible request, state the assumption in one line, go ahead, and invite correction. Every question costs the user a turn, and the failure threshold above counts them.

### 9.2 Escalation patterns and the escalate tool

Escalation is a **tool the model can call**, and the instructions say when. The four patterns are: immediate ("get me a manager"), after an attempt (offer a fix, escalate if declined), acknowledge → resolve → escalate on reiteration, and policy gap (reason `policy_gap`). The Agents SDK adds two pieces: `StopAtTools` ends the run when the escalate tool fires, and `error_handlers` turns "ran out of turns" into an escalation instead of a `MaxTurnsExceeded` exception.

```python
from agents import ModelSettings, StopAtTools, function_tool

@function_tool
def escalate_to_human(handoff: HumanHandoff) -> str:  # schema: see 9.7
    """Hand the case to a human agent."""
    ticket_id = create_ticket(handoff.model_dump())  # your ticketing system
    return json.dumps({"ticket_id": ticket_id})

support_agent = Agent(
    name="Support agent",
    instructions=INSTRUCTIONS,  # lists the escalation triggers above
    model=MODEL,
    tools=[lookup_order, issue_refund, escalate_to_human],
    model_settings=ModelSettings(parallel_tool_calls=False),
    tool_use_behavior=StopAtTools(stop_at_tool_names=["escalate_to_human"]),
)
```

With `StopAtTools`, `final_output` is the escalate tool's return value and no further model call happens. For the failure threshold, call `Runner.run(support_agent, user_text, max_turns=8, error_handlers={"max_turns": escalate_on_max_turns})`. The handler receives `data.run_data` (new items, history, last agent) and returns `RunErrorHandlerResult(final_output={"route": "human", ...})` with a `cannot_progress` ticket.

> **Gotcha: `StopAtTools` does not cancel sibling calls in the same response.** The SDK runs every tool call in a response first. If one response contains `escalate_to_human` **and** `issue_refund`, the refund still runs. Close the gap with `parallel_tool_calls=False` (it "ensures exactly zero or one tool is called") plus a code check: an `AgentHooks.on_llm_end` hook sets `ctx.context.escalating = True` when the response contains `escalate_to_human`, before any tool executes, and the policy gate (9.3) rejects every side-effect tool while that flag is set (practice notebook, 9.3).

### 9.3 Enforcement vs prompt guidance: guardrails and policy gates

Instructions are **probabilistic**: fine for tone, not for "never refund more than $500". **Money, identity, compliance and safety go into code.**

| Control | Runs | Good for | On failure |
|---|---|---|---|
| `@input_guardrail` | On user input, **first agent only** | Human request, off-topic, injection | `InputGuardrailTripwireTriggered` |
| `@output_guardrail` | On the final output | Unapproved promises, PII leaks | `OutputGuardrailTripwireTriggered` |
| `@tool_input_guardrail` | Before each call of that function tool | Ownership, limits, duplicates | `reject_content(msg)`: tool skipped, model reads `msg` |
| Check inside the tool | When the tool executes | Last line of defense | Return a structured error |

A deterministic policy gate reads the raw arguments and your run context. The customer ID comes from your auth layer (a `SupportCtx` dataclass), never from the model. Check the **lower** bound too: `amount > limit` lets `-50` through, and `NaN` fails every comparison.

```python
from agents import ToolGuardrailFunctionOutput, tool_input_guardrail

HARD_LIMIT_USD = 500  # above this, the agent may not refund at all
reject = ToolGuardrailFunctionOutput.reject_content

@tool_input_guardrail
def refund_policy_gate(data) -> ToolGuardrailFunctionOutput:
    ctx = data.context.context  # SupportCtx: customer_id from auth
    if getattr(ctx, "escalating", False):  # set by the 9.2 hook
        return reject("You are handing this case to a human. Do not refund now.")
    try:
        args = json.loads(data.context.tool_arguments or "{}")
    except json.JSONDecodeError:
        args = None
    if not isinstance(args, dict):  # fail closed, never raise
        return reject("Malformed refund request. Try again.")
    order = ORDERS.get(args.get("order_id"))
    amount = args.get("amount_usd")
    if order is None or order["customer_id"] != ctx.customer_id:
        return reject("Order not found for this customer. Ask again.")
    if not valid_amount(amount):  # real, finite, positive; not bool or NaN
        return reject("The refund amount must be a positive number.")
    if order["refunded"]:
        return reject("This order was already refunded.")
    if amount > order["total_usd"] or amount > HARD_LIMIT_USD:
        return reject(f"Refunds above the order total or ${HARD_LIMIT_USD} "
                      "need a human. Call escalate_to_human with "
                      "escalation_reason='policy_limit'.")
    return ToolGuardrailFunctionOutput.allow()
```

Repeat the checks inside the payment service, so neither an approval nor an outside caller can make an invalid refund valid.

**Blocking input guardrail.** To let "talk to a human" bypass the model, use `@input_guardrail(run_in_parallel=False)`, so the agent spends no tokens and runs no tools before the tripwire fires. Attach it to the first agent, catch `InputGuardrailTripwireTriggered` and route to a human. A regex is cheap but naive ("my manager bought this" matches); a small guardrail agent with a structured `output_type` is the alternative. Measure either one on a labeled set of real messages before you trust it.

**Workflow boundaries.** Input guardrails run only on the **first** agent, output guardrails only on the agent that produces the final output, and tool guardrails only on the **function tools** they're attached to. They don't run on handoffs or hosted tools. Put side-effect checks on the tool that has the side effect.

**Layered defense.** OpenAI's practical guide says a single guardrail "is unlikely to provide sufficient protection". Combine a rules-based check, an LLM classifier and the free Moderation API, and scale the layers to the risk: a read-only FAQ agent may need only moderation and a relevance check; an agent that moves money also needs a jailbreak classifier, tool gates and approvals.

### 9.4 Approval-gated tools in the Agents SDK

A guardrail decides automatically. An **approval** pauses the run until a person decides. The model still chooses the action; your application decides whether it happens.

```python
from agents import RunContextWrapper, function_tool

AUTO_LIMIT_USD = 100  # above this, a human approves

async def needs_human(ctx: RunContextWrapper[SupportCtx], params: dict,
                      call_id: str) -> bool:
    amount = params.get("amount_usd")  # per call; valid_amount from 9.3
    return not valid_amount(amount) or amount > AUTO_LIMIT_USD

@function_tool(needs_approval=needs_human,
               tool_input_guardrails=[refund_policy_gate])
def issue_refund(ctx: RunContextWrapper[SupportCtx], order_id: str,
                 amount_usd: float) -> str:
    """Refund one of the customer's orders. Amount in USD, more than 0
    and at most the order total."""
    # your payment service re-checks ownership, amount and limits
    return json.dumps(payments.refund(ctx.context.customer_id,
                                      order_id, amount_usd))
```

When a call needs approval, the tool doesn't run. `Runner.run` **returns** with `final_output = None` and `result.interruptions` holding `ToolApprovalItem`s (`.name`, `.arguments`, `.call_id`, `.agent`). You call `state = result.to_state()`, then `state.approve(item)` or `state.reject(item, rejection_message="...")`, and resume with `Runner.run(original_top_level_agent, state)`. It's the **same run**, not a new user turn.

| Feature | API | Note |
|---|---|---|
| Ask per call | `needs_approval=async fn(ctx, params, call_id)` | **Fails closed:** missing, malformed or non-object arguments skip your callable and require manual approval, and so do arguments the SDK would coerce (e.g. `39` for a `float`) |
| Sticky decision | `approve(item, always_approve=True)` / `always_reject=True` | Later calls of that tool by the same agent for the rest of this run; survives serialization |
| Nested approvals | Tool behind a handoff or `Agent.as_tool()` | Surfaces on the **outer** result; resume the top-level agent |
| Realtime | `RealtimeSession.approve_tool_call(call_id)` / `reject_tool_call(...)` | Same idea for voice agents |

**Guardrail before or after the human?** By default, tool input guardrails run **after** approval, so a reviewer can be asked to approve a $900 refund the gate would reject anyway. `RunConfig(tool_execution=ToolExecutionConfig(pre_approval_tool_input_guardrails=True))` runs the gate first, so reviewers see only calls that policy allows.

### 9.5 Pause, serialize, resume: long-running reviews

Real reviews take minutes to days, and your process will restart in between. `RunState` is designed to be durable:

```python
from datetime import timedelta
from agents import RunState
# RUN_CONFIG = RunConfig(tool_execution=ToolExecutionConfig(
#     pre_approval_tool_input_guardrails=True))  (9.4)

# 1. The run pauses: store the snapshot server-side under an opaque ID
if result.interruptions:
    review_id = reviews.create(
        state=result.to_state().to_string(),  # or .to_json()
        customer_id=ctx.customer_id,          # your SupportCtx
        agent_version="refund-desk@3",        # your version marker
        expires_at=now() + timedelta(hours=24),
    )
# 2. Later, in another process, through YOUR authenticated endpoint
async def on_decision(reviewer, review_id: str, decisions: dict) -> None:
    review = reviews.claim(review_id, reviewer)  # authZ, version, once
    agent = agent_for(review.agent_version)
    state = await RunState.from_string(agent, review.state,
        context_override=SupportCtx(customer_id=review.customer_id))
    for item in state.get_interruptions():       # server-owned items
        if decisions.get(item.call_id) is True:
            state.approve(item)
        else:                                    # fail closed
            state.reject(
                item, rejection_message="A supervisor declined this refund.")
    result = await Runner.run(agent, state, run_config=RUN_CONFIG)
    reviews.complete(review_id, result)
```

`RunState.from_string` and `from_json` are **async**. A snapshot holds pending tool calls, decisions, usage, server conversation settings and **your context object**. The docs say deserialization does "not authenticate the snapshot or the person submitting it". So keep the snapshot on the server, authenticate and authorize the reviewer from your session, apply decisions only to `state.get_interruptions()` from the stored snapshot, consume each review once (atomic `pending → resuming`, so a replay can't issue two refunds), keep secrets out of the context (or drop them with a `context_serializer`), and fail closed on timeout.

> **Gotcha: version drift and retention.** Each snapshot carries a `$schemaVersion`; older SDKs reject newer snapshots, and prompts and tools can change while a review waits. Store your own version marker and route resumes to matching code. Stored responses are kept for 30 days by default (Chapter 1). A resume that relies on `previous_response_id` after that will likely fail (our inference; the SDK docs don't cover it), so longer queues should use local history or a session.

### 9.6 MCP approvals: `require_approval` and `mcp_approval_request`

| Surface | Configure | You receive | You answer with |
|---|---|---|---|
| Responses API remote `mcp` tool | `require_approval`: `"always"`, `"never"` or `{"never": {"tool_names": [...]}}` (on **by default**) | `mcp_approval_request` item | `mcp_approval_response` with `previous_response_id` |
| Agents SDK local MCP server | `require_approval=` on the server | `result.interruptions` | `state.approve` / `state.reject` (9.4) |
| Agents SDK `HostedMCPTool` | `tool_config={..., "require_approval": "always"}` | Interruptions, or `on_approval_request` | Manual, or the callback returns `{"approve": bool, "reason": str}` |

```python
followup = client.responses.create(
    model=MODEL,
    tools=[crm_mcp_tool],  # resend the FULL tool config
    previous_response_id=response.id,
    input=[{"type": "mcp_approval_response",
            "approval_request_id": request_item.id,  # the mcpr_... id
            "approve": reviewer_said_yes}],  # optional: "reason"
)
```

Use a **split policy**: skip approvals only for read-only tools of a trusted server, and keep every write on approval. **Exam trap:** `on_approval_request` and `require_approval: "never"` are **not** human-in-the-loop. They are automated decisions; a callback that approves everything removes the protection.

### 9.7 Structured handoff to a human

The human usually sees **only the handoff**, not the transcript. Make it complete and self-contained, and use it as the escalate tool's argument type, so `function_tool` makes it a strict schema:

```python
from typing import Literal
from pydantic import BaseModel, Field

class HumanHandoff(BaseModel):
    customer_id: str
    order_id: str | None               # null if no order is involved
    escalation_reason: Literal[
        "customer_requested_human", "policy_gap", "policy_limit",
        "cannot_progress", "identity_ambiguous"]
    issue_summary: str = Field(
        description="2-3 sentences a human can act on without the transcript")
    customer_request: str = Field(
        description="What the customer wants, in their terms")
    actions_taken: list[str]
    amount_usd: float | None
    recommended_action: str
    customer_sentiment_note: str | None  # context, NOT a routing signal
```

A strict schema guarantees the shape, not the truth. **Fill facts from the run, not the model's memory.** The model writes the summary, request and recommendation. Your code sets `customer_id` from the authenticated context, builds `actions_taken` from the run's `new_items` (tool calls and outputs), and nulls any `order_id` the customer doesn't own. `new_items` holds only this run's items, so in a multi-turn conversation keep a server-side action ledger.

> **Gotcha:** Escalation is not an SDK handoff. An Agents SDK **handoff** transfers the conversation to another **agent**. Handing a case to a **human** means leaving the agent loop: a ticket, a queue, a CRM case. The deliverable for the person is still this structured summary.

### 9.8 Confidence calibration with labeled sets

Pipelines route on a **confidence score**: high goes straight through, low goes to a person. The score is useful only if it's **calibrated** (items scored 0.9 are about 90% correct), and only a **labeled validation set** tells you that. Signals on OpenAI: a model-reported `confidence` field (not calibrated), token logprobs (only with reasoning effort `none`: GPT-6.1 Terra, GPT-6 Sol and GPT-6 Luna; not GPT-6 Astra or GPT-6.1 Sol; not calibrated by default), agreement between independent runs (correlates, still measure), and deterministic checks such as totals adding up (strong evidence of an error when they fail).

Procedure: build a labeled set that looks like production; tabulate accuracy per score bin; pick the **lowest threshold** that reaches your target precision **per field**, with a minimum number of items; re-check on a held-out split and re-calibrate when the model, prompt or document mix changes. Target precision comes from the cost of an error, and the share of items below the threshold is your human-review workload. Put both numbers in the solution plan.

```python
def pick_threshold(scored: list[tuple[float, bool]],
                   target_precision: float = 0.98,
                   min_support: int = 50) -> float | None:
    """scored: (confidence, was_correct) pairs for ONE field."""
    for t in sorted({s for s, _ in scored}):
        above = [ok for s, ok in scored if s >= t]
        if len(above) < min_support:
            break                  # too few items to trust the estimate
        if sum(above) / len(above) >= target_precision:
            return t               # everything >= t goes straight through
    return None                    # no safe threshold: review this field
```

### 9.9 Stratified sampling for human review

You also need to keep checking the **high-confidence** items nobody reviews, because aggregate accuracy hides weak segments: a 97% overall score can include a small document type that is wrong 3 times in 10. **Stratified random sampling** splits the automated output into strata (document type × field × confidence band) and samples every stratum, with a minimum per stratum. **Report accuracy per stratum.** A stratum below target gets a higher threshold or full review until the cause is fixed. Every corrected item becomes a new labeled case for the eval set and the next calibration (9.8).

```python
import random
from collections import defaultdict

def stratified_sample(items: list[dict], strata_keys: tuple[str, ...],
                      rate: float = 0.02, min_per_stratum: int = 20,
                      seed: int = 7) -> list[dict]:
    rng = random.Random(seed)  # reproducible audit
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for item in items:
        groups[tuple(item[k] for k in strata_keys)].append(item)
    sample = []
    for _, group in sorted(groups.items()):
        n = min(len(group), max(min_per_stratum, round(rate * len(group))))
        sample.extend(rng.sample(group, n))
    return sample
```

### 9.10 Operating human-in-the-loop in production

| Concern | What to do |
|---|---|
| **Audit trail** | Log every approval request and decision: reviewer, time, tool, arguments, decision, resulting output |
| **Metrics** | Escalation rate by reason, approval vs rejection rate, time to decision, expired reviews. 99% approvals suggests the threshold is too low; many rejections suggest a prompt or gate problem |
| **Graduated autonomy** | Start with more approvals; raise thresholds only when metrics and the stratified audit support it |
| **Timeouts and outages** | Expire reviews, fail closed, tell the customer what happens next |
| **Platform stops** | A `403` with code `misalignment_policy_violation` (GPT-6 Astra): stop dispatching actions, don't auto-retry, route to a human. Match the code, not the message |
| **Separation of duties** | The approver must not be the one whose account receives the refund. Your authorization layer enforces this |

## Lesson code

Video-lesson code: [../../presentations/09-escalation/code/](../../presentations/09-escalation/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run 9.1–9.10 offline on `ScriptedModel`, then build the approval-gated refund desk (policy gate, `needs_approval`, server-side review store, resume). |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 auto-checked exercises, an insurance-claims architecture scenario and a scorecard (pass mark 72%). |

## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Customer explicitly asks for a person | Escalate on that turn (`escalate_to_human`, or a blocking input guardrail) | Trying to solve it first | Explicit request is the clearest trigger |
| Agent loops without progress | `max_turns` + `error_handlers` → escalation; counters for clarifications | Raising `max_turns` | Bounded attempts, then a human |
| Escalation must not coincide with an action | `StopAtTools` + `parallel_tool_calls=False` + a code check | `StopAtTools` alone | It doesn't cancel sibling calls in the same response |
| Hard business limit (refund cap, ownership) | Tool input guardrail and a check in the tool | A rule in the instructions | Deterministic vs probabilistic |
| Allowed but high-risk action | `needs_approval` (callable per amount/risk) | Always-on approval for every call | Reviewers' time goes where risk is |
| Review may take hours or days | Store `state.to_string()` server-side, resume with `RunState.from_string` | Keeping the process waiting, or sending the blob to the client | Survives restarts; snapshots are not authenticated |
| Remote MCP server with read and write tools | `require_approval: {"never": {"tool_names": [read-only]}}`, writes approved | `"never"` for the whole server | Human gate exactly where risk is |
| Human needs to act on an escalation | Strict handoff schema, facts filled from the run | Forwarding the raw transcript | Self-contained, verifiable |
| Auto-approve extractions by confidence | Per-field threshold calibrated on a labeled set | A self-rated 1–10 cutoff | Only calibration tells you what a score means |
| High overall accuracy reported | Stratified audit sample with per-stratum minimums | Trusting the aggregate | Small segments hide large error rates |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Escalating on sentiment**, or auto-approving on self-reported confidence or one global threshold chosen without a labeled set.
- **Enforcing limits with instructions** instead of a guardrail or a check in the tool, or checking only upper bounds (a negative or `NaN` amount passes `amount > limit`).
- **Trusting `StopAtTools` to cancel other calls** in the same model response.
- **Resuming an approval by sending a new user message** instead of `Runner.run(agent, state)`.
- **Sending the serialized `RunState` to the browser**, accepting decisions or state from the client, or failing **open** when a review times out.
- **Handing the human a transcript dump**, or an `actions_taken` list written from the model's memory instead of the run log.

## Self-check

**1.** A customer writes: "Your app charged me twice and I'm furious. This is the worst service ever." The agent's instructions say to escalate when customers are upset. What should the architect change?

- A) Nothing; anger is a reliable signal of a hard case
- B) Acknowledge the frustration, look up the charges and offer a fix; escalate if the customer asks for a person, the policy doesn't cover the case, or the agent can't resolve it
- C) Add a sentiment classifier and escalate above a negativity score of 0.8
- D) Ask the model to rate its confidence and escalate below 7

<details><summary>Answer</summary>

**B.** Sentiment doesn't track complexity, and this is a simple duplicate charge. C and D are the two weak triggers from 9.1: sentiment and uncalibrated self-reported confidence.
</details>

**2.** Refunds above $500 must never be issued by the agent. The current design states this in the refund agent's instructions, and logs show two violations last month. Which change enforces the rule?

- A) Repeat the rule in capital letters at the start and the end of the instructions
- B) A tool input guardrail on `issue_refund` that returns `reject_content` above $500 (telling the model to escalate), plus a check inside the tool
- C) An input guardrail on the refund agent that searches the user message for amounts above $500
- D) Switch to `gpt-6-astra`, which follows instructions more reliably

<details><summary>Answer</summary>

**B.** It's deterministic and sits on the tool that creates the side effect. A is still probabilistic. C checks the user's text, not the tool arguments, and only runs if the refund agent is the first agent of the run. D improves the odds but guarantees nothing.
</details>

**3.** `issue_refund` has `needs_approval=True`. A run returns with `result.interruptions` containing one `ToolApprovalItem`. The supervisor approves in the review UI. How should the application continue?

- A) Send the customer's next message with `Runner.run(agent, "approved")`
- B) `state = result.to_state()`, `state.approve(item)`, then `Runner.run(original_top_level_agent, state)`
- C) Call `issue_refund` directly, then start a new run with the refund result
- D) Re-run the original input with `needs_approval=False`

<details><summary>Answer</summary>

**B.** An approval resumes the same paused run. A creates a new turn and loses the pending call. C bypasses the agent's history and the SDK's bookkeeping. D removes the control and re-executes the whole run.
</details>

**4.** An invoice pipeline auto-approves fields whose model-reported confidence is at least 0.9. Overall accuracy on auto-approved fields is 97%. An audit finds that handwritten delivery notes (4% of volume) have 30% wrong amounts. What is the right design?

- A) Raise the global threshold to 0.95 for all fields
- B) Calibrate thresholds per field on a labeled set, and run stratified sampling (document type × field × confidence band, with a minimum per stratum) on auto-approved items; route weak strata to review until fixed
- C) Ask the model to be more careful with handwriting
- D) Review a uniform random 1% of all documents

<details><summary>Answer</summary>

**B.** Calibration tells you what a score means per field, and stratification makes small segments visible. A changes the threshold without data and still hides the segment. C is a prompt hope. D would draw very few handwritten notes, so the problem stays invisible.
</details>

## Official documentation

- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals): choosing a control, blocking guardrails, approval lifecycle, workflow boundaries
- [Agents SDK (Python): Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/): `needs_approval`, interruptions, long-running approvals, serialization
- [Agents SDK (Python): Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [MCP servers](https://developers.openai.com/api/docs/guides/tools-connectors-mcp): `require_approval`, `mcp_approval_request` / `mcp_approval_response`
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF): layered guardrails, tool risk ratings, human intervention
- [Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices): human in the loop, moderation, adversarial testing

---

[← Chapter 08 — Task decomposition and orchestration](../08-task-decomposition-and-orchestration/README.md) | [↑ OpenAI path](../README.md) | [Chapter 10 — Error handling in multi-agent systems →](../10-multi-agent-error-handling/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
