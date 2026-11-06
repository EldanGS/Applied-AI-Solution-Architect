# Chapter 3 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Requirement IDs come from the official exam guides and Anthropic Academy course outlines (via the repo's requirements checklist) and the Applied AI architect role map. "Primary" means this chapter is the main place the item is taught. "Supporting" means it is taught mainly in another chapter and reinforced here.

| Requirement ID | What it asks (short) | Where in this chapter | Depth |
|---|---|---|---|
| `CCAR-F/MQC/1` | Build agentic apps with the Agent SDK: orchestration, delegation, tools, hooks | Whole chapter; practice mini-project | Primary |
| `CCAR-F/D1/1.1/K1` | Agentic loop lifecycle and `stop_reason` (`tool_use` vs `end_turn`) | [3.1](../README.md#31-the-agentic-loop); practice 3.1 | Primary |
| `CCAR-F/D1/1.1/K2` | Tool results appended to history for the next step | [3.1](../README.md#31-the-agentic-loop) (manual loop); homework Ex. 5 | Primary |
| `CCAR-F/D1/1.1/K3` | Model-driven decisions vs pre-configured decision trees | [3.1](../README.md#31-the-agentic-loop) | Primary |
| `CCAR-F/D1/1.1/S1` | Loop continues on `tool_use`, ends on `end_turn` | [3.1](../README.md#31-the-agentic-loop); homework Ex. 5 | Primary |
| `CCAR-F/D1/1.1/S2` | Add tool results to context between iterations | [3.1](../README.md#31-the-agentic-loop); practice scripted fake client | Primary |
| `CCAR-F/D1/1.1/S3` | Avoid text-signal termination, iteration caps as the stop rule, "has text = done" | [3.1](../README.md#31-the-agentic-loop) anti-patterns; practice stop-rule experiment; Self-check Q1 | Primary |
| `CCAR-F/D1/1.2/K1` | Hub-and-spoke: coordinator manages all inter-agent traffic | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents) | Primary |
| `CCAR-F/D1/1.2/K2` | Subagents have isolated context | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents), [3.4](../README.md#34-the-subagent-tool-agent-formerly-task); Self-check Q2 | Primary |
| `CCAR-F/D1/1.2/K3` | Coordinator decomposes, delegates, aggregates, selects subagents | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents) | Primary |
| `CCAR-F/D1/1.2/K4` | Risk of overly narrow decomposition | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents); practice coverage check; More self-check questions 2 | Primary |
| `CCAR-F/D1/1.2/S1` | Coordinator selects subagents dynamically | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents) (dynamic selection); practice delegation planner | Primary |
| `CCAR-F/D1/1.2/S2` | Partition scope to minimize duplication | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents); homework Q8 | Primary |
| `CCAR-F/D1/1.2/S3` | Iterative refinement: find gaps, re-delegate, re-synthesize | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents) (iterative refinement loop); practice refinement loop | Primary |
| `CCAR-F/D1/1.2/S4` | Route all subagent communication through the coordinator | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents); More self-check questions 4 | Primary |
| `CCAR-F/D1/1.3/K1` | `Task` (now `Agent`) tool spawns subagents; allowed tools include it | [3.4](../README.md#34-the-subagent-tool-agent-formerly-task) | Primary |
| `CCAR-F/D1/1.3/K2` | Subagent context must be passed explicitly in the prompt | [3.4](../README.md#34-the-subagent-tool-agent-formerly-task) (explicit context passing) | Primary |
| `CCAR-F/D1/1.3/K3` | `AgentDefinition`: description, prompt, tool restrictions | [3.2](../README.md#32-agentdefinition-configuration); homework Ex. 1 | Primary |
| `CCAR-F/D1/1.3/K4` | Fork-based sessions from a shared baseline | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17) | Primary |
| `CCAR-F/D1/1.3/S1` | Pass complete prior findings in the subagent prompt | [3.4](../README.md#34-the-subagent-tool-agent-formerly-task); homework Q5 | Primary |
| `CCAR-F/D1/1.3/S2` | Structured formats separate content from metadata | [3.4](../README.md#34-the-subagent-tool-agent-formerly-task) (strong prompt example) | Primary |
| `CCAR-F/D1/1.3/S3` | Parallel subagents via several tool calls in one response | [3.4](../README.md#34-the-subagent-tool-agent-formerly-task) (parallel spawning); homework Ex. 6 | Primary |
| `CCAR-F/D1/1.3/S4` | Coordinator prompts state goals and quality criteria | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents); practice narrow vs coverage coordinator | Primary |
| `CCAR-F/D1/1.4/K1` | Programmatic enforcement vs prompt guidance for ordering | [Pattern B](../README.md#pattern-b-a-programmatic-precondition-verify-identity-before-any-money-moves), [Hooks vs prompt instructions](../README.md#hooks-vs-prompt-instructions) | Primary |
| `CCAR-F/D1/1.4/K2` | Prompt-only compliance has a non-zero failure rate | [Hooks vs prompt instructions](../README.md#hooks-vs-prompt-instructions); practice skip-rate experiment; Self-check Q3 | Primary |
| `CCAR-F/D1/1.4/S1` | Block downstream tools until a prerequisite succeeds | [Pattern B](../README.md#pattern-b-a-programmatic-precondition-verify-identity-before-any-money-moves); practice support hooks | Primary |
| `CCAR-F/D1/1.5/K1` | `PostToolUse` transforms results before the model sees them | [Pattern C](../README.md#pattern-c-normalize-heterogeneous-tool-output-posttooluse) | Primary |
| `CCAR-F/D1/1.5/K2` | Hooks intercept outgoing calls to enforce compliance | [Pattern A](../README.md#pattern-a-block-a-policy-violation-and-redirect-to-escalation-pretooluse) | Primary |
| `CCAR-F/D1/1.5/K3` | Hooks are deterministic, prompts are probabilistic | [Hooks vs prompt instructions](../README.md#hooks-vs-prompt-instructions) | Primary |
| `CCAR-F/D1/1.5/S1` | `PostToolUse` normalizes timestamps and status codes | [Pattern C](../README.md#pattern-c-normalize-heterogeneous-tool-output-posttooluse); practice normalizer; More self-check questions 1 | Primary |
| `CCAR-F/D1/1.5/S2` | Block policy violations (refund > $500) and redirect to escalation | [Pattern A](../README.md#pattern-a-block-a-policy-violation-and-redirect-to-escalation-pretooluse); homework Ex. 4 | Primary |
| `CCAR-F/D1/1.5/S3` | Choose hooks over prompts when compliance must be guaranteed | [Hooks vs prompt instructions](../README.md#hooks-vs-prompt-instructions); cheat-sheet | Primary |
| `CCAR-F/D1/1.7/K1` | Named session resumption with `--resume <session-name>` | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17) (named sessions) | Primary |
| `CCAR-F/D1/1.7/K2` | `fork_session` creates independent branches | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17); More self-check questions 5 | Primary |
| `CCAR-F/D1/1.7/K3` | Tell a resumed agent which files changed | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17) (resume or start fresh) | Primary |
| `CCAR-F/D1/1.7/K4` | A fresh session with a summary beats resuming stale results | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17); homework Q10 | Primary |
| `CCAR-F/D1/1.7/S1` | Use `--resume` with names across work sessions | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17) (named sessions); practice session lookup by title | Primary |
| `CCAR-F/D1/1.7/S2` | `fork_session` for parallel exploration branches | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17); practice fork cell | Primary |
| `CCAR-F/D1/1.7/S3` | Choose resume vs fresh start with an injected summary | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17); practice `session_strategy` | Primary |
| `CCAR-F/D1/1.7/S4` | Inform the resumed session about specific file changes | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17); practice `fresh_session_prompt` | Primary |
| `CCAR-F/APPX/TECH/1` | Agent SDK: definitions, loops, `stop_reason`, hooks, `Task` spawning, `allowedTools` | [3.1](../README.md#31-the-agentic-loop)–[3.5](../README.md#35-hooks-in-the-agent-sdk) | Primary |
| `CCAR-F/APPX/TECH/13` | Session resumption, `fork_session`, named sessions, isolation | [3.6](../README.md#36-sessions-resume-and-fork-bonus-from-domain-17), [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents) (isolation) | Primary |
| `CCAR-F/APPX/IN/1` | Loop control flow on `stop_reason`, tool results, termination | [3.1](../README.md#31-the-agentic-loop) | Primary |
| `CCAR-F/APPX/IN/2` | Coordinator-subagent patterns, decomposition, parallelism, refinement | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents), [3.4](../README.md#34-the-subagent-tool-agent-formerly-task) | Primary |
| `CCAR-P/D1/1.4/S1` | Design multi-agent systems and orchestration strategies | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents), cheat-sheet, homework Part C | Supporting |
| `CCDV-F/PURPOSE/1` | Build agents with the Agent SDK and custom agent loops | [3.1](../README.md#31-the-agentic-loop) (both loops), whole chapter | Primary |
| `CCDV-F/D1/1.1/K3` | Manager/supervisor hierarchies | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents) (coordinator as supervisor); depth caps in [3.4](../README.md#34-the-subagent-tool-agent-formerly-task) | Primary |
| `CCDV-F/D1/1.1/K4` | Role of subagents in task execution | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents) (context isolation, parallelism) | Primary |
| `CCDV-F/D1/1.2/K1` | Claude Agent SDK | Whole chapter | Primary |
| `CCDV-F/D1/1.2/K4` | Hooks for deterministic actions | [3.5](../README.md#35-hooks-in-the-agent-sdk) | Primary |
| `CCDV-F/D1/1.3/K2` | Sub-agents | [3.2](../README.md#32-agentdefinition-configuration)–[3.4](../README.md#34-the-subagent-tool-agent-formerly-task) | Primary |
| `CCDV-F/D8/8.1/K7` | Usage pattern: approval patterns | [3.7](../README.md#37-human-approval-for-irreversible-actions), [Approval patterns](../README.md#approval-patterns); practice 3.7; homework Ex. 7, Q11–Q12; Self-check Q4 | Primary |
| `ACAD/claude-platform-101/4` | The agent loop explained | [3.1](../README.md#31-the-agentic-loop) | Primary |
| `ACAD/claude-with-the-anthropic-api/80` | Agents and tools | [3.1](../README.md#31-the-agentic-loop) ([Two ways to own the loop](../README.md#two-ways-to-own-the-loop)), [3.2](../README.md#32-agentdefinition-configuration) (least privilege) | Primary |
| `ACAD/claude-with-the-anthropic-api/81` | Environment inspection | [Environment inspection](../README.md#environment-inspection-let-the-agent-see-what-its-actions-did) | Primary |
| `ACAD/claude-with-google-vertex/88` | Agents and tools (Vertex edition) | Same as `ACAD/claude-with-the-anthropic-api/80` | Primary |
| `ACAD/claude-with-google-vertex/89` | Environment inspection (Vertex edition) | Same as `ACAD/claude-with-the-anthropic-api/81` | Primary |
| `ACAD/partner-basecamp/7` | Agent SDK | Whole chapter | Primary |
| `ROLE/AGENT/4` | Multi-agent orchestration and sub-agents | [3.3](../README.md#33-hub-and-spoke-coordinator-and-subagents), [3.4](../README.md#34-the-subagent-tool-agent-formerly-task); mini-project | Primary |
| `ROLE/AGENT/7` | Claude agent stack: Agent SDK, Agent Skills, Claude Code config | Agent SDK: whole chapter; hooks and permissions: [3.5](../README.md#35-hooks-in-the-agent-sdk), [3.7](../README.md#37-human-approval-for-irreversible-actions); `AgentDefinition.skills` only briefly (Skills and Claude Code config are taught in [Chapter 5](../../05-claude-code/README.md)) | Supporting |

## More self-check questions

**Q1.** Two vendor MCP servers (`weather` and `prices`) return dates such as `1741132800` and `"05/03/25"`, and the agent reads `05/03` as May 3 when the vendor meant 5 March. You want every date to reach Claude as ISO 8601. Which hook design works?

- A) A `PreToolUse` hook on `^mcp__` that adds `"date_format": "iso"` to each call with `updatedInput`
- B) A `PostToolUse` hook on `^mcp__(weather|prices)__` that converts the dates and returns the result, in the same shape as the tool's output, in `updatedToolOutput`
- C) A `PostToolUse` hook with the matcher `weather|prices` that does the same conversion
- D) A `PostToolUse` hook that leaves the output alone and puts the converted dates in `additionalContext`

<details><summary>Answer</summary>

**B.** The fix belongs after the tool runs, and `updatedToolOutput` replaces what Claude reads. A runs before any output exists, and the vendors don't take a format argument. C is an exact-name list, so it matches no `mcp__<server>__<tool>` name and never fires. D still shows Claude the ambiguous raw values next to the converted ones.
</details>

**Q2.** A research system's final reports on "renewable energy policy" cover only solar subsidies. Logs show every subagent completed successfully, and the coordinator's subtasks were "solar subsidies US", "solar subsidies EU", and "solar subsidies China". What is the root cause?

- A) The web-search subagent's queries are too narrow
- B) The synthesis agent dropped content
- C) The coordinator's decomposition doesn't cover the topic's scope
- D) The context window overflowed

<details><summary>Answer</summary>

**C.** The subagents did what they were told. The assignment itself was too narrow (it missed wind, grid, carbon pricing, and so on). Fix the coordinator's prompt with explicit coverage criteria and add a coverage check before synthesis.
</details>

**Q3.** A web-search subagent times out on one of four source categories. What should it return to the coordinator?

- A) An empty list marked `success`
- B) A generic "search unavailable" error after internal retries
- C) Structured context: failure type (timeout), the query attempted, partial results from the other three categories, and suggested alternatives
- D) Raise an exception that aborts the whole workflow

<details><summary>Answer</summary>

**C.** It gives the coordinator what it needs to choose between retrying, rerouting, and continuing with partial data. A hides the failure, B throws away context, and D overreacts to a partial failure.
</details>

**Q4.** You need four independent document analyses as fast as possible before a synthesis step. How should the coordinator delegate?

- A) Spawn the four subagents sequentially, passing each result to the next
- B) Emit four subagent-tool calls (`Agent`, `Task` in older docs) in a single response, then pass all four results to the synthesizer
- C) Let the four subagents send results directly to the synthesizer
- D) Use one subagent and ask it to analyze all four in turn

