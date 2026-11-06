# Chapter 01 — AI fluency, prompting and output validation

> **Serves:** CCAO-F D1 Prompting and Task Execution (**14%**), D2 Output Evaluation and Validation (**21%**), D7 Troubleshooting and Optimization (**10%**) · Anthropic Academy AI Fluency courses and AI Capabilities and Limitations · OpenAI Academy AI Foundations · groundwork for the PROMPT and SAFE role areas
> **Est. time:** 4–5 hours (reading + 2 notebooks) · **Status:** [ ] not started

Every AI project starts with a person asking a model for something and deciding whether the answer is good enough. This chapter teaches that skill in a vendor-neutral way: how to decide what to hand to AI, how to describe it, how to judge the result, and how to take responsibility for what you ship. It works the same in Claude and ChatGPT. An architect needs it twice: to do their own work well, and to teach a customer's team to do the same.

## What you'll learn

- Use the **4D framework** (Delegation, Description, Discernment, Diligence) and the three modes of working with AI.
- Explain unexpected output with **four model properties** (next-token prediction, knowledge, working memory, steerability) and pick a targeted fix.
- Write prompts for business tasks with a **repeatable component structure**, adapted to analysis, research, drafting and brainstorming.
- Check output for **accuracy, completeness, consistency and bias**, and decide when a human must verify it.
- **Diagnose** a weak prompt to its root cause and turn recurring corrections into fixes that persist.

## Prerequisites

