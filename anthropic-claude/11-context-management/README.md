# Chapter 11 — Context Management in Production Systems

> **Exam domain(s):** Domain 5 — Context Management & Reliability (**15%**) [tasks 5.1, 5.4] · Domain 1 — Agentic Architecture & Orchestration (**27%**) [task 1.7 session state, resumption and forking] · also Domain 3 — Claude Code Configuration & Workflows (**20%**) [3.4, Explore subagent] · **Est. time:** 7–9 hours (reading + 2 notebooks) · **Status:** [ ] not started

Context management is deciding **what the model sees on every call**: which facts are durable, which tool output is noise, where the important parts sit, and what moves to a file or a subagent. Long systems fail quietly here: they forget the refund amount or ignore a finding in the middle, and answer with confidence. A 1M-token window does not remove this work, and the exam checks that you pick the structural fix over "use a bigger window".

## What you'll learn

- Keep exact values in a **case-facts block** outside the summarized history
- **Trim tool results** at ingest and order long input against **lost in the middle**
- Use **scratchpad files**, **subagents** and **state files with a manifest** for long and crash-prone work
- Choose between **resume, fork and fresh start**, and keep sessions clean
- Use the platform features: token counting, **compaction**, **context editing**, the **memory tool** and **prompt caching**

## Prerequisites

[Chapter 1](../01-claude-api-fundamentals/README.md) (statelessness, `count_tokens`), [Chapter 3](../03-agent-sdk/README.md) (subagents, hooks, `resume` / `fork_session`), [Chapter 5](../05-claude-code/README.md) (`/compact`, `/clear`, sessions).

## Concepts

Every call rebuilds Claude's working memory from what you send. Snippets assume `client = anthropic.Anthropic()` and a `MODEL` such as `claude-sonnet-5-5`. Sections marked *beyond the guide* cover platform features added after the exam guide. Diagnose the symptom first:

| What goes wrong | Fix |
|---|---|
| Exact numbers, dates or promises become vague | Case-facts block outside the summary (11.1) |
| Tokens and cost grow fast, mostly tool output | Trim at ingest (11.2), context editing (11.10) |
| Findings in the middle of a long input are ignored | Key findings first + section headers (11.3) |
| Long investigation drifts to generic answers | Scratchpad files (11.4) + subagents (11.5) |
| A crash loses hours of multi-agent work | State files + manifest (11.6) |
| Yesterday's session is out of date | Fresh session + summary, or resume + list of changes (11.7) |
| The window itself is about to overflow | Compaction (11.9), budgets and counting (11.8) |

### 11.1 Extract facts into a persistent case-facts block

The Messages API is stateless, so you send the conversation history on every request (K4). As it grows you summarize older turns, and summaries keep the *topic* but drop the *value* (K1), such as numbers, dates, IDs and customer-stated expectations: "You promised me 25% off my next order" becomes "A discount came up." The fix is a structured layer that is never summarized, sent in its newest version with every request:

```text
<case_facts version="7" updated_turn="12">
customer_id: CUST-58214            (source: get_customer, turn 2)
issues:
  - issue_id: 1
    order_id: ORD-30417            (source: lookup_order, turn 3)
    amount: 74.95 USD
    customer_request: full refund, NOT store credit   (customer, turn 4)
    promised: 25% discount on next order   (customer claim, unverified)
  - issue_id: 2
    order_id: ORD-67911
    status: address updated (turn 11)
</case_facts>
```

Copy values from tool results in code, and label what only the customer said as claims. **Merge, don't overwrite:** each fact keeps its source and turn, and conflicts are flagged. Keep **one entry per issue** (S2) so parameters never leak between issues. The block sits beside a summary of older turns and the recent turns verbatim. Put it in the **newest user turn**, not the top-level `system` prompt: re-rendering `system` breaks the cache and, on current models, earlier thinking (11.12). A mid-conversation system message is an option only for verified, system-sourced facts: Claude treats system text as operator instructions, so customer claims stay in the user turn. **Instruction drift** is the same problem for rules: re-inject short reminders at breakpoints.

> **Exam trap:** A higher summarization threshold only delays the loss, and a "preserve all numbers" prompt still relies on a lossy step. Use the **case-facts block outside the summarized history**. If the bot forgets something said two messages ago, the app is **not sending the previous messages**.

