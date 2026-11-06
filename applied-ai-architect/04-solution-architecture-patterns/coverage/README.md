# Chapter 04 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix ([COVERAGE.md](../../../COVERAGE.md)). **Primary** means this chapter is where the item is taught in depth; **Supporting** means it is applied or reinforced here and taught more fully elsewhere (the row says where).

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `CCAR-P/D1/1.2/S1` | Design end-to-end architectures (input → processing → output → feedback loops) | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback) (diagram, stage table, `handle()`), [4.8](../README.md#48-writing-it-down-the-architecture-one-pager); practice §4.1 and mini-project | Primary |
| `CCAR-P/D1/1.2/K1` | Input stage | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback) (stage table: validation, screening, identity) | Primary |
| `CCAR-P/D1/1.2/K2` | Processing stage | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback), [4.2](../README.md#42-augmented-llm-workflow-or-agent) (how much autonomy processing gets) | Primary |
| `CCAR-P/D1/1.2/K3` | Output stage | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback) (schema checks, business rules, approvals) | Primary |
| `CCAR-P/D1/1.2/K4` | Feedback loops | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback) (runtime, human and offline loops; exam trap), Self-check 1; practice §4.1 | Primary |
| `CCAR-P/D3/3.7/S1` | Evaluate connection protocols and select the integration mechanism (MCP, API/CLI, agent-to-agent) | [4.5](../README.md#45-integration-mechanisms-mcp-apicli-or-agent-to-agent) (decision table, `pick_integration`), Self-check 2, More self-check questions 2; homework exercise 1 | Primary |
| `CCAR-P/D3/3.7/K1` | MCP | [4.5](../README.md#45-integration-mechanisms-mcp-apicli-or-agent-to-agent) (when MCP pays off, context cost); mechanics in [Claude 04](../../../anthropic-claude/04-model-context-protocol/README.md) and [OpenAI 04](../../../openai-codex/04-built-in-tools-and-mcp/README.md) | Primary |
| `CCAR-P/D3/3.7/K2` | API/CLI | [4.5](../README.md#45-integration-mechanisms-mcp-apicli-or-agent-to-agent) (direct function tools, CLIs for coding agents) | Primary |
| `CCAR-P/D3/3.7/K3` | Agent-to-agent | [4.5](../README.md#45-integration-mechanisms-mcp-apicli-or-agent-to-agent) (A2A Agent Card, tasks, exam trap), More self-check questions 2 | Primary |
| `CCAR-P/PURPOSE/2` | Select appropriate models, architectures and API patterns for specific use cases | [4.2](../README.md#42-augmented-llm-workflow-or-agent)–[4.4](../README.md#44-platform-entry-points), [4.7](../README.md#47-one-interface-two-vendors-claude-vs-openai) (architectures and API patterns); model choice is in [applied chapter 05](../../05-model-strategy-and-customization/README.md) | Primary |
| `CCAR-P/MQC/1` | Designs, implements and governs Claude solutions in production; translates business requirements | [4.8](../README.md#48-writing-it-down-the-architecture-one-pager) (decisions with rejected alternatives); discovery is [applied chapter 03](../../03-discovery-and-use-case-scoping/README.md), governance chapters 11–12 (planned) | Supporting |
| `CCAR-P/MQC/2` | Designs end-to-end AI systems (prompting, context, RAG, agents, integration) | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback), [4.3](../README.md#43-reference-architectures) (blueprints that combine them); RAG in [applied chapter 06](../../06-rag-pipelines/README.md) (chapter 07 planned) | Supporting |
| `OAI/api/scope-ai-solutions/11` | Evaluate implementation options: API building blocks, model selection, prompting, tools, agents | [4.4](../README.md#44-platform-entry-points) (entry points on both vendors), [4.7](../README.md#47-one-interface-two-vendors-claude-vs-openai) (what to abstract); model selection in [applied chapter 05](../../05-model-strategy-and-customization/README.md) | Primary |
| `OAI/api/scope-ai-solutions/13` | Tell an agent apart from a chatbot (instructions, guardrails, tools, acts for the user) | [4.2](../README.md#42-augmented-llm-workflow-or-agent) ("Agent or chatbot?"), More self-check questions 1 | Primary |
| `OAI/tracks/ai-app-development/4` | Production apps combine core logic (agents) with evals | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback) (offline feedback loop and eval gate); eval design in applied chapter 08 (planned) | Primary |
| `ACAD/claude-certified-architect-professional/1/LO5` | Know where each platform entry point fits (Claude.ai, API, SDK, Claude Code, MCP server) | [4.4](../README.md#44-platform-entry-points) (entry-point table and rule of thumb), More self-check questions 3; practice §4.4 | Primary |
| `ACAD/claude-certified-architect-professional/1` | Academy module: Claude Platform & Solution Design | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback)–[4.4](../README.md#44-platform-entry-points); the module also spans [applied chapter 03](../../03-discovery-and-use-case-scoping/README.md) and [applied chapter 05](../../05-model-strategy-and-customization/README.md) | Supporting |
| `ACAD/claude-in-amazon-bedrock/73` | Academy lesson: Agents overview | [4.2](../README.md#42-augmented-llm-workflow-or-agent) | Primary |
| `ACAD/claude-in-amazon-bedrock/81` | Academy lesson: Qualities of agents | [4.2](../README.md#42-augmented-llm-workflow-or-agent) (agent test, four questions, autonomy costs) | Primary |
| `ACAD/claude-with-the-anthropic-api/83`, `ACAD/claude-with-google-vertex/91` | Academy quiz on agents and workflows (take it on the Academy site) | Prepares for it: [4.2](../README.md#42-augmented-llm-workflow-or-agent) and [Claude 08 §8.6–8.7](../../../anthropic-claude/08-task-decomposition/README.md#86-the-workflow-pattern-catalog) | Supporting |
| `ACAD/partner-basecamp/2` | Academy pre-work: Introduction to AI Applications | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback) (what an AI application is made of), [4.4](../README.md#44-platform-entry-points) | Primary |
| `ROLE/ARCH/1` | Design and review end-to-end GenAI and agent architectures | [4.1](../README.md#41-the-end-to-end-shape-input-processing-output-feedback), [4.8](../README.md#48-writing-it-down-the-architecture-one-pager); homework Part C | Primary |
| `ROLE/ARCH/4` | Reference architectures, blueprints and reusable patterns | [4.3](../README.md#43-reference-architectures) (six blueprints, blueprint card); practice §4.3 | Primary |
| `ROLE/ARCH/5` | Resilience: retries and backoff, fallbacks, rate limits, circuit breakers, idempotency | [4.6](../README.md#46-resilience-patterns), Self-check 3 and 4; homework exercises 2–4; SDK details in [Claude 10 §10.2](../../../anthropic-claude/10-multi-agent-error-handling/README.md#102-error-categories-and-the-retryable-flag) | Primary |
| `ROLE/ARCH/6` | Provider-agnostic and multi-model architecture | [4.7](../README.md#47-one-interface-two-vendors-claude-vs-openai) (thin task-level interface, what not to abstract); multi-model strategy in [applied chapter 05](../../05-model-strategy-and-customization/README.md) | Supporting |
| `ROLE/AGENT/1` | Agent architecture and agentic workflows (when to use an agent) | [4.2](../README.md#42-augmented-llm-workflow-or-agent), Self-check 1; patterns in [Claude 08](../../../anthropic-claude/08-task-decomposition/README.md) | Primary |
| `ROLE/AGENT/3` | MCP servers, clients and connectors | [4.5](../README.md#45-integration-mechanisms-mcp-apicli-or-agent-to-agent) (when to build a server); building them is [Claude 04](../../../anthropic-claude/04-model-context-protocol/README.md) | Supporting |

## More self-check questions

**1. (Scoping)** A bank's marketing team asks for "an AI agent" that answers employees' questions about the brand guidelines PDF. It never needs to take actions in other systems. What do you call it, and what do you build?

- A) An agent, because it uses a model; build it on an agent SDK with a tool loop
- B) A grounded Q&A assistant (an augmented LLM call with retrieval), most likely as a workspace project with the guidelines attached; it is not an agent, because it has no tools that act for the user
- C) A multi-agent system so one agent can check the other's answers
- D) A fine-tuned model trained on the guidelines

<details><summary>Answer</summary>

**B.** Answering questions over documents is the Q&A blueprint, and the highest-level entry point that meets the need is a workspace project. An agent acts on the user's behalf with tools; nothing here acts. A and C add loops and cost with no capability gain. D is slow to update when the guidelines change and still needs evaluation; retrieval keeps answers tied to the current document.
</details>

**2. (Integration)** A travel company's booking agent must hand over hotel bookings to a hotel chain's own agent. The hotel agent sometimes asks follow-up questions (room preferences, loyalty number) and can take minutes to confirm. Which mechanism fits?

- A) An MCP tool `book_hotel` that blocks until the booking is done
- B) Agent-to-agent (A2A): discover the hotel agent from its Agent Card and send a task, handling input-required states and progress until it completes or fails
- C) Screen-scrape the hotel's website with a browser agent
- D) Email the hotel's reservations desk

<details><summary>Answer</summary>

**B.** The other side reasons, asks for input and runs long: that is the agent-to-agent case. A hides the follow-up questions inside one opaque call and has no good way to wait or ask. C is brittle and bypasses the partner's supported interface. D is not an integration.
</details>

**3. (Entry points)** A manufacturer wants three things: engineers want Claude in their terminal for their monorepo, the product team wants to embed an agent with custom tools and approvals in their field-service app, and finance wants to analyze spreadsheets in a chat. Which mapping is right?

- A) Claude Code for engineers; the Claude Agent SDK inside the field-service app; Claude apps (a Project or Cowork) for finance
- B) The Messages API for all three, so there is one integration to maintain
- C) Claude Code for all three, because it is the most capable harness
- D) A managed agent runtime for all three

<details><summary>Answer</summary>

**A.** Each group gets the highest-level entry point that meets its need: a coding agent for repository work, an embedded agent runtime where the product must own tools and approvals, and a chat workspace where a person checks every result. B makes two teams build what already exists. C puts a coding harness in front of non-developers. D gives up the app's control over tools and approvals, and does nothing for the terminal or chat use cases.
</details>

**4. (Resilience)** Your design falls back from Claude to OpenAI when the circuit breaker for Claude opens. In a game-day test the fallback works, but the support team reports that answers during the fallback broke the output schema twice as often. What did the design miss?

- A) Nothing; fallbacks are allowed to be worse
- B) The fallback path needs its own tuned prompt and its own pass on the shared eval set (including schema checks) before it counts as a fallback
- C) The circuit breaker threshold should be higher so the fallback is used less
- D) Remove the fallback and wait for Claude to recover

<details><summary>Answer</summary>

**B.** Prompts do not transfer one-to-one between vendors. A fallback is part of the architecture, so it is tuned and evaluated like the primary path, on the same cases. A accepts a known, measurable defect. C hides the problem instead of fixing it. D turns a partial outage into a full one.
</details>

**5. (Reference architectures)** A team copies a "resolution agent" blueprint for a new use case: bulk extraction of 200,000 archived contracts, no customers involved, results needed within a week. What is the main problem?

- A) None; the agent blueprint is the most general one
- B) The problem shape is an extraction pipeline: fixed steps per document, strict schema with nullable fields, validation and repair, and a batch API at lower cost; an agent loop per document adds cost and variance
- C) They should use a research system blueprint so subagents can split the archive
- D) They should use a Q&A assistant and let users ask about the contracts later

<details><summary>Answer</summary>

**B.** The blueprint must match the problem shape. Bulk, non-urgent, same steps for every document is the extraction pipeline, and the deadline allows batching. A ignores cost and predictability. C solves breadth-first research, not record extraction. D changes the requirement instead of meeting it.
</details>

## Share your progress

```text
Chapter 04 of my Applied AI Architect track: solution architecture patterns.

3 takeaways:
1. Draw every system as input -> processing -> output -> feedback. No feedback stage, no way to prove it works.
2. MCP when many clients need one system, a CLI or API when one does, A2A when the other side is an agent that reasons.
3. Retries fix transport, not answers. Add breakers, fallbacks with their own evals, and idempotent tools.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#AIArchitecture #ClaudeAI #OpenAI #AIAgents #LearningInPublic
```
