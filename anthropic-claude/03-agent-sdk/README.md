# Chapter 3 — Claude Agent SDK: Building Agentic Systems

> **Exam domain(s):** Domain 1 — Agentic Architecture & Orchestration (**27%**, primary) · also touches Domain 2 — Tool Design & MCP Integration (18%) and Domain 5 — Context Management & Reliability (15%)
> **Est. time:** 5–7 hours (reading + 2 notebooks) · **Status:** [ ] not started

An agent is a model running in a loop: it picks a tool, sees the result, and decides again. This chapter shows how to run that loop yourself with the Client SDK, and how the Claude Agent SDK runs it for you with subagents, hooks, sessions, and approvals. As an architect you decide who owns the loop, how work is split across agents, and which rules must hold every time (code) versus most of the time (prompts).

## What you'll learn

- Why `stop_reason` (or `ResultMessage.subtype`) is the only reliable "done" signal
- How to define subagents with `AgentDefinition` and run a hub-and-spoke coordinator
- How to pass context to subagents explicitly and spawn them in parallel
- How to enforce rules with `PreToolUse` hooks and clean tool data with `PostToolUse` hooks
- When to resume, fork, or start fresh, and how to put a human in front of irreversible actions

## Prerequisites

- [Chapter 1 — Claude API Fundamentals](../01-claude-api-fundamentals/README.md) (`stop_reason`) and [Chapter 2 — Tool Use](../02-tool-use/README.md) (`tool_use` / `tool_result` blocks)
- [00 — Prerequisites](../../00-prerequisites/README.md): Python 3.11+, `async`/`await`, `.env` handling
- Install: `pip install anthropic claude-agent-sdk python-dotenv`. In Jupyter, use top-level `await main()`, not `asyncio.run(main())`.

## Concepts

### 3.1 The agentic loop

On each pass the model looks at the current state, picks an action (usually a tool call), sees the result, and decides again. The model chooses the next step from what it has learned so far. A hard-coded decision tree fixes the order of steps in advance instead.

#### Two ways to own the loop

| | **Client SDK** (`anthropic`) | **Agent SDK** (`claude-agent-sdk`) |
|---|---|---|
| Who runs the loop | Your code | The SDK (the same loop that powers Claude Code) |
| Tools | You define schemas **and** execute them | Built-in tools (`Read`, `Bash`, `Grep`, `Agent`...) plus your own and MCP tools |
| Extras | None. You build retries, permissions, context management | Permissions, hooks, subagents, sessions, compaction, cost caps |
| Choose when | You need full control, or a short, fixed workflow | You want a production agent quickly |

Write the manual loop once. It shows what the Agent SDK automates:

```python
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()                   # loads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic()  # reads the key from the environment

def run_agent(task, tools, impls, safety_cap=25):
    messages = [{"role": "user", "content": task}]
    for _ in range(safety_cap):  # safety net, never the success criterion
        resp = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=2048,
            tools=tools, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason == "end_turn":
            return resp                          # the task is done
        if resp.stop_reason == "tool_use":
            results = [{"type": "tool_result", "tool_use_id": b.id,
                        "content": json.dumps(impls[b.name](**b.input))}
                       for b in resp.content if b.type == "tool_use"]
            messages.append({"role": "user", "content": results})
            continue
        raise RuntimeError(f"Unhandled stop_reason: {resp.stop_reason}")
    raise RuntimeError("Safety cap reached. Investigate.")
```

Anti-patterns the exam targets:

- **Parsing the text for "Done".** The model can say "done" and still request a tool in the same response.
- **An iteration limit as the main stop condition.** It cuts off long tasks and hides runaway loops. Keep a cap (`max_turns`, `max_budget_usd` in the Agent SDK) only as a guardrail, and treat hitting it as an error.
- **"The response has text" means complete.** Claude often writes text **and** a `tool_use` block together.
- **Dropping `tool_result` blocks from history.** The model loses what it learned and repeats calls.

**In the Agent SDK** you don't write the loop. `query()` yields a stream of messages and ends with a `ResultMessage`. Iterate the stream to completion, then check `ResultMessage`: success is `subtype == "success" and not is_error` (final text in `result`). A run that ends on an API failure also arrives as `success`, but with `is_error=True` and the HTTP code in `api_error_status`. The error subtypes are `error_max_turns`, `error_max_budget_usd`, `error_during_execution`, or `error_max_structured_output_retries`. Use `ClaudeSDKClient` instead of `query()` for a multi-turn conversation in one process. The SDK does not load `.env` itself, so call `load_dotenv()`.

