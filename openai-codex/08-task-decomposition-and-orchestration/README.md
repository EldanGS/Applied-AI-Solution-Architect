# Chapter 8 — Task Decomposition and Orchestration

> **Claude counterpart:** [Chapter 8 — Task Decomposition Strategies](../../anthropic-claude/08-task-decomposition/README.md) · **Academy course(s):** Design and Build Agentic Systems (API pathway, 110 min); Scale Codex Across Governed Teams and Systems (Codex pathway) for 8.9–8.10 · developer track: Building agents · **Est. time:** 8–10 hours (reading + 2 notebooks) · **Status:** [ ] not started

Most "the agent is unreliable" escalations are really decomposition problems: one prompt does six jobs, a planner splits a topic too narrowly, or the session that wrote the code also reviews it. On OpenAI you can orchestrate in code, let the model orchestrate inside the Agents SDK, or let OpenAI's servers (and Codex) run subagents. The architect picks the cheapest shape that meets the outcome and safety requirements, then proves it with tests and traces.

## What you'll learn

- How to choose a shape: single call, fixed pipeline, routing, parallel fan-out, orchestrator-workers, or an evaluator-optimizer loop
- Pipelines and routing where code owns the flow and `output_type` acts as the gate between steps
- Bounded fan-out with `asyncio.gather`, partial-failure handling, and a coverage check on a structured `Plan`
- Agents-as-tools vs handoffs (only one handoff is honored per turn), and what hosted subagents can and cannot do
- Multi-pass code review with an independent reviewer, mapped to Codex `/review`, `codex review` and `@codex review`
- Verification contracts per workstream, offline tests with `ScriptedModel`, and one trace per orchestration

## Prerequisites

