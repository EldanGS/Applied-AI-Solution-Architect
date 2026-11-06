# Chapter 02 — Workflow design and delegation

> **Certs and courses served:** CCAO-F Domain 4 — Workflow Integration and Solution Design (**16%**, tasks 4.1–4.4) and Domain 7 — Troubleshooting and Optimization (**10%**, task 7.3) · OpenAI Academy Foundations pathway: **Applied AI Foundations** and **Agents and Workflows**; AI Leadership ("Designing AI workflows") · Role area **CHANGE** (workflow redesign)
> **Est. time:** 4–5 hours (reading + 2 notebooks) · **Status:** [ ] not started

Most people use AI one prompt at a time: they ask, read the answer, and start again the next day. This chapter is about the step after that, from **"I use AI"** to **"our process uses AI"**. You take a piece of recurring work, break it into steps, decide for each step whether AI does it, a human keeps it or the two share it, add review checkpoints where mistakes would hurt, and hand larger pieces to an agent with a clear brief. The design is the same whether the work runs in Claude or in ChatGPT; only the place it lives changes ([2.11](#211-claude-and-openai-side-by-side)).

The README needs no coding background. The notebooks turn the worksheets into small Python functions so you can test your decisions.

## What you'll learn

- Pick a recurring workflow worth redesigning and map it as steps with inputs, outputs, owners and "done" criteria.
- Use AI to analyze the requirements, plan the workflow and iterate on the design.
- Decide per step whether **code, AI, a human, or AI plus human review** should do it, using risk, reversibility and the cost of checking.
- Place **review checkpoints** and choose the **model and reasoning effort** per step to balance quality, speed and cost.
- Move from asking to **assigning work to an agent**: a brief with context, deliverable, boundaries and stop conditions.
- Improve the workflow over time by promoting recurring fixes into shared context, templates and checks, and share it with your team.

## Prerequisites

None for the README. For the notebooks: the venv from [00-prerequisites](../../00-prerequisites/README.md). Helpful background: [Claude 06 §6.4](../../anthropic-claude/06-prompt-engineering/README.md#64-the-interview-pattern) (the interview pattern), [Claude 08 §8.11](../../anthropic-claude/08-task-decomposition/README.md#811-decomposition-for-everyday-claude-use-associate-lens) (decomposing a request) and [chapter 01](../01-ai-fluency-prompting-and-output-validation/README.md) of this track (AI fluency, prompting and output validation; its [§1.3](../01-ai-fluency-prompting-and-output-validation/README.md#13-delegation-choosing-the-mode-of-collaboration) introduces Delegation for single tasks).

## Concepts

The running example is a fictional outdoor retailer, **Fernhill Outdoor**. Every Monday an analyst spends about four hours turning last week's support tickets and survey comments into a feedback digest for the product team. We will redesign that workflow.

### 2.1 From prompts to workflows

A **workflow** is recurring work with a trigger, a fixed set of steps, an output and an owner. A prompt helps with one step once. A workflow design decides how AI helps with every run, so the gain repeats and the quality is predictable.

Good first candidates share four traits: the work **recurs** (weekly or more), it has a **clear output** someone uses, it takes **real time**, and you can **tell a good result from a bad one**. Weak candidates are one-off tasks, work whose quality nobody can judge, and work that is mostly relationships or accountability.

There are two ways to bring AI in:

| | Augment | Redesign |
|---|---|---|
| What changes | AI speeds up existing steps | The steps themselves change |
| Example | AI drafts the digest the analyst used to write | Tagging moves from the analyst to AI, the analyst reviews a sample and spends the saved time on root causes |
| Risk | Low; the gain is often small | Higher; needs new checkpoints and new roles |

Redesign usually pays more, because AI changes **which step is the bottleneck**: when drafting becomes cheap, review and decisions become the slow part, and the process should be built around them. That is **process optimization**, not just faster typing.

Example workflows by role:

| Role | Recurring workflow |
|---|---|
| Operations | Weekly vendor-invoice exceptions report |
| Marketing | Monthly campaign performance summary |
| Project management | Status report from tickets and meeting notes |
| Support | Weekly feedback digest (our example) |
| HR | First-round screening notes against a fixed rubric (with strict human review) |

### 2.2 Map the workflow: steps, inputs and outputs

Before deciding anything about AI, write the workflow down as it runs today. For each step record the **input**, the **output**, the **owner** and **done when** (how you know the step is finished and right). Steps are small enough when each has one output that someone could check on its own.

| # | Step | Input | Output | Done when |
|---|---|---|---|---|
| 1 | Export last week's feedback | Help desk, survey tool | `feedback.csv` | All channels present, date range correct |
| 2 | Remove personal data | `feedback.csv` | Redacted comments | No names, emails or order numbers |
| 3 | Tag theme and sentiment | Redacted comments | Tagged rows | Every row has one theme from the list |
| 4 | Count themes, compare with last week | Tagged rows | Trend table | Totals match the row count |
| 5 | Pick quotes per top theme | Tagged rows | 2 quotes per theme | Quotes are verbatim and representative |
| 6 | Draft the digest | Trend table, quotes | Draft digest | Follows the template, cites counts |
| 7 | Review and edit | Draft, sources | Approved digest | Reviewer signs off |
| 8 | Choose backlog items | Approved digest | 1–3 backlog tickets | Product owner decides |
| 9 | Send to the product channel | Approved digest | Posted message | Posted after approval only |

In the notebook each row is a small record; the delegation and checkpoint rules in 2.4 and 2.5 read it.

```python
from dataclasses import dataclass

@dataclass
class Step:
    name: str
    input: str
    output: str
    done_when: str
    owner: str = "analyst"     # who is accountable today
```

### 2.3 Use AI to analyze, plan and design the workflow

AI is useful before it does any step: it can help you **analyze the requirements**, **plan** the workflow and **iterate on the design**. Three habits make that work:

1. **Let it interview you.** Describe the goal and ask it to ask you questions, one at a time, about inputs, users, volumes, deadlines and what "good" looks like ([Claude 06 §6.4](../../anthropic-claude/06-prompt-engineering/README.md#64-the-interview-pattern)).
2. **Ask for a structured plan, not prose:** the step table from 2.2 plus **assumptions** and **open questions**. You check the assumptions; the model cannot know your org.
3. **Ask for options, then choose.** "Give me two designs for this workflow, one that changes as little as possible and one that redesigns it, with the trade-offs." Then refine one with feedback from the people who run it.

```text
I run a weekly feedback digest (details below). Interview me, one question
at a time, until you can map it. Then return:
1. a table of steps: input, output, owner, done-when
2. assumptions you made
3. open questions I must answer before we change anything
<details>...</details>
```

The model drafts; you own the design. It can suggest a step order that looks sensible but ignores a rule only you know (for example, legal must approve anything sent outside the company).

### 2.4 Delegate, share or keep: the delegation worksheet

For each step, decide who does it. There are four answers, not two:

| Decision | Meaning | Typical steps |
|---|---|---|
| **Code** | Fixed rules give the right answer every time | Exports, totals, lookups, sending, redaction patterns |
| **AI** | AI does it; a human spot-checks a sample | High-volume, low-impact, easy-to-check work (tagging) |
| **Shared** | AI drafts, a human approves before it moves on | Drafts for an audience, quote selection, anything hard to undo |
| **Human** | A person does it (AI may prepare inputs) | Decisions someone is accountable for: priorities, money, people |

Score each step on a worksheet and apply the rules **in order**:

| # | Question | If yes |
|---|---|---|
| 1 | Do fixed rules give the right answer? | Code: cheaper, faster and exact |
| 2 | Is it a decision someone must own (priorities, money, people, commitments)? | Human |
| 3 | Is AI a poor fit (missing data, needs relationships or tacit knowledge)? | Human |
| 4 | Does checking the output take as long as doing the step? | Human: delegation saves nothing |
| 5 | Is an escaped error costly, or the action hard to undo? | Shared |
| 6 | Otherwise | AI, with sampled spot checks |

Rule 4 is the one people forget. Delegation pays only when **verification is cheaper than doing the work**: checking 20 of 400 tags takes minutes, but checking a legal summary line by line against the contract can take as long as writing it.

```python
def decide(s: dict) -> str:
    if s["rule_based"]:
        return "code"
    if s["owner_decision"] or s["ai_fit"] == "low":
        return "human"
    if s["check_minutes"] >= s["do_minutes"]:
        return "human"
    if s["impact"] == "high" or not s["reversible"]:
        return "shared"
    return "ai"
```

For Fernhill: steps 1, 2 (patterns), 4 and 9 are code; step 3 is AI; steps 5 and 6 are shared; steps 7 and 8 stay human.

### 2.5 Review checkpoints

A **checkpoint** is a place where a named person checks the work against written criteria before it moves on. Put one:

- **before any irreversible or external action** (sending, paying, publishing, deleting);
- **after every shared step** (that is what "shared" means);
- **after an early step that many later steps depend on**, when its errors would be hard to spot later (wrong tags silently skew every count after them).

Checkpoints cost human time, so do not add one after every step. A good checkpoint has a **checklist built from the "done when" column**, the **sources** next to the draft (so the reviewer checks facts, not tone), and a **record of what was corrected** (2.9 uses it).

**Review drafts and results, not just the final text.** For the digest: are the counts right (compare with the trend table), are the quotes verbatim (search the source), is every claim backed by the data, is anything important missing? Reading for style alone is a rubber stamp. Spot checks on AI-only steps work the same way on a sample, for example 20 random tags a week.

Escalation rules and approval gates in code are taught in [Claude 09](../../anthropic-claude/09-escalation-human-in-the-loop/README.md#91-when-to-escalate) and [OpenAI 09](../../openai-codex/09-escalation-human-in-the-loop/README.md#91-when-to-escalate); checking claims against sources in [Claude 12 §12.10](../../anthropic-claude/12-provenance/README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide).

### 2.6 Model and reasoning effort per step: quality, speed and cost

A **reasoning model** works through a problem before it answers. It is stronger on multi-step work (planning, analysis, reconciling sources) and slower and more expensive per answer. Most current Claude and OpenAI models reason, and you set **how much** with an effort level (Claude: `low` to `max`; OpenAI: model-dependent values such as `low`, `medium`, `high`, `xhigh`). The default differs by model, so set it explicitly. Give a reasoning model the goal and the criteria rather than step-by-step instructions; it plans the steps itself.

| Step kind | Effort | Why |
|---|---|---|
| Classify, tag, extract, reformat | `low` (or a small, fast model) | High volume, easy to check |
| Draft for a known audience from given facts | `medium` | Quality matters, the reasoning is short |
| Plan, analyze trends, reconcile conflicting sources | `high` | Multi-step reasoning pays off |
| Long agentic runs, the hardest problems | `xhigh` / `max` | Only when your tests show a gain; slow and costly |

**Balance quality, speed and cost in that order.** Set the quality bar per step from its "done when". Try the cheapest, fastest option on 10–20 real examples, and step up only if it misses the bar. Count **human minutes** too: a cheaper setting that doubles review edits often costs more overall (the practice notebook shows `low` passing the bar on tagging yet losing to `medium` once fix-up time is counted).

```python
import anthropic, openai

def claude_step(prompt: str, effort: str) -> str:
    r = anthropic.Anthropic().messages.create(
        model="claude-sonnet-5-5", max_tokens=4096,
        output_config={"effort": effort},
        messages=[{"role": "user", "content": prompt}])
    return next(b.text for b in r.content if b.type == "text")

def openai_step(prompt: str, effort: str) -> str:
    r = openai.OpenAI().responses.create(
        model="gpt-6-luna", reasoning={"effort": effort},
        input=prompt)
    return r.output_text

# Fernhill: measure tagging at "low" vs "medium"; trend analysis -> "high"
```

Model tiers and every effort value are in [Claude 06 §6.8](../../anthropic-claude/06-prompt-engineering/README.md#68-reasoning-sampling-and-grounding-on-current-models-expanded-beyond-the-guide) and [OpenAI 01 §1.7](../../openai-codex/01-responses-api-fundamentals/README.md#17-model-selection-and-reasoning-effort).

### 2.7 From asking to assigning: the agent brief

**Asking** is one turn: you prompt, read and steer. **Assigning** is handing a multi-step job to an agent that plans, uses tools and files, and works while you do something else. Assigning saves more time, but you are not there to correct each step, so the instructions must carry what you would have said along the way. Write a **brief**, as you would for a new colleague:

| Field | Fernhill example |
|---|---|
| **Goal** (outcome, not activity) | A draft digest the product team can act on in 5 minutes |
| **Context and sources** | The redacted export, last week's digest, the theme list |
| **Deliverable** | Markdown, following the template; counts in a table |
| **Done when** | Every number traces to the data; 2 verbatim quotes per top theme |
| **Allowed** | Read the shared folder; write to `/drafts` only |
| **Needs approval** | Anything sent or shared outside the folder |
| **Never** | Contact customers; open unredacted data |
| **Stop and ask when** | A theme is not on the list; data looks incomplete |
| **Budget** | 15 minutes or 30 steps, then report what is done |

Vague verbs ("look into", "improve", "handle") with no "done when" are the most common brief failure: the agent cannot tell when it has finished. Boundaries belong in the **tool's settings** too (which folders and connectors it can reach, which actions ask for approval), because an instruction in the brief is guidance, not enforcement.

```python
REQUIRED = ["goal", "context", "deliverable", "done_when",
            "allowed", "needs_approval", "stop_and_ask"]

def brief_gaps(brief: dict) -> list[str]:
    gaps = [f for f in REQUIRED if not brief.get(f)]
    vague = ("look into", "improve", "handle", "deal with")
    if any(v in brief.get("goal", "").lower() for v in vague):
        gaps.append("goal is an activity, not an outcome")
    return gaps
```

### 2.8 Context and the first draft

An agent is only as good as the context it starts with. Give it the **sources** (attach or connect them, do not paraphrase them), an **example of a good past output**, the **glossary and lists** it must use (the theme list), and **who the audience is**. Put context that every run needs into the **standing setup** (a Claude Project or ChatGPT Project with instructions and files), not into each prompt.

Then **draft small**. Run the brief on one week of data, review the first draft against the brief, and fix the brief before you scale or schedule it. A first draft that misses is information: it shows which instruction or source was missing. Do not judge a workflow by one lucky run; try three or four different weeks.

### 2.9 Improve, reuse and share the workflow

Keep a short **run log**: for each run, what the reviewer corrected and why. Sort each correction into one of four kinds and act when a kind repeats (say, in 3 of the last 5 runs):

| Correction kind | Example | Promote it into |
|---|---|---|
| **Context** | "Trail-X is a product, not a theme" | Project instructions or knowledge (the glossary) |
| **Format** | Counts written in prose again | The template, plus one good example |
| **Verification** | A quote was paraphrased, not verbatim | A checklist item, or a code check (search the source) |
| **One-off** | A holiday week had no survey | Nothing; note it |

This is how a workflow gets cheaper over time: fixes stop living in the reviewer's head and move into the setup, so every later run benefits. Track a few numbers per run: **minutes of human time**, **edits at review**, **errors that escaped** to the product team, and **cycle time**.

```python
from collections import Counter

def promotions(log: list[dict], threshold: int = 3) -> dict[str, str]:
    """log: one dict per run, e.g. {"run": 7, "kinds": ["format"]}."""
    seen = Counter(k for run in log for k in set(run["kinds"]))
    target = {"context": "project instructions/knowledge",
              "format": "template + example",
              "verification": "checklist item or code check"}
    return {k: target[k] for k, n in seen.items()
            if k in target and n >= threshold}
```

**Share it** as a one-page **workflow card**: purpose, trigger, the step table with decisions, the brief, the checkpoints and who owns them, known limits, and the metrics. A teammate should be able to run it, and a manager should be able to see what AI does and what people still decide. That is what makes a redesign stick: people know their new role (reviewer, decision owner) instead of fearing the old one is gone.

### 2.10 Responsible use inside the workflow

Responsible use is designed into the steps, not added at the end:

- **Data:** decide per step what data the AI may see. Remove personal data before the AI step (Fernhill's step 2), and use only tools your organization has approved for that data class.
- **Accountability:** every output has a named human owner. "The AI wrote it" is not an owner.
- **Decisions about people:** steps that affect someone's job, money, access or rights stay human or shared, with the criteria written down; check them for bias (swap names or groups and compare).
- **Transparency:** say where AI was used when your audience would expect to know.
- **Limits:** write the known limits on the workflow card (for example: "tags are 90% accurate on a 50-row sample; rare themes are often missed").

Governance, policy and regulated data are taught in the planned chapters 11 (responsible AI and safety controls) and 12 (compliance and governance) of this track.

### 2.11 Claude and OpenAI side by side

The design (steps, decisions, checkpoints, brief, run log) is vendor-neutral. What changes is where each piece lives:

| Need | Claude | OpenAI | Taught in |
|---|---|---|---|
| Standing context for a team workflow | Projects (instructions + knowledge) | ChatGPT Projects | Planned Claude 22 / OpenAI 22 |
| Hand a multi-step job to an agent in the app | Claude working on your files and apps (Cowork) | ChatGPT agent mode, workspace agents | Planned Claude 22 / OpenAI 22 |
| Build the workflow in code | Messages API chain, Claude Agent SDK | Responses API, OpenAI Agents SDK | [Claude 08](../../anthropic-claude/08-task-decomposition/README.md), [OpenAI 08](../../openai-codex/08-task-decomposition-and-orchestration/README.md) |
| Reasoning depth per step | `output_config={"effort": ...}` | `reasoning={"effort": ...}` | 2.6 |
| Approval before risky actions | Agent SDK permission modes, `can_use_tool`, hooks | Agents SDK `needs_approval` | [Claude 09 §9.5](../../anthropic-claude/09-escalation-human-in-the-loop/README.md#95-human-approval-checkpoints-on-each-claude-surface-expanded-beyond-the-guide), [OpenAI 09 §9.4](../../openai-codex/09-escalation-human-in-the-loop/README.md#94-approval-gated-tools-in-the-agents-sdk) |

Keep the workflow card free of vendor features so you can move it between tools; keep the vendor-specific setup (project instructions, approval settings) in a short appendix.

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Map the Fernhill workflow, run the delegation rules and checkpoint placement, compare effort levels on a scripted model, lint an agent brief, then run the redesigned workflow end to end through one small interface (offline Claude and OpenAI stand-ins, optional live cells) and promote recurring corrections |
| [`02_homework.ipynb`](02_homework.ipynb) | 8-question scenario quiz, 5 auto-checked exercises (delegation, checkpoints, brief, cost balance, promotions), an architecture scenario with a rubric and a scorecard (pass mark 72%) |

## Cheat-sheet

| Situation | Do | Not |
|---|---|---|
| Choosing where to start | A recurring task with a clear, checkable output | A one-off or a task nobody can judge |
| Fixed rules give the right answer | Code | An AI step "to be safe" |
| Decision someone must own | Human, AI prepares options | AI decides, human "glances" |
| Checking takes as long as doing | Keep it human | Delegate and re-do it at review |
| Costly or hard-to-undo output | Shared: AI drafts, human approves | AI with no checkpoint |
| Before sending, paying, publishing | A checkpoint with a checklist | Trusting the brief's "don't" |
| Picking model and effort | Cheapest setting that meets the bar on real examples | The biggest model at `max` |
| Assigning to an agent | Brief: goal, context, deliverable, done-when, boundaries, stop rules | "Look into the feedback" |
| Same correction every week | Promote it into context, template or a check | Fix it by hand forever |

## Common mistakes

- **Automating the old process.** Adding AI to every step as it is, instead of asking which steps should change.
- **Two-way thinking.** Treating each step as "AI or human" and missing code and shared.
- **Ignoring verification cost.** Delegating work whose check takes as long as doing it.
- **Rubber-stamp review.** Reading for tone without the sources, so factual errors pass.
- **A checkpoint after every step.** Review fatigue, then nobody reviews properly.
- **Briefs without "done when" or boundaries.** The agent stops early, wanders, or touches what it should not.
- **Fixes that never persist.** The reviewer corrects the same thing every run.

## Self-check

**1. (Workflow design)** A finance team wants AI in its monthly expense-report check: export reports, flag policy breaches, total the flagged amounts, decide which employees get a follow-up, email them. Which split is best?

- A) AI does every step, and the manager reads the final emails
- B) Code exports and totals; AI flags likely breaches with the rule it matched; a human reviews the flags and decides follow-ups; code sends the emails after that approval
- C) AI flags and totals, and a human does the rest
- D) Keep everything human, because money is involved

<details><summary>Answer</summary>

**B.** Exports, totals and sending follow fixed rules, so they are code. Flagging is a good AI step if each flag carries the rule it matched, which makes it fast to check. Deciding about employees is an accountable decision, so it stays human, and the emails go out only after that checkpoint. A puts decisions about people and an external action behind a glance at the end. C puts arithmetic in an AI step. D gives up a safe, checkable gain.
</details>

**2. (Delegation)** A legal team wants AI to summarize 30-page supplier contracts. Partners say they would still have to read every clause to trust a summary. What should you conclude first?

- A) Delegate it anyway; the AI is fast
- B) Use a stronger model at `max` effort so partners trust it
- C) As designed, verification costs as much as doing the work, so delegation saves nothing; change the design (for example, AI extracts specific clauses with page references the partner can check quickly) or keep the step human
- D) Ask partners to stop reading the contracts

<details><summary>Answer</summary>

**C.** Delegation pays only when checking is cheaper than doing. Clause extraction with page references makes each item fast to verify. A ignores the review cost. B does not change how the output must be checked. D removes accountability.
</details>

**3. (Assigning to an agent)** A manager hands an agent: "Look into our onboarding feedback and improve the welcome email." It returns after two minutes with a rewritten email based on one survey file and has already replaced the live template. What is the root cause?

- A) The model is too small
- B) The brief had no outcome or done-when, no list of sources, and no boundary saying that changing the live template needs approval
- C) The agent should have been given more time
- D) Onboarding feedback is not suitable for AI