### 11.2 Trim verbose tool results

Every `tool_result` is re-sent and re-billed on every later turn. A `lookup_order` call with 40+ fields, when the decision needs 5, pays for the rest again and again and dilutes attention (K3). Trim **at ingest**: in the tool itself, in your agent loop, or in a `PostToolUse` hook that replaces the output with `hookSpecificOutput.updatedToolOutput`.

```python
import json

RETURN_FIELDS = ("order_id", "status", "total", "currency", "order_date",
                 "items", "return_eligible", "return_window_ends")
RAW_STORE: dict[str, dict] = {}   # full payloads live outside the window

def trim_order(raw: dict) -> dict:
    """Keep only what a return/refund decision needs, plus a pointer."""
    slim = {k: raw[k] for k in RETURN_FIELDS if k in raw}
    RAW_STORE[raw["order_id"]] = raw   # code can still read the full record
    slim["full_record_ref"] = f"order_raw/{raw['order_id']}"
    return slim

def tool_result_block(tool_use_id: str, raw: dict) -> dict:
    return {"type": "tool_result", "tool_use_id": tool_use_id,
            "content": json.dumps(trim_order(raw))}
```

**Trim once, never later on the client.** On Fable 5.1, Opus 5.5 and Sonnet 5.5, earlier thinking blocks are tied to the exact prefix, so editing an old `tool_result` invalidates every later thinking block. Clear old results server-side (11.10). **At agent boundaries (S6)**, change the upstream agents' output contract: key facts, short quotes, source metadata and relevance scores, not raw content.

> **Exam trap:** When an agent's input is bloated, fix it where it is produced. Cleaning it up downstream costs another model call, loses detail and leaves the cause in place. Fix the upstream output format.

### 11.3 Position-aware input: lost in the middle

Models use the **beginning and end** of a long input reliably and miss more in the **middle** (K2). Lay it out (S4) with a **key-findings summary first**, **explicit section headers** (XML tags) for the details, and **the question last**. In Anthropic's tests, query-last improved response quality by up to 30%. Make `source`, `date` and `method` required fields in subagent output (S5), so synthesis can date and attribute each finding.

```python
def build_synthesis_input(findings: list[dict], question: str) -> str:
    """findings: [{"source", "date", "method", "key_points", "detail"}]."""
    summary = "\n".join(
        f"- [{i}] {pt} ({f['source']}, {f['date']})"
        for i, f in enumerate(findings, 1) for pt in f["key_points"]
    )
    sections = "\n".join(
        f'<document index="{i}">\n<source>{f["source"]}</source>\n'
        f'<date>{f["date"]}</date>\n<method>{f["method"]}</method>\n'
        f'<document_content>\n{f["detail"]}\n</document_content>\n'
        "</document>"
        for i, f in enumerate(findings, 1)
    )
    return (
        f"<key_findings>\n{summary}\n</key_findings>\n\n"           # top
        f"<detailed_results>\n{sections}\n</detailed_results>\n\n"  # middle
        f"<task>\n{question}\nCite findings by [index]. "
        "Cover every key finding listed above.\n</task>"            # end
    )
```

> **Exam trap:** This is a layout problem, not a size problem: answers that only cut tokens or buy a bigger window leave the middle where it is. Use a **key-findings summary at the start plus explicit section headers**, with the question last.

### 11.4 Scratchpad files

The first sign of a degrading context is **vagueness**: "typical patterns" instead of the classes found earlier (K1). A **scratchpad file** moves findings onto disk, where they survive compaction, `/clear` and new sessions (K2, S2):

```markdown
# investigation-scratchpad.md   (agent-maintained; read before answering)
## Confirmed findings (each with evidence)
- RefundService.issue() (src/billing/refunds.ts:41) needs manager approval over $50
- issue() is called from SupportController (src/api/support.ts:57) and RefundRetryJob (src/jobs/retry.ts:22)
## Open questions
- Does RefundRetryJob back off on gateway 429s? (not yet read)
```

Every finding needs a file and line. The agent reads the file before answering and appends after confirming. Unlike CLAUDE.md, it holds one investigation's findings. It also makes compaction safe: write the facts down first, then `/compact` (S5). The memory tool (11.11) is the API version.

### 11.5 Delegate exploration to subagents to protect the coordinator's context