> [!NOTE]
> **Changed since the guide:** the package was renamed from `claude-code-sdk` to **`claude-agent-sdk`**, and `ClaudeCodeOptions` became **`ClaudeAgentOptions`**. Tool search is on by default, so expect `ToolSearch` calls in your traces.

#### Environment inspection: let the agent see what its actions did

An agent can only correct itself if it can observe the result of its actions. Give it read-only tools that report the current state: read a file before editing it, run the tests after a change, check an order's status after a refund. Pair every action tool (`process_refund`) with a way to check its effect (`lookup_order`). Return results specific enough to verify ("refund RF-001 for $129.00 issued", not "ok").

### 3.2 `AgentDefinition` configuration

`AgentDefinition` describes a **subagent**: a specialist the main agent can delegate to. You pass a dict of definitions to `ClaudeAgentOptions(agents=...)`, and the **dict key is the agent's name**.

```python
from claude_agent_sdk import AgentDefinition

AGENTS = {
    "order-specialist": AgentDefinition(
        description=(  # REQUIRED: tells the coordinator WHEN to delegate
            "Looks up orders and refund eligibility for a verified "
            "customer. Use after the customer ID is known. "
            "Never use for billing disputes."
        ),
        prompt=(       # REQUIRED: the subagent's system prompt
            "You are an order specialist. Use only the data passed to "
            "you. Return JSON: {order_id, status, refundable, reason}."
        ),
        tools=["mcp__support__lookup_order"],  # least privilege
        model="haiku",                         # alias; or a full model ID
        maxTurns=8,                            # camelCase (wire format)
    ),
}
```

The coordinator routes mainly by `description`, so write it like a good tool description. `prompt` holds the role, constraints, and output format. `model` takes an alias (`"haiku"`, `"sonnet"`, `"opus"`, `"fable"`, `"inherit"`) or a full model ID. **Omit `tools` and the subagent inherits every tool available to subagents.** Other optional fields include `disallowedTools`, `permissionMode`, `mcpServers`, `skills`, and `memory`.

Three settings are easy to mix up:

| Setting | Where | Effect |
|---|---|---|
| `ClaudeAgentOptions.allowed_tools` | Session | **Auto-approves** the listed tools. It does **not** hide other tools |
| `ClaudeAgentOptions.disallowed_tools` | Session | A bare name (`"Bash"`) **removes** the tool; a scoped rule (`"Bash(rm *)"`) denies matching calls |
| `AgentDefinition.tools` | Per subagent | The subagent's tool **set**. Tools you leave out don't exist for it |

> [!NOTE]
> **Changed since the guide:** the guide shows `AgentDefinition(name=..., system_prompt=..., allowed_tools=[...])`. The current SDK has **no `name` field** (the dict key is the name), and uses **`prompt`** and **`tools`**. A hard restriction comes from `AgentDefinition.tools` or `disallowed_tools`, not `allowed_tools`.

**Least privilege matters for quality, not only security.** An agent with 15+ tools picks the wrong one more often than one with 4–5 focused tools. Give each role only the tools it needs, plus a small, constrained utility when it saves round trips (a narrow `verify_fact` tool for a synthesis agent instead of full web search).

### 3.3 Hub-and-spoke: coordinator and subagents

One coordinator talks to the user and to every subagent. Subagents never talk to each other, so the coordinator sees every interaction, handles errors the same way everywhere, and controls what each subagent sees. It owns **decomposition** (subtasks that together cover the whole scope), **dynamic selection** (only the subagents a request needs), **delegation** with a self-contained prompt per subagent, **aggregation and validation** (merge, spot gaps or conflicts, re-delegate), **error handling** (retry, reroute, or continue with partial results), and **user communication** (the single voice to the user).

**Context isolation is the defining property.** A (non-fork) subagent starts with a **fresh** context: its own system prompt, the prompt string from the coordinator, and its tools. It does **not** see the parent's conversation. It returns **only its final message**, so its intermediate tool calls don't fill the coordinator's context. The exception is a **fork** (`subagent_type: "fork"`, Claude Code v2.1.302+), which copies the whole conversation; deny it with `disallowed_tools=["Agent(fork)"]` if you need strict isolation. Spawned subagents run in the background by default (the `Agent` result says `async_launched`), and their reports arrive in a later turn.

