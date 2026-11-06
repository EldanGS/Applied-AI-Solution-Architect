# Chapter 9 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/api/design-build-agentic-systems/24` | Human-in-the-loop designs where a person accepts or rejects agent suggestions | [9.4](../README.md#94-approval-gated-tools-in-the-agents-sdk) (approve / reject on `RunState`), [9.5](../README.md#95-pause-serialize-resume-long-running-reviews) (durable review), [9.6](../README.md#96-mcp-approvals-require_approval-and-mcp_approval_request) (MCP approvals); practice mini-project in [`01_practice.ipynb`](../01_practice.ipynb); homework exercises 2–3 in [`02_homework.ipynb`](../02_homework.ipynb) | Primary |
| `OAI/api/design-build-agentic-systems/2` | Control tool access so tool use stays within safety limits | [9.1](../README.md#91-when-to-escalate) (tool risk ratings), [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) (tool input guardrail policy gate), [9.4](../README.md#94-approval-gated-tools-in-the-agents-sdk) (`needs_approval`), [9.6](../README.md#96-mcp-approvals-require_approval-and-mcp_approval_request) (`require_approval` split policy) | Primary |
| `OAI/api/design-build-agentic-systems/3` | Design reliable, safe handoffs between agents | [9.7](../README.md#97-structured-handoff-to-a-human) (handoff to a human vs an SDK agent handoff); agent-to-agent handoffs are taught in [Chapter 8](../../08-task-decomposition-and-orchestration/README.md) (8.3) | Supporting |
| `OAI/api/design-build-agentic-systems/5` | Preserve ownership at every handoff | [9.2](../README.md#92-escalation-patterns-and-the-escalate-tool) (`StopAtTools` ends the run when the escalate tool fires, so the agent can't keep acting after handing over), [9.7](../README.md#97-structured-handoff-to-a-human) (code-owned facts in the handoff) | Supporting |
| `OAI/api/design-build-agentic-systems/6` | Define outcome and safety requirements for the workflow | [9.1](../README.md#91-when-to-escalate) (triggers, tool risk ratings), [9.8](../README.md#98-confidence-calibration-with-labeled-sets) (target precision), [9.10](../README.md#910-operating-human-in-the-loop-in-production) (metrics) | Supporting |
| `OAI/api/design-build-agentic-systems/7` | Test whether decisions and handoffs meet those requirements | [9.8](../README.md#98-confidence-calibration-with-labeled-sets), [9.9](../README.md#99-stratified-sampling-for-human-review); homework exercises 1, 4–6 and the architecture scenario | Supporting |
| `OAI/api/design-build-agentic-systems/19` | Input/output guardrails, tripwires, jailbreak and irrelevant-input protection | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) (blocking input guardrail, output guardrail, workflow boundaries, layered defense) | Supporting |
| `OAI/api/design-build-agentic-systems/22` | Structured outputs for agent output the app consumes | [9.7](../README.md#97-structured-handoff-to-a-human) (strict `HumanHandoff` schema as the escalate tool's argument) | Supporting |
| `OAI/api/scope-ai-solutions/5` | Solution plan that helps decide whether to build | [9.1](../README.md#91-when-to-escalate) (risk ratings in the plan), [9.8](../README.md#98-confidence-calibration-with-labeled-sets) (review workload), [9.10](../README.md#910-operating-human-in-the-loop-in-production) | Supporting |
| `OAI/api/scope-ai-solutions/12` | Considerations from prototype toward production | [9.5](../README.md#95-pause-serialize-resume-long-running-reviews) (durable reviews, version drift), [9.10](../README.md#910-operating-human-in-the-loop-in-production) (operations) | Supporting |
| `OAI/api/evaluate-ai-applications/3` | Build representative test cases | [9.8](../README.md#98-confidence-calibration-with-labeled-sets) (labeled validation set), [9.9](../README.md#99-stratified-sampling-for-human-review) (reviewed corrections become cases) | Supporting |
| `OAI/api/evaluate-ai-applications/5` | Diagnose failures | [9.9](../README.md#99-stratified-sampling-for-human-review) (per-stratum accuracy), [9.10](../README.md#910-operating-human-in-the-loop-in-production) (approval / rejection metrics) | Supporting |
| `OAI/api/evaluate-ai-applications/18` | Pair evals with input and output guardrails | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) (measure a guardrail on labeled messages; Moderation API in the layered defense) | Supporting |
| `OAI/bootcamp/api-builder/12` | Agents: guardrails and guardrail tripwires | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) (tripwire exceptions, `run_in_parallel=False`, `reject_content`) | Primary |
| `OAI/bootcamp/api-builder/20` | Realtime: guardrails, identity verification, action confirmation | [9.4](../README.md#94-approval-gated-tools-in-the-agents-sdk) (Realtime `approve_tool_call` / `reject_tool_call` row only; Realtime gets its own chapter) | Supporting |
| `OAI/tracks/ai-app-development/13` | Reference demo: support agent with human-in-the-loop | Practice mini-project (approval-gated refund desk) in [`01_practice.ipynb`](../01_practice.ipynb) | Primary |
| `OAI/tracks/ai-app-development/20` | Input and output guardrails against unsafe behavior | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) | Supporting |
| `OAI/tracks/building-agents/20` | Input guardrails scaled to the risk | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) (rules-based + classifier + moderation, sized to the risk) | Supporting |
| `OAI/tracks/building-agents/21` | Structured outputs for app-consumed output; output guardrails for user-facing agents | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) (output guardrail), [9.7](../README.md#97-structured-handoff-to-a-human) (strict schema) | Supporting |
| `OAI/foundations/applied-ai-foundations/10` | Build review points, checkpoints and human review into the process | [9.1](../README.md#91-when-to-escalate), [9.4](../README.md#94-approval-gated-tools-in-the-agents-sdk) | Supporting |
| `OAI/foundations/agents-and-workflows/9` | Decide what to delegate; place checkpoints and human review | [9.1](../README.md#91-when-to-escalate) (risk ratings), [9.4](../README.md#94-approval-gated-tools-in-the-agents-sdk), [9.10](../README.md#910-operating-human-in-the-loop-in-production) (graduated autonomy) | Supporting |
| `OAI/foundations/agents-and-workflows/12` | Identify where human judgment and oversight are required | [9.1](../README.md#91-when-to-escalate), [9.10](../README.md#910-operating-human-in-the-loop-in-production) (9.1: conflicting user statements, don't over-ask; More self-check questions 5, 6) | Supporting |
| `ROLE/AGENT/6` | Human-in-the-loop and autonomy safeguards: approval gates, escalation paths, stop conditions | Whole chapter ([9.1](../README.md#91-when-to-escalate)–[9.10](../README.md#910-operating-human-in-the-loop-in-production)) | Primary |
| `ROLE/AGENT/5` | Agent memory and state management | [9.5](../README.md#95-pause-serialize-resume-long-running-reviews) (`RunState` persistence, sessions, 30-day response retention) | Supporting |
| `ROLE/SAFE/2` | Guardrails, content filters, moderation, policy enforcement | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) | Supporting |
| `ROLE/SAFE/3` | Hallucination mitigation: verification and confidence signals | [9.7](../README.md#97-structured-handoff-to-a-human) (facts filled from the run), [9.8](../README.md#98-confidence-calibration-with-labeled-sets) (calibrated confidence) | Supporting |
| `ROLE/SAFE/7` | Auditability, logging and provenance | [9.7](../README.md#97-structured-handoff-to-a-human) (`actions_taken` from the run log), [9.10](../README.md#910-operating-human-in-the-loop-in-production) (audit trail) | Supporting |
| `ROLE/SAFE/9` | Responsible AI and safety-first judgment | [9.1](../README.md#91-when-to-escalate), [9.10](../README.md#910-operating-human-in-the-loop-in-production) (fail closed, separation of duties, platform stops) | Supporting |
| `ROLE/SAFE/10` | Securing agent and tool access | [9.3](../README.md#93-enforcement-vs-prompt-guidance-guardrails-and-policy-gates) (ownership checks), [9.5](../README.md#95-pause-serialize-resume-long-running-reviews) (server-side, authenticated approvals), [9.6](../README.md#96-mcp-approvals-require_approval-and-mcp_approval_request) | Supporting |
| `ROLE/EVAL/3` | Representative datasets, baselines and human judgment | [9.8](../README.md#98-confidence-calibration-with-labeled-sets), [9.9](../README.md#99-stratified-sampling-for-human-review) | Supporting |

OpenAI Academy course internals are gated. `design-build-agentic-systems/19`, `/22`, `/24`, `scope-ai-solutions/12` and `evaluate-ai-applications/18` are inferred from public bootcamp sessions and developer tracks (course internals are gated), so treat those mappings as best-effort until the course content is public.

## More self-check questions

**1.** Refund approvals sometimes wait overnight. The team wants to send the serialized `RunState` to the reviewer's browser and accept it back with the decision, to avoid a database. What does the architect say?

- A) Fine; `RunState.from_string` validates the schema version, so tampering is detected
- B) Keep the snapshot in server storage; send the browser only displayable details and opaque IDs; authenticate and authorize the reviewer on the server; apply decisions only to `state.get_interruptions()` from the stored snapshot; consume each review once
- C) Fine, as long as the blob is base64-encoded
- D) Use `context_override` on load; that makes a client-supplied snapshot safe

<details><summary>Answer</summary>

**B.** The SDK docs say deserialization does not authenticate the snapshot or the submitter, and that a schema check or fingerprint is not authentication. The snapshot also contains tool arguments, decisions and the context. C is encoding, not security. D: replacing the context does not neutralize the other fields.
</details>

**2.** Reviewers complain that they're asked to approve refunds of $900, and after they approve, the policy gate rejects them anyway. What is the fix?

- A) Lower the approval threshold to $0 so reviewers see everything
- B) `RunConfig(tool_execution=ToolExecutionConfig(pre_approval_tool_input_guardrails=True))` so the tool input guardrail runs before the approval request
- C) Move the policy gate into the instructions
- D) Remove `needs_approval` and rely on the guardrail alone

<details><summary>Answer</summary>

**B.** By default, tool input guardrails run after approval, just before execution. This setting runs them first, so reviewers only see calls that policy allows. D removes the human gate for allowed high-risk refunds.
</details>

**3.** A team connects a remote CRM MCP server through the Responses API `mcp` tool and sets `"require_approval": "never"` to save latency. The server exposes `search_contacts`, `get_contact`, `update_contact` and `delete_contact`. What should change?

- A) Nothing; approvals are only for debugging
- B) `{"never": {"tool_names": ["search_contacts", "get_contact"]}}`, so writes still produce `mcp_approval_request` items that a human answers with `mcp_approval_response`
- C) Keep `"never"` and add "don't delete contacts" to the instructions
- D) Use `HostedMCPTool` with an `on_approval_request` callback that always returns `{"approve": True}`

<details><summary>Answer</summary>

**B.** Skip approvals only for read-only tools of a trusted server. C is a probabilistic rule for a destructive action. D is automated approval of everything, which keeps the latency and removes the protection.
</details>

**4.** A support agent escalates by forwarding the full 40-turn transcript to the human queue. Agents complain it takes 5 minutes to understand each case, and some summaries mention order IDs that don't exist. What is the best fix?

- A) Ask the model to write a longer summary
- B) A strict `HumanHandoff` schema as the escalate tool's argument (reason enum, summary, request, actions taken, amount, recommendation), with `customer_id` and `actions_taken` filled from the authenticated context and the run's `new_items`, and order IDs checked against the database
- C) Hand off to a second agent that rewrites the transcript
- D) Show the human only the last customer message

