# Chapter 8 — Task Decomposition Strategies

> **Exam domain(s):** Domain 1 — Agentic Architecture & Orchestration (**27%**, task 1.6; supports 1.2 coordinator decomposition) · Domain 4 — Prompt Engineering & Structured Output (**20%**, task 4.6 multi-instance and multi-pass review) · also feeds CCAR-P Solution Design (1.3–1.5), CCDV-F Agents and Workflows (1.1, 1.3) and CCAO-F Prompting and Task Execution (1.2)
> **Est. time:** 6–8 hours (reading + 2 notebooks) · **Status:** [ ] not started

This chapter is about **how to split the work** in a Claude system: one call, a fixed chain, a router, or a planner that picks subtasks at runtime. Each choice moves cost, latency, reliability and debuggability. The exam (and every design review) checks that you can read the shape of a task and pick the **simplest structure that fixes the root cause**.

## What you'll learn

- Choose between a **fixed pipeline** (prompt chaining) and **dynamic adaptive decomposition** from the shape of the task.
- Split large code reviews into **per-file local passes** plus a **cross-file integration pass**.
- Explain why self-review is weak and design an **independent reviewer instance**.
- Add a **verification pass** with per-finding confidence, calibrated on labeled data.
- Map problems onto the workflow patterns, know when an agent is justified, and build a bounded **async fan-out**.

## Prerequisites

