# Chapter 11 — Context Management in Production Systems

> **Claude counterpart:** [Chapter 11 — Context Management in Production Systems](../../anthropic-claude/11-context-management/README.md) · **Academy course(s):** Optimize AI Application Performance (API pathway, 30 min); Design and Build Agentic Systems (API pathway, 110 min) · **Est. time:** 6–8 hours (reading + 2 notebooks) · **Status:** [ ] not started

<a id="why-this-matters-for-a-solution-architect"></a>
Long-running systems (a three-week support chat, a two-hour code investigation, a workflow that waits overnight for a human) all hit the same wall. Context grows every turn, every turn re-bills the whole history, quality drops as stale tool output piles up, and a crash loses state nobody wrote down. The architect decides where state lives, what goes into each request, how history shrinks and how work survives a crash. On OpenAI the compaction item is **encrypted and opaque**, so the facts the business depends on must live in a structured block that **you** own.

<a id="learning-objectives"></a>
## What you'll learn

- What fills a GPT-6 request's window, why a long chat's bill grows roughly quadratically, and how to measure and budget it (including the 272K pricing threshold)
- How to pick a state strategy by asking **who can edit the history**, and why compaction beats `truncation="auto"`
- How to manage long Agents SDK runs: session limits, input filters, `ToolOutputTrimmer`, compacting sessions
- The case-facts block, tool-output trimming, position-aware input, scratchpads and delegation to sub-agents
- Checkpoint/restore for crash recovery, and how all of this interacts with prompt caching

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md), [Chapter 01](../01-responses-api-fundamentals/README.md) (conversation state, tokens and cost), [Chapter 03](../03-agents-sdk-and-agents-api/README.md) (`Runner`, sessions, agents-as-tools, `RunState`) and [Chapter 07](../07-batch-and-cost/README.md) (prompt caching). Snippets assume `client = OpenAI()` and `MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")`. Responses Multi-agent (beta) needs `gpt-6.1-sol` or a GPT-5.6 model, not Luna.

## Concepts

### 11.1 What fills the window, and what it costs

The context window counts **input, output and reasoning tokens together**. The GPT-6 models (`gpt-6-astra`, `gpt-6.1-sol`, `gpt-6-luna`) list a 1,050,000-token window, at most 922,000 of it input, and 128,000 maximum output tokens. Instructions and tool definitions stay fixed if you keep them stable. Messages, tool outputs (usually the fastest-growing part) and earlier reasoning items grow every turn. With `reasoning={"context": "current_turn"}`, earlier reasoning items are not rendered into the next sample. `all_turns` renders them; the reasoning guide lists it for GPT-5.6 (its default there) and `gpt-6.1-sol`. Omit the field (`auto`) to use the model's default, and read `response.reasoning.context` to see the mode used.

**Why long chats get expensive.** Every turn re-bills the whole history as input, even with `previous_response_id`. At about 3,000 tokens per turn, 60 turns bill 3,000 × (1 + 2 + … + 60) = **5.49M input tokens**: about $0.55 on `gpt-6-luna` and about $55 on `gpt-6-astra` before caching. Caching lowers the **price** of the repeated prefix; trimming and compaction lower the **size**.

**The 272K threshold.** On GPT-6, prompts with more than 272K input tokens are priced at 2x input and cache rates and 1.5x output **for the full request**. That is a natural ceiling for your budget.

**Measure before and after.** `client.responses.input_tokens.count(...)` takes the same payload as `responses.create` (also `previous_response_id` or `conversation`) and returns exact `input_tokens`. After the call, log per turn `usage.input_tokens`, `usage.input_tokens_details.cached_tokens` and `.cache_write_tokens`, `usage.output_tokens`, and `usage.output_tokens_details.reasoning_tokens` (counted inside `output_tokens`). The trend tells you when to compact.

A context budget turns these numbers into a policy. Quality usually degrades well before the window is full, so set the soft limit from your **evals**, not from the model card.

