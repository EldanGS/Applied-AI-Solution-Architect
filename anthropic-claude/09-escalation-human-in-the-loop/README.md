# Chapter 9 — Escalation and Human-in-the-Loop

> **Exam domain(s):** Domain 5 — Context Management & Reliability (**15%**, tasks 5.2 escalation and ambiguity, 5.5 human review and confidence calibration) · Domain 1 — Agentic Architecture & Orchestration (**27%**, task 1.4 enforcement and handoff; reinforces 1.5 hooks) · touches Domain 4 (4.1 report/skip criteria, 4.3 `"unclear"` values, 4.6 confidence on findings)
> **Est. time:** 6–8 hours (reading + 2 notebooks) · **Status:** [ ] not started

<a id="why-this-matters-for-a-solution-architect"></a>
Every production agent meets cases it should not handle alone: a refund above its authority, a request the policy doesn't cover, a customer who wants a person. What makes a system trustworthy is what happens at that boundary. Your job is to put each decision in the right layer: **the prompt** owns judgment, **your code** owns guarantees (identity before money, amount limits, a fallback escalation), and **humans** own the exceptions and the labeled data that shows whether automation works.

<a id="learning-objectives"></a>
## What you'll learn

- The three appropriate escalation triggers (explicit request, policy gap, no progress), plus code-owned thresholds, and why sentiment and self-rated confidence are poor triggers
- The four conversational escalation patterns, and asking instead of guessing when a request is ambiguous
- How to enforce workflow order and limits in code (gates, `PreToolUse` hooks, tokens), because prompts have a non-zero failure rate
- Which human-approval mechanism to use on each Claude surface, and how to write a self-contained handoff summary
- How to calibrate field-level confidence, analyze accuracy per segment, keep a stratified audit sample, and measure the escalation system

## Prerequisites