[00-prerequisites](../../00-prerequisites/README.md) (Python, `.env`, `asyncio`) · [Chapter 1](../01-claude-api-fundamentals/README.md) · [Chapter 2](../02-tool-use/README.md) (structured outputs) · [Chapter 3](../03-agent-sdk/README.md#33-hub-and-spoke-coordinator-and-subagents) (coordinator and subagents) · [Chapter 5](../05-claude-code/README.md#59-claude-code-in-cicd-headless-mode) (headless CI review) · [Chapter 6](../06-prompt-engineering/README.md#63-prompt-chaining) (prompt chaining basics) · [Chapter 7](../07-message-batches/README.md) (batches for fan-outs that can wait)

## Concepts

Snippets assume the notebooks' setup: the usual imports (`asyncio`, `json`, `anthropic`, Pydantic `BaseModel`, `typing.Literal`), `client = anthropic.Anthropic()`, `aclient = anthropic.AsyncAnthropic()`, `MODEL` (default `claude-sonnet-5-5`) and `FAST_MODEL = "claude-haiku-5-5"`. Names like `Metadata` or `Review` are small Pydantic models defined in the notebooks.

Start every design by diagnosing the shape of the task (the decision list):

- One well-prompted call does it reliably → an **augmented LLM call** (retrieval, tools, structured output).
- Steps known up front, each feeds the next → **prompt chain with gates** (8.1).
- Steps known up front, independent slices → **parallelization: sectioning** (8.6).
- Steps depend on what you find, bounded per run → **orchestrator-workers** (8.2, 8.8).
- Long, exploratory, environment-driven → **agent loop / coordinator + subagents** (8.7).
- Inputs fall into distinct categories → **routing** in front of any of the above (8.6).

### 8.1 Fixed pipelines (prompt chaining)

A **fixed pipeline** decides every step before the first call runs. Each call does one focused job, and its output feeds the next. The control flow lives in **your code**, so you can evaluate each step, put **programmatic gates** between steps (a schema check, a business rule, a route to a human), and regression-test the run. Use it when the steps are known and the same for every input.

Two rules: totals, lookups and formatting belong in code, not in a model call; and gates decide on **structured fields**, never on prose. `parsed_or_raise()` (used in every snippet) raises unless `stop_reason` is `end_turn` and `parsed_output` is set, because structured outputs guarantee shape only on a normal finish.

```python
def step(system: str, user: str, schema: type[BaseModel]):
    response = client.messages.parse(
        model=MODEL, max_tokens=4096, system=system,
        messages=[{"role": "user", "content": user}], output_format=schema)
    return parsed_or_raise(response)

def invoice_pipeline(document: str) -> dict:
    meta = step("Classify the document. Use 'other' if unsure.",
                document, Metadata)
    if meta.doc_type != "invoice":            # gate 1: code decides the route
        return {"status": "routed", "reason": f"doc_type={meta.doc_type}"}
    data = step("Extract the invoice fields. "
                "Use null when a value is not printed.", document, InvoiceData)
    total = round(sum(data.line_item_amounts), 2)   # gate 2: business rule
    if data.stated_total is not None and abs(total - data.stated_total) > 0.01:
        return {"status": "needs_review",
                "reason": f"items sum to {total}, stated {data.stated_total}"}
    return {"status": "ok", "data": data.model_dump(), "computed_total": total}
```

### 8.2 Dynamic adaptive decomposition

In **dynamic adaptive decomposition**, subtasks come from intermediate results: you discover something, then re-plan. Use it for open-ended work whose scope is unknown (debugging, research, root-cause analysis). The official exam guide's example (task 1.6) is "add comprehensive tests to a legacy codebase": **map the structure** first (`Glob` for modules and tests, `Grep` for entry points), because you cannot plan before you know what exists. **Findings:** four modules have no tests and one has only a smoke test. **Prioritize** by impact: start with `billing` (it moves money and changes most often). **Discover a dependency:** `billing` reads the current time to decide late fees. **Adapt:** add an injectable clock first, then write the billing tests.

The core is a **planner loop**. A planner call reads the goal plus compact findings and returns the next 1-3 subtasks, highest impact first, as structured output. The loop stops on a boolean field, not on the text "done", and the round cap is only a safety net.

```python
class Plan(BaseModel):
    done: bool                      # explicit, structured completion signal
    next_subtasks: list[Subtask]    # Subtask: goal, rationale, priority
    open_questions: list[str]

def adaptive_investigation(goal, run_subtask, max_rounds: int = 8):
    findings: list[dict] = []
    for _ in range(max_rounds):        # safety net, not the primary stop
        plan = step(PLANNER_SYSTEM, f"<goal>{goal}</goal>\n"
                    f"<findings>{json.dumps(findings)}</findings>", Plan)
        if plan.done or not plan.next_subtasks:
            return findings
        for sub in plan.next_subtasks[:3]:      # cap the fan-out per round
            findings.append({"subtask": sub.goal, "result": run_subtask(sub)})
    findings.append({"status": "budget_exhausted",
                     "note": "report partial results and open questions"})
    return findings
```

**The main risk is a bad decomposition that raises no error.** Split "AI in creative industries" into digital art, graphic design and photography, and every worker succeeds while the report misses music, film and writing. Ask the planner for a **coverage map** (which part of the goal each subtask covers) and check it before fanning out.

> **Exam trap:** When every subagent reports success but the output has a gap, the root cause is the **coordinator's decomposition**, not the workers or the synthesis prompt.

| | Fixed pipeline (prompt chaining) | Dynamic adaptive decomposition |
|---|---|---|
| Who decides the next step | Your code | A planner model, from intermediate results |
| Typical task | Multi-aspect review, document pipeline | Debugging, research, tests for an unknown codebase |
| Typical failure | Cannot handle an unplanned branch | Too-narrow decomposition, runaway loops |

### 8.3 Multi-pass code review

On a PR past roughly ten files, one review call fails in three ways: **attention dilution** (deep on some files, shallow on others), **inconsistent findings** (flagged in one file, approved in identical code elsewhere), and **missed obvious bugs**. The fix is two passes:

- **Local pass, one per file**, with the same rubric and schema. It reports only issues visible inside that file and returns a `FileReview`: findings plus the file's exports and imports (`review_file` is one `messages.parse` call with `LOCAL_RULES` that returns `(path, FileReview)`).
- **Integration pass, once.** It gets the interfaces and local findings, never the full source again (that would recreate the dilution), and reports only cross-file issues: contracts, types, data flow, error propagation, circular dependencies.

The official exam guide calls this **prompt chaining**, because the integration pass depends on the local passes. Inside the first stage the per-file passes are independent, so they run in parallel (sectioning, 8.6).

```python
async def multi_pass_review(files: dict[str, str]) -> dict:
    sem = asyncio.Semaphore(5)
    local = dict(await asyncio.gather(
        *(review_file(p, s, sem) for p, s in files.items())))
    summary = "\n".join(
        f'<file path="{p}">\n<exports>{r.exports}</exports>\n'
        f"<imports>{r.imports}</imports>\n"
        f"<local_findings>{[f.issue for f in r.findings]}</local_findings>\n"
        "</file>"
        for p, r in local.items())
    integration = parsed_or_raise(await aclient.messages.parse(
        model=MODEL, max_tokens=8000, system=INTEGRATION_RULES,
        messages=[{"role": "user", "content": summary}],
        output_format=CrossFileReview))
    return {"local": local, "cross_file": integration.findings}
```

> **Exam trap:** In the official sample question (a 14-file PR reviewed in one pass), reject "use a larger context window" (more room does not improve attention), "run three full-PR passes and keep issues found twice" (votes away real bugs detected inconsistently), and "make developers split PRs" (pushes the problem onto people).

### 8.4 Independent review instances: why self-review is weak

A model reviewing its own output **in the same session** still has its generation reasoning in context, so it tends to confirm its approach. The official exam guide (task 3.6) calls this **session context isolation**: the generating session reviews its own changes less well than an independent instance. The fix is a **second, independent Claude instance** that gets the artifact, the spec and the criteria, and **none** of the generator's messages, tool results, thinking or rationale. The Messages API is stateless, so independence is just what you put in `messages`. In Claude Code, use a separate session or a CI job with its own `claude -p` reviewer.

```python
REVIEWER_SYSTEM = """You are a code reviewer who did not write this change.
Check it against the spec and the criteria. Assume nothing is correct until
you have checked it. Report only issues you can point to in the diff."""

def independent_review(spec: str, diff: str, criteria: str) -> Review:
    # A brand-new request: no generator messages, thinking or rationale.
    response = client.messages.parse(
        model=MODEL, max_tokens=8000, system=REVIEWER_SYSTEM,
        messages=[{"role": "user", "content":
                   f"<spec>\n{spec}\n</spec>\n"
                   f"<criteria>\n{criteria}\n</criteria>\n"
                   f"<diff>\n{diff}\n</diff>"}],
        output_format=Review)     # Review: approved, findings
    return parsed_or_raise(response)
```

> **Exam trap:** For the root cause of self-review blind spots, reject any fix that keeps the review inside the generating context, such as a "check your own work" line in the prompt or more thinking for the generator. The answer is a second instance **without the generator's reasoning context**. Note: on current models (Opus 5.5, Sonnet 5.5, Fable 5.1) thinking is adaptive and on by default, steered by `effort`, but it still happens inside the generator's context.

### 8.5 Verification passes and confidence-based routing

Review passes produce **candidate** findings. A **verification pass** (an independent instance) re-checks each one and returns a `Verdict`: `confirmed`, `plausible` or `refuted`, with evidence and a self-reported **confidence alongside each finding**. Confidence drives routing. Self-reported confidence is not trustworthy on its own, so **calibrate** it: label a sample of past findings, compute precision per confidence bucket, and auto-post only buckets that meet your target (say 95%). The human-review side is in [Chapter 9](../09-escalation-human-in-the-loop/README.md).

```python
def route(v: Verdict, auto_post: set[str]) -> str:
    """auto_post comes from calibration on labeled data, e.g. {"high"}."""
    if v.verdict == "refuted":
        return "drop_and_log"
    if v.verdict == "confirmed" and v.confidence in auto_post:
        return "post_inline"
    return "human_triage"

def precision_by_bucket(labeled: list[tuple[str, bool]]) -> dict[str, float]:
    """labeled = [(confidence, was_real_issue), ...] from a reviewed sample."""
    buckets: dict[str, list[bool]] = {}
    for confidence, real in labeled:
        buckets.setdefault(confidence, []).append(real)
    return {c: round(sum(v) / len(v), 3) for c, v in buckets.items()}
```

> **Exam trap:** "Have the model rate its confidence and escalate below a threshold" is **wrong** as the only, uncalibrated gate (Domain 5). "The verification pass reports confidence alongside each finding to enable calibrated routing" is **right** for review architectures (task 4.6).

### 8.6 The workflow pattern catalog

Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) separates **workflows** ("LLMs and tools are orchestrated through predefined code paths") from **agents** ("LLMs dynamically direct their own processes and tool usage"). Every pattern is built from an **augmented LLM**: one model call enhanced with retrieval, tools and memory.