Reading 20 files can cost 60K tokens when the answer is one line. A **subagent** reads in its own fresh window and returns only its final message (K3, S1):

```text
Coordinator: "Trace the refund flow's dependencies. Return JSON:
  {dependencies: [{name, file, line, kind}], open_questions: []}"
  -> Explore subagent (read-only), in ITS own window: opens 20 files, ~60K tokens
  <- {"dependencies": [{"name": "AuthService",
      "file": "src/auth/service.ts", "line": 4, "kind": "import"}, ...]}
Coordinator: keeps ~300 tokens instead of 60K
```

Subagents **do not inherit** the coordinator's history, so put the question and the facts it needs in the prompt. Ask for structured results, and scope tools with `AgentDefinition(tools=["Read", "Grep", "Glob"])`. Between phases (S3), inject phase 1's short summary into the phase-2 subagents' prompts, not its transcript. The guide calls the spawning tool `Task`; current versions emit `Agent`. In Claude Code, use the read-only **Explore** subagent or a skill with `context: fork`; neither gets your history.

> **Exam trap:** Compacting after verbose exploration cleans up damage a subagent would have prevented. **Isolate discovery in an Explore subagent** (or a `context: fork` skill) that returns a summary.

### 11.6 Structured state persistence and crash recovery

If the coordinator dies mid-run, completed work must survive without a transcript (K4, S4). Each agent writes its state (status, key findings, coverage, gaps) to a known file on every status change, atomically (temp file, then `os.replace`). The coordinator keeps a **manifest** with each agent's status and state-file path. On resume it skips `completed` agents, re-runs the rest (so reruns must be idempotent), and injects completed findings into their prompts:

```python
import json
from pathlib import Path

def resume_plan(manifest: dict) -> tuple[list[str], str]:
    """Agents still to run, and the findings to inject into their prompts."""
    done, todo = [], []
    for name, entry in manifest["agents"].items():
        (done if entry["status"] == "completed" else todo).append(name)
    injected = []
    for name in done:
        path = Path(manifest["agents"][name]["state_file"])
        state = json.loads(path.read_text())
        injected.append(f"<prior_results agent='{name}'>\n"
                        f"{json.dumps(state['key_findings'])}\n"
                        f"coverage={state['coverage']} "
                        f"gaps={state['gaps']}\n</prior_results>")
    return todo, "\n".join(injected)
```

> **Exam trap:** "Re-run everything" wastes work, "replay the transcript" brings back stale output, and "ask the subagents" fails because they keep no memory. Use **per-agent state plus a manifest**.

### 11.7 Sessions: resume, fork, or start fresh (task 1.7)

What you resume is the *context*, including every old tool result. [Chapter 5](../05-claude-code/README.md#510-sessions-resume-name-fork) covers the commands.

| Mechanism | Claude Code / Agent SDK | Use when |
|---|---|---|
| Resume a named session | `claude -n auth-bug`, then `claude --resume auth-bug`; `resume=session_id` | Prior context is mostly valid (K1, S1) |
| Fork from a baseline | `claude --resume <id> --fork-session`; `fork_session=True` | Compare two approaches (K2, S2) |
| Fresh + structured summary | `/clear` or a new session whose first message is the summary | Prior tool results are stale (K4, S3) |

A resumed session cannot know its file reads are stale. If many or unknown files changed, start fresh with a summary. If a few known files changed, resume and name them (K3, S4):

```text
Since this session last ran, these files changed:
- src/payments/processor.ts (refund() now takes a reason argument)
- src/payments/gateway.ts (retry logic added)
Your earlier reads of these two files are outdated. Re-read them before
answering, then update the dependency map. Everything else is unchanged.
```

For Claude.ai users the same choice is **restart** (stale or wandering), **summarize** (right thread, too long), or **persist** (project knowledge, memory or a file).

#### Session hygiene

Keep each session about one task ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). Run `/clear` between unrelated tasks (it keeps CLAUDE.md), and after two failed corrections on the same issue, run `/clear` and restart with a better prompt. When the window fills on the same task, write findings to a scratchpad, then `/compact <focus>`. Use `/btw <question>` for side questions that should not enter history, and name sessions you may return to (`claude -n <name>` or `/rename`). In an API app: one conversation per case, and seed a reopened case from its case-facts block.