<details><summary>Answer</summary>

**B.** "Look into" and "improve" are activities, so the agent cannot tell when it is done or which sources count, and nothing required approval before an external change. Approval should also be set in the tool's permissions. A and C do not address the missing instructions. D is wrong; the task is a good fit once briefed.
</details>

**4. (Improving the workflow)** After eight weekly runs, the digest reviewer still fixes the same things: product names tagged as themes (6 runs), counts written in prose (5 runs), and one week with a broken export (1 run). What is the best next step?

- A) Keep fixing them at review; that is what review is for
- B) Add the product list to the project knowledge, update the template with a counts table and one example, and leave the broken export as a logged one-off
- C) Switch to a stronger model
- D) Add a second reviewer

<details><summary>Answer</summary>

**B.** Repeated corrections should be promoted into the standing setup: missing context into knowledge, format into the template. A one-off needs no change. A keeps paying the cost every week. C does not supply the missing product list. D doubles the human cost without fixing the cause.
</details>

## Official documentation

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (Anthropic Engineering): workflows vs agents, start simple
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (OpenAI): when to use an agent, instructions, guardrails, human intervention
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) (Claude docs): effort levels and when to use each
- [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning) (OpenAI docs): `reasoning.effort` and how to prompt reasoning models
- [What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects) (Claude Help Center): standing instructions and knowledge for a workflow
- [AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) (Anthropic Academy): Delegation and project planning
- [Workflow Integration & Solution Design](https://anthropic-partners.skilljar.com/path/claude-associate/workflow-integration-solution-design) (Anthropic Partner Academy, CCAO-F prep module)
- [OpenAI Academy](https://academy.openai.com/): Foundations pathway (Applied AI Foundations, Agents and Workflows)

[↑ Applied AI Architect track](../README.md) | [← Chapter 01 — AI fluency, prompting and output validation](../01-ai-fluency-prompting-and-output-validation/README.md) | [Chapter 03 — Discovery, use-case scoping and value case →](../03-discovery-and-use-case-scoping/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