| Pattern | Shape and when to use it | Example |
|---|---|---|
| **Prompt chaining** | Fixed sequence with gates; the task splits into fixed subtasks | Write an outline, check it, then write the document |
| **Routing** | A classifier sends each input to a specialized prompt, tool set or model | Support queries to different flows; easy ones to Haiku 5.5, hard ones to Sonnet or Opus |
| **Parallelization: sectioning** | Independent slices run at once, then merge | One call answers while another screens content; per-file review |
| **Parallelization: voting** | The same task runs several times; the vote threshold picks the trade-off: **any** = higher recall, **majority** = higher precision | Several prompts check code for vulnerabilities |
| **Orchestrator-workers** | A central model picks subtasks at runtime, delegates, synthesizes | Multi-file coding changes, multi-source research |
| **Evaluator-optimizer** | One call generates, a separate call evaluates against criteria, loop with a round cap | Literary translation; keep the evaluator independent (8.4) |
| **Agent** | A model in a tool loop until a stop condition | Coding agents; highest cost, needs guardrails |

Voting is a valid pattern, but for a large PR reviewed in one pass it only hides attention dilution: fix the structure (per-file passes) first. **Routing in code:** a cheap model classifies into structured fields, and your code dispatches.

```python
class Route(BaseModel):
    category: Literal["billing", "technical", "refund", "other"]
    complexity: Literal["simple", "complex"]

def route_request(query: str) -> tuple[str, str]:
    choice = parsed_or_raise(client.messages.parse(
        model=FAST_MODEL, max_tokens=512,
        system="Classify the support request. "
               "Use 'other' when no category fits.",
        messages=[{"role": "user", "content": query}], output_format=Route,
    ))
    model = FAST_MODEL if choice.complexity == "simple" else MODEL  # tiering
    return choice.category, model
```