### 11.8 Context windows, token budgets and counting *(beyond the guide)*

Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5 have a **1M-token** window; legacy Haiku 4.5 has **200K**. Everything counts, including thinking and output. Recall degrades as context grows (*context rot*), so the window is a ceiling, not a target. Give each layer a token budget, count before sending, and measure after:

```python
count = client.messages.count_tokens(       # free; returns an estimate
    model=MODEL, system=SYSTEM, tools=TOOLS, messages=history)
if count.input_tokens > INPUT_BUDGET:
    ...                                     # compact first (11.9)

u = response.usage                          # all four fields count
window_used = (u.input_tokens + (u.cache_read_input_tokens or 0)
               + (u.cache_creation_input_tokens or 0) + u.output_tokens)
```

Count with the model you will call: Claude 4.7 and later produce roughly 30% more tokens for the same text. If the input alone exceeds the window, the API returns 400 "prompt is too long"; the fix is a smaller input. Tokenization specifics are out of scope for CCAR-F; the reasoning is not.

### 11.9 Server-side compaction *(beyond the guide)*

Compaction replaces older turns with a summary Claude writes **on the server**. It is in beta on Opus and Sonnet 4.6 and later, Haiku 5.5, and the Fable and Mythos models (not legacy Haiku 4.5). **On demand** (`compact-2026-09-04`): you send `compaction={"type": "summarize"}` and put the returned block first in place of what it summarized. **At a threshold** (`compact-2026-01-12`): a `compact_20260112` edit runs when input reaches `trigger` (default 150,000 input tokens).

```python
COMPACT_AT = 120_000          # your input budget, below the window

def maybe_compact(history: list, system: str, tools: list, last_usage) -> list:
    u = last_usage
    used = (u.input_tokens + (u.cache_read_input_tokens or 0)
            + (u.cache_creation_input_tokens or 0) + u.output_tokens)
    if used < COMPACT_AT:
        return history
    summary = client.beta.messages.create(
        model=MODEL, max_tokens=8192, system=system, tools=tools,
        betas=["compact-2026-09-04"], messages=history,   # same system + tools
        compaction={"type": "summarize", "instructions": (
            "Summarize this support conversation so it can continue. "
            "Preserve every order ID, amount, percentage, date and "
            "customer-stated expectation exactly as written. Do not call "
            "tools; respond with the summary only.")},
    )
    if summary.stop_reason != "compaction":   # keep history, retry later
        return history
    return [{"role": "assistant", "content": summary.content}]
```