**Too-narrow decomposition.** Topic: "AI in creative industries". The coordinator splits it into digital art, graphic design, and photography. Every subagent succeeds, and the report still misses music, film, and writing. When every subagent succeeds but the output has gaps, look at the **coordinator's decomposition** first. **Partition before you delegate:** if two subagents search the same sources, assign **distinct subtopics or source types up front**. Deduplicating afterwards still wastes the tokens.

**Iterative refinement loop.** The coordinator checks the draft against its quality criteria (every area covered, every claim cited, conflicts flagged). For each gap it re-delegates a **targeted** query, then re-runs synthesis. It stops when the criteria are met or a round limit is reached, and it reports remaining gaps. **Write coordinator prompts as goals and quality criteria** ("cover all major sub-domains; every claim needs a source; flag conflicts"), not rigid step-by-step scripts. Scripts stop the coordinator from adapting.

**Error propagation (Domain 5.3):** a subagent retries transient failures locally. For an unrecoverable failure it returns **structured** context: failure type, what it tried, partial results, and alternatives. "0 results" and "connection timeout" are different reports. Never return an empty result marked as success.

### 3.4 The subagent tool (`Agent`, formerly `Task`)

The coordinator spawns a subagent by calling the built-in **`Agent`** tool. The tool input names the agent type (`subagent_type`) and carries the prompt string. The official examples list `"Agent"` in `allowed_tools`, but it is not strictly required: `Agent` runs without approval in the default permission mode.

> [!NOTE]
> **Changed since the guide:** the guide (and likely the exam) calls this tool **`Task`** and says `allowedTools` must include `"Task"`. `tool_use` blocks say `"Agent"` (older CLIs: `"Task"`), and the `system:init` tool list still says `"Task"`, so match **both names** in code. On the exam, read `Task` as "the subagent-spawning tool". Subagents can spawn their own subagents (default depth 3). Cap depth and spend with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and `max_budget_usd`.

**Explicit context passing.** For a non-fork subagent, the prompt string is the **only** thing that travels from parent to subagent:

```text
# Weak: the subagent has no idea what "the document" is
"Analyze the document."

# Strong: self-contained, data separated from instructions, defined output
"Analyze the contract below for termination clauses.
<document>…full text…</document>
<prior_findings source="web-researcher" retrieved="2026-10-01">
…</prior_findings>
Return JSON: {clause, section, risk_level, quote}.
If a field is missing, use null."
```

Include **full outputs** from earlier agents (not your paraphrase). Use tags or JSON to separate **data** from **metadata** (source, date). State the **output schema** so the coordinator can merge results.

**Parallel spawning.** Put independent subtasks in **several `Agent` calls in one coordinator response**. They run concurrently, so wall-clock time is set by the slowest subagent. Dependent steps (synthesis needs research) stay sequential.

### 3.5 Hooks in the Agent SDK

Hooks are **your code** running at fixed points in the agent lifecycle. They run in your process, outside the model's context, so they are **deterministic**: they fire on every matching event (a run cut off at `max_turns` may skip them).

- **Events (Python):** `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `Notification`, `PermissionRequest`.
- **Registration:** `hooks={Event: [HookMatcher(matcher=..., hooks=[cb])]}`. The `matcher` tests the **tool name** (exact, `"A|B"`, or a regex like `"^mcp__"`), never the arguments.
- **Callback:** `async def cb(input_data, tool_use_id, context) -> dict`. Return `{}` to let the call through.

#### Pattern A: block a policy violation and redirect to escalation (`PreToolUse`)

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

REFUND_LIMIT_USD = 500

def deny(reason):
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",        # the tool never executes
        "permissionDecisionReason": reason,  # Claude reads this and adapts
    }}

async def enforce_refund_limit(input_data, tool_use_id, context):
    try:                                     # fail closed: no default of 0
        amount = float(input_data["tool_input"].get("amount"))
    except (TypeError, ValueError):
        return deny("Refund amount is missing or not a number.")
    if amount > REFUND_LIMIT_USD:
        return deny(f"Refunds over ${REFUND_LIMIT_USD} need human approval. "
                    "Call mcp__support__escalate_to_human with customer_id, "
                    "amount, and reason.")
    return {}

options = ClaudeAgentOptions(hooks={"PreToolUse": [HookMatcher(
    matcher="mcp__support__process_refund", hooks=[enforce_refund_limit])]})
```