[00-prerequisites](../../00-prerequisites/README.md) (Python, `.env`; read [2.6 Hallucination](../../00-prerequisites/README.md#26-hallucination) and [2.9 Next-token generation](../../00-prerequisites/README.md#29-next-token-generation)). No API knowledge is needed: the API-level versions of these ideas are in [Claude 06](../../anthropic-claude/06-prompt-engineering/README.md) and [OpenAI 06](../../openai-codex/06-prompt-engineering-and-evals/README.md).

## Concepts

Snippets are plain Python and run offline. The notebooks wrap them around a small fake model, so you can practise the loop without an API key.

### 1.1 AI fluency and the 4D framework

**AI fluency** means working with AI in a way that is effective, efficient, ethical and safe. The AI Fluency framework (Rick Dakan and Joseph Feller, with Anthropic) breaks it into four competencies:

| Competency | The question it answers | Sub-skills |
|---|---|---|
| **Delegation** | Should AI do this, which tool, and which part? | Goal and task awareness, platform awareness, task delegation |
| **Description** | How do I say what I want? | Describe the product (the output), the process (how to work together) and the performance (how the AI should behave) |
| **Discernment** | Is the output, and the collaboration, any good? | Judge the product, the process and the performance |
| **Diligence** | Am I responsible about how I use it? | Creation diligence (what you share and how), transparency diligence (disclosing AI use), deployment diligence (verifying and owning what you release) |

The framework also names three **modes** of working with AI:

| Mode | What happens | Example | What it needs most |
|---|---|---|---|
| **Automation** | AI does a defined task from your instructions | Summarize these notes into five bullets | A precise description and a quality check |
| **Augmentation** | You and AI think and create together, turn by turn | Shape a strategy memo through several drafts | Process description and ongoing discernment |
| **Agency** | You set up AI to act later, for you or for others | A Project or custom GPT that answers staff questions | Performance description, testing, and deployment diligence |

The modes are not a ranking. Most failures come from a **mismatch**: treating an open problem as one automation request, or chatting turn by turn through a task a template could do.

Two competencies form loops. **Description and Discernment** run together on every task: describe, read the result, refine (1.10). **Delegation and Diligence** run together on every decision about responsibility: what to hand over, and what you must still check and own (1.11).

### 1.2 How LLMs behave: four properties behind every surprise

A large language model is first **pretrained** to predict the next token on a very large amount of text, then **fine-tuned** (with human feedback and written principles) into an assistant with a stable character. Four properties explain most of its surprising behavior:

| Property | What it means | Typical surprise | Targeted fix |
|---|---|---|---|
| **Next-token prediction** | It writes the most plausible continuation, not a looked-up fact | Fluent but wrong detail; an invented citation; a different answer each run | Give sources, ask for quotes, allow "not stated", verify specifics |
| **Knowledge** | It knows what was frequent, recent and consistent in its training data, up to a cutoff | Outdated facts; weak answers on niche, internal or contested topics | Provide the source, turn on search or research, check dates |
| **Working memory** | It sees only the current context window; attention over a long context is uneven; a new chat starts empty | Misses a detail on page 40; forgets an early instruction; does not know last week's chat | Put key material first and labelled, split the work, use Projects or memory |
| **Steerability** | Its behavior follows instructions, examples and framing, sometimes too closely | Copies an example's length; agrees with a leading question; drifts in tone | Neutral framing, explicit criteria, several varied examples, ask for counterarguments |

**When properties collide** the failure looks like one problem but has several causes. "Summarize the 90-page vendor contract and confirm the liability cap is fine" combines a long input (working memory), a leading question (steerability) and specific numbers (next-token prediction). The fix combines levers: ask a neutral question, point at the clause, and check the quoted figure. Naming the property is the point: "the model is bad" leads to random retries; "this is a knowledge gap" leads to "attach the source".

### 1.3 Delegation: choosing the mode of collaboration

Before writing a prompt, decide three things: **what the goal is** (and what a good result looks like), **which platform** fits (chat, a Project, research mode, a coding agent, an API workflow), and **which parts** AI does, which you do, and which you do together.

| Task | Mode | AI does | You keep |
|---|---|---|---|
| Weekly status update from meeting notes | Automation | First draft in a fixed format | Check figures, dates and owners; send it |
| A pricing strategy for a new market | Augmentation | Options, counterarguments, a draft | The goal, the judgment, the final call |
| A help bot for the HR policy | Agency | Answers within set instructions and sources | Instructions, test cases, monitoring, escalation path |

Good candidates are tasks where a draft is cheap to check and costly to write. Poor ones are tasks where checking costs as much as doing, or where a mistake cannot be undone. The step-by-step delegate-or-keep worksheet for whole workflows is in [Chapter 02](../02-workflow-design-and-delegation/README.md).

### 1.4 Description: a repeatable prompt structure

A good prompt reads like a brief to a capable new colleague who knows nothing about your situation. Use the same components every time, in this order:

| Component | What to write | Example |
|---|---|---|
| **Task** | One sentence, verb first | "Write the weekly status update for Project Atlas." |
| **Context** | Who it is for and why it matters | "For the steering committee; they decide on budget." |
| **Inputs** | The material to use, clearly marked | The meeting notes, pasted inside `<notes>` tags |
| **Output** | Format, length, tone | "Five bullets, under 20 words each, plain English." |
| **Constraints** | Scope, must and must-not | "Use only the notes. No new numbers." |
| **Examples** | A sample of good output, when format matters | Last week's approved update |
| **When unsure** | What to do with gaps | "Write 'not in the notes' instead of guessing." |

This is **product description**. Add **process description** when you want a way of working ("ask me three questions before you start"), and **performance description** when you set up behavior for later (a Project's instructions). A short brief that covers every component beats a long one that skips the audience. The check below is what the notebook runs on every brief:

```python
COMPONENTS = ("task", "context", "inputs", "output",
              "constraints", "examples", "when_unsure")
REQUIRED = ("task", "context", "inputs", "output", "when_unsure")

def gaps(brief: dict[str, str]) -> list[str]:
    return [c for c in REQUIRED if not brief.get(c, "").strip()]

def render(brief: dict[str, str]) -> str:
    return "\n\n".join(f"<{c}>\n{brief[c]}\n</{c}>"
                       for c in COMPONENTS if brief.get(c, "").strip())
```

The API-level version (XML tags, system vs user, output constraints) is [Claude 06 §6.10](../../anthropic-claude/06-prompt-engineering/README.md#610-the-prompt-structure-toolkit-expanded-beyond-the-guide) and [OpenAI 06 §6.13](../../openai-codex/06-prompt-engineering-and-evals/README.md#613-the-prompt-structure-toolkit).

### 1.5 Adding useful context

Context is what the model cannot guess: your audience, your sources, your constraints and your past decisions. Useful context is **specific and relevant**: the actual policy text rather than "our policy", one approved example rather than "our usual style", the definition of an internal term. Leave out what does not change the answer; extra material spends working memory (1.2) and dilutes attention.

Match where context lives to how long it should last:

| How long it applies | Put it in | Claude | ChatGPT |
|---|---|---|---|
| This request only | The message itself | Chat message, attached files | Chat message, attached files |
| Every chat on one piece of work | A project | Project instructions and project knowledge | Project instructions and files |
| Everything you do | Personal settings | Profile preferences, styles, memory | Custom instructions, memory |
| Other people's chats | A configured assistant | A shared Project | A custom GPT or a shared project |

Feature names change; check each vendor's help pages. Configuring Projects in depth is planned for Claude chapter 22. Before you paste anything, apply creation diligence (1.11): is this data allowed in this tool?

### 1.6 Matching the prompt to the task type

The same structure adapts to the kind of work. Each type has its own most important component and its own check:

| Task type | Give it | Ask for | Check it by |
|---|---|---|---|
| **Analysis** | The data or document first; explicit criteria | Findings tied to the criteria, with quotes or figures | Recompute numbers; trace each finding to the input |
| **Research** | The question, the scope, the source rules | Claims with sources, gaps stated | Open the sources; check dates; cross-check key claims |
| **Drafting** | Audience, purpose, tone, length, facts to use | A draft in the target format | Read it as the audience would; check every fact |
| **Brainstorming** | The goal and the constraints | Many varied options, unfiltered | Score them against criteria in a separate step |
| **Summarizing** | The source and what the reader needs | Key points in a set length | Every point is in the source; nothing important missing |
| **Planning** | The goal, the deadline, the resources | Steps with owners and dates | Dependencies and dates are realistic |

Two habits help across types. **Split mixed tasks** ("analyze these survey results, then draft an email to the team" is two requests, see [Claude 08 §8.11](../../anthropic-claude/08-task-decomposition/README.md#811-decomposition-for-everyday-claude-use-associate-lens)). **Separate generating from judging**: brainstorm first, then evaluate the list against your criteria. Asking for "the single best name" in one go tends to return one safe, average option.

### 1.7 Discernment: accuracy, completeness, consistency and bias

Read every output against four questions, in this order:

| Check | Question | Common failure |
|---|---|---|
| **Accuracy** | Is each claim true and supported by the source? | Invented figures, citations or quotes; a real source that says something else |
| **Completeness** | Is everything required there? | A dropped decision, owner or caveat; only the easy half of the question |
| **Consistency** | Does it agree with itself and the source? | A total that does not match its parts; a date that contradicts the notes |
| **Bias** | Would it change if only a name, gender or group changed? | Different adjectives for different people; one-sided framing |

A **hallucination** is fluent content that is not grounded in the input or in fact. It is most likely where next-token prediction meets weak knowledge: specific numbers, dates, names, citations, and anything recent or internal. **Sycophancy**, agreeing with a wrong premise because of how you asked, is the steerability version.

Fact-checking techniques that work: **trace each claim** to a quote in the source; **recompute** totals and percentages yourself; **check dates and versions**; **cross-check** key facts against a second source; **regenerate and compare** (claims that change between runs are weak); and run a **swap test** for bias (same prompt, one attribute changed, compare the outputs). Do not ask the model "are you sure?" and accept a confident yes: its self-rating is not evidence. Simple checks can run in code:

```python
import re

NUM = re.compile(r"\d[\d,.]*\d|\d")

def numbers(text: str) -> set[str]:
    return {n.replace(",", "") for n in NUM.findall(text)}

def check_output(answer: str, source: str, required: list[str]) -> dict:
    return {
        "numbers_not_in_source": sorted(numbers(answer) - numbers(source)),
        "quotes_not_in_source": [q for q in re.findall(r'"([^"]+)"', answer)
                                 if q.lower() not in source.lower()],
        "missing_points": [r for r in required
                           if r.lower() not in answer.lower()],
    }
```

A clean result does not prove the output is right. It only tells you where to look first. Citations and claim-to-source mapping at scale are in [Claude 12](../../anthropic-claude/12-provenance/README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide).

### 1.8 When a human must verify

Every output gets a quick read. Some need more. Decide the level from the task, not from how confident the output sounds:

| Signal | Raises the review level |
|---|---|
| **Stakes** | Money, health, legal, safety or someone's job depends on it |
| **Audience** | It leaves the team: customers, regulators, the public |
| **Reversibility** | It cannot easily be taken back once sent or acted on |
| **Verifiability** | You cannot check it yourself from a source you trust |
| **Novelty** | A new kind of task, a new tool, or a topic past the model's knowledge |

```python
def review_level(stakes: str, external: bool, reversible: bool,
                 checkable: bool) -> str:
    """stakes: 'low' | 'medium' | 'high'."""
    if stakes == "high" or not checkable:
        return "expert_signoff"     # a qualified person signs it off
    if external or not reversible or stakes == "medium":
        return "fact_check"         # check every claim against sources
    return "self_check"             # a careful read by the author
```

The architect's version of this decision, escalation inside an automated system, is [Claude 09 §9.1](../../anthropic-claude/09-escalation-human-in-the-loop/README.md#91-when-to-escalate) and [OpenAI 09 §9.1](../../openai-codex/09-escalation-human-in-the-loop/README.md#91-when-to-escalate).

### 1.9 Editing, comparing and formatting for the audience

An accurate output can still be wrong **for its reader**. Adapt it on four dials: **length** (a director reads five bullets, an analyst reads the appendix), **vocabulary** (remove internal jargon for outsiders, keep the precise terms for experts), **structure** (lead with the decision or the ask), and **tone** (formal for a regulator, warm for a customer apology). Ask the model to rewrite for a named reader ("rewrite for a customer who is not technical, under 120 words"), then edit the result yourself: you know the reader, it does not.

When you have two or more versions, **compare them against the same written criteria**, not by which one feels better. Write the rubric before you read the drafts:

```python
def score(draft: str, must_include: list[str], max_words: int,
          banned: list[str]) -> int:
    text = draft.lower()
    points = sum(term.lower() in text for term in must_include)
    points += len(draft.split()) <= max_words
    points -= sum(word.lower() in text for word in banned)
    return points

def best(drafts: dict[str, str], **rubric) -> str:
    return max(drafts, key=lambda k: score(drafts[k], **rubric))
```

**Choose the format for how it will be used.** Inline text for a quick answer you read once; a document (Claude artifacts, ChatGPT canvas) for something you will edit and share; a table for comparisons; structured data (CSV, JSON) for anything another tool or person will process. Rendering rules per content type are in [Claude 12 §12.4](../../anthropic-claude/12-provenance/README.md#124-render-by-content-type).

### 1.10 The Description-Discernment loop: diagnosing weak output

Discernment feeds Description: read the output, name what is wrong, trace it to a cause, change one thing, try again. Retrying the same prompt or adding "make it better" skips the diagnosis. Common root causes and their fixes:

| Symptom | Root cause | Fix |
|---|---|---|
| Generic, could be about any company | **Under-specification**: no context or audience | Add context, audience and purpose (1.4) |
| Invented figures or policies | **Missing source**; knowledge gap | Attach the source; "use only the notes"; allow "not stated" |
| Wrong format or length each time | **Output not described**, or one example copied too closely | State the format; give 3–5 varied examples |
| Good parts, but half the request ignored | **Too much in one request** | Split into steps; check each step (1.6) |
| Ignores a rule in a long prompt | **Buried or conflicting instructions** | Put rules in one labelled block; remove the conflict |
| Confidently outdated | **Knowledge cutoff** | Provide current sources or turn on search |
| Misses detail late in a long file | **Working memory** | Point to the section; split the document |
| Still wrong after the prompt is clear | **Wrong tool or model** for the job | A stronger model, research mode, or a different approach |

**Adjust to what you see.** If the first output is close, give targeted feedback ("keep the structure; bullets 2 and 4 need the figures from the notes"). If it is far off, rewrite the brief rather than arguing in a long chat; a fresh conversation with a better brief often beats ten corrections. **Make recurring fixes persist.** If you type the same correction three times, it belongs in the template, the Project instructions or your custom instructions:

```python
from collections import Counter

def promote(corrections: list[str], threshold: int = 3) -> list[str]:
    """Corrections you keep typing become standing instructions."""
    counts = Counter(c.strip().lower() for c in corrections)
    return [c for c, n in counts.most_common() if n >= threshold]
```

Making a whole workflow efficient (shared context, formats and checks promoted into it) is [Chapter 02](../02-workflow-design-and-delegation/README.md); measuring prompt changes with evals is [Claude 06 §6.9](../../anthropic-claude/06-prompt-engineering/README.md#69-matching-the-strategy-to-the-task-and-iterating-expanded-beyond-the-guide) and Chapter 08 (planned).

### 1.11 Diligence: own it, disclose it, deploy it carefully

Diligence means you stay responsible for AI-assisted work.

- **Creation diligence.** Choose tools your organization allows. Do not paste confidential, personal or regulated data into a tool that is not approved for it. Respect copyright and other people's work.
- **Transparency diligence.** Say when AI shaped the work where your audience, employer, school or client expects to know. Follow their rules on disclosure.
- **Deployment diligence.** Before you share, verify (1.7, 1.8). After you share, own the result: if it is wrong, it is your mistake, not the model's. For anything you set up for others (agency mode), keep testing and watching it after launch.

The short habit: **right tool, right data, checked output, honest credit**. The system-level controls (guardrails, data handling, policy, audit) are Chapters 10–12 (planned).

### 1.12 Claude and ChatGPT side by side, and in your role

The skills in this chapter do not depend on the vendor. The product names differ:

| Need | Claude | ChatGPT |
|---|---|---|
| A shared workspace with sources and instructions | Projects | Projects |
| A document you edit with the model | Artifacts | Canvas |
| Multi-source research with citations | Research | Deep research |
| Standing preferences | Profile preferences, styles, memory | Custom instructions, memory |
| An assistant others use | Shared Projects | Custom GPTs |

The same brief also works through both APIs. This is the one small interface the notebook's mini-project uses (live cells only):

```python
import anthropic
import openai

def ask_claude(system: str, prompt: str) -> str:
    msg = anthropic.Anthropic().messages.create(
        model="claude-sonnet-5-5", max_tokens=2048, system=system,
        messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in msg.content if b.type == "text")

def ask_openai(system: str, prompt: str) -> str:
    resp = openai.OpenAI().responses.create(
        model="gpt-6-luna", instructions=system, input=prompt)
    return resp.output_text
```

**The same loop in different roles.** The Academy courses apply the 4Ds to particular jobs. What changes is the source of truth you check against:

| Role | Typical task | Check it against |
|---|---|---|
| Educator | Session plan, activity, assessment, messages to families | Learning objectives, your own materials, school policy |
| Student | Study plan, group-project plan, CV and interview prep | Your course materials, the assignment rules, your institution's AI policy |
| Small business, nonprofit | Customer replies, grant drafts, a repeatable workflow, a short AI use policy | Your facts, prices and mission; the policy you wrote |
| Builder | Specs, code, tests | Acceptance tests written before the work |
| Creative work | Ideas, drafts, variations | Your own voice and intent; rights to the material |

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Run every idea from 1.1–1.12 offline against a small fake model: lint a brief, see the four properties fail and get fixed, check outputs for unsupported numbers and missing points, run a swap test for bias, pick a review level, score drafts with a rubric, and promote recurring corrections. Mini-project: improve a recurring task (a weekly status update) through the Description-Discernment loop, through one interface that also runs on Claude and OpenAI (optional live cell) |
| [`02_homework.ipynb`](02_homework.ipynb) | 7-question scenario quiz, 5 auto-checked exercises, an architecture scenario with a rubric, and a scorecard (pass mark 72%) |

## Cheat-sheet

| Situation | Do | Not |
|---|---|---|
| Output is generic | Add audience, purpose and context | Retry the same prompt |
| Output invents figures | Attach the source, "use only", allow "not stated" | Ask "are you sure?" |
| Format is wrong every time | State the format; 3–5 varied examples | One example it will copy |
| Need ideas | Generate many, then score against criteria | "Give me the best one" |
| Two drafts to choose from | Same written rubric for both | Pick the one that sounds better |
| Same correction three times | Put it in the template or Project instructions | Keep typing it |
| Customer-facing, hard to undo | Fact-check every claim; expert sign-off if high stakes | Trust a confident tone |

## Common mistakes

- **Prompting before deciding.** No clear goal, no idea of what good looks like, wrong mode for the task.
- **Briefs without an audience.** The model writes for nobody in particular.
- **Trusting fluency.** Treating confident, well-written text as checked text.
- **Retrying instead of diagnosing.** Regenerating until something looks fine, then never fixing the cause.
- **One-off fixes.** Correcting the same thing in every chat instead of making it persist.
- **"The AI did it."** Shipping without owning the result or saying that AI was used.

## Self-check

**1. (Operations reporting)** A team lead asks a chat assistant to summarize the quarter's sales notes for the board. The summary says revenue grew 12%; the notes say 9%. When asked "are you sure?", the assistant says it is confident. What should the team lead do?

- A) Accept the figure, since the assistant confirmed it
- B) Regenerate until two runs agree on the same figure
- C) Check each figure against the notes, correct it, and change the prompt to use only figures from the notes and to write "not in the notes" when a figure is missing
- D) Switch to a larger model and send the same prompt

<details><summary>Answer</summary>

**C.** The figure is a hallucination at a known weak spot (specific numbers). Checking against the source catches it, and the grounding instruction fixes the cause. A trusts a self-rating, which is not evidence. B can make two runs agree on the same wrong number. D may still invent figures when the prompt does not tie them to the source.
</details>

**2. (Marketing team)** A marketing team uses Claude for product announcements. Every draft comes back long and full of internal jargon, and each writer corrects "shorter, plain words, for customers" by hand in every chat. Quality is good after the corrections. What is the best fix?

- A) Switch to a more capable model
- B) Put the audience, length and plain-language rule into the team's Project instructions (with one approved example), so every chat starts with them
- C) Add "make it better" to the end of each request
- D) Ask the model to rate its drafts for readability before it answers