It is still summarization, so the case-facts block stays outside. Send the block exactly as returned, signature included, and never combine `compaction` and `context_management` on one request. After the swap the layers sit in this order: the block first, then any recent turns you chose to keep word for word (compact only the older turns; see [Compaction that keeps recent turns](https://platform.claude.com/docs/en/build-with-claude/compaction-keep-recent-turns)), then the newest user turn with the current case-facts block. Prefer it to a client summarizer that rewrites old turns: those fail the prefix check (11.2). In Claude Code and the Agent SDK, compaction runs automatically near the limit; `/compact <focus>` steers it, and a `PreCompact` hook can flush facts to a file first.

### 11.10 Context editing: clearing tool results and thinking *(beyond the guide)*

Context editing clears content **by rule** on the server while your client keeps the full history (beta `context-management-2025-06-27`). `clear_tool_uses_20250919` clears the oldest tool results past a `trigger`; `clear_thinking_20251015` clears earlier thinking.

```python
response = client.beta.messages.create(
    model=MODEL, max_tokens=4096, betas=["context-management-2025-06-27"],
    tools=TOOLS, messages=history,
    context_management={"edits": [{
        "type": "clear_tool_uses_20250919",
        "trigger": {"type": "input_tokens", "value": 60_000},
        "keep": {"type": "tool_uses", "value": 4},
        "clear_at_least": {"type": "input_tokens", "value": 10_000},
        "exclude_tools": ["get_customer"],   # never clear identity checks
    }]},
)
```

Trimming (11.2) makes each result small once, in your code. Clearing removes whole old results later, on the server. Clearing **breaks the prompt cache** from that point, so `clear_at_least` makes each break worth it.

### 11.11 The memory tool *(beyond the guide)*

The memory tool, `{"type": "memory_20250818", "name": "memory"}`, is the API's built-in scratchpad (11.4). Claude reads and writes files in `/memories`, and **your application executes every operation** against storage you control. The SDK helper `BetaLocalFilesystemMemoryTool` runs it on local files. Treat memory as helpful but unverified, unlike case facts. **Security is your job:** keep paths inside `/memories` (reject `../`), cap file sizes, and scope memory per customer or tenant.

### 11.12 Prompt caching and context management *(beyond the guide)*

**Caching changes what you pay for tokens, not whether they count toward the window.** The cache key is the exact prefix, `tools` → `system` → `messages`; a change invalidates that level and everything after it. Writes cost 1.25× base input (5 minutes) or 2× (1 hour). Reads cost 0.1× on most models, 0.05× on Opus 5.5 and Sonnet 5.5, and 0.025× on Fable 5.1 and Mythos 5.1.

| Decision | Cache-friendly | Cache-breaking |
|---|---|---|
| Static instructions and policy | First, in `system`, with a `cache_control` breakpoint | Mixed with per-turn content |
| Changing state (case facts) | Newest turn (verified facts may use a mid-conversation system message) | Re-rendering `system` every turn |
| Old tool results | Trimmed at ingest; cleared server-side | Edited in place on the client |
| Tool set | Declared up front | Editing `tools` mid-session |

> **Exam trap (CCAR-P sample question):** The same 8,000-token system prompt goes with every short request. **Put the static content first and enable prompt caching.** Truncating the policy loses required context.

### 11.13 Putting it together: progressive discovery vs monolithic context

**Monolithic context** loads everything up front: simple and cacheable, but it brings context rot, lost in the middle and a high cost per call. **Progressive discovery** starts lean and pulls data on demand through tools, subagents, memory files and skills: focused and scalable, but with retrieval misses and more round trips. Most systems combine them: a **cached, monolithic stable prefix** (policy and tool definitions) plus **progressive discovery** for case-specific data.

**History far beyond the window.** An assistant used for months builds up far more history than any window holds, so do not stuff it all into each request. Store past exchanges (or their conclusions) outside the request, and retrieve only the ones the current question needs. Two ways: the memory tool (11.11), where Claude writes conclusions to `/memories` files and opens the relevant ones later, or a search tool you build over the stored sessions. Scope the store per customer or tenant, and treat what comes back as notes to check, not verified facts. How the search index works inside (embeddings, vector databases) is out of scope here.

## Lesson code

Video-lesson code: [../../presentations/11-context-management/code/](../../presentations/11-context-management/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Work through 11.1–11.13 (mostly offline), then build a long-running support conversation manager with facts, trimming, compaction and crash-safe checkpoints |
| [`02_homework.ipynb`](02_homework.ipynb) | 11-question quiz, 6 auto-checked coding exercises, an architecture scenario and a scorecard |

Run them from the repo root venv (see [../../00-prerequisites/README.md](../../00-prerequisites/README.md)).

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Exact values come back wrong after summarization | Case-facts block outside the summary | Higher threshold, "preserve numbers" prompt |
| Tool returns 40 fields, 5 matter | Trim at ingest (tool, loop or `PostToolUse` hook) | Bigger window, "ignore fields" instruction |
| Old tool results no longer needed | Server-side context editing | Deleting `tool_result` content on the client |
| Synthesis misses mid-input findings | Key findings first + headers, question last | Shorter input, bigger window |
| Upstream agents forward raw pages or reasoning | Structured output contract upstream | Cleaning it up downstream |
| Long investigation drifts to "typical patterns" | Scratchpad with evidence + subagents | Keep going and `/compact` |
| Multi-agent run must survive crashes | State files + manifest, atomic writes | Re-run everything, replay the transcript |
| Files changed since the last session | Fresh + summary, or resume + list of changes | Resume as-is |
| Conversation will outgrow the window | Server-side compaction (+ facts outside) | Hand-rolled summarizer keeping old thinking |
| Large static policy on every call | Static content first + prompt caching | Truncating the policy |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **"We have 1M tokens, so we don't need to manage context."** Cost grows with every re-sent turn and recall degrades.
- **Trusting a summary with numbers.** Keep exact values in a structured layer.
- **Re-rendering `system` with changing state, or editing old turns on the client.** Both break the cache and earlier thinking.
- **Saving state only at the end**, or writing it non-atomically.

## Self-check

**1. (Customer support agent)** A phone-plan support agent already keeps a case-facts block. To keep it current, the app asks the model each turn to "rewrite the facts block from the conversation so far" and replaces the old block with the result. At turn 30 the block says the customer's monthly price is $43, although the billing tool returned $34.00 at turn 6. What is the best fix?

- A) Ask the model to rewrite the block twice each turn and keep it only when both versions agree
- B) Copy values from tool results into the block in code, merge new facts into the existing entries instead of rewriting the block, and flag a conflict instead of overwriting a verified value
- C) Move the facts block into the history that gets summarized, so the summarizer can correct it
- D) Remove the facts block and raise the model's effort so it reads the full history more carefully