[00 — Prerequisites](../../00-prerequisites/README.md), [Chapter 03 — Agents SDK and the Agents API](../03-agents-sdk-and-agents-api/README.md) (`Agent`, `Runner`, `output_type`, handoffs vs agents-as-tools, tracing), [Chapter 05 — Codex](../05-codex/README.md), [Chapter 06 — Prompt engineering and evals](../06-prompt-engineering-and-evals/README.md) ([6.5](../06-prompt-engineering-and-evals/README.md#65-prompt-chaining) chaining, [6.7](../06-prompt-engineering-and-evals/README.md#67-self-correction) self-correction, [6.9](../06-prompt-engineering-and-evals/README.md#69-building-your-own-eval-harness) eval harness) and [Chapter 07 — Batch and cost](../07-batch-and-cost/README.md). Optional: the Claude counterpart above. Snippets assume `import asyncio`, `from typing import Literal`, `from pydantic import BaseModel, Field`, `from agents import Agent, Runner, trace` and `MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")`. `gpt-6-luna` ($0.10 / $0.50 per million input / output tokens) runs workers, routers and drafts; `gpt-6.1-sol` ($2 / $10) runs planning, integration reviews and judging. In Jupyter, use top-level `await`.

## Concepts

### 8.1 Workflows vs agents: choosing a decomposition shape

In a **workflow**, your code fixes the steps and the model fills them in. In an **agent**, the model decides the next step at run time. OpenAI's Responses Multi-agent guide says to prefer one agent when "each step depends directly on the previous step" or when "you require a fixed, deterministic execution graph".

| Shape | Who decides the next step | Use when | OpenAI building block |
|---|---|---|---|
| **Single call** | Nobody (one step) | The task fits one focused request | `responses.create` / one `Runner.run` |
| **Fixed pipeline** | Your code | Steps are known up front and the same every time | Sequential `Runner.run` calls, `output_type` gates (8.2) |
| **Routing** | A classifier, then code (or a handoff) | Inputs fall into distinct categories | Classifier agent + dict, or `handoffs=[...]` (8.3) |
| **Parallelization** | Your code | Independent parts, or several attempts at one thing | `asyncio.gather` over `Runner.run` (8.4) |
| **Orchestrator-workers** | A planner model | Subtasks are unknown until you see the input | `output_type=Plan` + fan-out, or `Agent.as_tool()` workers (8.5) |
| **Evaluator-optimizer** | An evaluator, in a loop code caps | Clear quality criteria, and feedback helps | Generator + evaluator with a structured verdict (8.6) |
| **Hosted multi-agent** | OpenAI's servers or Codex | Broad, parallel, exploratory work | Responses Multi-agent, Agents API, Codex subagents (8.8) |

**Start with one agent.** OpenAI's orchestration guide adds specialists only when they "materially improve capability isolation, policy isolation, prompt clarity, or trace legibility". The Building agents track says several agents pay off for separate tasks that **do not overlap**, when one of them has very complex instructions or many (or similar, confusable) tools. The gains are **separation of concerns**, **parallelism** and **focused evals** per agent. OpenAI's eval guide adds that going multi-agent "should be driven by your evals".

### 8.2 Fixed pipelines (prompt chaining) with the Agents SDK

Each step is an `Agent` with one job. Code passes one step's output to the next, and a **gate** decides whether to continue. The SDK's `deterministic.py` example has this shape.

```python
class OutlineCheck(BaseModel):
    covers_all_sections: bool
    missing: list[str]

outliner = Agent(name="Outliner", model=MODEL,
    instructions="Outline a migration runbook for the system described.")
checker = Agent(name="Outline checker", model=MODEL, output_type=OutlineCheck,
    instructions="Check the outline has: rollback, data backfill, "
                 "cutover, customer comms.")
writer = Agent(name="Runbook writer", model=MODEL,
    instructions="Write the runbook from the approved outline.")

async def runbook_pipeline(system: str) -> str:
    with trace("Runbook pipeline"):             # all steps in ONE trace
        outline = await Runner.run(outliner, system)
        check = await Runner.run(checker, outline.final_output)
        verdict = check.final_output_as(OutlineCheck)
        if not verdict.covers_all_sections:     # gate: code decides
            raise ValueError(f"outline rejected, missing: {verdict.missing}")
        draft = await Runner.run(writer, outline.final_output)
        return draft.final_output
```

Each step is testable on its own, the `if` runs every time (an instruction holds only most of the time), and each step can use its own model. **Structured outputs are the contract between steps**: the Building agents track recommends them for any agent output your application consumes. Each `Runner.run` sees only the input you pass: if step 3 needs the original request *and* step 1's result, pass both explicitly.

### 8.3 Routing: by code, by handoff, and by model tier

There are three ways to route, from most to least deterministic.

1. **Classifier plus code.** A small agent with a structured `output_type` classifies the input, and a dictionary keyed by both `Route` fields picks the next agent (code below). The SDK docs call this orchestrating via code.
2. **Handoffs.** The triage model calls `transfer_to_<agent_name>`, and that specialist owns the rest of the turn ([3.4](../03-agents-sdk-and-agents-api/README.md#34-handoffs-vs-agents-as-tools)). Use it when the specialist should talk to the user directly. The routing signal is each `handoff_description`, so keep them short and non-overlapping.
3. **Model tiering (cascading).** Route by difficulty: routine inputs go to `gpt-6-luna`, hard ones to `gpt-6.1-sol` or `gpt-6-astra`. You can also escalate after a failed check: retry once on the stronger model.

```python
class Route(BaseModel):
    category: Literal["billing", "technical", "account", "other"]
    complexity: Literal["simple", "complex"]

router = Agent(name="Router", model="gpt-6-luna", output_type=Route,
    instructions="Classify the support ticket.")
# SPECIALISTS: {("technical", "complex"): Agent(...), ...}; FALLBACK: Agent

async def handle(ticket: str) -> str:
    route = (await Runner.run(router, ticket)).final_output_as(Route)
    # unknown combos never crash: they fall back to a generalist agent
    agent = SPECIALISTS.get((route.category, route.complexity), FALLBACK)
    return (await Runner.run(agent, ticket)).final_output
```

The Building agents track frames model choice the same way: start with the flagship (`gpt-6-astra`), then use smaller models where latency or cost matter. For a conversational interface its example is `gpt-5.6-terra` for the back-and-forth, delegating demanding tasks to `gpt-6-astra`. Move each step down a tier only while its eval still passes.

### 8.4 Parallelization: fan-out, voting, and parallel tool calls

**Sectioning (fan-out)** runs one worker per independent part, so wall-clock time is the slowest worker. **Voting (best-of-n)** runs the same task several times and picks the best. Production fan-out needs a **concurrency bound** and **partial-failure handling**. A semaphore limits requests *in flight*, not requests or tokens per minute, so also retry 429s (honor `Retry-After`, else exponential backoff with jitter).

```python
async def fan_out(agent: Agent, inputs: list[str],
                  limit: int = 4) -> list[str | Exception]:
    gate = asyncio.Semaphore(limit)    # bounds bursts, not RPM / TPM

    async def one(text: str) -> str:
        async with gate:
            result = await Runner.run(agent, text, max_turns=4)
            return result.final_output

    # a failed worker becomes an Exception in its slot; others survive
    return await asyncio.gather(*(one(t) for t in inputs),
                                return_exceptions=True)
```

Then decide **per slot** what a failure means. A missing facet in a research brief can be reported as a gap. A missing file in a security review should block the verdict. A manager agent can also fan out by itself, with several tool calls in one turn ([2.4](../02-function-calling-and-structured-outputs/README.md#24-tool_choice-and-parallel_tool_calls)). `ModelSettings(parallel_tool_calls=...)` controls whether the **model** may emit several calls. `RunConfig(tool_execution=ToolExecutionConfig(max_function_tool_concurrency=N))` controls how many the **SDK** runs at once; the default `None` starts all of them, so three `as_tool()` workers run concurrently.

> **Gotcha:** Parallel is safe only for **independent** work. Two workers that write the same file or row need a lock, a merge step, or sequential runs. Fan-out also multiplies input tokens: put the shared prefix first for prompt caching, or use the Batch API when results are not interactive.

### 8.5 Dynamic decomposition: orchestrator-workers

When subtasks depend on the input ("assess this vendor", "review this PR"), a planner decides them. You can build it two ways.

**A. Plan in a structured output, fan out in code.** The planner (`output_type=Plan`, on `gpt-6.1-sol`) returns the subtasks. Code checks coverage, runs workers in parallel (8.4), and a synthesizer merges findings by facet, marking failed slots. The model decides *what*; code decides *how*.

```python
class Subtask(BaseModel):
    id: str
    facet: str = Field(
        description="Which required facet this subtask covers")
    question: str
    context: str = Field(
        description="Every fact the worker needs. Workers see nothing else.")

class Plan(BaseModel):
    subtasks: list[Subtask] = Field(max_length=6)  # maxItems in schema

REQUIRED_FACETS = {"security", "data", "cost", "operations"}

planner = Agent(name="Planner", output_type=Plan, model="gpt-6.1-sol",
    instructions="Split the request into independent subtasks, at least "
                 "one per facet: security, data, cost, operations. Put "
                 "every fact a worker needs into its context.")
worker = Agent(name="Worker", model=MODEL,
    instructions="Answer ONE subtask using only its context.")

async def orchestrate(request: str, planner: Agent = planner,
                      worker: Agent = worker) -> list[str | Exception]:
    plan = (await Runner.run(planner, request)).final_output_as(Plan)
    missing = REQUIRED_FACETS - {s.facet for s in plan.subtasks}
    if missing:                      # catches over-narrow decomposition
        raise ValueError(f"plan too narrow, missing facets: {sorted(missing)}")
    prompts = [f"<subtask id='{s.id}'>\n{s.question}\n"
               f"<context>{s.context}</context>\n</subtask>"
               for s in plan.subtasks]
    return await fan_out(worker, prompts)   # then the synthesizer merges
```

**B. A manager agent with workers as tools.** The manager plans *and* dispatches by calling `Agent.as_tool()` workers, for example `file_reviewer.as_tool(tool_name="review_file", tool_description=..., parameters=ReviewTask)`, where `parameters=` gives the worker structured input. This is orchestration via LLM: more adaptive, less predictable.

**Context passing is explicit.** An `as_tool()` worker sees **only the tool input**, not the manager's conversation. In option A it sees only the prompt your code builds. Put facts, constraints and the output format into structured fields. **Shared memory, when agents continue one conversation.** The Building agents track says to share memory **keyed by `conversation_id`** instead of copying transcripts. In the SDK that is a `Session` (for example `SQLiteSession(conversation_id)`) passed to each `Runner.run(..., session=...)`. Never pass it to parallel workers or an independent reviewer (8.9).

> **Exam trap: over-narrow decomposition.** A planner splits "AI's impact on creative industries" into digital art, graphic design and photography. Every worker succeeds and the report is still wrong. Fix the plan: a code-side **coverage check**, a planner prompt framed as coverage goals, or an evaluator on the plan. Stronger workers do not fix a bad plan.

**Adaptive re-planning.** In option A, loop: plan → run → let the planner see results and emit the next plan, with a round cap. In option B the manager re-plans across turns, bounded by `max_turns`. Cap everything the model controls: subtasks, rounds and turns.

### 8.6 Evaluator-optimizer loops

A generator drafts, an evaluator grades against explicit criteria, and the generator revises until the draft passes or a cap is hit. The SDK example is `llm_as_a_judge.py`, which notes you can use a small model to generate and a larger one to judge. Here `drafter` is a plain `Agent` on `MODEL`. `evaluator` runs on `gpt-6.1-sol` with `output_type=Review` and a four-point rubric (outage window in UTC, affected regions, no blame on third parties, under 120 words); it returns "pass" only if all four hold.

```python
class Review(BaseModel):
    rationale: str            # generated first: reason before the verdict
    verdict: Literal["pass", "revise"]
    feedback: list[str]       # specific, actionable items

async def draft_with_review(brief: str, max_rounds: int = 3):
    prompt = brief
    for round_no in range(1, max_rounds + 1):   # the cap is part of the design
        draft = (await Runner.run(drafter, prompt)).final_output
        review = (await Runner.run(evaluator,
            f"<brief>{brief}</brief>\n<draft>{draft}</draft>")
        ).final_output_as(Review)
        if review.verdict == "pass":
            return draft, review, round_no
        prompt = (f"<brief>{brief}</brief>\n"
                  f"<previous_draft>{draft}</previous_draft>\n<feedback>\n"
                  + "\n".join(f"- {item}" for item in review.feedback)
                  + "\n</feedback>")
    return draft, review, max_rounds   # still failing: route to a human
```

Design rules: write the rubric first, with pass/fail verdicts ([6.4](../06-prompt-engineering-and-evals/README.md#64-explicit-criteria-and-rubrics)). Give the evaluator a **fresh context** (brief and draft only). Make feedback specific. **Always cap the rounds** and decide what happens at the cap. Measure whether the loop changes outcomes; if not, it is cost without benefit.

### 8.7 Orchestrating via LLM vs via code

**Via LLM**, the model decides the flow with tools, agents-as-tools and handoffs. It adapts to open-ended tasks but is harder to test. **Via code**, your Python decides with sequences, `if`, loops and `asyncio.gather`, which the SDK docs call "more deterministic and predictable, in terms of speed, cost and performance". A good production default is **code outside, LLM inside**: code owns stages, budgets, gates and failure handling, and the model decides only the plan, a route, or the next worker inside a bounded run. You can combine the primitives below: triage hands off to a specialist, and the specialist calls narrow helpers as tools.

| | `Agent.as_tool()` (manager keeps control) | Handoff (ownership moves) |
|---|---|---|
| Fan out to several specialists in one turn | **Yes.** Calls in one response run concurrently | **No.** One handoff per turn; extras get "Multiple handoffs detected, ignoring this one." (`openai-agents` 0.23.1 source, not the docs) |
| Merge results | Yes: the manager writes the answer | No: the triage agent is out of the turn |
| Context the specialist sees | Only the tool input (`parameters=`) | The history, unless filtered (`input_filter`) |
| Guardrails | On the manager, which writes the final answer (each tool agent's own guardrails still run inside its run) | On every agent that can answer ([3.5](../03-agents-sdk-and-agents-api/README.md#35-guardrails-and-tripwires)), or one `RunConfig(output_guardrails=[...])` |

### 8.8 Hosted subagents: Responses API Multi-agent, Agents API, Codex

Here a root agent spawns subagents on OpenAI's side through hosted actions. These are newer and less controllable than code orchestration, so verify details before you build on them.

| | **Responses API Multi-agent** (beta) | **Agents API subagents** (beta) | **Codex subagents** |
|---|---|---|---|
| Turn it on | `multi_agent={"enabled": True}`, `betas=["responses_multi_agent=v1"]` on `client.beta.responses.create` | `agent={"multi_agent": {"enabled": True, ...}}` on `client.beta.agents.sessions.create` | On by default; ask for it, or request it in `AGENTS.md` / a skill |
| Concurrency | `max_concurrent_subagents`, default **3** | `max_concurrent_subagents`, default **6** | `[agents] max_concurrent_threads_per_session` |
| Models | `gpt-6.1-sol` and GPT-5.6 models; subagents **share the request's model and tools** | The session's `agent.model` | Per custom agent in `.codex/agents/*.toml`, else the parent's |
| Your function tools | Any agent can emit `function_call`; you run it and return `function_call_output` | **Not supported** for subagents | Not applicable; subagents inherit the sandbox, MCP servers and skills |

Your app must **not** execute `multi_agent_call` items (`spawn_agent`, `wait_agent`, ...): the API runs them. You still run every `function_call`, whichever agent emitted it. The final answer is the message from agent `/root` with phase `final_answer`. Your developer message is additive to OpenAI's fixed instructions, so use it to tune delegation. Agents API subagents share one environment filesystem, so "agents that edit the same files must coordinate their changes". Codex subagents ([5.7](../05-codex/README.md#57-hooks-subagents-and-plugins-concept-level)) include built-in `default`, `worker` and `explorer` agents. Hosted multi-agent fits concrete, independent workstreams (exploring separate code areas, researching sources in parallel). Prefer one agent when steps depend on each other or share a mutable resource. Subagents also **increase token usage**.

> **Gotcha:** "Hosted" does not mean "governed". In Responses Multi-agent every agent can call every configured tool, and you cannot give one subagent a different model. For least privilege or per-branch models, orchestrate with the Agents SDK. Do not build new orchestrations in **Agent Builder** (deprecated 2026-06-03, shuts down 2026-11-30); the **Assistants API** was retired on 2026-08-26.

### 8.9 Multi-pass code review and independent reviewers

One pass over a 14-file PR gives uneven depth and missed bugs. Use three passes:

1. **Per-file pass.** One worker per file, in parallel (8.4), on the same severity rubric.
2. **Integration pass.** Sees the per-file findings plus the public interfaces and reports **only cross-file issues**.
3. **Independent reviewer pass.** A fresh instance that **never saw the workers' reasoning** marks each finding confirmed, rejected or needs a human, and flags what everyone missed. Here it runs on `gpt-6.1-sol`, a stronger model than the workers, with `output_type=ReviewerReport` and the instruction "Confirm only if the diff shows the problem. Reject anything you cannot tie to a line."

```python
class Adjudication(BaseModel):
    finding_id: str
    rationale: str                         # reason before the decision
    decision: Literal["confirmed", "rejected", "needs_human"]

class ReviewerReport(BaseModel):
    adjudications: list[Adjudication]
    missed_issues: list[str]

async def independent_review(diff: str, findings_json: str) -> ReviewerReport:
    # Fresh run: no to_input_list(), no previous_response_id.
    result = await Runner.run(independent_reviewer,
        f"<diff>\n{diff}\n</diff>\n<findings>\n{findings_json}\n</findings>")
    return result.final_output_as(ReviewerReport)
```

Structured Outputs guarantees the report's shape, not that it covers every finding exactly once. Check that in code, and escalate unknown, duplicate or missing ids, `needs_human` decisions and missed issues instead of approving. A model reviewing its own work in the same context tends to confirm its reasoning; "be critical" or more reasoning effort does not remove that bias.

**Codex review is this pattern, productized.** Its review rules "don't replace tests, branch protections, or required approvals", so keep lint in CI and the AI review for repository-specific behavior.

| Codex surface | What it does |
|---|---|
| `/review` | A dedicated, read-only reviewer. CLI scopes: base branch, uncommitted changes, a commit, or custom instructions (IDE and app: the first two) |
| `review_model` in `config.toml` | Runs `/review` on a different model from the author |
| `codex review --base <branch>` / `--uncommitted` / `--commit <sha>` | Non-interactive review for scripts and CI |
| `@codex review` on a GitHub PR | Flags only **P0 and P1** issues; follows `## Code Review Rules` in `AGENTS.md` |
| Subagent review prompt | "Spawn one subagent for security risks, one for test gaps, and one for maintainability. Wait for all three, then summarize the findings by category." |

### 8.10 Verification contracts, testing, and tracing an orchestration

Decomposition creates **seams** (plan → workers → merge → review), and most failures happen there. The Codex pathway asks you to split a change into workstreams, define *the evidence each must produce*, and *what each does when verification fails*:

| Field | Example for a per-file review worker |
|---|---|
| **Owner and scope** | One file, local issues only; read-only |
| **Evidence to return** | Structured findings: `path`, `line`, `severity`, `rule`, quoted code |
| **Acceptance check (in code)** | Every finding cites a line in the diff and quotes non-empty code from it; severity is in the enum |
| **On failure** | One retry with the validation error; then mark the file `unreviewed` and block "approve" |
| **Reintegration** | The integration pass reads only validated findings; duplicates merge by `path` + `line` + `rule`; code gives every candidate a unique id |

**Ownership** is part of the contract: "keep ownership clear when work runs in parallel". In Codex that means one worktree (and branch) per parallel writer. In an agent system, one worker owns each output and only the merge step writes the combined result. **Test offline.** The course asks you to test "whether agent decisions and handoffs meet those outcome and safety requirements". `agents.testing.ScriptedModel` replays scripted outputs through the real runner, records every call, and `assert_complete()` catches a run that stopped early.

```python
from agents.testing import ScriptedModel, assistant_message

async def test_narrow_plan_is_rejected() -> None:
    narrow = Plan(subtasks=[Subtask(id="1", facet="security",
                                    question="...", context="...")])
    scripted_planner = planner.clone(model=ScriptedModel(
        [[assistant_message(narrow.model_dump_json())]]))
    must_not_run = worker.clone(model=ScriptedModel([]))  # a call raises
    try:
        await orchestrate("Assess vendor X", planner=scripted_planner,
                          worker=must_not_run)         # the REAL gate
    except ValueError as exc:
        assert "cost" in str(exc) and "operations" in str(exc), exc
    else:
        raise AssertionError("the coverage check did not fire")
    finally:
        scripted_planner.model.assert_complete()   # planner ran once
    assert must_not_run.model.calls == ()   # no worker on a rejected plan
```

Use scripted runs for gates, routing tables, caps and partial failures. Use evals with the real model for model decisions: an eval per workflow step, **tool-selection** and **data-precision** evals for agents, **handoff accuracy** for multi-agent systems, and a **coverage** eval for planners. **Trace the orchestration as one unit.** Wrap all stages in one `trace("...", group_id=...)` so planner, workers, merge and review show as spans in one trace ([3.8](../03-agents-sdk-and-agents-api/README.md#38-tracing-and-lifecycle-hooks)). Tracing is unavailable under Zero Data Retention.

> **Gotcha:** `max_turns` limits one `Runner.run`, not the orchestration. Budget in code: sum `result.context_wrapper.usage` and check the ceiling **before** each run, reserving its worst case (`max_turns` requests), and cap output with `ModelSettings(max_tokens=...)`.

## Lesson code

Code from the video lesson: [../../presentations/08-task-decomposition/code/](../../presentations/08-task-decomposition/code/). The video script is the minimal version (a bare `asyncio.gather`, and it only prints the review verdict); the notebook shows the production pattern from 8.4 and 8.9.

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run 8.1–8.10 offline on scripted models, then build a PR review desk: planner with a coverage check, parallel file reviewers, an integration pass and an independent reviewer (flip `RUN_LIVE` to use the API) |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 exercises with auto-checks (5 offline, 1 optional live, ~$0.01), an architecture scenario and a scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>
## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Same steps every time | Fixed pipeline with `output_type` gates | An autonomous agent | Deterministic, testable per step, cheaper |
| Steps depend on what you find | Orchestrator-workers with capped re-planning | A fixed pipeline | The subtasks are unknown up front |
| Inputs fall into known categories | Classifier agent + code dispatch | One prompt that "acts like" each role | Testable routing, separate prompts and tools |
| Specialist should own the conversation | Handoff | Agent as tool | Ownership transfer |
| Manager must consult several specialists and merge | Agents as tools or code fan-out | Handoffs | One handoff per turn, and no merge after a handoff |
| Independent parts, latency matters | `asyncio.gather` with a semaphore | Sequential runs | Wall clock = slowest worker; bounded against bursts, with 429 retries |
| Most traffic is easy, a few cases are hard | Model tiering: `gpt-6-luna` first, escalate to `gpt-6.1-sol` / `gpt-6-astra` | The top model for everything | Cost tracks difficulty |
| Planner keeps missing whole areas | Code-side coverage check + goal-based planner prompt | Stronger workers | The defect is in the plan |
| Branches need different models, tools or approvals | Agents SDK orchestration | Hosted multi-agent | Hosted subagents share the request's model and tools |
| Reviewing AI-written code | Independent reviewer (`/review`, a fresh run, `@codex review`) | Same-session self-review | No confirmation bias |

<a id="common-mistakes-and-anti-patterns"></a>
## Common mistakes

- **Decomposing too early.** Five agents before one has been measured. Let evals justify every split.
- **Over-narrow decomposition.** The report silently omits music and film. Check coverage in code.
- **Handoffs for fan-out or synthesis.** One handoff per turn, and no merge after it.
- **Unbounded or all-or-nothing fan-out.** No semaphore, no 429 retries, or `asyncio.gather` without `return_exceptions=True`.
- **Uncapped loops, or budgeting with `max_turns` alone.** It bounds one run, not the orchestration.
- **Self-review in the same context**, or a reviewer that receives the generator's reasoning.

## Self-check

**Q1.** A due-diligence coordinator must query the pricing, legal and security specialists **in parallel** and write one merged memo. A developer configures `handoffs=[pricing, legal, security]`. What happens, and what is the fix?

- A) All three run in parallel; nothing to fix
- B) The SDK honors only one handoff per turn, and after it the coordinator cannot merge. Expose the specialists with `Agent.as_tool()` (or fan out in code) and let the coordinator synthesize
- C) Add `parallel_tool_calls=True` so handoffs run concurrently
- D) Chain the handoffs pricing → legal → security

<details><summary>Answer</summary>

**B.** Extra handoff calls in a turn are ignored ("Multiple handoffs detected, ignoring this one"), and control leaves the coordinator. Agents-as-tools keep the manager in control and run concurrently when emitted in one turn. C does not change handoff semantics. D is sequential, and nobody merges at the end.
</details>

**Q2.** A research system on "AI's impact on creative industries" returns a polished report that covers only visual art. Traces show the planner created three subtasks: digital art, graphic design, photography. Every worker succeeded. What is the root cause, and the strongest fix?

- A) The workers searched badly; give them a stronger model
- B) The planner decomposed too narrowly; add a code-side coverage check against required facets (and a goal-based planner prompt)
- C) The synthesizer dropped content; raise its `max_output_tokens`
- D) Tracing hid the other subtasks; disable `trace_include_sensitive_data`

<details><summary>Answer</summary>

**B.** The workers did exactly what they were assigned. The defect is in the plan, so the fix belongs at the plan seam: a deterministic coverage check, plus a planner prompt framed as coverage goals. A, C and D address stages that worked correctly.
</details>

**Q3.** A nightly job fans out 60 `Runner.run` calls with a bare `asyncio.gather`. Most nights a burst of 429 errors aborts the whole job, and all results are lost. What should change?

- A) Run the 60 calls sequentially
- B) Bound concurrency (a semaphore), use `return_exceptions=True` with retries for transient errors, and report any slot that still fails; consider the Batch API if results are not needed interactively
- C) Switch every worker to `gpt-6-astra` so requests finish faster
- D) Raise `max_turns` on each run