```python
WINDOW_CEILING = 272_000   # pricing threshold, not the 1.05M window
OUTPUT_RESERVE = 25_000    # reserve >= 25K for reasoning + output
SOFT_LIMIT = 0.6 * (WINDOW_CEILING - OUTPUT_RESERVE)  # compact here
HARD_LIMIT = WINDOW_CEILING - OUTPUT_RESERVE          # never send above

def next_action(input_tokens: int) -> str:
    if input_tokens >= HARD_LIMIT:
        return "compact_now"  # or delegate / start fresh from case facts
    if input_tokens >= SOFT_LIMIT:
        return "compact"
    return "send"
```

### 11.2 Conversation state for long-running work: who can edit the history?

For context management the deciding question is: **can you curate what the model sees next turn?**

| Strategy | Can you remove or rewrite items? | Retention | Fits when… |
|---|---|---|---|
| **Stateless** (`store=False`, replay `response.output`) | **Yes, fully.** You build `input` every turn | No application state; abuse logs up to 30 days unless ZDR is approved | You need ZDR, full control or portability |
| **Chained** (`previous_response_id`) | **No.** The chain is immutable; start a new chain to drop content | 30 days per response | Short-to-medium sessions |
| **Durable** (Conversations API, `conversation=conv.id`) | **Partly.** `conversations.items.delete` / `items.create` | Until you delete it; not ZDR-eligible | Threads shared across workers, devices or jobs |
| **Agents SDK session** (`SQLiteSession`, `RedisSession`, …) | **Yes.** `get_items`, `pop_item`, input callbacks (11.5) | Your infrastructure | Agent apps that need durable, inspectable state |