<details><summary>Answer</summary>

**B.** The root cause is under-specification (no audience or length), and it recurs, so the fix must persist where every chat sees it. A treats a description problem as a capability problem. C gives no information. D relies on self-assessment and still leaves the audience undefined.
</details>

**3. (Legal operations)** Which output most needs expert sign-off before it is used?

- A) Ten brainstormed titles for an internal training session
- B) A summary of a supplier's contract terms that will be sent to the customer as the firm's position on its liability
- C) A first draft of a team lunch invitation
- D) A list of questions to ask in a kickoff meeting

<details><summary>Answer</summary>

**B.** It is high-stakes (legal liability), external and hard to take back. A, C and D are internal, low-stakes and easy to fix, so a careful read by the author is enough.
</details>

**4. (Product team)** A product manager wants a name for a new feature and asks, "What is the single best name for this feature?" The answers are bland and similar each time. What should she change?

- A) Ask the same question again with "be creative"
- B) Ask for 25 varied names with the constraints (short, no existing trademarks in the list she provides, works in English and Spanish), then in a second step score them against her criteria and shortlist five
- C) Ask for a detailed explanation of why each name is the best
- D) Paste a competitor's feature name as the example to imitate

<details><summary>Answer</summary>

**B.** Brainstorming works best when generating and judging are separate steps: many varied options first, then scoring against criteria. A adds no constraints or criteria. C keeps the single-answer framing. D steers the model to copy the example (steerability), which also creates a trademark risk.
</details>

## Official documentation

- [AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) (Anthropic Academy): the 4D framework and the three modes
- [AI Capabilities and Limitations](https://anthropic.skilljar.com/ai-capabilities-and-limitations) (Anthropic Academy): the four model properties
- [The AI Fluency Framework](https://aifluencyframework.org/) (Dakan and Feller): the framework and its licence
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (Claude docs): clear instructions, context, examples
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) (Claude docs): grounding, quotes, "I don't know"
- [What are Projects?](https://support.claude.com/en/articles/9517075-what-are-projects) (Claude Help Center): persistent instructions and knowledge
- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) (OpenAI docs): instructions, examples, context
- [OpenAI Academy](https://academy.openai.com/): AI Foundations and the role courses for educators and students

[↑ Applied AI Architect track](../README.md) | [Chapter 02 — Workflow design and delegation →](../02-workflow-design-and-delegation/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