<details><summary>Answer</summary>

**B.** The block failed because a model rewrote it from scratch every turn, which is the same lossy step the block exists to avoid. Values from tools should be copied by code, and merging keeps each fact's source so a wrong value shows up as a conflict. A runs the lossy step twice, and two runs can agree on the same wrong number. C puts the facts back where they get blurred. D gives up the structure and hopes the model finds a value from 24 turns ago.
</details>

**2. (Multi-agent research system)** A research coordinator sends synthesis the question first, then a short key-findings list, then about 120K tokens of subagent output pasted as one plain-text block with no labels. Reports mention findings from the list but often credit them to the wrong subagent, and details from the middle of the pasted text are rarely used. What change helps most?

- A) Remove the key-findings list so the model has to read the full details
- B) Ask the subagents for longer key findings so the list carries more of the detail
- C) Move the question to the end and leave the details as one block
- D) Put each subagent's output in its own section with headers for source, date and method, number the key findings to match those sections, and put the question last

<details><summary>Answer</summary>

**D.** The summary is already in the right place. What is missing is structure in the middle: headers let the model find each section and tie every finding to its source, and a question at the end is used more reliably. A removes the part the model reads best. B makes the list longer but still gives no way to trace a finding. C helps a little, but the details are still one wall of text with nothing to cite.
</details>

**3. (Developer productivity)** After two hours of exploring a legacy codebase in one Claude Code session, answers become inconsistent and refer to "typical service-layer patterns" instead of the specific classes found earlier. The investigation has several more days to go. What is the best approach?

- A) Switch to a model with a larger context window and continue in the same session
- B) Run `/compact` every 30 minutes and continue
- C) Have the agent record confirmed findings (with file and line) in a scratchpad file it reads before answering, and delegate new exploration questions to subagents that return structured summaries
- D) Start a new session each morning with no notes so stale context never accumulates

<details><summary>Answer</summary>

**C.** The symptom is context degradation. Persisting specifics outside the window and isolating verbose exploration in subagents addresses both causes. A keeps the noise. B summarizes the specifics away unless they were written down first. D throws away the findings along with the noise.
</details>

**4. (Code generation with Claude Code)** Yesterday you mapped a billing module in a named session, `billing-map`. Overnight, a teammate changed two files, `invoice.ts` and `tax.ts`; nothing else changed. What is the most efficient reliable way to continue?

- A) `claude --resume billing-map` and continue as if nothing changed
- B) `claude --resume billing-map`, then tell it that `invoice.ts` and `tax.ts` changed, that its earlier reads of them are outdated, and ask it to re-read those two files and update its map
- C) Start a fresh session with no context and redo the whole mapping
- D) Resume and say "some files may have changed, please re-check everything"

<details><summary>Answer</summary>

**B.** Most of the prior context is still valid, so resuming is efficient, and naming the changed files gives targeted re-analysis. A reasons on stale results. C discards valid work (a fresh session *with a structured summary* would be the better choice if many or unknown files had changed). D forces a full re-exploration.
</details>

## Official documentation

- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Compaction overview](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Syllabus source: community study guide by paullarionov, [Chapter 11 and Domain 5](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-11-context-management-in-production-systems), restructured and expanded here in my own words.

---

[← Chapter 10 — Error Handling in Multi-agent Systems](../10-multi-agent-error-handling/README.md) | [↑ Claude path overview](../README.md) | [Chapter 12 — Preserving Provenance →](../12-provenance/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