A guard must fail closed by itself: if a `PreToolUse` callback raises, the call is **not** blocked, it goes on to the normal permission flow. (`HookMatcher(..., on_failure="block")` changes that, but needs Python SDK 0.2.177+.)

#### Pattern B: a programmatic precondition (verify identity before any money moves)

Block downstream tools until a prerequisite succeeds. A `PostToolUse` hook on `mcp__support__get_customer` adds the session ID to a `verified_sessions` set, but only after it checks that the response is a real match. A `PreToolUse` hook on `mcp__support__lookup_order|mcp__support__process_refund` (MCP matchers need the full name) denies the call with "Call get_customer first to verify the customer's identity" until the session is verified.

#### Pattern C: normalize heterogeneous tool output (`PostToolUse`)

Third-party MCP servers return Unix timestamps, ISO strings, or numeric status codes, and you can't change their code. One `PostToolUse` hook (matcher `"^mcp__"`) converts everything into one format and returns it in `hookSpecificOutput.updatedToolOutput` before Claude reads it. The replacement must keep the **same shape** as the tool's output. For built-in tools a wrong shape is ignored. For MCP tools it reaches Claude unvalidated. The tool has **already run** when `PostToolUse` fires, so use `PreToolUse` to stop or change a call.

> [!NOTE]
> **Changed since the guide:** the guide's `@hook("PostToolUse")` decorator is pseudocode. You register async callbacks through `HookMatcher`. A deny is a **return value**, not a redirect function. `PreToolUse` can rewrite arguments with `updatedInput`. When several hooks match, the most restrictive decision wins. A hook `deny` applies even in `bypassPermissions`, but a hook `allow` does **not** skip deny and ask rules (see [3.7](#37-human-approval-for-irreversible-actions)).

#### Hooks vs prompt instructions

| | **Hooks / programmatic checks** | **Prompt instructions** |
|---|---|---|
| Guarantee | Deterministic: runs on every matching call | Probabilistic: usually followed, never guaranteed |
| Use for | Money, identity, compliance, safety, data formats | Tone, preferences, soft heuristics |
| Failure mode | Code bug (testable) | Silent skip in some percentage of runs |

**Rule:** if a single violation would have **financial, legal, or safety** consequences, enforce it in code. Better prompts and few-shot examples reduce the failure rate. They don't eliminate it.

<a id="36-sessions-resume-and-fork-bonus-from-domain-17"></a>

### 3.6 Sessions: resume and fork (Domain 1.7)

| Need | Agent SDK (Python) |
|---|---|
| Multi-turn chat in one process | `ClaudeSDKClient`: each `client.query()` continues the session |
| Continue the most recent session | `ClaudeAgentOptions(continue_conversation=True)` |
| Return to a specific session | Capture `ResultMessage.session_id`, then `resume=session_id` |
| Try an alternative, keep the original | `resume=session_id, fork_session=True` gives a **new** session ID |

**Named sessions.** In the Claude Code CLI you name a session with `--name` (`-n`) and return with `--resume <name>`:

```bash
claude -n auth-refactor-investigation         # day 1: start and name it
claude --resume auth-refactor-investigation   # day 2: continue it
claude --resume auth-refactor-investigation --fork-session  # branch
```

In the Python SDK, `resume=` takes a **session ID**. Title the session with `rename_session(session_id, "...")`, find it later with `list_sessions(directory=...)` by its `custom_title`, and pass its `session_id` to `resume=`. Forking branches the **conversation**, not the filesystem.

**Resume or start fresh?** Resume when the earlier context is still accurate. If files changed, **tell the agent what changed** when you resume. If most earlier tool results are stale, a **new session seeded with a structured summary** is more reliable.

### 3.7 Human approval for irreversible actions

Hooks enforce rules that never change ("no refund above $500, ever"). Other actions are fine **sometimes**, but a human should look first: sending email, deploying, deleting data, paying an invoice. The SDK checks a tool request in this order, and a call approved early never reaches later steps:

