# Chapter 9 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table maps requirement IDs from the official exam guides, the Anthropic Academy courses and the role competency matrix to this chapter. **Primary** means this chapter is where the item is taught in depth. **Supporting** means the chapter applies or reinforces an item whose main home is elsewhere. "practice" is [01_practice](../01_practice.ipynb), "hw" is [02_homework](../02_homework.ipynb).

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `CCAR-F/D5/5.2/K1` | Appropriate triggers: explicit request for a human, policy gap/exception, no meaningful progress | [9.1](../README.md#91-when-to-escalate), practice §9.1 router scorecard, hw Ex. 1 | Primary |
| `CCAR-F/D5/5.2/K2` | Escalate at once on an explicit demand vs offer to resolve a straightforward issue | [9.1](../README.md#91-when-to-escalate), [9.2](../README.md#92-escalation-patterns), More self-check questions 1, hw Q1 | Primary |
| `CCAR-F/D5/5.2/K3` | Why sentiment and self-reported confidence are unreliable proxies for complexity | [9.1](../README.md#91-when-to-escalate), [9.7](../README.md#97-confidence-calibration), practice §9.1 three routers, Self-check Q1 | Primary |
| `CCAR-F/D5/5.2/K4` | Multiple customer matches need clarification (extra identifiers), not heuristic selection | [9.3](../README.md#93-resolving-ambiguity-ask-dont-guess), practice §9.3 wrong-account simulation, More self-check questions 2 | Primary |
| `CCAR-F/D5/5.2/S1` | Explicit escalation criteria with few-shot examples in the system prompt | [9.2](../README.md#92-escalation-patterns), `ESCALATION_POLICY`, practice §9.2 live evaluation | Primary |
| `CCAR-F/D5/5.2/S2` | Honor explicit requests for a human immediately, without investigating first | [9.2](../README.md#92-escalation-patterns), pattern 1, hw Q1 | Primary |
| `CCAR-F/D5/5.2/S3` | Acknowledge frustration, offer a resolution, escalate only if the customer reiterates | [9.2](../README.md#92-escalation-patterns), pattern 3, practice §9.2 state machine, More self-check questions 1 | Primary |
| `CCAR-F/D5/5.2/S4` | Escalate when policy is ambiguous or silent (competitor price match) | [9.2](../README.md#92-escalation-patterns), pattern 4, hw Q2 | Primary |
| `CCAR-F/D5/5.2/S5` | Instruct the agent to ask for more identifiers when a tool returns multiple matches | [9.3](../README.md#93-resolving-ambiguity-ask-dont-guess), `get_customer` multiple_matches result, hw Ex. 2 | Primary |
| `CCAR-F/D5/5.5/K1` | Aggregate accuracy (e.g. 97%) can mask poor document types or fields | [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), practice §9.8 "97% that hides 60%", Self-check Q4 | Primary |
| `CCAR-F/D5/5.5/K2` | Stratified random sampling to measure high-confidence error rates and catch novel patterns | [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), practice §9.8 drift simulation, More self-check questions 3 | Primary |
| `CCAR-F/D5/5.5/K3` | Field-level confidence calibrated on labeled validation sets to route review | [9.7](../README.md#97-confidence-calibration), practice §9.7 reliability tables | Primary |
| `CCAR-F/D5/5.5/K4` | Validate accuracy by document type and field before automating | [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), Self-check Q4 | Primary |
| `CCAR-F/D5/5.5/S1` | Implement stratified random sampling of high-confidence extractions | [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), `stratified_audit_sample`, hw Ex. 6 | Primary |
| `CCAR-F/D5/5.5/S2` | Analyze accuracy by document type × field before reducing human review | [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), hw Ex. 6 | Primary |
| `CCAR-F/D5/5.5/S3` | Output field-level confidence, then calibrate thresholds on labeled data | [9.7](../README.md#97-confidence-calibration), `reliability_table`, `pick_threshold`, hw Ex. 5 | Primary |
| `CCAR-F/D5/5.5/S4` | Route low-confidence or contradictory-source items to review; prioritize scarce capacity | [9.9](../README.md#99-routing-review-work-with-limited-capacity), practice §9.9 priority queue, hw Q8, Q9 | Primary |
| `CCAR-F/D1/1.4/K1` | Programmatic enforcement (hooks, prerequisite gates) vs prompt guidance for workflow order | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), practice §9.4 prompt-only vs gate | Primary |
| `CCAR-F/D1/1.4/K2` | Prompt-only compliance has a non-zero failure rate when determinism is required | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), Self-check Q2 | Primary |
| `CCAR-F/D1/1.4/K3` | Structured handoff protocols: customer details, root cause, recommended action | [9.6](../README.md#96-structured-handoff-protocols), `HandoffSummary` | Primary |
| `CCAR-F/D1/1.4/S1` | Prerequisites that block downstream tools until verification completes | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), `gate`, hw Ex. 3 | Primary |
| `CCAR-F/D1/1.4/S2` | Multi-concern requests: resolve in-scope items, escalate only the rest (decomposition itself is taught in Ch 8) | [9.6](../README.md#96-structured-handoff-protocols), hw Q10 | Supporting |
| `CCAR-F/D1/1.4/S3` | Handoff summaries (customer ID, root cause, amount, recommended action) for humans without the transcript | [9.6](../README.md#96-structured-handoff-protocols), `HandoffSummary`, `handoff_problems`, hw Ex. 4, Self-check Q3 | Primary |
| `CCAR-F/D1/1.5/K2` | Hooks that intercept outgoing tool calls to enforce rules (refund threshold) | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), `refund_approval` | Supporting |
| `CCAR-F/D1/1.5/K3` | Hooks for deterministic guarantees vs prompts for probabilistic compliance | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance) | Supporting |
| `CCAR-F/D1/1.5/S2` | Interception hooks that block violations and redirect to human escalation | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), More self-check questions 4 | Supporting |
| `CCAR-F/D1/1.5/S3` | Choose hooks over prompts when rules need guaranteed compliance | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), More self-check questions 4 | Supporting |
| `CCAR-F/D4/4.1/K2` | "Only report high-confidence findings" doesn't improve precision vs categorical criteria | [9.7](../README.md#97-confidence-calibration), exam trap | Supporting |
| `CCAR-F/D4/4.1/S1` | Specific report/skip criteria instead of confidence-based filtering | [9.7](../README.md#97-confidence-calibration), exam trap | Supporting |
| `CCAR-F/D4/4.3/S5` | `"unclear"` / `"other"` enum values for ambiguous cases (used here as routing signals) | [9.9](../README.md#99-routing-review-work-with-limited-capacity) | Supporting |
| `CCAR-F/D4/4.6/S3` | Self-reported confidence per finding for calibrated review routing | [9.7](../README.md#97-confidence-calibration) | Supporting |
| `CCAR-F/APPX/IN/7` | Local recovery before escalation (primary in Ch 10) | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), design point 3 | Supporting |
| `CCAR-F/APPX/IN/8` | Escalation decision-making: explicit criteria, honoring customer preferences, policy gaps | [9.1](../README.md#91-when-to-escalate), [9.2](../README.md#92-escalation-patterns), [9.3](../README.md#93-resolving-ambiguity-ask-dont-guess) (conflicting statements, don't over-ask), More self-check questions 5, 6 | Primary |
| `CCAR-F/APPX/IN/17` | Human review workflows: calibration, stratified sampling, segmentation by doc type and field | [9.7](../README.md#97-confidence-calibration), [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), [9.9](../README.md#99-routing-review-work-with-limited-capacity) | Primary |
| `CCAR-F/APPX/TECH/14` | Confidence scoring: field-level confidence, calibration, stratified error-rate sampling | [9.7](../README.md#97-confidence-calibration), [9.8](../README.md#98-segment-accuracy-and-stratified-sampling) | Primary |
| `CCAR-F/SC1` | Customer Support Resolution Agent scenario (80%+ FCR while knowing when to escalate) | [9.1](../README.md#91-when-to-escalate), [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.6](../README.md#96-structured-handoff-protocols), practice mini-project | Supporting |
| `CCAR-F/SQ1` | Sample Q: agent skips `get_customer` in 12% of cases → programmatic prerequisite | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), exam trap, Self-check Q2 | Supporting |
| `CCAR-F/SQ3` | Sample Q: 55% FCR from miscalibrated escalation → explicit criteria + few-shot | [9.1](../README.md#91-when-to-escalate), exam trap, Self-check Q1 | Supporting |
| `CCAR-F/EX1/4` | Exercise: hook that blocks over-threshold actions and redirects to escalation | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), practice mini-project | Supporting |
| `CCAR-F/EX3/5` | Exercise: field-level confidence, review routing, accuracy by doc type and field | [9.7](../README.md#97-confidence-calibration), [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), [9.9](../README.md#99-routing-review-work-with-limited-capacity), practice mini-project Part 2 | Supporting |
| `CCAR-F/MQC/7` | Sound escalation and reliability decisions, HITL workflows, self-evaluation patterns | [9.1](../README.md#91-when-to-escalate), [9.2](../README.md#92-escalation-patterns), [9.3](../README.md#93-resolving-ambiguity-ask-dont-guess), [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), [9.6](../README.md#96-structured-handoff-protocols), [9.7](../README.md#97-confidence-calibration), [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), [9.9](../README.md#99-routing-review-work-with-limited-capacity), [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Primary |
| `CCAR-F/PREP/7` | Review escalation and HITL patterns; practice human review workflow design | [9.1](../README.md#91-when-to-escalate), [9.2](../README.md#92-escalation-patterns), [9.9](../README.md#99-routing-review-work-with-limited-capacity), hw Part C | Supporting |
| `CCAR-P/D5/5.3/S1` | Apply human-in-the-loop validation strategies | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), [9.7](../README.md#97-confidence-calibration), [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), [9.9](../README.md#99-routing-review-work-with-limited-capacity) | Supporting |
| `CCAR-P/D5/5.1/S1` | Implement guardrails and safety controls (layered control ladder) | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), preview token, More self-check questions 7 | Supporting |
| `CCAR-P/D5/5.2/S1` | Failure modes of LLM systems: non-zero prompt compliance, confident errors | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.7](../README.md#97-confidence-calibration), [9.8](../README.md#98-segment-accuracy-and-stratified-sampling) | Supporting |
| `CCAR-P/D4/4.2/S1` | Evaluation datasets: labeled conversation and extraction sets | [9.7](../README.md#97-confidence-calibration), [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D4/4.6/S1` | Monitor escalation and calibration metrics in production | [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D3/3.1/S1` | Capability bloat: remove tools the agent doesn't need | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), control ladder | Supporting |
| `CCAR-P/D3/3.2/S1` | Least privilege as the authorization fix | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), exam trap | Supporting |
| `CCAR-P/SQ1` | Sample Q: remove unneeded refund/delete tools instead of adding confirmations | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), exam trap | Supporting |
| `ACAD/claude-certified-architect-professional/LO5` | Route decisions to reviewers by confidence, reversibility and cost | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), reversibility × cost matrix, [9.9](../README.md#99-routing-review-work-with-limited-capacity) | Supporting |
| `ACAD/claude-certified-architect-professional/3/LO4` | Route decisions to the right reviewer by confidence, reversibility and cost | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), [9.9](../README.md#99-routing-review-work-with-limited-capacity) | Supporting |
| `ACAD/claude-certified-architect-professional/3/LO2` | Deterministic vs model-based checks at the right points in the request path | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance) | Supporting |
| `ACAD/claude-certified-architect-professional/1/LO1` | Split a request into what Claude does, what code does, what humans do | [Intro](../README.md#why-this-matters-for-a-solution-architect), [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance) | Supporting |
| `CCDV-F/D1/1.2/K4` | Hooks for deterministic actions | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D7/7.3/S1` | Hooks as guardrails that prevent destructive actions | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D8/8.1/K7` | Tool approval patterns | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D7/7.2/K2` | Guardrail layering | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), control ladder | Supporting |
| `CCDV-F/D7/7.2/K3` | Privacy by design: tool results that don't leak other customers' data | [9.3](../README.md#93-resolving-ambiguity-ask-dont-guess), `get_customer` | Supporting |
| `CCDV-F/D7/7.2/K5` | Least privilege: remove tools the agent doesn't need | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), control ladder | Supporting |
| `CCDV-F/D6/6.3/K4` | Skepticism toward confident output | [9.7](../README.md#97-confidence-calibration), [9.8](../README.md#98-segment-accuracy-and-stratified-sampling) | Supporting |
| `ACAD/claude-certified-developer-foundations/LO4` | HITL checkpoints for irreversible actions in a production agent | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide) | Supporting |
| `ACAD/claude-certified-developer-foundations/2/LO6` | Production agent: tools and context wired into a working loop (here: with escalation states) | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), practice mini-project | Supporting |
| `ACAD/claude-certified-developer-foundations/3/LO2` | Place a human review gate where a wrong call is costly | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/PURPOSE/5` | Recognize limitations and escalate | [9.1](../README.md#91-when-to-escalate), CCAO-F lens | Supporting |
| `CCAO-F/MQC/1` | Critically evaluate AI-generated content | [9.1](../README.md#91-when-to-escalate), CCAO-F lens, [9.7](../README.md#97-confidence-calibration) | Supporting |
| `CCAO-F/D2/2.4/S1` | Decide when human review or verification is required | [9.1](../README.md#91-when-to-escalate), CCAO-F lens, [9.7](../README.md#97-confidence-calibration) | Supporting |
| `CCAO-F/PREP/5` | Responsible-use judgment: when to escalate or seek human review | [9.1](../README.md#91-when-to-escalate), CCAO-F lens | Supporting |
| `CCAO-F/D2/2.2/K1` | Hallucinations: self-rated confidence is not verification; check citations | [9.1](../README.md#91-when-to-escalate), CCAO-F lens | Supporting |
| `CCAO-F/SQ1` | Sample Q: verify a cited subsection before sharing | [9.1](../README.md#91-when-to-escalate), CCAO-F lens | Supporting |
| `ACAD/claude-certified-associate-foundations/LO3` | Know when human verification of Claude's output is required | [9.1](../README.md#91-when-to-escalate), CCAO-F lens, [9.7](../README.md#97-confidence-calibration) | Supporting |
| `ACAD/claude-certified-associate-foundations/3/LO4` | Determine when human review or more verification is required | [9.1](../README.md#91-when-to-escalate), CCAO-F lens | Supporting |
| `ROLE/AGENT/6` | Human-in-the-loop and autonomy safeguards: approval gates, permissions, escalation paths, stop conditions | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), [9.6](../README.md#96-structured-handoff-protocols) | Primary |
| `ROLE/AGENT/1` | Agent control flow with terminal escalation states and stop conditions | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), design point 3 | Supporting |
| `ROLE/AGENT/7` | Agent SDK hooks and permissions for approvals | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide) | Supporting |
| `ROLE/SAFE/2` | Guardrails and policy enforcement | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide) | Supporting |
| `ROLE/SAFE/9` | Safety-first judgment: where humans must stay in the loop | [9.5](../README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), checkpoint matrix | Supporting |
| `ROLE/SAFE/3` | Confidence signals to reduce fabrication | [9.7](../README.md#97-confidence-calibration), [9.9](../README.md#99-routing-review-work-with-limited-capacity) | Supporting |
| `ROLE/SAFE/7` | Audit trail: gate log and handoff records | [9.4](../README.md#94-programmatic-enforcement-vs-prompt-guidance), [9.6](../README.md#96-structured-handoff-protocols) | Supporting |
| `ROLE/EVAL/1` | Use-case evals for the escalation decision | [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Supporting |
| `ROLE/EVAL/3` | Labeled sets and human judgment (reviewer agreement) | [9.7](../README.md#97-confidence-calibration), [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Supporting |
| `ROLE/EVAL/6` | Agent decision evaluation: escalation precision, recall, reason accuracy | [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Supporting |
| `ROLE/EVAL/4` | Production feedback loops: audit findings feed recalibration | [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Supporting |
| `ROLE/OBS/2` | Production monitoring: calibration drift, gate block rate | [9.8](../README.md#98-segment-accuracy-and-stratified-sampling), [9.10](../README.md#910-measuring-the-escalation-system-expanded-beyond-the-guide) | Supporting |

## More self-check questions

**Q1. (Customer support agent)** A customer writes: "This is the third kettle that leaked, I'm so fed up!" The order is within the replacement window. They have not asked for a person. What should the agent do?

- A) Escalate immediately, because the customer is clearly frustrated
- B) Acknowledge the frustration, verify the order, and offer a replacement or refund; escalate if the customer then says they want a person
- C) Offer a replacement without acknowledging the frustration, to keep the reply short
- D) Ask the customer to rate their frustration from 1 to 10 to decide whether to escalate

<details><summary>Answer</summary>

**B.** The issue is within the agent's capability, so acknowledge, then offer a concrete resolution. Frustration is not a request for a human. Escalate only if they reiterate that they want one. A escalates on sentiment. C skips the acknowledgement that keeps the conversation working. D is a made-up trigger.
</details>

**Q2. (Customer support agent)** A caller gives an energy supplier's agent a surname and a postcode. `find_account` returns two accounts. The agent picks the older one. An audit found that choice wrong in about 1 of every 8 two-match calls. The next step is setting up a payment plan on the account. What is the best fix?

- A) Ask the model to pick the more likely account and explain its choice in the reply
- B) Show the caller both accounts' addresses and balances and let them choose
- C) Ask for one more identifier the caller knows (account number, email or phone on file), and block `set_up_payment_plan` in code until exactly one account is verified
- D) Keep the older-account rule and log each choice for a weekly review

<details><summary>Answer</summary>

**C.** The caller can settle the ambiguity for the cost of one turn, and the code gate means nobody acts on a guess. A still guesses; a written explanation doesn't make the guess right. B leaks another customer's address and balance; the tool result should never carry the candidates' details (9.3). D finds the wrong account only after the plan is in place.
</details>

**Q3. (Structured data extraction)** High-confidence invoice extractions are now auto-accepted. Three months later a large vendor changes its invoice layout and the `tax_amount` field starts coming out wrong, with high confidence. Which practice would have caught this soonest?

- A) Reviewing all low-confidence extractions
- B) A monthly report of overall accuracy
- C) Ongoing stratified random sampling of auto-accepted extractions by document type and vendor, with reviewer findings tracked per field
- D) Asking the model to flag layouts it hasn't seen before

<details><summary>Answer</summary>

**C.** The new errors are *confident* ones, so low-confidence review (A) never sees them. A stratified random audit of the auto-accepted stream measures the error rate where it is invisible, and per-field tracking shows exactly which field drifted. B is too coarse and too late. D relies on the model knowing what it doesn't know, which is the problem here.
</details>

**Q4. (Agent SDK)** Refunds over $500 need a supervisor's approval, which can take hours. A developer added `can_use_tool` to ask the supervisor, and set `allowed_tools=["mcp__support__process_refund", ...]` so routine refunds don't prompt. Large refunds go through without approval. What is the right fix?

- A) Add "ask a supervisor for refunds over $500" to the system prompt
- B) Register a `PreToolUse` hook on `process_refund` that checks the amount and returns `defer` (or `deny` with a redirect to `escalate_to_human`) above $500
- C) Switch the session to `bypassPermissions` so the callback runs for every tool
- D) Add a `PostToolUse` hook that reverses refunds over $500

<details><summary>Answer</summary>

**B.** A bare `allowed_tools` entry approves the call *before* `can_use_tool` runs, so the callback never fires for it (the SDK even warns about this shadowing). A `PreToolUse` hook runs on every matching call before any allow rule, so the `allowed_tools` entry can stay for routine refunds while the hook still sees every call. `defer` lets the run stop and resume when the supervisor decides, hours later. A is probabilistic. C makes it worse: `bypassPermissions` approves almost everything without reaching the callback. D undoes the damage after the money has moved, instead of preventing it.
</details>

**Q5. (Conversational assistant)** A meal-kit assistant is confirming next week's order. In turn 3 the customer said: "Keep my weekly spend under $60." In turn 9 they said: "Add the premium seafood box every week." With the seafood box, next week costs $72. What should the assistant do?

- A) Pick a cheaper seafood option so the total lands near $66, halfway between the two
- B) Follow the newer instruction and confirm the $72 order
- C) Name the conflict ("You asked to stay under $60, and the seafood box makes it $72") and ask which one wins
- D) Ask the customer to restate all their preferences from the start

<details><summary>Answer</summary>

**C.** The two statements can't both hold, and only the customer knows which matters more. Naming both is one short turn. A averages and satisfies neither statement. B silently drops the budget rule. D is over-asking: one targeted question is enough.
</details>

**Q6. (Conversational assistant)** Team leads ask an internal assistant: "Make a one-page summary of this incident report for the team." Before writing anything, the assistant asks five questions: audience, tone, length, format and sections. Logs show the first draft comes after a median of four back-and-forth turns, and some team leads now write the summaries by hand. The summary is easy to redo. What is the best change?

- A) Stop asking clarifying questions everywhere, including for refunds and account changes
- B) Pick sensible defaults, state them in one line above the draft ("I assumed an engineering audience and bullet points; tell me if you want something else"), and keep asking first only when a wrong guess is costly
- C) Switch to a larger model so it needs fewer questions
- D) Keep the questions, and if the user doesn't answer within two minutes, fill in defaults without saying which ones

<details><summary>Answer</summary>

**B.** A one-page summary is low-risk and reversible, so a stated assumption costs less than a turn of questions, and the user can still correct it. A removes asking where a wrong guess costs money or identity (9.3). C doesn't change the behavior, because the instruction to ask is the cause. D still blocks the user first, then hides what it assumed.
</details>

**Q7. (Agent design)** An admin agent has `delete_folder(path, dry_run)`. Its instructions say: "Always call with `dry_run=true` first and show the result to the user." In testing, the agent once called `dry_run=false` straight away and deleted a shared folder. Deletions must always follow a preview the user confirmed. What is the most reliable fix?

- A) Write the instruction in capital letters and add three examples of the preview-then-delete order
- B) Make `dry_run` default to `true`
- C) Split the tool: `preview_delete_folder` returns the files that would be deleted plus a single-use confirmation token, and `delete_folder` refuses to run without a valid, unused token from a preview of the same folder
- D) Log every `delete_folder` call and review the log each week

<details><summary>Answer</summary>

**C.** A flag can be skipped. A required token can't, because code checks it before anything is deleted. A and B still depend on the model choosing the safe path. D detects the deletion after it happened. If users never need deletes at all, removing the tool is stronger still (the control ladder in 9.4).
</details>

## Share your progress

```text
Chapter 9 of my Claude Certified Architect journey: when should an AI agent hand off to a human?

3 takeaways:
1. Escalate on an explicit request, a policy gap, or no progress. Not on angry tone, not on "I'm 7/10 sure".
2. If a rule must hold every time (ID check before a refund, a $500 limit), put it in code, not the prompt.
3. "97% accurate" can include a document type that is only 60% right. Calibrate per field, then keep a stratified audit sample.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #AIAgents #HumanInTheLoop #AIArchitecture #LearningInPublic
```