<details><summary>Answer</summary>

**B.** The human needs a self-contained summary. Facts the code can know should come from the run log and trusted data, not from the model's recollection. A and C keep facts model-generated. D loses context.
</details>

**5.** Early in a chat with a retail agent, the customer said: "Don't share my details with partner companies." Ten turns later they say: "Sign me up for the partner rewards programme." Joining the programme sends the customer's email to partner companies. What should the agent do?

- A) Sign them up, because the newest instruction wins
- B) Skip the sign-up without saying why, because privacy comes first
- C) Name the conflict ("The rewards programme shares your email with partners, which you asked us not to do") and ask which one they want
- D) Sign them up with as few details as possible, as a compromise

<details><summary>Answer</summary>

**C.** The two statements can't both hold, and only the customer can say which wins. A and B each pick one silently. D is averaging: it still shares the email and honors neither statement fully.
</details>

**6.** An internal analytics agent gets: "Chart last quarter's sign-ups." Its instructions say to confirm every request before acting, so it asks about chart type, date range, grouping and colors before running the read-only query. Users say it's slower than building the chart themselves. The same agent can also email reports to customers. What should change?

- A) Nothing; confirming every request is the safe default
- B) For low-risk, reversible requests, pick defaults (for example weekly sign-ups for the last full quarter as a line chart), say them in one line next to the chart and invite changes; keep confirm-first for actions like emailing customers
- C) Ask the model to rate how ambiguous each request is from 1 to 10, and ask questions above 5
- D) Remove confirmations everywhere, including before emailing customers

<details><summary>Answer</summary>

**B.** A chart is cheap to redo, so a stated assumption beats a round of questions, and the user can still correct it. Emailing customers can't be undone, so it keeps its confirmation. A wastes the user's turns on a read-only request. C is an uncalibrated self-rating, the weak signal from 9.1. D removes the check where a wrong guess is costly.
</details>

## Share your progress

```text
OpenAI branch, chapter 9: when an agent should stop and hand over to a human.

3 takeaways:
1. Escalate on explicit requests, policy gaps, failure limits and risky actions. Not on sentiment or a self-rated 1-10.
2. Agents SDK: needs_approval pauses the run, RunState serializes it, and you resume the same run. Keep that blob on the server.
3. Confidence means nothing until it's calibrated on labeled data. Then stratified audits catch the 4% segment that's 30% wrong.

#OpenAI #AIAgents #HumanInTheLoop #AIArchitecture #BuildInPublic
```
