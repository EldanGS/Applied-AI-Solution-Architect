# Chapter 03 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix. IDs come from the Claude exam guides (CCAR-P, CCDV-F), the Anthropic and OpenAI Academy course pages and the role competency matrix. **Primary** means this chapter is where the item is taught in depth; **Supporting** means it is applied or reinforced here and taught more fully elsewhere.

| Requirement ID | What it asks (short) | Where in this chapter | Depth |
|---|---|---|---|
| `CCAR-P/D1/1.1/S1` | Translate business problems into Claude-based AI solutions | [3.6](../README.md#36-the-problem-statement), [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements), [3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai); practice mini-project | Primary |
| `CCAR-P/D1/1.6/S1` | Align solutions to business value pillars | [3.5](../README.md#35-value-pillars-structural-vs-marginal-gain) (pillar table), [3.9](../README.md#39-baselines-the-value-case-and-roi) | Primary |
| `CCAR-P/D1/1.6/K1` | Efficiency pillar | [3.5](../README.md#35-value-pillars-structural-vs-marginal-gain), [3.9](../README.md#39-baselines-the-value-case-and-roi) | Primary |
| `CCAR-P/D1/1.6/K2` | Transformation pillar | [3.5](../README.md#35-value-pillars-structural-vs-marginal-gain) (structural gain, transformation row) | Primary |
| `CCAR-P/D1/1.6/K3` | Productivity pillar | [3.5](../README.md#35-value-pillars-structural-vs-marginal-gain) | Primary |
| `CCAR-P/D1/1.6/K4` | Cost pillar | [3.5](../README.md#35-value-pillars-structural-vs-marginal-gain), [3.9](../README.md#39-baselines-the-value-case-and-roi) (cost per successful task); token math in [Claude 07 §7.9](../../../anthropic-claude/07-message-batches/README.md#79-cost-modeling-batch-discount-prompt-caching-and-model-choice) | Supporting |
| `CCAR-P/D1/1.6/K5` | Performance SLAs pillar | [3.5](../README.md#35-value-pillars-structural-vs-marginal-gain), [3.10](../README.md#310-success-criteria-pilot-design-and-the-evaluation-plan) (p95 guardrail); SLA math in [Claude 07 §7.8](../../../anthropic-claude/07-message-batches/README.md#78-sla-planning-and-submission-cadence) | Supporting |
| `CCAR-P/D6/6.1/S1` | Conduct structured discovery and requirement gathering | [3.2](../README.md#32-structured-discovery-with-stakeholders), [3.3](../README.md#33-finding-ai-opportunities-in-a-real-workflow), [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements), Self-check 1 | Primary |
| `CCAR-P/PURPOSE/1` | Design and prototype AI-driven solutions for real business problems | [3.1](../README.md#31-the-discovery-arc-and-owning-ambiguity) (the arc), [3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai); practice mini-project (scope brief) | Primary |
| `CCDV-F/D2/2.1/S1` | Functional and infrastructure requirements from business requirements | [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements), Self-check 4; homework exercise 3 | Primary |
| `CCDV-F/D2/2.1/K1` | Functional requirements derived from business requirements | [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements) (FR column) | Primary |
| `CCDV-F/D2/2.1/K2` | Infrastructure requirements derived from business requirements | [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements) (IR column) | Primary |
| `OAI/api/scope-ai-solutions/1` | Identify AI opportunities within real workflows, with a method | [3.3](../README.md#33-finding-ai-opportunities-in-a-real-workflow) (workflow walk and step tags) | Primary |
| `OAI/api/scope-ai-solutions/2` | Decide which AI ideas are worth pursuing | [3.4](../README.md#34-qualifying-and-prioritizing-use-cases) (hard gates), Self-check 2; homework exercise 1 | Primary |
| `OAI/api/scope-ai-solutions/3` | Compare opportunities on value and feasibility | [3.4](../README.md#34-qualifying-and-prioritizing-use-cases) (`prioritize`, quadrants) | Primary |
| `OAI/api/scope-ai-solutions/4` | Turn the strongest candidate into a clear problem statement | [3.6](../README.md#36-the-problem-statement) | Primary |
| `OAI/api/scope-ai-solutions/5` | A solution plan that helps decide whether the idea is worth building | [3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai), [3.10](../README.md#310-success-criteria-pilot-design-and-the-evaluation-plan); practice mini-project (one-page scope brief) | Primary |
| `OAI/api/scope-ai-solutions/10` | Frame the technical requirements for an AI use case | [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements) | Primary |
| `OAI/api/scope-ai-solutions/11` | Evaluate implementation options (building blocks, model, prompting) | [3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai) (first cut only; full treatment in [chapter 04](../../04-solution-architecture-patterns/README.md) and [chapter 05](../../05-model-strategy-and-customization/README.md)) | Supporting |
| `OAI/leadership/ai-leadership/3` | Connecting AI to business value | [3.5](../README.md#35-value-pillars-structural-vs-marginal-gain), [3.9](../README.md#39-baselines-the-value-case-and-roi) | Primary |
| `OAI/leadership/ai-leadership/9` | Choose AI opportunities worth backing and set priorities | [3.4](../README.md#34-qualifying-and-prioritizing-use-cases), Self-check 2 | Primary |
| `OAI/leadership/ai-leadership/10` | Connect an initiative to business priorities | [3.4](../README.md#34-qualifying-and-prioritizing-use-cases) (strategic fit), [3.2](../README.md#32-structured-discovery-with-stakeholders) (sponsor question), [3.6](../README.md#36-the-problem-statement) | Primary |
| `OAI/bootcamp/api-builder/7` | Frame technical requirements and evaluate implementation options | [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements), [3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai) | Primary |
| `ACAD/claude-certified-architect-professional/LO1` | Ambiguous problem → scoped Claude solution (architecture, model, context strategy, entry point) | [3.1](../README.md#31-the-discovery-arc-and-owning-ambiguity), [3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai) (the four decisions) | Primary |
| `ACAD/claude-certified-architect-professional/4/LO1` | Structured discovery with a non-technical stakeholder, translated into requirements | [3.2](../README.md#32-structured-discovery-with-stakeholders) (translation habits, `extract_notes`), [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements) | Primary |
| `ACAD/claude-certified-architect-professional/LO6` | Discovery with non-technical stakeholders, actionable trade-offs, durable handoff | [3.2](../README.md#32-structured-discovery-with-stakeholders) (discovery part only; trade-off briefs and handoff in planned chapters 18 and 19) | Supporting |
| `ACAD/claude-certified-architect-professional/1/LO5` | Where each platform entry point fits | [3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai) (entry-point table; depth in [chapter 04 §4.4](../../04-solution-architecture-patterns/README.md#44-platform-entry-points)) | Supporting |
| `ACAD/claude-certified-architect-professional/2/LO3` | Create a use case by estimating volume, tokens and cost, and assess feasibility | [3.4](../README.md#34-qualifying-and-prioritizing-use-cases), [3.9](../README.md#39-baselines-the-value-case-and-roi) | Supporting |
| `ROLE/DISC/1` | Technical discovery and requirements translation | [3.2](../README.md#32-structured-discovery-with-stakeholders), [3.7](../README.md#37-from-business-requirements-to-functional-and-infrastructure-requirements) | Primary |
| `ROLE/DISC/2` | Use-case identification, qualification and prioritization | [3.3](../README.md#33-finding-ai-opportunities-in-a-real-workflow), [3.4](../README.md#34-qualifying-and-prioritizing-use-cases) | Primary |
| `ROLE/DISC/3` | Business value case and ROI | [3.9](../README.md#39-baselines-the-value-case-and-roi), Self-check 3; homework exercise 2 | Primary |
| `ROLE/DISC/4` | Success criteria and technical-evaluation planning | [3.10](../README.md#310-success-criteria-pilot-design-and-the-evaluation-plan); homework exercise 4 | Primary |
| `ROLE/DISC/5` | Industry and domain fluency | [3.11](../README.md#311-domain-fluency-what-changes-by-industry), More self-check questions 4 | Primary |
| `ROLE/CHANGE/8` | Ambiguity, prioritization and ownership | [3.1](../README.md#31-the-discovery-arc-and-owning-ambiguity) (assumptions log, time-box), More self-check questions 3 | Primary |

Topic sources (topics only, written in my own words): the Anthropic Partner Academy course outlines Claude Platform & Solution Design and [Stakeholder Engagement, Lifecycle & GTM](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional/stakeholder-engagement-lifecycle-gtm) (CCAR-P prep) and [Delivery Methodology](https://anthropic-partners.skilljar.com/path/partner-badge-claude-code/delivery-methodology) (use-case qualification, structural vs marginal gain, baselines before day 1), and OpenAI's business guides linked in the chapter.

## More self-check questions

**1. (Value pillars)** A software firm pilots AI coding assistants for 30 days. Developers say they "feel faster", but cycle time per ticket is within the normal noise, and the CIO asks what changed. Which reframing is most likely to give a defensible result in the next pilot?

- A) Run the same pilot for another 30 days and ask developers for a satisfaction score
- B) Pick a unit of work the tool can change structurally, such as a test-backfill or migration backlog that used to need four people for six weeks, measure its baseline, and report the change in people-weeks per unit
- C) Count lines of code generated per developer
- D) Report the vendor's published productivity benchmark

<details><summary>Answer</summary>

**B.** A structural gain changes the unit of work, so it shows up clearly in a short pilot against a measured baseline ([3.5](../README.md#35-value-pillars-structural-vs-marginal-gain)). A repeats a marginal measurement that is too noisy to show. C measures activity, not value. D is not the customer's data.
</details>

**2. (Success criteria)** The draft success criteria for a support-reply assistant read: "Agents like it; replies are better; it is fast." What should you replace them with?

- A) A promise to collect feedback after launch and decide then
- B) A business target (for example, median handle time from 11 to 7 minutes, from ticket timestamps), a quality threshold measured on a labeled sample of 300 real tickets, and guardrails such as zero replies with another customer's data, p95 latency and cost per ticket
- C) A single overall score from an LLM judge
- D) The model's benchmark results on public datasets

<details><summary>Answer</summary>

**B.** Each criterion has a number, a method and a data source, agreed before the build, and the guardrails can block a go ([3.10](../README.md#310-success-criteria-pilot-design-and-the-evaluation-plan)). A defines success after the results are in. C hides which dimension failed, and an uncalibrated judge is not evidence. D says nothing about this customer's tickets.
</details>

**3. (Ambiguity and ownership)** The process owner has not delivered volume data after a week, and the steering meeting is in six days. What do you do?

- A) Postpone the steering meeting until the data arrives
- B) Use a public industry average and present it as the customer's number
- C) Log the volume as an unconfirmed assumption with an owner and a date, pull a proxy (such as a one-week export or a sample count), present the decision with its confidence and the condition that would change it
- D) Drop the use case because the data is late

<details><summary>Answer</summary>

**C.** Owning ambiguity means deciding on time with stated assumptions and a plan to confirm them ([3.1](../README.md#31-the-discovery-arc-and-owning-ambiguity)). A gives up control of the timeline. B hides an assumption as a fact. D kills a possibly good idea on a missing input that a proxy can fill.
</details>

**4. (Domain fluency)** In the first call with a clinic network about summarizing referral letters, which question must come before any discussion of models?

- A) "Do you prefer Claude or OpenAI?"
- B) "Is protected health information in scope, which platforms are covered by a business associate agreement, and in which region may data be processed?"
- C) "How long should each summary be?"
- D) "Do you want a chat interface?"

<details><summary>Answer</summary>

**B.** In healthcare, PHI scope and BAA coverage decide which platforms are allowed at all, so they come first ([3.11](../README.md#311-domain-fluency-what-changes-by-industry)). A, C and D are real questions, but they only matter once the platform is allowed.
</details>

**5. (Solution shape)** Forty policy analysts want help drafting briefing memos from internal reports they already have in shared folders. There is no system to integrate, and the content varies every time. What first-cut entry point fits best?

- A) A custom application on the Messages or Responses API with a retrieval pipeline
- B) An embedded multi-agent system built with an agent SDK
- C) An enterprise chat app (Claude Enterprise or ChatGPT Enterprise) with projects and connected document sources, plus a short prompt guide
- D) A fine-tuned model trained on past memos

<details><summary>Answer</summary>

**C.** Knowledge work with no system to integrate fits the chat-app entry point, which is the simplest shape that meets the need ([3.8](../README.md#38-a-first-cut-solution-shape-on-claude-and-openai)). A and B build what the product already provides. D adds cost and lifecycle work before anyone has shown that prompting falls short.
</details>

## Share your progress

```text
Chapter 03 of my Applied AI Architect journey: discovery comes before models.

3 takeaways:
1. Start from one real workflow and its numbers, not from "we need a chatbot".
2. Gate first (data, owner, measurable, reversible), then score value x feasibility.
3. No baseline, no ROI. Measure before day 1 and agree on go/no-go criteria up front.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#AIArchitecture #ClaudeAI #OpenAI #LearningInPublic
```