<details><summary>Answer</summary>

**B.** Bounded parallelism removes the burst without giving up the speedup, retries with backoff absorb the 429s that per-minute limits still cause (a semaphore caps requests in flight, not RPM or TPM), and per-slot failure handling keeps the good results. A throws away the speedup. C raises cost and does not address rate limits. D is unrelated to 429s.
</details>

**Q4.** An agent writes a patch and then reviews it in the same session with "be very critical of your own work". Reviewers keep finding bugs it missed. What is the best change?

- A) Raise `reasoning.effort` for the review step
- B) Run the review in an independent instance that sees only the diff and the review criteria, for example Codex `/review` (optionally with a different `review_model`), a fresh `Runner.run`, or `@codex review` on the PR
- C) Add "you MUST find at least three bugs" to the prompt
- D) Continue the session with `previous_response_id` so the reviewer has full context

<details><summary>Answer</summary>

**B.** The generating context carries the author's reasoning and biases the review toward confirming it. An independent instance removes that. A and C keep the same context, and C invents findings. D does the opposite of what is needed.
</details>

## Official documentation

- [Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration): the ownership question, "start with one agent"
- [Agents SDK: Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/): orchestrating via LLM vs via code
- [Agents SDK: Testing](https://openai.github.io/openai-agents-python/testing/): `agents.testing.ScriptedModel`
- [Responses API Multi-agent (beta)](https://developers.openai.com/api/docs/guides/responses-multi-agent)
- [Building agents track](https://developers.openai.com/tracks/building-agents): model selection, when to use multiple agents, shared memory keyed by `conversation_id`
- [Codex code review](https://learn.chatgpt.com/docs/code-review): `/review` and review scopes
- [Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github): `@codex review`, P0/P1 only, `## Code Review Rules`

[← Chapter 07 — Batch and cost](../07-batch-and-cost/README.md) | [↑ OpenAI path](../README.md) | [Chapter 09 — Escalation and human-in-the-loop →](../09-escalation-human-in-the-loop/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