### 8.7 Workflow or agent: choosing the level of autonomy

Find the simplest solution that works, and add complexity only when it measurably improves outcomes.

| | Augmented LLM call | Workflow | Agent (single loop) | Multi-agent |
|---|---|---|---|---|
| Who decides the path | Nobody: one call | Your code | The model, turn by turn | A lead model delegating to workers |
| Cost and latency | Lowest | Low to medium | Higher | Highest |
| Pick it when | One prompt with retrieval or tools is enough | The shape is known or planned per run | Many unpredictable tool steps | Breadth-first work that splits into independent, context-heavy subtasks |

**Multi-agent is expensive.** Anthropic's [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) post reports that agents use about **4×** the tokens of a chat and multi-agent systems about **15×**. It fits poorly when all agents need the same context or depend on each other, which is why most coding tasks parallelize less well than research.

**Manager/supervisor hierarchies.** The exam expects **hub-and-spoke**: one coordinator owns decomposition, delegation, aggregation, error handling and talking to the user. Subagents start with a fresh context and return only their result. Deep hierarchies multiply cost and lose observability.

**What subagents buy you:** **context isolation**, **parallelism**, **specialization** and **independence**. Parallelism needs several subagent-tool calls (`Agent`, `Task` in older docs) **in a single response** ([Chapter 3](../03-agent-sdk/README.md#34-the-subagent-tool-agent-formerly-task)). Give each worker a complete brief: objective, output format, tools and sources, and boundaries. Newer models can over-delegate, so say when subagents are warranted.

**Frameworks** such as Strands, LangGraph and PydanticAI implement the same patterns. Start with the API directly; if you adopt a framework, understand what it does underneath.

> **Exam trap:** "Build an autonomous multi-agent system to classify tickets into four queues" is **routing**, a workflow. An agent adds cost and unpredictability without adding capability.

### 8.8 Fan-out in code: orchestrator-workers with `asyncio` and the Messages API

The practice notebook's mini-project has this shape: **decompose → fan out workers → synthesize → independent review**, on the plain Messages API. The orchestrator returns a `Decomposition`: worker briefs plus a `coverage` list mapping each aspect to a subtask. `WORKER_SYSTEM` is the shared worker instructions with `cache_control`. A failed worker becomes a structured result, not a crash.

```python
async def run_worker(brief: WorkerBrief, sem) -> WorkerResult:
    async with sem:
        try:
            return parsed_or_raise(await aclient.messages.parse(
                model=MODEL, max_tokens=4000, system=WORKER_SYSTEM,
                messages=[{"role": "user", "content": brief.model_dump_json()}],
                output_format=WorkerResult))
        except (anthropic.APIError, ValueError, RuntimeError) as exc:
            return WorkerResult(task_id=brief.id, status="failed", evidence=[],
                                summary=f"{type(exc).__name__}: {exc}")

async def orchestrate(goal: str, max_workers=6, concurrency=4) -> dict:
    plan = parsed_or_raise(await aclient.messages.parse(
        model=MODEL, max_tokens=4000, output_format=Decomposition,
        system="Decompose the goal into independent, non-overlapping "
               "subtasks that together cover it fully.",
        messages=[{"role": "user", "content": goal}]))
    briefs = plan.subtasks[:max_workers]        # cap the fan-out in code
    sem = asyncio.Semaphore(concurrency)
    results = await asyncio.gather(*(run_worker(b, sem) for b in briefs))
    gaps = [r.task_id for r in results if r.status != "ok"]
    # Then: one synthesis call that states coverage gaps explicitly, and
    # independent_review() of the draft (8.4), never the worker transcripts.
    return {"plan": plan, "results": results, "gaps": gaps}
```

| Concern | What to do |
|---|---|
| **Concurrency, rate limits, retries** | Bound concurrency with an `asyncio.Semaphore`. Limits are per organization and **per model** (RPM, ITPM, OTPM, token bucket); exceeding one returns **429** with `retry-after`. The Python SDK retries 408, 409, 429, 5xx and connection errors **twice by default**, honoring `retry-after` (tune with `max_retries`). Do not go sequential or disable retries. |
| **Partial failure** | Return a structured `failed`/`partial` result, continue, and state the gap in the synthesis ([Chapter 10](../10-multi-agent-error-handling/README.md)). |
| **Prompt caching** | A cache entry exists only **after the first response starts**: send one request first, then the rest. Cached reads do not count toward ITPM. Minimum cacheable length: 512 tokens on Sonnet 5.5, Opus 5.5, Fable 5.1 and Haiku 5.5; 4,096 on the legacy Haiku 4.5. |
| **Cost** | Roughly `orchestrator + N × (prefix + brief + output) + synthesis + reviewer`; latency is about the slowest worker. Not urgent? Message Batches at 50% cost, one batch per pass. |
| **Observability** | Give every subtask an id; log brief, model, tokens, latency and status per call. |

### 8.9 Decomposing multi-concern requests

"My bill went up, the roaming pack I paid for isn't active, and I want a cheaper plan" holds three concerns. Two symptoms need two different fixes:

| Symptom | Best fix |
|---|---|
| With several issues the agent solves only one or **mixes parameters between orders** | **Few-shot examples** of multi-issue handling that keep each issue's parameters separate ([Chapter 6](../06-prompt-engineering/README.md#61-few-shot-prompting)) |
| **Far more tool calls** than a single issue needs, issues handled one after another, the **same customer data fetched again** each time | **Decompose** into issues, fetch shared context **once**, **investigate in parallel**, then **synthesize one resolution** |

The CCAR-F prep exercise tests this: send multi-concern messages and verify the agent decomposes the request, handles each concern and synthesizes a unified response. A preprocessing call that handles each part fully independently loses the shared context (one customer, one account).

### 8.10 Decomposition in Claude Code today *(beyond the guide)*

Claude Code packages these patterns. This goes beyond the official exam guide: you do not need their flags for CCAR-F, but they help on scenario questions.

| Feature | Pattern it implements |
|---|---|
| **`/batch <instruction>`** | Orchestrator-workers: splits a large change into 5–30 units, one background subagent per unit in its own git worktree |
| **Code Review** (managed) | Parallel specialists plus a verification step that filters false positives ([8.5](#85-verification-passes-and-confidence-based-routing)) |
| **`/code-review`** (local) | Review in a background subagent with its own context; for full independence, run it from a fresh session or CI |
| **Agent teams** (experimental) | Supervisor + peers: a lead coordinates teammates through a shared task list |

### 8.11 Decomposition for everyday Claude use (Associate lens)

CCAO-F tests the same idea in Claude apps: **break a complex request into stages and check each stage before moving on.** For "prepare a market-entry recommendation for Brazil": (1) **clarify and scope** by asking Claude what it needs to know ([Chapter 6](../06-prompt-engineering/README.md#64-the-interview-pattern)); (2) **gather** inputs per dimension (market size, regulation, competitors), ideally in a Project with the shared sources; (3) **analyze** each dimension, **synthesize** across them and **draft** for the audience; (4) **review independently** in a fresh conversation, and verify citations yourself before sharing.

## Lesson code

Video-lesson code: [../../presentations/08-task-decomposition/code/](../../presentations/08-task-decomposition/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run every pattern from 8.1–8.11 offline against a fake client (optional live cells), then build the mini-project: a research orchestrator with a coverage check, bounded fan-out, synthesis and an independent reviewer |
| [`02_homework.ipynb`](02_homework.ipynb) | 10-question quiz, 6 auto-checked coding exercises, an architecture scenario and a scorecard (pass mark 72%) |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Same steps for every input | Prompt chain with gates | Autonomous agent / orchestrator |
| Scope unknown, next step depends on findings | Adaptive decomposition (planner loop / orchestrator-workers) | Fixed chain |
| 14-file PR, inconsistent depth, contradictory comments | Per-file local passes + integration pass | Bigger context, majority voting, smaller PRs |
| AI-generated code needs review | Independent instance without the generator's context | Self-critique prompt, more thinking |
| Too many findings for humans to read | Verification pass with confidence calibrated on labeled data | Uncalibrated "drop below 7/10" |
| Inputs fall into distinct categories | Routing (cheap model classifies, code dispatches) | One giant prompt |
| Tight dependencies, shared context (most coding) | Single agent or chain | Multi-agent |
| Parallel calls hit 429s | Semaphore + SDK retries + caching + partial results | Sequential calls, disabling retries |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Agent-by-default.** Reaching for an agent when the task has a known shape.
- **Chains without gates.** One bad step poisons the rest because nothing checks it.
- **One mega-review.** A whole PR in one call, "fixed" with a bigger model or majority voting.
- **Self-review in the same session.** Appending "now review your work" to the generator's conversation.
- **Trusting raw confidence.** Using self-rated confidence as a gate without calibrating it.
- **Unbounded or silent fan-out.** No semaphore, no cap on subtasks, and failed workers that vanish.

## Self-check

**1. (Claude Code for CI)** A PR touches 17 files in a payroll-export service. The automated review sends all of them in one call. The result is uneven: long comments on the first few files and one-liners on the rest, an unhandled empty list that nobody flagged, and a retry helper that is called risky in one file but approved where it is copied unchanged into another. What should you change?

- A) Move to a model with a bigger context window so all 17 files fit with room to spare
- B) Review the whole PR three times and keep only the issues that come up at least twice
- C) Review each file in its own pass for local issues, then run a separate integration pass for cross-file data flow
- D) Ask developers to keep every PR under five files

<details><summary>Answer</summary>

**C.** The root cause is attention dilution. Per-file passes with one shared rubric give consistent depth and remove contradictory findings, and the integration pass covers the boundaries. A confuses context size with attention quality. B votes away real bugs that are detected inconsistently. D pushes the problem onto developers.
</details>

**2. (Claude Code for CI)** Your CI job has Claude Code write data-pipeline transforms, then reviews each change before a person opens the PR. You want the review to be independent of the author. Which design gives you that?

- A) In the same session, send "Now act as a strict reviewer and list every bug in the change above"
- B) Start a new request for the reviewer, and pass in the generator's thinking blocks and its final explanation so the reviewer knows what was intended
- C) Start a new request with a reviewer system prompt that receives only the diff, the ticket and the review criteria
- D) Keep the same session, but switch it to a larger model for the review turn