- **Pick one strategy per conversation.** Mixing local replay with server-managed state can duplicate context. `previous_response_id` and `conversation` cannot be combined, and a session cannot be combined with either.
- **`store=False` is not ZDR.** ZDR is an org- or project-level control that OpenAI must approve. Stateless replay must keep every output item, including reasoning items. **Chained IDs expire after 30 days.** A long pause must be resumable from **your** state (11.11). Compaction with Conversations is not documented (`/responses/compact` has no `conversation` parameter).
- **The managed [Agents API](../03-agents-sdk-and-agents-api/README.md#39-the-managed-agents-api-beta)** (beta) manages sessions, compaction and recovery for you. You write less code but control even less of what is kept, so the case-facts block (11.6) still applies.

### 11.3 Truncation: the blunt instrument

`truncation` has two values. `"disabled"` (the **default**) fails with HTTP 400 when the input exceeds the window. `"auto"` drops items **from the beginning of the conversation** until it fits. Those first turns are where the customer gave their account number and order ID. It drops them silently and changes the prefix, so the next turns miss the cache. The Agents SDK exposes it as `ModelSettings(truncation="auto")`. It is acceptable for a disposable chat UI and risky for anything transactional. Production default: leave it `"disabled"`, measure (11.1), and compact or delegate **before** the limit. Treat a context-overflow 400 as a bug in your budget policy, not a retryable error.

### 11.4 Compaction: server-side and standalone

Compaction replaces earlier context with a shorter representation. **Server-side** compaction runs inside `responses.create`: when the rendered tokens cross `compact_threshold`, the server emits a **compaction item** in the same response and continues. **Standalone** compaction (`client.responses.compact(...)`) is an extra, billed call you make at a moment you choose.

```python
# Server-side: the API compacts when the window crosses the threshold
response = client.responses.create(
    model=MODEL,
    input=conversation,
    store=False,                       # ZDR-friendly with store=False
    context_management=[{"type": "compaction", "compact_threshold": 150_000}],
)
conversation.extend(response.output)   # includes any compaction item

# Standalone: you decide when (the input must still fit the window)
compacted = client.responses.compact(model=MODEL, input=long_input_items)
next_input = [*compacted.output, new_user_message]  # AS-IS, never prune
```

| | Server-side (`context_management`) | Standalone (`responses.compact`) |
|---|---|---|
| Who decides when | The API, at `compact_threshold` | Your code |
| Extra call | No | Yes (billed) |
| Pruning | Stateless: may drop items before the latest compaction item (a latency optimization). `previous_response_id`: pass only the new message, **do not prune** | Use the returned window as-is |
| Typical use | Long agent loops | After a phase ends, before a handoff, at a checkpoint |

Compact after major milestones, not every turn, and compact **before** you run out of room. **The compaction item is opaque**: you cannot read, audit or move it to another provider (Claude's compaction block holds a readable summary). So exact facts live in your case-facts block (11.6), and everything the business must reconstruct goes to your store (11.11). Also: do not combine `configuration_update` items with automatic compaction. If you need both, turn automatic compaction off and compact explicitly with a `compaction_trigger` item as the final input item, then add a fresh `configuration_update`. With Responses Multi-agent, `/responses/compact` is not supported and compaction runs per agent.

### 11.5 Long runs in the Agents SDK: limits, filters, trimmers and compacting sessions

| Tool | What it does |
|---|---|
| `SessionSettings(limit=N)` | Loads only the latest N stored items for this run |
| `session_input_callback(history, new_input)` | Runs once per `Runner.run`; decides how history and new input combine. Stored data is not changed |
| `call_model_input_filter(CallModelData)` | Runs **before every model call** in the loop; edits `input` and `instructions`. A good place to inject fresh case facts |
| `ToolOutputTrimmer(...)` | Replaces large tool outputs from older turns with a short preview. Never trims inside the current turn |
| `OpenAIResponsesCompactionSession` | Wraps another session; calls `responses.compact` when a decision hook says so |

```python
from agents import OpenAIResponsesCompactionSession, RunConfig, Runner, SessionSettings, SQLiteSession
from agents.extensions import ToolOutputTrimmer   # not exported from `agents`

store = SQLiteSession("case_4711", "support.db")   # file-backed
session = OpenAIResponsesCompactionSession(
    session_id="case_4711",
    underlying_session=store,
    model=MODEL,                  # the default is "gpt-4.1": set it
    should_trigger_compaction=lambda ctx:
        len(ctx["compaction_candidate_items"]) >= 40,
)
run_config = RunConfig(
    session_settings=SessionSettings(limit=200),  # max 200 items
    call_model_input_filter=ToolOutputTrimmer(
        recent_turns=2,             # last 2 user turns stay full
        max_output_chars=800,       # older outputs above this...
        preview_chars=200,          # ...become a 200-char preview
        trimmable_tools={"lookup_order", "search_kb"},
    ),
)
result = await Runner.run(support_agent, user_message,
                          session=session, run_config=run_config)
```

- The default compaction trigger is 10 or more candidate items, which is aggressive for chat; set your own. `await session.run_compaction({"force": True})` compacts on demand. It **cannot wrap** `OpenAIConversationsSession` (it raises `ValueError`).
- `ToolOutputTrimmer` has **no error exemption**. Wrap it so error outputs stay readable (the notebook's `preserve_errors`).
- If you cut history by item count, cut at a **user-message boundary**, or a `function_call_output` can be left without its parallel `function_call` (an orphaned output). `SQLiteSession("case_4711")` without a path is in-memory. For crash recovery or many workers, use a file or a shared backend (`SQLAlchemySession`, `RedisSession`, `MongoDBSession`, `DaprSession`).

### 11.6 The case-facts block

Some information is **transactional**: customer ID, order ID, amounts, dates, what we promised, status. Summaries blur it ("around $90"), truncation drops it and compaction hides it. Keep it in a structured object your code owns and render it into every request. Update fields from **tool results** and a small structured extraction, merge in code, bump `version` and log the change. Do not let the model rewrite the block from memory. `render_facts` turns the object into a `<case_facts version="N">` block.

```python
class CaseFacts(BaseModel):
    customer_id: str
    order_id: str | None = None
    order_total: str | None = None   # exact string, e.g. "74.95 USD"
    issue: str | None = None
    commitments: list[str] = Field(default_factory=list)  # with dates
    status: str = "open"
    version: int = 1

def build_input(stored_history, facts, user_message) -> list:
    return [
        *stored_history,                      # append-only, cacheable
        {"role": "developer", "content": render_facts(facts)},  # ephemeral
        {"role": "user", "content": user_message},
    ]
```

**Where to put it.** In `instructions`, it can never go stale, but expect every facts change to invalidate the cached prefix. As an **ephemeral** developer message at the end of `input` (not saved to history), it sits near the question and the prefix stays cacheable. This is the default for stateless and Agents SDK designs. In a chained conversation each copy is stored, so label versions ("supersedes all earlier case_facts").

### 11.7 Trimming verbose tool outputs

Tool outputs are the largest and least durable part of the context. Trim at three levels:

1. **At the source (best).** The function tool returns only the fields the agent needs.
2. **In older turns.** `ToolOutputTrimmer` (11.5), or in your own loop replace the `output` string of old `function_call_output` items. Never delete the item.
3. **Into facts.** Once a result has updated the case-facts block, the full output is not needed after a few turns.

```python
ORDER_FIELDS = ("order_id", "status", "total", "placed_at", "refund_window_ends")

@function_tool
def lookup_order(order_id: str) -> str:
    """Look up an order by ID. Returns status, total, date, refund deadline."""
    record = orders_api.get(order_id)                       # ~35 fields
    return json.dumps({k: record.get(k) for k in ORDER_FIELDS})
```

Keep every `function_call` paired with its `function_call_output` (same `call_id`). Do not trim inside the current turn: items between the last user message and the latest function call output must reach the model untouched. Keep error outputs readable. Trimming changes the prefix and misses the cache, so trim in batches (for example when you compact).

### 11.8 Position-aware input

Models use the beginning and end of a long input more reliably than the middle. OpenAI's GPT-4.1 guide says to put instructions **at both the beginning and the end** of long context; if only once, above works better than below. It is an older guide, so validate on GPT-6 with your own evals. For aggregated sub-agent results, use a `## SUMMARY (read first)` section, then `## EVIDENCE`, then `## TASK (restated)`.

| Position | Content | Why |
|---|---|---|
| Start (stable) | Instructions, developer rules, tool definitions | Attention and **cacheable prefix** |
| Middle | Compacted context, older turns, trimmed tool outputs | Least critical; may be compacted |
| End (dynamic) | Case-facts block, latest tool results, new user message | Near the question; after the cached prefix |

### 11.9 Scratchpad files and memory across sessions

A **scratchpad** is a file (or database row) where the agent writes key findings with sources, then reads them back after compaction or in a new session. You can build it with function tools, a shell tool or sandbox file, or `apply_patch`; pair `append_note` with a `read_notes` tool the agent calls before re-running discovery. In Codex, `/compact`, `/status`, `/new`, `/resume` and `/fork` manage context, and `AGENTS.md` carries project guidance across sessions.

```python
NOTES = Path("case-notes/findings.md")

@function_tool
def append_note(finding: str, source: str) -> str:
    """Record one verified finding with its source (file:line, URL)."""
    NOTES.parent.mkdir(parents=True, exist_ok=True)
    with NOTES.open("a") as f:
        f.write(f"- {finding} (source: {source})\n")
    return "saved"
```

**History across months.** Do not replay months of sessions in one request or one chain; stored responses also expire after 30 days (11.11). Save each session's conclusions to your own store with a date, and give the agent a function tool, like `read_notes`, that returns only the entries that match the current question. How you index them (keyword or vector search) is out of scope here.

**Resume or start fresh?** If tool results are stale (files changed, an order was refunded), start a new session seeded with a **structured summary**: the scratchpad, the case facts and "what changed since". If you resume, tell the agent what changed.

### 11.10 Delegating to sub-agents to protect context

Exploration is verbose. Give it to a sub-agent with its own context and keep **one structured line** in the coordinator.

| Mechanism | Context behavior |
|---|---|
| **Agent-as-tool** (`agent.as_tool(...)`) | Only the tool result returns; `custom_output_extractor` controls it. For bounded questions |
| **Handoff** | The specialist takes over **with the history**; filter it with `input_filter` (for example `remove_all_tools`) |
| **Responses Multi-agent** (beta) | Each subagent gets a bounded task and its own context; compaction runs per agent; for parallel work on `gpt-6.1-sol` or GPT-5.6 |

```python
explorer = Agent(
    name="Dependency explorer",
    instructions="Map what the given module imports. "
                 "Return only the structured report.",
    tools=[read_file, grep],          # minimal toolset
    output_type=DependencyReport,     # module, depends_on, evidence, gaps
)

async def compact_report(result) -> str:
    r = result.final_output           # keep file:line evidence
    return json.dumps({"module": r.module, "depends_on": r.depends_on,
                       "evidence": r.evidence[:10], "gaps": r.gaps})

coordinator = Agent(
    name="Coordinator",
    instructions="Plan the change. Delegate exploration; "
                 "never read more than 3 files yourself.",
    tools=[explorer.as_tool(
        tool_name="explore_dependencies",
        tool_description="Investigate a module's dependencies "
                         "and return a short report.",
        custom_output_extractor=compact_report)],
)
```

Send the sub-agent minimal context, require structured results with sources and gaps, and limit its tools. Delegation adds total tokens; it saves the **coordinator's** context. Prefer one agent when each step depends on the previous one. **Ownership at a handoff is a context decision.** With agent-as-tool, the coordinator keeps the case. With a handoff, the specialist owns the next turns, so give it the current case facts plus a filtered history, not the raw exploration. Start the next turn with `result.last_agent`, and record each phase's owner in your manifest (11.11).

### 11.11 Structured state persistence and crash recovery

Server-side IDs are not a recovery plan (stored responses expire after 30 days). Persist **your** state in `checkpoints/`: a `manifest.json` (phase statuses, phase owners, `last_response_id`, `facts_version`, side effects with IDs), the versioned case facts, per-worker results, and a serialized `RunState` for paused runs. **Checkpoint after each completed step**, atomically (write a temp file, then rename). **Side effects need idempotency keys** (`refund-4711-1`); on restore, check the external system before repeating a `requested` action. **Restore = rebuild the request**: load the manifest, facts and session, skip completed phases, and tell the agent what changed.

```python
from pathlib import Path
from agents import RunState

STATE_FILE = Path("checkpoints/run-4711.state")   # write atomically in production
result = await Runner.run(agent, "Refund order A-17", session=session)
if result.interruptions:                       # waiting for a human
    STATE_FILE.write_text(result.to_state().to_string())

# ...later, in a different process...
saved = STATE_FILE.read_text()
state = await RunState.from_string(agent, saved)   # a coroutine: await it
for item in state.get_interruptions():
    state.approve(item)                        # or state.reject(item)
result = await Runner.run(agent, state, session=session)
```

### 11.12 Context management and prompt caching

Every context-management action edits the prompt, and caching rewards prompts that do not change ([chapter 07, 7.7](../07-batch-and-cost/README.md#77-prompt-caching) covers the mechanics). On GPT-5.6 and later, cache reuse needs the **entire rendered prefix** to match; changing `model`, `tools`, `reasoning.effort` or `context_management` can prevent it. So append history instead of rewriting it, keep tools stable (`tool_choice="none"` or `allowed_tools`, not removing definitions), and change effort with a `{"type": "configuration_update", "reasoning": {"effort": "high"}}` item, not the request field (with explicit compaction only, see 11.4). Writes cost 1.25x input, reads 0.1x (0.05x on `gpt-6.1-sol`); the minimum cacheable prefix is 1,024 tokens. Compaction resets part of the cache, but fewer input tokens can still save money. Compare total cost:

```python
def input_cost(uncached, cached, writes, rate_per_m):
    """GPT-5.6+: reads 0.1x, writes 1.25x (0.05x reads on gpt-6.1-sol)."""
    return (uncached + 0.1 * cached + 1.25 * writes) * rate_per_m / 1e6

# gpt-6-astra, $10 per M input, 3K new tokens per turn. Before: 180K input
before = input_cost(0, cached=177_000, writes=3_000, rate_per_m=10.0)
# After compaction: 30K window; the first turn rewrites the cache
after_first = input_cost(0, cached=0, writes=30_000, rate_per_m=10.0)
after_next = input_cost(0, cached=27_000, writes=3_000, rate_per_m=10.0)
# prints: 0.214 vs 0.375 then 0.065 per turn
print(f"{before:.3f} vs {after_first:.3f} then {after_next:.3f} per turn")
```

The turn after compaction costs more; every later turn costs much less. Add the billed compaction pass itself before you claim a payback. Measure `usage.input_tokens_details.cached_tokens` and `.cache_write_tokens`, and compute the hit rate as cached ÷ input tokens per conversation. A timestamp or the case facts at the **top** of `instructions` makes every request a cache miss.

## Lesson code

Code from the video lesson: [../../presentations/11-context-management/code/](../../presentations/11-context-management/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run 11.1–11.12 mostly offline, then build a long-running support conversation manager: case facts, trimming, budget, compaction, checkpoint and crash restore |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 offline exercises with auto-checks, an architecture scenario and a scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>
## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Long chat, ZDR required | Stateless `store=False` + compaction + case facts in your store | `previous_response_id` or Conversations | Conversations are not ZDR-eligible; stateless gives you full control |
| You must remove content from history | Stateless or Agents SDK session (or Conversations `items.delete`) | A `previous_response_id` chain | Chains are immutable |
| Context approaching the budget | Compact at a soft limit, or delegate | `truncation="auto"` | Auto truncation drops the earliest (often most important) items silently |
| Amounts, IDs, dates must survive | Case-facts block re-rendered every request, updated from tools | Trusting summaries or compaction | Compaction is opaque; summaries blur numbers |
| Facts change often, history is long | Ephemeral facts message at the end of input | Facts in `instructions` | Changing the prefix kills caching for the whole history |
| A tool returns 35 fields, 5 needed | Return the 5 fields from the tool | Letting the model "ignore" the rest | Unused fields cost tokens every later turn and distract |
| Old tool outputs pile up across turns of an agent chat | `ToolOutputTrimmer` as `call_model_input_filter`, wrapped so error outputs stay intact | Deleting the items | Item pairs must stay valid; previews keep the trail |
| Verbose exploration inside a coordinator | Agent-as-tool with a structured, compact result | Reading everything in the main agent | Protects the coordinator's context |
| Run paused for approval overnight | `result.to_state().to_string()` + manifest + idempotency keys | Keeping the process alive or re-running from scratch | Survives restarts without repeating side effects |
| Cache hit rate dropped after adding context management | Stable prefix, append-only history, batch compaction and trimming, `configuration_update` for effort (only with explicit `compaction_trigger` compaction) | Turning compaction off | Measure total cost; smaller context can still be cheaper |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **"We have 1M tokens, so we don't manage context."** Quality, cost and the 272K pricing threshold all say otherwise.
- **Turning on `truncation="auto"`** in a transactional system and losing the customer's account number from turn 1.
- **Pruning the wrong things:** manually pruning a `previous_response_id` chain, pruning the output of `/responses/compact`, or dropping reasoning items and `function_call` / `function_call_output` pairs.
- **Relying on the compaction item for facts you must audit.** It is encrypted and opaque.
- **Putting dynamic data (facts, timestamps, user names) at the top of `instructions`**, then wondering why `cached_tokens` is zero.
- **Restarting a crashed workflow from scratch**, repeating refunds or emails because side effects had no idempotency keys.

## Self-check

**1.** A support bot uses `previous_response_id` chaining with `truncation="auto"`. After about 150 turns, it asks customers again for the order number they gave in turn 1. What is the best fix?

- A) Switch to `gpt-6-astra`, which has better long-context recall
- B) Keep `truncation` at its default `"disabled"`, maintain a case-facts block (order number, amounts, status) that is re-sent every request, and compact at a soft token limit
- C) Ask the model to repeat the order number at the end of every answer so it stays in context
- D) Raise `max_output_tokens` so the model has room to remember

<details><summary>Answer</summary>

**B.** `truncation="auto"` drops items from the beginning of the conversation, which is where the order number was. A curated facts block plus deliberate compaction fixes the root cause. A does not stop truncation. C stores facts inside the history that gets truncated and compacted. D controls output length, not what survives in the input.
</details>

**2.** A healthcare client requires Zero Data Retention. Their triage assistant holds conversations of 300+ turns. Which design fits?

- A) Conversations API, deleting the conversation when the case closes
- B) `previous_response_id` chaining with `store=True`
- C) Stateless requests with `store=False`, replaying every output item, server-side compaction via `context_management`, and the case facts and checkpoints stored in the client's own database
- D) `truncation="auto"` with `store=False`, so no compaction is needed