1. **`PreToolUse` hooks** can deny, allow, ask, defer, or rewrite. A hook `deny` wins even in `bypassPermissions`.
2. **Deny rules** (`disallowed_tools`, settings `deny`) block in **every** mode.
3. **Ask rules** send a match to `can_use_tool`, even in `bypassPermissions`.
4. **Permission mode.** `bypassPermissions` approves everything that reaches this step.
5. **Allow rules** (`allowed_tools`) approve the call, and **`can_use_tool` never sees it**.
6. **`can_use_tool`**, your callback, decides what is still unresolved. In `dontAsk` mode it is never called, and the call is denied.

**Permission modes:** `default` asks your callback for anything not pre-approved. `dontAsk` denies anything that would ask. `acceptEdits` auto-approves file edits and filesystem commands inside the working directories. `bypassPermissions` approves everything except a few protected actions. `plan` sends every edit to your callback. `auto` lets a model classifier decide. An unset mode starts in `default` (Claude Code v2.1.302+) unless a loaded settings file sets `permissions.defaultMode`; older CLIs could start in `auto` when feature flags weren't fetched. **Always set the mode explicitly**, so behavior doesn't depend on settings files or the CLI version.

#### Approval patterns

| Action class | Pattern | Mechanism |
|---|---|---|
| Read-only lookups | **Pre-approve** | Bare names in `allowed_tools` |
| Reversible edits in a sandbox | **Auto-approve within scope** | `acceptEdits` with `cwd` set to the sandbox |
| Hard-to-undo side effects (email, pay, deploy) | **Ask a human** | Keep it **out of** `allowed_tools`, `permission_mode="default"`, decide in `can_use_tool` |
| Never acceptable (`rm -rf`, over the hard limit) | **Deny** | `disallowed_tools` or a `PreToolUse` deny |
| Approval may take hours or days | **Defer** | A `PreToolUse` hook returns `"defer"`; resume once a person decides |

```python
from claude_agent_sdk import (
    ClaudeAgentOptions, PermissionResultAllow, PermissionResultDeny)

async def approval_gate(tool_name, input_data, context):
    """Reached only by calls that nothing earlier resolved."""
    decision = await ask_reviewer(tool_name, input_data)  # your UI
    if decision.approved:
        # Approve as-is or with edits. Claude isn't told about the edit.
        return PermissionResultAllow(
            updated_input=decision.edited_input or input_data)
    return PermissionResultDeny(
        message=f"Reviewer rejected this: {decision.reason}. "
                "Propose an alternative.")

options = ClaudeAgentOptions(
    permission_mode="default",     # explicit: don't depend on settings/CLI
    allowed_tools=["Read", "Glob", "Grep",
                   "mcp__crm__lookup_customer"],    # pre-approved reads
    disallowed_tools=["Bash(rm *)",
                      "mcp__crm__delete_customer"], # never, in any mode
    can_use_tool=approval_gate,    # everything else waits for a human
)
```

**Rule:** put rules that must **always** hold in a hook, and judgment calls in the approval callback. Never add a tool you want reviewed to `allowed_tools`: the allow rule approves the call at step 5, so the callback never runs. [Chapter 9](../09-escalation-human-in-the-loop/README.md) builds on this.

## Lesson code

Code from the video lesson: [../../presentations/03-agent-sdk/code/](../../presentations/03-agent-sdk/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Walk through 3.1–3.7 in code, then build a research coordinator with a spend gate, date normalization, and budget caps |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: a 12-question quiz, 7 auto-checked exercises, and an architecture scenario |

## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Short, fixed workflow; full control of every call | Client SDK manual loop | Agent SDK | Fewer moving parts |
| Production agent with files, shell, web, permissions, sessions | Agent SDK | Hand-rolled loop | Loop, tools, compaction, hooks, cost caps are built in |
| Rule with financial, legal, or safety impact | `PreToolUse` hook / programmatic precondition | Stronger system prompt | Deterministic vs probabilistic |
| Tools return inconsistent formats | `PostToolUse` normalization hook | Format notes in the prompt | Applied centrally on every call |
| Broad task with independent parts | Coordinator + parallel subagents | One agent doing everything | Context isolation and speed |
| Small, sequential task | Single agent | Multi-agent | Every hop adds tokens, latency, failure points |
| Subagent needs prior findings | Full findings in the `Agent` prompt | "It will remember" | Subagents start fresh |
| Exploring two alternative approaches | `fork_session=True` | Restarting from scratch | Same starting context, independent branches |
| Earlier session's tool results are stale | New session + structured summary | `resume` | Avoids outdated observations |
| A human should confirm the action | Leave it out of `allowed_tools`, decide in `can_use_tool` | Pre-approving it | Allow rules resolve the call before the callback |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Text or iteration caps as the completion signal.** Use `stop_reason` or `ResultMessage.subtype`; treat a cap as an error.
- **Assuming subagents share memory.** Anything a subagent needs must be in its prompt.
- **Omitting `tools` on a subagent "to be safe".** It grants every available tool.
- **Thinking `allowed_tools` is a sandbox.** It only auto-approves. Restrict with `disallowed_tools`, `AgentDefinition.tools`, or hooks.
- **Business rules only in the prompt.** Refund limits and identity checks get skipped in some fraction of runs.
- **Leaving `permission_mode` unset, or pre-approving a tool you want reviewed.** The mode then depends on settings files and the CLI version, and an allow rule skips `can_use_tool`.

## Self-check

**Q1.** An agent built with the Client SDK sometimes stops early. The loop ends when the assistant's text contains "complete", or after 5 iterations. What is the best fix?

- A) Raise the iteration limit to 20
- B) Add "Only say 'complete' when truly finished" to the system prompt
- C) Continue while `stop_reason == "tool_use"` and finish on `"end_turn"`, keeping a high cap only as a safety net
- D) Stop when the response contains no text block