<details><summary>Answer</summary>

**C.** Independence depends on what is in the reviewer's context, not on the prompt or the model. A keeps the author's reasoning in the same conversation. B is a new request in name only: the thinking blocks and the explanation bring the author's conclusions with them. D changes the model, but the author's reasoning is still in the context.
</details>

**3. (Developer productivity)** You are asked to "add comprehensive tests to a legacy codebase" you have never seen. Which plan fits best?

- A) Generate tests for every file in alphabetical order with a fixed prompt per file
- B) Map the structure first (modules, existing tests, entry points), rank areas by risk and coverage gaps, start with the highest-impact module, and re-plan when something new turns up (such as code that reads the system clock and needs a controllable time source before it can be tested)
- C) Ask one call to write all the tests at once to save tokens
- D) Write a fixed five-step chain: list files, write tests, run tests, fix tests, commit

<details><summary>Answer</summary>

**B.** This is an open-ended task whose scope is unknown, so it needs adaptive decomposition: map, prioritize, adapt. A and D are fixed pipelines that cannot react to what they discover (and A ignores risk). C ignores scope and attention entirely.
</details>

**4. (Claude Code for CI)** Your review bot produces about 200 findings a day and engineers have stopped reading them. Leadership wants fewer false positives without hiding real bugs. What is the best design?

