# Chapter 01 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix. IDs come from the official CCAO-F guide checklist (`req_anthropic`), the Anthropic Academy course pages (`ACAD`) and the OpenAI Academy course pages (`OAI`). **Primary** means this chapter is where the item is taught in depth; **Supporting** means it is applied or reinforced here and taught more fully elsewhere (the row says where).

| Requirement ID | What it asks (short) | Where in this chapter | Depth |
|---|---|---|---|
| `CCAO-F/D1/1.1/S1` | Create effective prompts for business and technical tasks | [1.4](../README.md#14-description-a-repeatable-prompt-structure) (component structure, `gaps()`), [1.5](../README.md#15-adding-useful-context); practice §1.4, homework exercise 1 | Primary |
| `CCAO-F/D1/1.2/S1` | Decompose complex requests | [1.6](../README.md#16-matching-the-prompt-to-the-task-type) ("split mixed tasks"); taught fully in [Claude 08 §8.11](../../../anthropic-claude/08-task-decomposition/README.md#811-decomposition-for-everyday-claude-use-associate-lens) | Supporting |
| `CCAO-F/D1/1.3/S1` | Iterate prompts to improve output quality | [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output), Self-check 2; practice mini-project | Primary |
| `CCAO-F/D1/1.4/S1`, `CCAO-F/D1/1.4/K1`, `CCAO-F/D1/1.4/K2`, `CCAO-F/D1/1.4/K3`, `CCAO-F/D1/1.4/K4` | Adapt the prompt to analysis, research, drafting, brainstorming | [1.6](../README.md#16-matching-the-prompt-to-the-task-type) (task-type table), Self-check 4; practice §1.6 | Primary |
| `CCAO-F/D2/2.1/S1` | Evaluate outputs for accuracy and completeness | [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias) (`check_output`), Self-check 1; homework exercise 2 | Primary |
| `CCAO-F/D2/2.2/S1`, `CCAO-F/D2/2.2/K1`, `CCAO-F/D2/2.2/K2`, `CCAO-F/D2/2.2/K3` | Identify hallucinations, inconsistencies and biases | [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias) (four checks, swap test), [1.2](../README.md#12-how-llms-behave-four-properties-behind-every-surprise); practice §1.7 | Primary |
| `CCAO-F/D2/2.3/S1` | Apply fact-checking and validation techniques | [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias) (trace, recompute, cross-check, regenerate, swap) | Primary |
| `CCAO-F/D2/2.4/S1` | Decide when human review or more verification is needed | [1.8](../README.md#18-when-a-human-must-verify) (`review_level`), Self-check 3; homework exercise 3 | Primary |
| `CCAO-F/D2/2.5/S1` | Edit, adapt, refine and compare outputs for the audience | [1.9](../README.md#19-editing-comparing-and-formatting-for-the-audience) (four dials, rubric `best()`); homework exercise 4 | Primary |
| `CCAO-F/D2/2.6/S1`, `CCAO-F/D2/2.6/K1`, `CCAO-F/D2/2.6/K2`, `CCAO-F/D2/2.6/K3` | Choose output formats: artifacts, inline, structured data | [1.9](../README.md#19-editing-comparing-and-formatting-for-the-audience) (format paragraph); rendering rules in [Claude 12 §12.4](../../../anthropic-claude/12-provenance/README.md#124-render-by-content-type) | Supporting |
| `CCAO-F/D7/7.1/S1` | Diagnose and fix underperforming prompts or poor outputs | [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output) (symptom → root cause → fix), [1.2](../README.md#12-how-llms-behave-four-properties-behind-every-surprise); More self-check questions 1, 2 | Primary |
| `CCAO-F/D7/7.2/S1` | Adjust approach based on feedback and results | [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output) (targeted feedback vs rewrite, `promote()`); homework exercise 5 | Primary |
| `CCAO-F/D7/7.3/S1` | Optimize workflows for efficiency | [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output) (persistent fixes); taught fully in [Chapter 02](../../02-workflow-design-and-delegation/README.md) | Supporting |
| `CCAO-F/PURPOSE/1` | Complete structured business tasks with minimal guidance | [1.4](../README.md#14-description-a-repeatable-prompt-structure), [1.6](../README.md#16-matching-the-prompt-to-the-task-type); practice mini-project | Primary |
| `ACAD/claude-certified-associate-foundations/LO7`, `ACAD/claude-certified-associate-foundations/7/LO1`, `ACAD/claude-certified-associate-foundations/7/LO2` | Trace weak output to a root cause; make corrections persist | [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output); homework exercise 5 | Primary |
| `ACAD/claude-certified-associate-foundations/2/LO1` | Prompts with a repeatable component structure | [1.4](../README.md#14-description-a-repeatable-prompt-structure) | Primary |
| `ACAD/claude-certified-associate-foundations/2/LO3` | Adapt prompting to analysis, research, drafting, brainstorming | [1.6](../README.md#16-matching-the-prompt-to-the-task-type) | Primary |
| `ACAD/claude-certified-associate-foundations/3/LO1`, `ACAD/claude-certified-associate-foundations/3/LO2`, `ACAD/claude-certified-associate-foundations/3/LO3`, `ACAD/claude-certified-associate-foundations/3/LO4` | Evaluate accuracy and completeness, spot hallucinations and bias, fact-check, decide on human review | [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias), [1.8](../README.md#18-when-a-human-must-verify) | Primary |
| `ACAD/claude-certified-associate-foundations/3/LO5` | Edit, adapt, refine and compare output for the audience | [1.9](../README.md#19-editing-comparing-and-formatting-for-the-audience) | Primary |
| `ACAD/claude-certified-associate-foundations/3/LO6` | Select output formats and organize information | [1.9](../README.md#19-editing-comparing-and-formatting-for-the-audience); fuller in [Claude 12 §12.4](../../../anthropic-claude/12-provenance/README.md#124-render-by-content-type) | Supporting |
| `ACAD/claude-certified-associate-foundations/2`, `ACAD/claude-certified-associate-foundations/3`, `ACAD/claude-certified-associate-foundations/7` | Prep-course modules: prompting, evaluating output, troubleshooting | [1.4](../README.md#14-description-a-repeatable-prompt-structure)–[1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output); [notebooks](../README.md#notebooks) | Primary |
| `ACAD/claude-101/3` | Claude 101 lesson: getting better results | [1.4](../README.md#14-description-a-repeatable-prompt-structure), [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output) | Primary |
| `ACAD/ai-fluency-framework-foundations/1` – `ACAD/ai-fluency-framework-foundations/5` | AI Fluency lessons: introduction, why fluency, the 4D framework, generative AI fundamentals, capabilities and limitations | [1.1](../README.md#11-ai-fluency-and-the-4d-framework), [1.2](../README.md#12-how-llms-behave-four-properties-behind-every-surprise) | Primary |
| `ACAD/ai-fluency-framework-foundations/6`, `ACAD/ai-fluency-framework-foundations/7` | AI Fluency lessons: delegation, project planning and delegation | [1.3](../README.md#13-delegation-choosing-the-mode-of-collaboration) (the three questions and modes); the per-step worksheet is in [Chapter 02](../../02-workflow-design-and-delegation/README.md) | Supporting |
| `ACAD/ai-fluency-framework-foundations/8` – `ACAD/ai-fluency-framework-foundations/12` | AI Fluency lessons: description, prompting techniques, discernment, the Description-Discernment loop, diligence | [1.4](../README.md#14-description-a-repeatable-prompt-structure), [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias), [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output), [1.11](../README.md#111-diligence-own-it-disclose-it-deploy-it-carefully) | Primary |
| `ACAD/ai-fluency-framework-foundations/13` – `ACAD/ai-fluency-framework-foundations/15` | AI Fluency lessons: conclusion, certificate, additional activities | [Self-check](../README.md#self-check), [notebooks](../README.md#notebooks) (take the course's own final assessment for the certificate) | Supporting |
| `ACAD/ai-capabilities-and-limitations/1` – `ACAD/ai-capabilities-and-limitations/14` | AI Capabilities and Limitations: what AI is, how it gets its character, next-token prediction, knowledge, working memory, steerability, when properties collide, quiz | [1.2](../README.md#12-how-llms-behave-four-properties-behind-every-surprise) (four-property table, collisions); practice §1.2, homework Q1–Q2 | Primary |
| `ACAD/ai-fluency-for-builders/1` – `ACAD/ai-fluency-for-builders/10` | 4Ds for builders: briefs, acceptance tests as "done", ship-fix-stop | [1.1](../README.md#11-ai-fluency-and-the-4d-framework), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role) (role table); acceptance tests in Chapter 08 (planned); role activities are in the course itself | Supporting |
| `ACAD/ai-fluency-for-educators/1` – `ACAD/ai-fluency-for-educators/5`, `ACAD/teaching-ai-fluency/1` – `ACAD/teaching-ai-fluency/8`, `ACAD/ai-fluency-for-pk-12-educators/1`, `ACAD/ai-fluency-for-pk-12-educators/2` | 4Ds for educators and for teaching AI fluency | [1.1](../README.md#11-ai-fluency-and-the-4d-framework), [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role); homework Q6; classroom activities are in the courses themselves | Supporting |
| `ACAD/ai-fluency-for-students/1` – `ACAD/ai-fluency-for-students/6` | 4Ds for students, personal commitments | [1.1](../README.md#11-ai-fluency-and-the-4d-framework), [1.11](../README.md#111-diligence-own-it-disclose-it-deploy-it-carefully), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role); homework Q7 | Supporting |
| `ACAD/ai-fluency-for-nonprofits/1` – `ACAD/ai-fluency-for-nonprofits/6`, `ACAD/ai-fluency-for-nonprofits/9`, `ACAD/ai-fluency-for-nonprofits/10`, `ACAD/ai-fluency-for-small-businesses/1` – `ACAD/ai-fluency-for-small-businesses/10` | 4Ds for nonprofits and small businesses: both loops, a repeatable workflow, a short AI use policy | [1.1](../README.md#11-ai-fluency-and-the-4d-framework), [1.2](../README.md#12-how-llms-behave-four-properties-behind-every-surprise), [1.11](../README.md#111-diligence-own-it-disclose-it-deploy-it-carefully), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role); workflow design in [Chapter 02](../../02-workflow-design-and-delegation/README.md), policy in Chapter 12 (planned) | Supporting |
| `ACAD/ai-fluency-for-creative-work/1` – `ACAD/ai-fluency-for-creative-work/9` | 4Ds for creative work | [1.1](../README.md#11-ai-fluency-and-the-4d-framework), [1.11](../README.md#111-diligence-own-it-disclose-it-deploy-it-carefully) (rights, disclosure), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role) | Supporting |
| `OAI/foundations/ai-foundations/1`, `OAI/foundations/ai-foundations/2`, `OAI/foundations/ai-foundations/6` | AI Foundations: introduction; LLMs; basics of AI, LLMs and ChatGPT | [1.1](../README.md#11-ai-fluency-and-the-4d-framework), [1.2](../README.md#12-how-llms-behave-four-properties-behind-every-surprise), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role) | Primary |
| `OAI/foundations/ai-foundations/3`, `OAI/foundations/ai-foundations/7`, `OAI/foundations/ai-foundations/9` | Prompting and evaluation; clearer instructions; review outputs | [1.4](../README.md#14-description-a-repeatable-prompt-structure), [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias), [1.9](../README.md#19-editing-comparing-and-formatting-for-the-audience) | Primary |
| `OAI/foundations/ai-foundations/4`, `OAI/foundations/ai-foundations/8` | Add useful context | [1.5](../README.md#15-adding-useful-context) | Primary |
| `OAI/foundations/ai-foundations/5`, `OAI/foundations/ai-foundations/10` | Use AI responsibly in everyday work | [1.11](../README.md#111-diligence-own-it-disclose-it-deploy-it-carefully); system-level controls in Chapters 10–12 (planned) | Primary |
| `OAI/foundations/ai-foundations/11` | Deliverable: an improved version of a real recurring task | Practice mini-project (weekly status update, before/after scorecard); homework Part C | Primary |
| `OAI/education/ai-for-educators/6` | Review outputs against learning objectives and source materials | [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role) (role table); homework Q6 | Primary |
| `OAI/education/ai-for-educators/1` – `OAI/education/ai-for-educators/5`, `OAI/education/ai-for-educators/7` | Session plans, activities, messages, approved materials and routines | [1.4](../README.md#14-description-a-repeatable-prompt-structure), [1.9](../README.md#19-editing-comparing-and-formatting-for-the-audience), [1.10](../README.md#110-the-description-discernment-loop-diagnosing-weak-output) (persistent routines), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role); the teaching artifacts themselves are built in the OpenAI Academy course | Supporting |
| `OAI/education/ai-for-college-students/4` | Review responses against your own materials and assignment rules | [1.7](../README.md#17-discernment-accuracy-completeness-consistency-and-bias), [1.11](../README.md#111-diligence-own-it-disclose-it-deploy-it-carefully), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role); homework Q7 | Primary |
| `OAI/education/ai-for-college-students/1` – `OAI/education/ai-for-college-students/3`, `OAI/education/ai-for-college-students/5`, `OAI/education/ai-for-college-students/6` | Study plans, group projects, applications and interviews, portfolio evidence | [1.6](../README.md#16-matching-the-prompt-to-the-task-type) (planning), [1.9](../README.md#19-editing-comparing-and-formatting-for-the-audience) (drafts), [1.12](../README.md#112-claude-and-chatgpt-side-by-side-and-in-your-role); the student artifacts themselves are built in the OpenAI Academy course | Supporting |

## More self-check questions

**1. (Policy assistant)** An HR team asks Claude about the parental-leave policy and gets a confident answer that matches last year's rules. The new policy was published two months ago on the intranet. Which property explains this, and what is the fix?

- A) Steerability; rephrase the question more neutrally
- B) Knowledge; attach the current policy (or add it to the team's Project knowledge) and ask Claude to answer only from it
- C) Working memory; split the question into smaller parts
- D) Next-token prediction; regenerate until the answer changes

<details><summary>Answer</summary>

**B.** The model cannot know an internal document published after its training, so this is a knowledge gap, and the fix is to provide the source. A changes the wording but not what the model knows. C does not add the missing information. D can only produce another guess.
</details>

**2. (Finance analyst)** An analyst pastes a 70-page annual report and asks for "all risks related to currency exposure". The answer is good on the first pages but misses a currency hedge described in a note near the end. What is the most effective next step?

- A) Ask again in the same chat with "be thorough"
- B) Point to the notes section (or paste it separately), ask for risks from that section with quotes, then combine the two lists
- C) Switch to brainstorming mode and ask for possible currency risks
- D) Accept the answer, since the main risks are in the front of the report

<details><summary>Answer</summary>

**B.** This is a working-memory failure: attention over a long input is uneven. Pointing to the section and asking for quotes targets the cause and makes the result checkable. A adds no information. C invents risks instead of reading them. D ignores a real gap in completeness.
</details>

**3. (Recruiting)** A recruiter uses ChatGPT to draft feedback summaries for candidates. A colleague notices that summaries for women use words like "supportive" and "pleasant" more often, while men get "decisive" and "strong". What should the recruiter do first?

- A) Add "do not be biased" to the prompt and continue
- B) Run a swap test: the same interview notes with only the name and pronouns changed, compare the wording, then rewrite the prompt to tie every adjective to evidence in the notes, and review all summaries before they are used
- C) Stop writing summaries for women
- D) Ask the model to rate how biased its summaries are

<details><summary>Answer</summary>

**B.** A swap test turns a suspicion into evidence. Tying wording to the notes removes the room for stereotyped filler, and human review is required because hiring is high-stakes. A is a vague instruction with no check. C creates a different unfairness. D relies on self-assessment.
</details>

**4. (Consulting team)** Two drafts of a client email answer the same question. One is warmer and reads better; the other includes the agreed delivery date and the price change the client asked about, but is longer. The rubric, written before reading, requires both facts and at most 150 words. What do you do?

- A) Send the warmer draft, because tone matters most with clients
- B) Score both against the rubric; take the draft with both facts and edit it down to 150 words, borrowing the warmer opening if it helps
- C) Ask the model which draft is better
- D) Send both drafts to the client and let them choose

<details><summary>Answer</summary>

**B.** Comparing against criteria written in advance stops "sounds better" from winning over "is complete". Editing combines the strengths of both. A drops required facts. C hands the judgment to the generator. D pushes your job onto the client.
</details>

**5. (Operations manager)** For three months a manager has corrected the weekly report in the same three ways: use the company's fiscal quarters, list owners by name, and mark blocked items in bold. What turns this into a lasting improvement?

- A) Keep correcting; it only takes a minute
- B) Put the three rules and one approved report into a reusable template or the Project instructions, then check the next reports against them
- C) Ask the model to remember the corrections in a long-running chat
- D) Use a different model each week to see which one gets it right

<details><summary>Answer</summary>

**B.** Corrections repeated many times belong in a place every new chat reads: a template or the Project instructions, with an example. A wastes time and the errors still slip through. C depends on one long conversation whose early turns get less attention. D changes the model instead of the missing description.
</details>

## Share your progress

```text
Chapter 01 of my Applied AI Architect track: AI fluency.

3 takeaways:
1. Delegation, Description, Discernment, Diligence: decide, describe, judge, own.
2. Most odd outputs come from one of four model properties. Name the
   property, then fix that, instead of hitting "regenerate".
3. Check what's missing, not just what's there, and if you type the same
   correction three times, put it in the template.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#AIFluency #ClaudeAI #ChatGPT #AIArchitecture #LearningInPublic
```