<details><summary>Answer</summary>

**C.** ZDR itself is an organization- or project-level control that OpenAI approves (`store=False` alone still leaves abuse-monitoring logs); under ZDR `store` is always treated as false and the Conversations API is not ZDR-eligible. Server-side compaction is ZDR-friendly with `store=False`. A and B depend on OpenAI-side storage. D silently drops early turns, which is unacceptable for clinical facts.
</details>

**3.** An auditor asks the team to show exactly which refund amounts and promises the agent "remembered" after compaction on a disputed case. What should the architect have designed?

- A) Decrypt the compaction item with the organization's API key
- B) A versioned, application-owned case-facts record (updated from tool results, logged on every change) and per-turn checkpoints, because the compaction item is opaque
- C) A prompt asking the model to list everything in its compacted memory
- D) Turn off compaction so the full transcript is always in context

<details><summary>Answer</summary>

**B.** OpenAI's compaction item is encrypted and not intended to be human-interpretable, so auditability has to come from your own state. A is not possible. C produces a model-generated claim, not evidence. D trades auditability for cost and quality problems, and the transcript still is not a structured record of commitments.
</details>

**4.** A refund workflow pauses for manager approval. The worker process is redeployed overnight. Next morning the run must continue without issuing the refund twice. Which design works?

- A) Keep the process alive with a long timeout
- B) Store `result.to_state().to_string()`, a manifest with phase statuses, and an idempotency key for the refund; on restart load them with `await RunState.from_string(agent, saved)`, verify the refund's status in the payment system, approve, and run from that state
- C) Re-run the workflow from the first user message; the model will notice the refund was already requested
- D) Rely on `previous_response_id` alone; OpenAI keeps the paused run