<details><summary>Answer</summary>

**C.** `stop_reason` is the structured, explicit signal. A and B keep the unreliable mechanisms (an arbitrary cap and text matching). D is wrong because Claude often returns text together with a `tool_use` block.
</details>

**Q2.** A coordinator researched a customer's contract history over 12 turns, then delegated "Draft the renewal recommendation" to a `writer` subagent. The draft ignores everything learned. Why?

- A) The writer's model is too small
- B) Subagents start with a fresh context, and the coordinator didn't include its findings in the delegation prompt
- C) The writer's `maxTurns` is too low
- D) The coordinator should share its memory store with the writer

<details><summary>Answer</summary>

**B.** The Agent tool's prompt string is the only channel from parent to subagent. The fix is to pass the full findings, ideally structured, in that prompt. D is not how context reaches a subagent: a named custom subagent such as `writer` doesn't receive the coordinator's conversation. Only a fork (`subagent_type: "fork"`, Claude Code v2.1.302+) inherits it, and then it inherits all of it. (`AgentDefinition.memory` exists, but it gives a subagent its own persistent memory source across runs. It does not share the coordinator's conversation.)
</details>

**Q3.** In 9% of conversations a support agent calls `process_refund` before `get_customer` has verified identity. Prompt changes cut this to 4%. What should you do next?

- A) Add more few-shot examples showing the correct order
- B) Add a programmatic precondition (a `PreToolUse` hook) that denies `lookup_order` and `process_refund` until `get_customer` has succeeded in the session
- C) Add a routing classifier in front of the agent
- D) Move the verification instruction to the end of the system prompt

<details><summary>Answer</summary>

**B.** Identity before money is a deterministic requirement. Prompt-based options (A, D) only lower the probability of a skip. C addresses routing, not tool ordering.
</details>

**Q4.** An operations agent may send customer emails, but a person must approve each one. The team lists `mcp__mail__send` in `allowed_tools` and writes the review logic in `can_use_tool`. Emails go out without review. What is the fix?

- A) Add "always ask before sending email" to the system prompt
- B) Switch to `permission_mode="bypassPermissions"` so that the callback runs for every tool
- C) Remove `mcp__mail__send` from `allowed_tools`, set `permission_mode="default"` explicitly, and keep the review in `can_use_tool`
- D) Switch to `permission_mode="dontAsk"` so that unlisted calls are reviewed

<details><summary>Answer</summary>

**C.** An allow rule approves the call before the callback is consulted, so a tool you want reviewed must not be pre-approved. A is probabilistic. B approves every call that reaches the mode step, so the callback never runs. D never calls the callback and denies instead of asking. If the review must happen even when someone later adds an allow rule, return `"ask"` from a `PreToolUse` hook.
</details>

## Official documentation

- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop)
- [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents)
- [Hooks in the SDK](https://code.claude.com/docs/en/agent-sdk/hooks)
- [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

[← Chapter 2 — Tool Use](../02-tool-use/README.md) | [↑ Claude path overview](../README.md) | [Chapter 4 — Model Context Protocol →](../04-model-context-protocol/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