- [Chapter 2 — Tool Use](../02-tool-use/README.md) (tool loop, `is_error`, strict schemas) and [Chapter 3 — Agent SDK](../03-agent-sdk/README.md) ([3.5 Hooks in the Agent SDK](../03-agent-sdk/README.md#35-hooks-in-the-agent-sdk))
- [Chapter 6 — Prompt Engineering](../06-prompt-engineering/README.md) (few-shot, validation) and [Chapter 8 — Task Decomposition](../08-task-decomposition/README.md) (multi-concern requests)

## Concepts

### 9.1 When to escalate

An escalation is an architectural decision, not a feeling. The exam (task 5.2) names three appropriate triggers. Code adds a fourth.

| Trigger | Example | What the agent does | Who decides |
|---|---|---|---|
| **Customer explicitly asks for a human** | "Get me a manager." | Escalate **immediately**, without investigating first | Prompt |
| **Policy gap or exception** | Policy covers own-site price drops; customer wants a *competitor's* price | Escalate. Don't invent policy | Prompt (criteria + examples) |
| **No meaningful progress** | Identity unverified after asking twice; a backend keeps failing; two offers rejected | Escalate after a **bounded** number of attempts | Prompt + a counter in code |
| **Business limit** | Refund above $500; account closure | Block the action, route to a human | **Code** (9.4) |

What does **not** trigger escalation:

- **Complexity alone.** A damaged item with photo proof is a standard replacement, even if the story is long.
- **Negative sentiment.** Mood does not predict complexity. An angry customer with a broken blender needs a replacement, not a manager. (Sentiment is fine to *measure* as an outcome; it is poor to *route on*.)
- **The model's self-rated confidence (1–10).** The model can be confidently wrong, and its verbal scores are poorly calibrated (9.7 shows when confidence *does* help).
- **A classifier trained on old tickets.** Over-engineering as a first step, and it doesn't encode your policy.

> **Exam trap:** A support agent sits at 55% first-contact resolution (target 80%). It escalates easy, policy-covered cases and handles exceptions on its own. The fix is **explicit escalation criteria plus few-shot examples**, because the decision boundary is unclear. Self-rated confidence, a sentiment threshold and a trained classifier are the distractors.

> **CCAO-F lens:** The Associate exam tests the same judgment from the user's side. Recognize when a task needs human verification. If Claude cites "subsection 4(b)" of a regulation, check the official text before you share it. How confident an answer sounds is not evidence.

### 9.2 Escalation patterns

Four patterns cover nearly every exam scenario:

1. **Immediate escalation.** "I want to speak to a manager" → call `escalate_to_human` now. Don't look up the order first. What the agent already knows goes into the handoff.
2. **Resolve first.** The issue is in scope (fridge broke inside the warranty window) → verify and offer a replacement. Escalate only if the customer wants something policy doesn't allow.
3. **Acknowledge → offer → escalate on reiteration.** Frustration is not a request for a human. Acknowledge it and make a concrete offer. If the customer then **repeats** that they want a person, pattern 1 applies.
4. **Policy-gap escalation.** "Match the competitor's price" when policy only covers own-site drops → escalate. Don't stretch the policy or refuse on a technicality.

Turn the patterns into a prompt (task 5.2, S1): categorical rules, the reason, and a few boundary examples ([Chapter 6](../06-prompt-engineering/README.md#61-few-shot-prompting)). "Escalate when in doubt" is a calibration failure, not a safe default.

```python
ESCALATION_POLICY = """You are the support agent for Acme Home. You resolve
most cases yourself. Escalating a case you could have resolved is a failure too.

Call escalate_to_human when, and only when, one of these is true:
1. The customer explicitly asks for a human. Escalate immediately.
2. Our policy does not cover the request, or is ambiguous for this case
   (for example price matching against competitors). Do not stretch policy.
3. You cannot make progress (identity unverified after two requests, a tool
   keeps failing, or the customer rejected two valid resolutions).
4. A tool result says the action needs human approval.

Do NOT escalate because the customer is upset, the story is long, or you
feel unsure. Acknowledge frustration and offer a concrete resolution.

<examples>
<example><customer>My blender broke after 3 days, this is ridiculous.</customer>
<decision>resolve</decision></example>
<example><customer>Your competitor has it cheaper. Match their price.</customer>
<decision>escalate: policy_gap</decision></example>
</examples>"""
```

### 9.3 Resolving ambiguity: ask, don't guess

If the customer can resolve the ambiguity, ask them. If only the business can, escalate (9.1). If source documents contradict each other, route both values to a reviewer (9.9). When `get_customer` returns three "Maria Lopez" records, picking the oldest account is a heuristic, and it picks the wrong account some of the time. One extra turn costs seconds. A refund to the wrong account costs money and trust. Any rule that picks an account for the customer still guesses, however clever it is: it hides the ambiguity without removing the error.

Design the tool result so asking is the natural next step and no other customer's data leaks. On several matches, `get_customer` returns `{"status": "multiple_matches", "count": 3, "ask_for_one_of": ["email", "phone", "order_number"]}`, never the candidates' details. Pair it with an instruction to ask for one of those identifiers, and with the gate in 9.4, which blocks customer-specific actions until there is **exactly one** verified ID. In the Agent SDK and Claude Code, Claude can ask clarifying questions itself with the built-in **`AskUserQuestion`** tool (1–4 questions, 2–4 options each). Your `can_use_tool` callback returns the answers in `updated_input`. It is not available inside subagents.

**When the customer's own statements conflict.** Earlier the customer said "ship everything in one box". Now they say "send the blender today", but the rest of the order is back-ordered. Name both statements and ask which one wins. Don't split the difference, and don't quietly follow the newer (or the older) one.

**Don't over-ask.** "Ask, don't guess" is for cases where a wrong guess is costly: identity, money, or an action you can't undo. For a low-risk, reversible request (the tone of a draft reply, the format of a summary), state your assumptions in one line, go ahead, and invite correction. A string of questions before any useful answer is a failure too.

### 9.4 Programmatic enforcement vs prompt guidance

Task 1.4 is about workflow order: identity before lookups, lookups before refunds, approval before large refunds. A prompt makes that order **probable**. Code makes it **guaranteed**. Use prompts for judgment (tone, when a policy gap exists) and code for ordering, identity, money limits and irreversible actions.

> **Exam trap:** "The agent skips `get_customer` in 12% of cases." The fix is a **programmatic prerequisite** that blocks `lookup_order` and `process_refund` until `get_customer` returns a verified ID. Better prompts never reach zero: at 99.5% compliance, 10,000 refund conversations a day still produce about **50 unverified refunds a day**.

A prerequisite gate for your own Messages API loop. Its state comes from tool **results**, never from what the model says:

```python
from dataclasses import dataclass, field
REFUND_LIMIT_USD = 500.00
@dataclass
class CaseState:
    verified_customer_id: str | None = None   # set from get_customer RESULT
    orders: dict[str, dict] = field(default_factory=dict)  # from lookup_order
    refunded: dict[str, float] = field(default_factory=dict)  # order -> paid
    gate_log: list[dict] = field(default_factory=list)     # every allow/deny
    threshold_denials: int = 0
    escalated: bool = False

def gate(tool: str, args: dict, state: CaseState) -> str | None:
    if (tool in ("lookup_order", "process_refund")
            and state.verified_customer_id is None):
        return "BLOCKED: verify the customer with get_customer first."
    if tool == "process_refund":
        order = state.orders.get(args.get("order_id"))
        if order is None or order["customer_id"] != state.verified_customer_id:
            return "BLOCKED: refund only orders lookup_order returned."
        total = state.refunded.get(order["order_id"], 0.0) + args["amount"]
        if total > order["total"]:
            return "BLOCKED: the refunds would exceed the order total."
        if total > REFUND_LIMIT_USD:                # running total, not one call
            state.threshold_denials += 1
            return ("BLOCKED by policy: refunds over $500 need human approval. "
                    "Call escalate_to_human (reason 'threshold_exceeded').")
    return None  # allow
```

An `execute()` wrapper calls `gate()` before each tool, writes the decision to `gate_log` (your audit trail), returns a denial as an `is_error: true` tool result, and updates `CaseState` from the tool's result (a successful refund adds to `refunded`). Four design points matter:

1. **Deny with direction.** A denial that says what to do instead (escalate, with which reason) turns a block into a redirect.
2. **Fail closed.** After the loop ends, if `threshold_denials > 0` and `not escalated`, the harness creates the escalation itself.
3. **Escalation is a terminal state.** Count failed attempts in code (identity requests, repeated tool errors, `max_turns`) and escalate with `cannot_make_progress` when the budget runs out. Recover transient failures locally first ([Chapter 10](../10-multi-agent-error-handling/README.md)).
4. **Check running totals, not single calls.** Otherwise a $900 refund split into two $450 calls passes a $500 limit. That is why `gate()` adds `refunded` to the new amount.

In the Agent SDK, the same gate is a `PreToolUse` hook that returns `permissionDecision: "deny"` with a `permissionDecisionReason` ([Chapter 3, Patterns A and B](../03-agent-sdk/README.md#pattern-a-block-a-policy-violation-and-redirect-to-escalation-pretooluse)). A hook `deny` applies even in `bypassPermissions` mode, and the most restrictive decision wins (`deny` > `defer` > `ask` > `allow`).

For irreversible actions, make the unsafe call impossible: a `preview_delete_card` tool returns a **single-use confirmation token** that `delete_card` requires. A `dry_run` flag plus "always preview first" can be skipped. A required token cannot. **The control ladder, strongest first:** remove the capability (least privilege) → deterministic gate → human approval (9.5) → prompt guidance → after-the-fact audit (detects, doesn't prevent).

> **Exam trap:** If users only read tickets and draft replies, the best control for refunds is to **remove** the refund tool. A confirmation prompt or extra logging is a compensating control, not least privilege.

### 9.5 Human approval checkpoints on each Claude surface *(expanded beyond the guide)*

Pick the mechanism by surface and by how long the human may take:

| Surface | Mechanism | Key facts |
|---|---|---|
| **Messages API, your loop** | Don't execute the `tool_use`; persist `messages`; send the `tool_result` later | The API is stateless, so a pending approval is stored data. On resume, send a `tool_result` for **every** `tool_use` in that turn |
| **Agent SDK** `can_use_tool` | Callback returns `PermissionResultAllow` or `PermissionResultDeny` | Fires **only** for calls nothing earlier resolved. An `allowed_tools` entry or `bypassPermissions` approves first; `dontAsk` denies |
| **Agent SDK** `PreToolUse` → `"ask"` | Routes the call to `can_use_tool` | Code decides *that* a human looks; a human decides *what* happens |
| **Agent SDK** `PreToolUse` → `"defer"` | Run stops with `stop_reason: "tool_deferred"` | For approvals that take hours or days. Resume with `resume=<session_id>` and **no new prompt**; the hook fires again (and may `defer` again). A prompt sent with or after the resume drops the deferred call. Only for a single tool call in that turn, in non-interactive runs |
| **Claude Code** | Permission modes, ask rules, hooks; MCP `_meta["anthropic/requiresUserInteraction"]: true` | That flag prompts on **every** call, even in `bypassPermissions` |
| **Claude Managed Agents** (beta) | `permission_policy: {"type": "always_ask"}` | Session idles with `requires_action`; you send `user.tool_confirmation`. `auto` is **not** a human checkpoint. Custom tools are your responsibility |

A `defer`-based supervisor approval for refunds over `REFUND_LIMIT_USD`:

```python
decisions: dict[str, str] = {}  # stand-in for a persistent approval store
                                # (DB row: tool_use_id -> approved/rejected)

async def refund_approval(input_data, tool_use_id, context):  # PreToolUse
    if float(input_data["tool_input"].get("amount", 0)) <= REFUND_LIMIT_USD:
        return {}                                    # within authority
    decision = decisions.get(tool_use_id)
    out = {"hookEventName": "PreToolUse"}
    if decision is None:                             # nobody decided: pause
        open_approval_ticket(tool_use_id, input_data["tool_input"])  # yours
        out["permissionDecision"] = "defer"
    elif decision == "approved":
        out["permissionDecision"] = "allow"
    else:
        out["permissionDecision"] = "deny"
        out["permissionDecisionReason"] = (
            "A supervisor declined this refund. Offer store credit instead.")
    return {"hookSpecificOutput": out}
```

Register it with `HookMatcher(matcher="mcp__support__process_refund", hooks=[refund_approval])` under `PreToolUse`. Routine refunds can stay in `allowed_tools`: hooks run first, so every call still passes through the hook. `open_approval_ticket` is your own ticketing call. When a `ResultMessage` carries `deferred_tool_use`, store its `session_id`. The approval may arrive in another process, so keep decisions in a database, not in memory. When the supervisor decides, record it in your approval store and resume with the same options plus `resume=<session_id>`, **without a new prompt**. A prompt sent with or after the resume makes Claude answer it and drop the deferred refund. If nobody has decided yet, the hook simply returns `defer` again.

**Where to put checkpoints (the reversibility × cost matrix).** Approving everything turns reviewers into rubber stamps, so place checkpoints by reversibility and cost of a wrong action. Reversible and cheap: automate and log it. Reversible and expensive: automate with limits and sample-audit (9.8). Irreversible and cheap: automate with a preview/confirm step. Irreversible and expensive: **human approval**, with an impact preview.

### 9.6 Structured handoff protocols

When the agent escalates, the human usually **cannot see the conversation**. The test for a handoff: *could someone who never saw the chat make the decision and reply without asking anything again?* Make the summary the **input schema of the `escalate_to_human` tool**, so the model can't escalate without filling it in:

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict

class ActionTaken(BaseModel):
    model_config = ConfigDict(extra="forbid")  # strict tools need this
    step: str                     # "lookup_order(ORD-31544)"
    outcome: str                  # what the tool returned

class HandoffSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    escalation_reason: Literal["customer_requested_human", "policy_gap",
        "cannot_make_progress", "threshold_exceeded", "other"]
    reason_detail: str            # one sentence: why a human, specifically
    customer_id: str | None       # null only if identity not verified
    identity_verified: bool
    order_ids: list[str]
    issue_summary: str            # what the customer wants, 1-3 sentences
    root_cause: str | None        # what actually went wrong, if known
    facts_verified: list[str]     # confirmed by tool results
    customer_claims: list[str]    # stated by the customer, not verified
    actions_taken: list[ActionTaken]
    offers_made: list[str]        # each offer and how the customer responded
    amount_at_stake_usd: float | None
    recommended_action: str
    recommendation_rationale: str
    urgency: Literal["low", "normal", "high"]
    open_questions: list[str]     # what the human must decide or find out
```

Register the tool with `"strict": True` and `"input_schema": HandoffSummary.model_json_schema()`, and say in its description that the specialist will NOT see the conversation. Design rules:

- **Separate verified facts from claims.** Humans decide differently on each.
- **Code owns the hard facts.** Customer ID, verification status, totals and the gate log come from `CaseState`; overwrite or cross-check them before filing. The model writes the narrative and **recommends, but doesn't decide**: the decision stays with the human.
- **Validate before you file.** A schema guarantees shape, not completeness. `handoff_problems(h, state)` checks that `identity_verified` and `customer_id` match the gate state, that `actions_taken` is not empty (unless the customer asked for a human), that a `policy_gap` has an open question, and that `recommended_action` is set. Problems go back to the model as an `is_error` result.
- **Escalate only the part that needs a human.** With two concerns, resolve the in-scope one, escalate the other, and say in the handoff what was already done.

> **Exam trap:** "Attach the full transcript" is not a handoff protocol: the scenario says humans lack access to it, and reading 40 turns is slow. A free-text "customer is upset about a refund" has no IDs, amounts or recommendation.

### 9.7 Confidence calibration

Self-rated confidence is a poor escalation trigger (9.1), yet task 5.5 asks for **field-level confidence** calibrated on labeled data. The difference is calibration. A confidence score is a useful **ranking** signal. It becomes a **probability** only after you check it against ground truth. The Messages API has no log-probability field, so confidence is something you ask the model to output (a 0–1 score or a `high`/`medium`/`low` enum). Steps: collect a labeled set that matches production; extract with a defined confidence per field; build a reliability table per field (`reliability_table` groups predictions into confidence bands and reports n and observed accuracy per band); pick a threshold per field and document type; **recalibrate** whenever the model, prompt, schema or document mix changes.

```python
def pick_threshold(records, target_accuracy=0.99, min_n=200):
    """records: {'confidence': 0-1, 'correct': bool} for ONE field. Lowest
    cut-off that meets the target. None = keep the field on human review."""
    for t in sorted({r["confidence"] for r in records}):
        accepted = [r["correct"] for r in records if r["confidence"] >= t]
        if len(accepted) < min_n:
            break                       # too few items left to trust it
        if sum(accepted) / len(accepted) >= target_accuracy:
            return t
    return None
```

An illustrative reliability table for `total`: 0.95–1.00 → 99.6% (auto-accept); 0.90–0.95 → 98.1%; 0.80–0.90 → 91.4% (review); below 0.80 → 72.9% (review first). "0.9" did not mean "90% accurate". Here it meant 98%. In another field it might mean 80%. Strict tool schemas don't support `minimum` / `maximum`: a raw strict schema with them is rejected with a 400 error. `parse()` strips them from the wire schema, notes them in the description and validates the response against them. `transform_schema()` only does the stripping, so validate the range in your own code when you use it.

> **Exam trap:** "Only report high-confidence findings" does not raise precision (task 4.1). Specific report/skip criteria do. Confidence belongs in **routing**, after calibration. To speed up triage while keeping every finding, show a rationale and a confidence per finding (task 4.6).

### 9.8 Segment accuracy and stratified sampling

**Aggregate accuracy hides segments.** Typed invoices (9,000 at 99%), contracts (500 at 98%) and handwritten receipts (500 at **60%**) add up to **97%** overall, while 40% of receipts are wrong with nobody looking. Fields hide errors the same way. Before reducing human review, measure accuracy **per document type × field** on labeled data, and automate only segments that meet the target with enough samples.

**Stratified random sampling.** Low-confidence items already go to humans. The blind spot is items the system is *confident* about, where new error patterns appear (a vendor changes its layout, a model update shifts behavior). So audit a random sample of **auto-accepted** items, stratified so small segments aren't drowned out:

```python
import random
from collections import defaultdict

def stratified_audit_sample(auto_accepted, rate, min_per_stratum=30, seed=7):
    """Random audit sample of AUTO-ACCEPTED items. Strata = doc type x
    confidence band. `rate`: doc_type -> rate (oversample rare/risky)."""
    rng = random.Random(seed)
    strata = defaultdict(list)
    for item in auto_accepted:
        strata[(item["doc_type"], item["confidence_band"])].append(item)
    sample = []
    for (doc_type, _band), group in strata.items():
        k = max(min_per_stratum, round(len(group) * rate.get(doc_type, 0.02)))
        sample += rng.sample(group, min(k, len(group)))
    return sample
```

- **Random within a stratum.** Picking "the odd-looking ones" measures your intuition.
- **Stratified.** A simple 2% sample of 10,000 items holds only about 10 of the 500 receipts. Weight results back by volume when you report one number.
- **Enough samples.** Zero errors in *n* audited items gives a 95% upper bound of about **3/n** (the rule of three). To claim "below 1%", audit about 300 items in that stratum.
- **Feed findings back.** Reviewer findings become new labeled data for calibration (9.7). If a stratum's error rate rises above target, put it back on full review.

### 9.9 Routing review work with limited capacity

Reviewers are the scarce resource. Send these to humans: validation failures after retry, **contradictory sources** (show both values; recompute in code, [Chapter 6, 6.6](../06-prompt-engineering/README.md#66-self-correction)), and critical fields below their calibrated threshold or marked `"unclear"`. Everything else is auto-accepted, and the stratified audit sample still runs.

- **Route fields, not whole documents.** Show only the flagged fields next to their source snippets.
- **Prioritize by expected cost:** P(error) from the calibration table × the impact of that field being wrong. When the queue exceeds capacity, the low-cost tail waits.
- **Never drop the audit sample** to save capacity. It is your only unbiased measurement of the automated path. "Route only low-confidence items and auto-accept the rest" leaves confident errors unmeasured.
- **Use `"unclear"` and `null` as routing signals** ([Chapter 2](../02-tool-use/README.md#24-json-schemas-for-structured-output)). An honest `"unclear"` is cheap to route; a confident made-up value is not.

### 9.10 Measuring the escalation system *(expanded beyond the guide)*

An escalation policy is a classifier with two costly errors: **over-escalation** (wasted human time, lower resolution) and **under-escalation** (risk). Measure both on a labeled set of conversations, and re-run it whenever the prompt, examples, model or policy change:

| Metric | What it tells you |
|---|---|
| First-contact resolution / deflection | Share resolved without a human (Anthropic's support guide suggests 70–80% deflection) |
| Escalation recall, precision, reason accuracy | Did cases that should escalate do so (the guide suggests 95%+ escalation accuracy)? Were escalations necessary, with the right `escalation_reason`? |
| Handoff completeness | How often the human had to ask the customer again |
| Gate block rate, calibration drift | A block spike means prompt and code disagree (or probing); drift is audited error per stratum vs the calibration table |
| Reviewer agreement | Low agreement means noisy labels, and noisy calibration |

## Lesson code

Video-lesson code: [../../presentations/09-escalation/code/](../../presentations/09-escalation/code/)

## Notebooks

Run them from the repo root venv (see [../../00-prerequisites/README.md](../../00-prerequisites/README.md)).

| Notebook | What you do |
|---|---|
| [01_practice.ipynb](01_practice.ipynb) | Work through 9.1–9.10 offline (no key needed; three optional live cells), then build a support agent with a policy gate, fail-closed escalation and a validated handoff, plus a review plan for an extraction pipeline |
| [02_homework.ipynb](02_homework.ipynb) | 10-question quiz, 6 offline coding exercises, an optional live exercise, an architecture scenario and a scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>
## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Customer explicitly asks for a human | Escalate immediately | Investigating or "let me try first" | Honor the request; put what you know in the handoff |
| Agent escalates easy cases and keeps hard ones | Explicit criteria + few-shot examples | Self-rated confidence, sentiment, a trained classifier | Fixes the unclear decision boundary directly |
| Rule must hold every time (identity, limits, ordering) | Prerequisite gate / `PreToolUse` deny | Stronger prompt, more examples | Deterministic vs probabilistic |
| Users never need the dangerous action | Remove the tool | Confirmation prompts, logging | Least privilege beats compensating controls |
| Approval may take hours (Agent SDK) | `PreToolUse` → `defer`, resume later | Blocking inside `can_use_tool` | The process can exit; the session persists |
| Human takes over without the transcript | Structured handoff as the `escalate_to_human` schema; hard facts filled by code | Transcript dump, free-text note | Self-contained, verifiable, fast to act on |
| "97% accurate, let's automate" | Per doc type × field analysis first | Trusting the aggregate | Aggregates hide failing segments |
| Monitoring automated, high-confidence output | Stratified random audit sample | Reviewing only low-confidence items | Measures confident errors, catches new patterns |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **Escalating "when unsure", on sentiment, or on the model's 1–10 self-rating.** It sends easy cases to humans and lowers resolution.
- **Guessing between matching customers** with a heuristic, or returning other customers' details in a tool result.
- **Enforcing identity or refund limits with prompt text only**, or checking limits per call instead of running totals.
- **Relying on `can_use_tool` while the tool is in `allowed_tools`** or the session is in `bypassPermissions`. The callback never fires.
- **Handoffs without IDs, amounts, what was tried, or a recommendation**, or that mix verified facts with customer claims.
- **Treating confidence as a probability** without a reliability table, automating on aggregate accuracy, or auditing only low-confidence items.

## Self-check

**Q1. (Customer support agent)** A phone carrier's support agent resolves 62% of chats without a human (goal: 78%). Logs show it hands routine SIM-card replacements for lost phones, which policy fully covers, to humans. Meanwhile it tries to settle early-termination fee waivers, a policy exception, on its own. A teammate proposes escalating whenever sentiment drops below −0.6, because escalated customers were often angry. What should you do?

- A) Deploy the sentiment threshold, since it correlates with past escalations
- B) Add explicit escalation criteria (explicit request, policy gap, no progress) with a few boundary examples of "resolve" vs "escalate" to the system prompt
- C) Ask the model to rate its confidence 1–10 and escalate below 6
- D) Train a classifier on last year's tickets to predict escalation

<details><summary>Answer</summary>

**B.** The root cause is an unclear decision boundary, and criteria plus examples define it directly. A routes on mood, which doesn't measure case complexity. An angry customer who lost a phone needs a new SIM, and a calm customer asking for a fee waiver needs a human. C is unreliable because the model can be confidently wrong. D is heavy infrastructure for a first fix and doesn't encode your policy.
</details>

**Q2. (Customer support agent)** After you added few-shot examples, the agent skips identity verification before refunds in 0.4% of conversations, down from 12%. Compliance requires zero unverified refunds. What should you do next?

- A) Add more few-shot examples until the rate reaches zero
- B) Add a programmatic prerequisite that blocks `lookup_order` and `process_refund` until `get_customer` has returned exactly one verified customer ID
- C) Put the rule in capital letters at the top of the system prompt
- D) Review a weekly sample of refunds for missing verification

<details><summary>Answer</summary>

**B.** Prompt techniques lower the failure rate but cannot guarantee zero. A deterministic gate holds on every call. A and C are still probabilistic. (Anthropic's [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) also advise replacing emphatic "CRITICAL: You MUST…" wording with plain instructions, because recent models respond strongly to the system prompt and can overtrigger on it.) D only detects violations after the money has moved.
</details>

**Q3. (Customer support agent)** Human specialists say escalated tickets are slow to handle: they get "customer wants refund, upset" and have to message the customer again for the order number, what was already offered, and the amount. They can't see the chat transcript. What change helps most?

- A) Give specialists access to the full transcript
- B) Make `escalate_to_human` require a structured handoff: verified customer ID, order IDs, issue and root cause, verified facts vs customer claims, actions taken and offers made, amount, recommended action with rationale, open questions
- C) Add the customer's sentiment score to each ticket
- D) Ask the agent to write longer free-text summaries

<details><summary>Answer</summary>

**B.** A structured, self-contained summary gives the specialist everything needed to act in one pass, and the schema makes the missing fields impossible to leave out. A is outside the scenario's constraint (no transcript access) and is still slow. C adds no actionable facts. D makes summaries longer but not complete.
</details>

**Q4. (Structured data extraction)** Your extraction pipeline is 97% accurate on a labeled set, and the accuracy target is 95%. The team wants to stop human review for every extraction with model confidence ≥ 0.9. What should you do first?

- A) Approve it, since 97% exceeds the 95% target
- B) Measure accuracy per document type and per field, and calibrate per-field thresholds against the labeled set; automate only the segments that meet the target
- C) Raise the threshold to 0.99 to be safe
- D) Ask the model to double-check every field it rated below 0.9

<details><summary>Answer</summary>

**B.** An aggregate can hide a failing segment (for example handwritten receipts at 60%), and an uncalibrated 0.9 does not mean 90% accurate in every field. A trusts the aggregate. C is still uncalibrated and may still hide a bad segment. D adds cost without measuring anything.
</details>

## Official documentation

- [Handle approvals and user input (Agent SDK)](https://code.claude.com/docs/en/agent-sdk/user-input): `can_use_tool`, `AskUserQuestion`, when to use `defer`
- [Configure permissions (Agent SDK)](https://code.claude.com/docs/en/agent-sdk/permissions): the evaluation order (hooks → deny → ask → mode → allow → `canUseTool`), permission modes
- [Hooks reference (Claude Code)](https://code.claude.com/docs/en/hooks): `PreToolUse` decision control, "Defer a tool call for later", `PermissionRequest`
- [Permission policies (Claude Managed Agents)](https://platform.claude.com/docs/en/managed-agents/permission-policies): `always_allow`, `always_ask`, `auto`, `user.tool_confirmation`
- [Customer support agent guide](https://platform.claude.com/docs/en/about-claude/use-case-guides/customer-support-chat): escalation efficiency, deflection rate and sentiment as metrics
- Syllabus source: community study guide by paullarionov, [Chapter 9 and Domain 5](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-9-escalation-and-human-in-the-loop), restructured and expanded here in my own words.

[← Chapter 8 — Task Decomposition](../08-task-decomposition/README.md) | [↑ Claude path overview](../README.md) | [Chapter 10 — Error Handling in Multi-agent Systems →](../10-multi-agent-error-handling/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
