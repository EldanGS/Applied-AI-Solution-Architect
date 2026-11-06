# Chapter 02 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix. IDs come from the official CCAO-F guide checklist, the Anthropic Academy and OpenAI Academy course pages, and the role competency matrix. **Primary** means this chapter is where the item is taught in depth; **Supporting** means it is applied or reinforced here and taught more fully elsewhere.

| Requirement ID | What it asks (short) | Where in this chapter | Depth |
|---|---|---|---|
| `CCAO-F/D4/4.1/S1` | Apply Claude to analyze requirements and use cases | [2.3](../README.md#23-use-ai-to-analyze-plan-and-design-the-workflow), [2.1](../README.md#21-from-prompts-to-workflows) (choosing candidates) | Primary |
| `CCAO-F/D4/4.2/S1` | Use Claude for research, planning and process optimization | [2.3](../README.md#23-use-ai-to-analyze-plan-and-design-the-workflow), [2.9](../README.md#29-improve-reuse-and-share-the-workflow) (research is taught in [Claude 12 §12.9](../../../anthropic-claude/12-provenance/README.md#129-web-search-and-web-fetch-citations-expanded-beyond-the-guide)) | Supporting |
| `CCAO-F/D4/4.2/K2` | Planning | [2.3](../README.md#23-use-ai-to-analyze-plan-and-design-the-workflow) (interview, structured plan, assumptions and open questions) | Primary |
| `CCAO-F/D4/4.2/K3` | Process optimization | [2.1](../README.md#21-from-prompts-to-workflows) (the bottleneck moves), [2.9](../README.md#29-improve-reuse-and-share-the-workflow) | Primary |
| `CCAO-F/D4/4.3/S1` | Use Claude for solution design, development and iteration | [2.3](../README.md#23-use-ai-to-analyze-plan-and-design-the-workflow) (options, then refine), [2.8](../README.md#28-context-and-the-first-draft) (draft small, iterate) | Primary |
| `CCAO-F/D4/4.4/S1` | Integrate Claude into existing workflows to augment or redesign them | [2.1](../README.md#21-from-prompts-to-workflows) (augment vs redesign), [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet), Self-check 1 | Primary |
| `CCAO-F/D7/7.3/S1` | Optimize workflows for efficiency and effectiveness | [2.9](../README.md#29-improve-reuse-and-share-the-workflow), [2.6](../README.md#26-model-and-reasoning-effort-per-step-quality-speed-and-cost), Self-check 4 | Primary |
| `CCAO-F/PURPOSE/3` | Identify opportunities to improve processes using Claude | [2.1](../README.md#21-from-prompts-to-workflows) (four traits, examples by role) | Primary |
| `OAI/foundations/applied-ai-foundations/1` | Module: From Prompts to Workflows | [2.1](../README.md#21-from-prompts-to-workflows) | Primary |
| `OAI/foundations/applied-ai-foundations/2` | Module: Reasoning Models | [2.6](../README.md#26-model-and-reasoning-effort-per-step-quality-speed-and-cost) (API detail in [OpenAI 01 §1.7](../../../openai-codex/01-responses-api-fundamentals/README.md#17-model-selection-and-reasoning-effort)) | Primary |
| `OAI/foundations/applied-ai-foundations/4` | Module: Design the Workflow | [2.2](../README.md#22-map-the-workflow-steps-inputs-and-outputs), [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet), [2.5](../README.md#25-review-checkpoints) | Primary |
| `OAI/foundations/applied-ai-foundations/5` | Module: Responsible Use in Workflows | [2.10](../README.md#210-responsible-use-inside-the-workflow) (governance depth in planned chapters 11 and 12) | Primary |
| `OAI/foundations/applied-ai-foundations/6` | Choose a recurring workflow and break it into steps | [2.1](../README.md#21-from-prompts-to-workflows), [2.2](../README.md#22-map-the-workflow-steps-inputs-and-outputs) | Primary |
| `OAI/foundations/applied-ai-foundations/7` | Identify where ChatGPT can help in each step | [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet); homework exercise 1 | Primary |
| `OAI/foundations/applied-ai-foundations/8` | Define inputs and outputs for each step | [2.2](../README.md#22-map-the-workflow-steps-inputs-and-outputs) | Primary |
| `OAI/foundations/applied-ai-foundations/10` | Build review points, checkpoints and human review into the process | [2.5](../README.md#25-review-checkpoints); homework exercise 2 (approval gates in code: [Claude 09](../../../anthropic-claude/09-escalation-human-in-the-loop/README.md), [OpenAI 09](../../../openai-codex/09-escalation-human-in-the-loop/README.md)) | Supporting |
| `OAI/foundations/applied-ai-foundations/11` | Balance quality, speed and cost | [2.6](../README.md#26-model-and-reasoning-effort-per-step-quality-speed-and-cost); homework exercise 4 | Primary |
| `OAI/foundations/applied-ai-foundations/12` | Deliverable: a repeatable workflow or plan for a recurring process | [2.9](../README.md#29-improve-reuse-and-share-the-workflow) (workflow card), practice mini-project, homework Part C | Primary |
| `OAI/foundations/agents-and-workflows/1` | Module: From Asking to Assigning Work | [2.7](../README.md#27-from-asking-to-assigning-the-agent-brief) | Primary |
| `OAI/foundations/agents-and-workflows/2` | Module: Give the Agent a Clear Job | [2.7](../README.md#27-from-asking-to-assigning-the-agent-brief), Self-check 3 | Primary |
| `OAI/foundations/agents-and-workflows/3` | Module: Add Context and create your First Draft | [2.8](../README.md#28-context-and-the-first-draft) | Primary |
| `OAI/foundations/agents-and-workflows/4` | Module: Improve and Share the Workflow | [2.9](../README.md#29-improve-reuse-and-share-the-workflow) | Primary |
| `OAI/foundations/agents-and-workflows/6` | Module: Responsible Use | [2.10](../README.md#210-responsible-use-inside-the-workflow), boundaries in [2.7](../README.md#27-from-asking-to-assigning-the-agent-brief) | Primary |
| `OAI/foundations/agents-and-workflows/7` | Give agents context and define tasks and outputs | [2.7](../README.md#27-from-asking-to-assigning-the-agent-brief), [2.8](../README.md#28-context-and-the-first-draft); homework exercise 3 | Primary |
| `OAI/foundations/agents-and-workflows/8` | Set boundaries for agent work | [2.7](../README.md#27-from-asking-to-assigning-the-agent-brief) (allowed, needs approval, never, stop and ask, budget) | Primary |
| `OAI/foundations/agents-and-workflows/9` | Decide what to delegate, and place checkpoints and human review | [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet), [2.5](../README.md#25-review-checkpoints); homework exercises 1–2 | Primary |
| `OAI/foundations/agents-and-workflows/10` | Review drafts and results | [2.5](../README.md#25-review-checkpoints) ("review drafts and results"), [2.8](../README.md#28-context-and-the-first-draft) | Primary |
| `OAI/foundations/agents-and-workflows/11` | Improve the workflow over time and reuse what works | [2.9](../README.md#29-improve-reuse-and-share-the-workflow); homework exercise 5 | Primary |
| `OAI/foundations/agents-and-workflows/12` | Run and refine a reusable workflow; identify where human judgment is required | [2.9](../README.md#29-improve-reuse-and-share-the-workflow), [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet), practice mini-project | Primary |
| `OAI/leadership/ai-leadership/6` | Core content: Designing AI workflows | [2.1](../README.md#21-from-prompts-to-workflows)–[2.5](../README.md#25-review-checkpoints), [2.9](../README.md#29-improve-reuse-and-share-the-workflow) (roles after a redesign) | Primary |
| `ACAD/claude-certified-associate-foundations/LO4` | Decide which workflow steps to delegate; communicate value and limits | [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet), limits on the workflow card in [2.9](../README.md#29-improve-reuse-and-share-the-workflow) and [2.10](../README.md#210-responsible-use-inside-the-workflow) (stakeholder communication in planned chapter 18) | Primary |
| `ACAD/claude-certified-associate-foundations/4` | Module: Workflow Integration & Solution Design | Whole chapter | Primary |
| `ACAD/claude-certified-associate-foundations/4/LO1` | Apply Claude to analyze requirements and use cases | [2.3](../README.md#23-use-ai-to-analyze-plan-and-design-the-workflow) | Primary |
| `ACAD/claude-certified-associate-foundations/4/LO2` | Leverage Claude for research, planning and process optimization | [2.3](../README.md#23-use-ai-to-analyze-plan-and-design-the-workflow), [2.9](../README.md#29-improve-reuse-and-share-the-workflow) | Primary |
| `ACAD/claude-certified-associate-foundations/4/LO3` | Use Claude for solution design, development and iteration | [2.3](../README.md#23-use-ai-to-analyze-plan-and-design-the-workflow), [2.8](../README.md#28-context-and-the-first-draft) | Primary |
| `ACAD/claude-certified-associate-foundations/4/LO4` | Integrate Claude into existing workflows to augment or redesign them | [2.1](../README.md#21-from-prompts-to-workflows), [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet) | Primary |
| `ACAD/claude-certified-associate-foundations/7/LO3` | Optimize a workflow by promoting shared context, format and verification steps into persistent setup | [2.9](../README.md#29-improve-reuse-and-share-the-workflow) (promotion table, `promotions()`); homework exercise 5 | Primary |
| `ACAD/claude-101/11` | Lesson: Claude in action, use cases by role | [2.1](../README.md#21-from-prompts-to-workflows) (example workflows by role) | Primary |
| `ACAD/ai-fluency-framework-foundations/6` | Lesson: a closer look at Delegation | [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet) (the 4D framework itself is in [chapter 01 §1.1](../../01-ai-fluency-prompting-and-output-validation/README.md#11-ai-fluency-and-the-4d-framework)) | Primary |
| `ACAD/ai-fluency-framework-foundations/7` | Lesson: project planning and Delegation | [2.2](../README.md#22-map-the-workflow-steps-inputs-and-outputs)–[2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet) | Primary |
| `ACAD/ai-fluency-for-nonprofits/7` | Lessons on delegation and diligence | [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet), [2.10](../README.md#210-responsible-use-inside-the-workflow) (no nonprofit-specific examples; the 4D framework is in [chapter 01 §1.1](../../01-ai-fluency-prompting-and-output-validation/README.md#11-ai-fluency-and-the-4d-framework)) | Supporting |
| `ACAD/ai-fluency-for-nonprofits/8` | Lessons on putting the 4D framework into workflows | [2.2](../README.md#22-map-the-workflow-steps-inputs-and-outputs)–[2.9](../README.md#29-improve-reuse-and-share-the-workflow) | Supporting |
| `ROLE/CHANGE/9` | Organizational change and workflow redesign so AI adoption sticks | [2.1](../README.md#21-from-prompts-to-workflows) (augment vs redesign), [2.9](../README.md#29-improve-reuse-and-share-the-workflow) (workflow card, new roles); adoption at scale in planned chapter 17 | Primary |

Concept coverage beyond the checklist: the gap-review item "a delegate-or-keep worksheet per step (risk, reversibility, verification cost)" is [2.4](../README.md#24-delegate-share-or-keep-the-delegation-worksheet). The Claude and OpenAI comparison is [2.11](../README.md#211-claude-and-openai-side-by-side).

## More self-check questions

**1. (Choosing a workflow)** A marketing lead has four candidates for a first AI workflow. Which one should go first?

- A) A one-time rebrand strategy for next year
- B) The monthly campaign performance summary: same data sources every month, a fixed template, and a manager who knows exactly what a good summary looks like
- C) Negotiating the agency contract renewal
- D) "Being more creative" across the team

<details><summary>Answer</summary>

**B.** It recurs, has a clear output, takes real time and has a known quality bar, so the gain repeats and you can measure it. A is a one-off. C is relationship and accountability work. D has no steps, output or quality bar.
</details>

**2. (Checkpoints)** A redesigned workflow has nine steps, and the team placed a human review after every one. Two weeks in, reviewers click "approve" in seconds and an error reached a customer. What is the best fix?

- A) Add a tenth review step at the end
- B) Keep checkpoints only before external or irreversible actions, after shared steps and after early steps whose errors spread; give each one a checklist and the sources; spot-check AI-only steps on a sample
- C) Remove all reviews; they are not working anyway
- D) Ask reviewers to work more slowly

<details><summary>Answer</summary>

**B.** Too many checkpoints cause review fatigue, so the important ones get rubber-stamped. Fewer, well-placed checkpoints with checklists and sources make review real. A adds more of the same problem. C removes the safety net. D does not tell reviewers what to check.
</details>

**3. (Model and effort)** Tagging 2,000 comments a week at high effort takes 40 minutes and costs more than the rest of the workflow. On 50 labeled comments, low effort scores the same as high. What do you do?

- A) Keep high effort; quality matters
- B) Switch tagging to low effort (or a small, fast model), keep the weekly spot check, and keep high effort only for the trend analysis step
- C) Use `max` effort for every step so the whole workflow is consistent
- D) Remove the spot check to save even more time

<details><summary>Answer</summary>

**B.** The quality bar is met at low effort on real examples, so the cheaper, faster setting wins for that step; the spot check is what tells you if that changes. A pays for quality you measured you do not need. C ignores that steps differ. D removes the only signal that tagging quality is drifting.
</details>

**4. (Responsible use)** An HR team wants AI to rank job applicants and send rejection emails automatically to the bottom half. What is the right design?

- A) Fully automate it; the AI is unbiased
- B) AI summarizes each application against the written criteria with evidence; a recruiter makes and owns every decision; the summaries are checked for bias by swapping names and groups; no message goes out without approval
- C) Let the AI rank, and have a recruiter skim the top ten
- D) Do not use AI anywhere in hiring

<details><summary>Answer</summary>

**B.** Decisions about people stay human, with written criteria, a bias check and an approval before any external message. A and C hand an accountable, hard-to-undo decision to the model. D gives up a useful, reviewable assist.
</details>

**5. (Sharing the workflow)** The analyst who built the feedback-digest workflow is going on leave, and nobody else knows how it runs. What should exist so a teammate can run it next Monday?

- A) The analyst's chat history with the AI
- B) A workflow card: purpose, trigger, steps with their decisions and owners, the agent brief, checkpoints and checklists, known limits and metrics, with standing context in a shared project
- C) A recording of the analyst running it once
- D) Nothing; the AI remembers how to do it

<details><summary>Answer</summary>

**B.** A workflow that lives in one person's head or chat history is not repeatable. The card and the shared project make it runnable and reviewable by others. A and C are hard to follow and miss the decisions and checklists. D is wrong: the setup, not the model, holds the workflow.
</details>

## Share your progress

```text
Chapter 02 of my AI architect track: workflow design and delegation.

3 takeaways:
1. Every step gets one of four owners: code, AI, AI + human approval, or human.
2. Only delegate when checking the result is cheaper than doing the work.
3. Fix it once: repeat corrections go into context, templates or checks.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#AIArchitecture #ClaudeAI #OpenAI #LearningInPublic
```