- A) Add an independent verification pass that confirms or refutes each finding with evidence and a confidence level; calibrate which confidence levels to auto-post using a labeled sample, and send the rest to a triage queue
- B) Ask the reviewer for a 1–10 confidence score and silently drop everything below 7
- C) Keep only findings that three separate review runs agree on
- D) Show all findings but sort them by severity

<details><summary>Answer</summary>

**A.** Verification plus calibrated routing reduces noise while keeping uncertain findings visible to humans. B trusts uncalibrated self-ratings and hides findings with no measurement. C votes away inconsistently detected real bugs. D leaves the noise in place.
</details>

## Official documentation

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (Anthropic Engineering): workflows vs agents, the six patterns
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (Anthropic Engineering): orchestrator-worker in production, token costs, delegation lessons
- [Agent pattern notebooks in the Claude Cookbooks](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents): `basic_workflows`, `orchestrator_workers`, `evaluator_optimizer`
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices): chain complex prompts, subagent orchestration, parallel tool calling
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits): RPM / ITPM / OTPM per model, `retry-after`, cache-aware ITPM
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): shared prefixes, concurrent requests, minimum lengths

[← Chapter 7 — Message Batches API](../07-message-batches/README.md) | [↑ Claude path overview](../README.md) | [Chapter 9 — Escalation and Human-in-the-Loop →](../09-escalation-human-in-the-loop/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