<details><summary>Answer</summary>

**B.** Several subagent calls in one turn run concurrently, and synthesis stays sequential because it depends on all four. C bypasses the hub and loses observability and consistent error handling.
</details>

**Q5.** After a long code investigation you want to compare two refactoring strategies without either one contaminating the other's reasoning. What do you do?

- A) Ask the same session to try strategy 1, then "forget it" and try strategy 2
- B) Resume the session twice with `fork_session=True`, once per strategy
- C) Start two blank sessions with no context
- D) Increase `max_turns` and let the agent decide

<details><summary>Answer</summary>

**B.** Each fork starts from the same analyzed context and gets its own session ID, and the original stays unchanged. C throws away the investigation. Only consider a fresh session with a summary if the original findings are stale.
</details>

## Share your progress

```text
Week 3 of my AI Solution Architect journey: I built a multi-agent system with the Claude Agent SDK.

3 takeaways:
1. The loop ends on stop_reason, not on "Done!" in the text
2. Subagents start with a blank context. Pass everything they need in the prompt
3. Rules that touch money or compliance go in hooks, not prompts. Hooks run on every call; prompts only usually get followed

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #AIAgents #SolutionArchitect #LearningInPublic
```

*Syllabus source: Chapter 3 and Domain 1 of the community study guide by [paullarionov/claude-certified-architect](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md), restructured and updated against the official docs (October 2026).*