<details><summary>Answer</summary>

**B.** Paused runs resume from serialized state, and side effects need idempotency checks. A fails on any deploy. C repeats side effects and relies on the model to prevent duplicates. D: a response ID only points to stored conversation output; the pending approval lives in the SDK's `RunState`, which you must save yourself. It also does nothing to prevent a second refund.
</details>

## Official documentation

- [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state): manual history, Conversations API, `previous_response_id`, data retention, managing the context window
- [Compaction](https://developers.openai.com/api/docs/guides/compaction): server-side `context_management`, standalone `/responses/compact`, pruning rules
- [Counting tokens](https://developers.openai.com/api/docs/guides/token-counting): `responses.input_tokens.count`, output token counts
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching): prefix rules, compaction and caching, tools, effort updates
- [Agents SDK (Python) sessions](https://openai.github.io/openai-agents-python/sessions/): backends, `SessionSettings`, `session_input_callback`, `OpenAIResponsesCompactionSession`
- [Agents SDK: Results and state](https://developers.openai.com/api/docs/guides/agents/results)

[← Chapter 10 — Multi-agent Error Handling](../10-multi-agent-error-handling/README.md) | [↑ OpenAI path](../README.md) | Chapter 12 — Provenance: citations and annotations (coming soon, see the [planned chapter folders](../README.md#planned-chapter-folders)) →

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
