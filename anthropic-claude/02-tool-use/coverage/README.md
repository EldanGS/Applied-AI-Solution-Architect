# Chapter 2 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Requirement IDs come from the repo's requirements checklist, built from the official exam guides (v1.0, July 2026), the Anthropic Academy course pages and the role skill map. "Primary" means this chapter is the main place the item is taught; "Supporting" means the chapter teaches the content but the item itself is completed or examined elsewhere. Academy lessons with the same title in several courses (Claude API, Amazon Bedrock, Google Cloud) are each listed. "Practice" and "homework" refer to this chapter's two notebooks.

| Requirement ID | What it asks (short) | Where in this chapter | Depth |
|---|---|---|---|
| `CCAR-F/D2/2.1/K1` | Descriptions are the main tool-selection signal; minimal ones cause unreliable selection | [2.2](../README.md#22-tool-definition) (required fields, "what a strong description contains", exam trap); practice 2.2 minimal-vs-rich experiment; Self-check Q1; homework Q10 | Primary |
| `CCAR-F/D2/2.1/K2` | Input formats, example queries, edge cases and boundaries in descriptions | [2.2](../README.md#22-tool-definition) (`get_customer` example, four-point checklist, `input_examples`); practice 2.2 linter; homework Ex 1 | Primary |
| `CCAR-F/D2/2.1/K3` | Overlapping descriptions cause misrouting (`analyze_content` vs `analyze_document`) | [2.2](../README.md#22-tool-definition) "No overlap"; More self-check questions 1 | Primary |
| `CCAR-F/D2/2.1/K4` | System prompt wording creates keyword-driven tool associations | [2.2](../README.md#22-tool-definition) "Check the system prompt too"; practice 2.2 system-prompt keyword audit | Primary |
| `CCAR-F/D2/2.1/S1` | Write descriptions that differentiate purpose, inputs, outputs and when to use each | [2.2](../README.md#22-tool-definition); practice 2.2 linter and rich descriptions; homework Ex 1 | Primary |
| `CCAR-F/D2/2.1/S2` | Rename and re-describe tools to remove overlap | [2.2](../README.md#22-tool-definition) (`extract_web_results`); More self-check questions 1; homework Q10 | Primary |
| `CCAR-F/D2/2.1/S3` | Split generic tools into purpose-specific tools with I/O contracts | [2.2](../README.md#22-tool-definition) (`analyze_document` split, split vs. consolidate); practice 2.2 "Scope, split and constrain the toolset" | Primary |
| `CCAR-F/D2/2.1/S4` | Review system prompts for keyword-sensitive instructions | [2.2](../README.md#22-tool-definition); practice 2.2 keyword audit with a "Try it" rewrite | Primary |
| `CCAR-F/D2/2.3/K1` | Too many tools (18 vs 4–5) degrades selection | [2.2](../README.md#22-tool-definition) "Keep each agent's toolset small", [Tool-set construction checklist](../README.md#tool-set-construction-checklist) item 1; homework Q10 | Primary |
| `CCAR-F/D2/2.3/K2` | Agents misuse tools outside their specialization | [2.2](../README.md#22-tool-definition) (synthesis agent doing web research); [cheat-sheet](../README.md#cheat-sheet) row | Primary |
| `CCAR-F/D2/2.3/K3` | Scoped tool access with limited cross-role tools | [2.2](../README.md#22-tool-definition) (`ROLE_TOOLS`, `verify_fact`); practice 2.2 role-scoped toolsets | Primary |
| `CCAR-F/D2/2.3/K4` | `tool_choice` options `auto`, `any`, forced tool | [2.3](../README.md#23-the-tool_choice-parameter) (table, current-model restrictions); practice 2.3 four-mode comparison; homework Ex 2 | Primary |
| `CCAR-F/D2/2.3/S1` | Restrict each subagent's tools to its role | [2.2](../README.md#22-tool-definition) `ROLE_TOOLS`; practice 2.2 scope check | Primary |
| `CCAR-F/D2/2.3/S2` | Replace generic tools with constrained ones (`fetch_url` → `load_document`) | [2.2](../README.md#22-tool-definition) "Replace generic tools with constrained ones"; practice 2.2 constrained `load_document` | Primary |
| `CCAR-F/D2/2.3/S3` | Scoped cross-role tools for frequent needs; complex cases via the coordinator | [2.2](../README.md#22-tool-definition) (`verify_fact`, route back to coordinator); practice 2.2 | Primary |
| `CCAR-F/D2/2.3/S4` | Force a specific tool first, then continue in follow-up turns | [2.3](../README.md#23-the-tool_choice-parameter) forced `extract_metadata` + follow-up with `auto`; practice 2.3 "Force the first step, then continue with `auto`" | Primary |
| `CCAR-F/D2/2.3/S5` | `tool_choice: "any"` guarantees a tool call instead of text | [2.3](../README.md#23-the-tool_choice-parameter); `require_tool_call()` for models that reject `any`; More self-check questions 2 | Primary |
| `CCAR-F/D4/4.3/K1` | Tool use with JSON schemas for schema-compliant structured output | [2.4](../README.md#24-json-schemas-for-structured-output) (three mechanisms, "changed since the guide": strict mode and `output_config.format` carry the guarantee); practice 2.4 "One contract, three request shapes" | Primary |
| `CCAR-F/D4/4.3/K2` | `auto` vs `any` vs forced tool selection | [2.3](../README.md#23-the-tool_choice-parameter); More self-check questions 2–3; homework Ex 2 | Primary |
| `CCAR-F/D4/4.3/K3` | Strict schemas stop syntax errors, not semantic errors | [2.5](../README.md#25-syntax-vs-semantic-errors); practice 2.5 three scenarios; Self-check Q3; homework Q5, Ex 4 | Primary |
| `CCAR-F/D4/4.3/K4` | Required vs optional fields; enum + `"other"` + detail | [2.4](../README.md#24-json-schemas-for-structured-output) schema design principles 1–3; homework Q7, Ex 3 | Primary |
| `CCAR-F/D4/4.3/S1` | Define extraction tools and read data from the `tool_use` block | [2.4](../README.md#24-json-schemas-for-structured-output) `record_ticket_classification`; practice 2.4 ticket classifier (plain tool, strict tool, `parse()`) | Primary |
| `CCAR-F/D4/4.3/S2` | `any` when several extraction schemas exist and the type is unknown | [2.3](../README.md#23-the-tool_choice-parameter) table; More self-check questions 2; [cheat-sheet](../README.md#cheat-sheet) | Primary |
| `CCAR-F/D4/4.3/S3` | Force `extract_metadata` before enrichment | [2.3](../README.md#23-the-tool_choice-parameter) forced-selection example; practice 2.3; More self-check questions 3 (migration on current models) | Primary |
| `CCAR-F/D4/4.3/S4` | Nullable fields to stop fabrication of absent data | [2.4](../README.md#24-json-schemas-for-structured-output) principle 2 and exam trap; Self-check Q2; homework Q6, Ex 3 | Primary |
| `CCAR-F/D4/4.3/S5` | `"unclear"` enum value and `"other"` + detail | [2.4](../README.md#24-json-schemas-for-structured-output) principles 3–4 and the strict classifier; homework Q7 | Primary |
| `CCAR-F/D4/4.3/S6` | Normalization rules in the prompt next to strict schemas | [2.4](../README.md#24-json-schemas-for-structured-output) principle 6 (`NORMALIZATION_RULES`); practice 2.4 "Normalization rules and flexible attributes" | Primary |
| `CCAR-F/APPX/TECH/5` | Claude API: `tool_use`, `tool_choice`, `stop_reason`, `max_tokens`, system prompts | [2.3](../README.md#23-the-tool_choice-parameter), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) (`stop_reason` table, `max_tokens` truncation), system-prompt effects in [2.2](../README.md#22-tool-definition); request basics in [Chapter 1](../../01-claude-api-fundamentals/README.md) | Primary |
| `CCAR-F/APPX/TECH/7` | JSON Schema: required/optional, enums, nullable, "other" + detail, strict mode | [2.4](../README.md#24-json-schemas-for-structured-output) (principles, strict-mode limits); practice 2.4 strict-schema linter | Primary |
| `CCAR-F/APPX/IN/4` | Tool interface design: descriptions, splitting vs consolidating, naming | [2.2](../README.md#22-tool-definition), [Tool-set construction checklist](../README.md#tool-set-construction-checklist) | Primary |
| `CCAR-F/APPX/IN/13` | Structured output via `tool_use`: schema design, `tool_choice`, nullable fields | [2.3](../README.md#23-the-tool_choice-parameter), [2.4](../README.md#24-json-schemas-for-structured-output) | Primary |
| `CCDV-F/D1/1.3/K1` | Tool-use loops | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) (`run_agent`, formatting rules); practice 2.6 bounded loop; homework Ex 5–6, Q2, Q8 | Primary |
| `CCDV-F/D2/2.3/K2` | Claude API mechanics: tools | [2.1](../README.md#21-what-is-tool_use)–[2.3](../README.md#23-the-tool_choice-parameter), [2.7](../README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide) | Primary |
| `CCDV-F/D2/2.5/K3` | Schema design | [2.4](../README.md#24-json-schemas-for-structured-output); homework Ex 3 | Primary |
| `CCDV-F/D6/6.3/K1` | Structured output patterns | [2.4](../README.md#24-json-schemas-for-structured-output) (strict tools, `output_config.format`, `messages.parse()`, flexible extraction), [2.5](../README.md#25-syntax-vs-semantic-errors) (retry with feedback) | Primary |
| `CCDV-F/D8/8.1/S1` | Tool implementation: function calling, descriptions, errors, usage patterns, tool-set construction | Whole chapter: [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide), [2.7](../README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide); approval patterns (`K7`) and external-system configuration (`K2`) are taught in other chapters | Primary |
| `CCDV-F/D8/8.1/K1` | Tool use and function calling | [2.1](../README.md#21-what-is-tool_use), [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide); practice 2.1 round trip | Primary |
| `CCDV-F/D8/8.1/K3` | Tool description writing | [2.2](../README.md#22-tool-definition); practice 2.2; homework Ex 1 | Primary |
| `CCDV-F/D8/8.1/K4` | Error handling | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) "Errors as information" (`is_error`, transient vs validation); server-tool errors in [2.7](../README.md#server-tools-what-changes-in-the-loop); practice 2.6; More self-check questions 4; homework Q9 | Primary |
| `CCDV-F/D8/8.1/K5` | Usage pattern: agentic harness dispatch | [The harness dispatch table](../README.md#the-harness-dispatch-table); practice 2.7 dispatch-table harness | Primary |
| `CCDV-F/D8/8.1/K6` | Usage pattern: client-side vs server-side tools | [2.7](../README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide) execution-model table and [server tools in the loop](../README.md#server-tools-what-changes-in-the-loop); practice 2.7; More self-check questions 5; homework Ex 7 | Primary |
| `CCDV-F/D8/8.1/K8` | Tool set construction best practices | [Tool-set construction checklist](../README.md#tool-set-construction-checklist); practice 2.7 checklist cell | Primary |
| `ACAD/claude-certified-developer-foundations/LO3` | Tool schemas, the tool-use loop, extended thinking across multi-turn work | [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) (loop, "Thinking blocks in the loop"); thinking configuration in depth: planned Chapter 14 | Primary |
| `ACAD/claude-certified-developer-foundations/2/LO3` | Schema Claude selects correctly, the loop, multi-turn blocks, single vs parallel calls | [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) ("Single call or parallel calls?"); practice 2.6 parallel calls | Primary |
| `ACAD/claude-platform-101/5` | What is tool use? | [2.1](../README.md#21-what-is-tool_use); practice 2.1 | Primary |
| `ACAD/claude-platform-101/7` | Built-in tools | [2.7](../README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide) (server tools, Anthropic-schema client tools) | Primary |
| `ACAD/claude-with-the-anthropic-api/LO6` | Custom tools, batch operations and web search | [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide), [batch tool](../README.md#the-batch-tool-pattern-legacy), [server tools](../README.md#server-tools-what-changes-in-the-loop) | Primary |
| `ACAD/claude-with-the-anthropic-api/13` | Structured data | [2.4](../README.md#24-json-schemas-for-structured-output) (current methods; why the older prefill trick no longer works) | Primary |
| `ACAD/claude-with-the-anthropic-api/14` | Structured data exercise | Practice 2.4 (ticket classifier three ways); homework Ex 3 | Primary |
| `ACAD/claude-with-the-anthropic-api/31` | Introducing tool use | [2.1](../README.md#21-what-is-tool_use) | Primary |
| `ACAD/claude-with-the-anthropic-api/32` | Project overview | The chapter's running example (practice "a tiny support backend") and the mini-project play the role of the course project | Supporting |
| `ACAD/claude-with-the-anthropic-api/33` | Tool functions | Practice running example (`get_customer`, `lookup_order`, `process_refund`); error messages in [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) | Primary |
| `ACAD/claude-with-the-anthropic-api/34` | Tool schemas | [2.2](../README.md#22-tool-definition); practice 2.2 linter and "schemas from Python functions" | Primary |
| `ACAD/claude-with-the-anthropic-api/35` | Handling message blocks | [2.1](../README.md#21-what-is-tool_use) round trip, [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) (append full `response.content`); practice 2.1 | Primary |
| `ACAD/claude-with-the-anthropic-api/36` | Sending tool results | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) formatting rules; practice 2.6 protocol validator; homework Ex 5 | Primary |
| `ACAD/claude-with-the-anthropic-api/37` | Multi-turn conversations with tools | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide); practice mini-project | Primary |
| `ACAD/claude-with-the-anthropic-api/38` | Implementing multiple turns | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) `run_agent`; practice 2.6 loop; homework Ex 6 | Primary |
| `ACAD/claude-with-the-anthropic-api/39` | Using multiple tools | [2.2](../README.md#22-tool-definition) tool-set design, parallel calls in [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide); practice 2.6 parallel calls | Primary |
| `ACAD/claude-with-the-anthropic-api/41` | The text edit tool | [Anthropic-schema client tools in brief](../README.md#anthropic-schema-client-tools-in-brief); practice 2.7 sandboxed text editor handler | Primary |
| `ACAD/claude-with-the-anthropic-api/42` | The web search tool | [Server tools: what changes in the loop](../README.md#server-tools-what-changes-in-the-loop); practice 2.7 result parsing (offline) and optional paid web search | Primary |
| `ACAD/claude-with-the-anthropic-api/43` | Quiz on tool use with Claude | [Self-check](../README.md#self-check) Q1–Q4, [More self-check questions](#more-self-check-questions) 1–5 and homework Part A; the Academy quiz itself is taken on the Academy site | Supporting |
| `ACAD/claude-in-amazon-bedrock/LO3` | Custom tools with JSON Schema; batch processing | [2.2](../README.md#22-tool-definition), [2.4](../README.md#24-json-schemas-for-structured-output), [batch tool](../README.md#the-batch-tool-pattern-legacy) | Primary |
| `ACAD/claude-in-amazon-bedrock/12` | Structured data | [2.4](../README.md#24-json-schemas-for-structured-output) | Primary |
| `ACAD/claude-in-amazon-bedrock/13` | Structured data exercise | Practice 2.4; homework Ex 3 | Primary |
| `ACAD/claude-in-amazon-bedrock/30` | Introducing tool use | [2.1](../README.md#21-what-is-tool_use) | Primary |
| `ACAD/claude-in-amazon-bedrock/31` | Tool functions | Practice running example; [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) error messages | Primary |
| `ACAD/claude-in-amazon-bedrock/32` | JSON Schema for tools | [2.2](../README.md#22-tool-definition), [2.4](../README.md#24-json-schemas-for-structured-output) | Primary |
| `ACAD/claude-in-amazon-bedrock/33` | Handling tool use responses | [2.1](../README.md#21-what-is-tool_use), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) | Primary |
| `ACAD/claude-in-amazon-bedrock/34` | Running tool functions | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) handler dispatch; [harness dispatch table](../README.md#the-harness-dispatch-table) | Primary |
| `ACAD/claude-in-amazon-bedrock/35` | Sending tool results | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide); homework Ex 5 | Primary |
| `ACAD/claude-in-amazon-bedrock/36` | Multi-turn conversations with tools | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide); practice mini-project | Primary |
| `ACAD/claude-in-amazon-bedrock/37` | Adding multiple tools | [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) parallel calls | Primary |
| `ACAD/claude-in-amazon-bedrock/38` | Batch tool use | [The "batch tool" pattern (legacy)](../README.md#the-batch-tool-pattern-legacy); practice 2.7 batch tool vs native parallel calls | Primary |
| `ACAD/claude-in-amazon-bedrock/39` | Structured data with tools | [2.4](../README.md#24-json-schemas-for-structured-output) strict extraction tool | Primary |
| `ACAD/claude-in-amazon-bedrock/40` | Flexible tool extraction | [2.4](../README.md#24-json-schemas-for-structured-output) "Flexible extraction"; practice 2.4 flexible attributes | Primary |
| `ACAD/claude-in-amazon-bedrock/41` | The text editor tool | [Anthropic-schema client tools in brief](../README.md#anthropic-schema-client-tools-in-brief); practice 2.7 text editor handler | Primary |
| `ACAD/claude-in-amazon-bedrock/42` | Quiz on tool use | [Self-check](../README.md#self-check), [More self-check questions](#more-self-check-questions) and homework Part A; the Academy quiz itself is taken on the Academy site | Supporting |
| `ACAD/claude-in-amazon-bedrock/79` | Computer Use | [Anthropic-schema client tools in brief](../README.md#anthropic-schema-client-tools-in-brief) (computer toolset, safety); practice 2.7 harness | Primary |
| `ACAD/claude-in-amazon-bedrock/80` | How Computer Use works | Same section: member `tool_use` blocks with `toolset_name`, batch actions in order, screenshot results; practice 2.7 batch action with a failing click | Primary |
| `ACAD/claude-with-google-vertex/LO5` | Tool-use implementations against external functions and APIs | [2.1](../README.md#21-what-is-tool_use)–[2.7](../README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide) | Primary |
| `ACAD/claude-with-google-vertex/14` | Structured data | [2.4](../README.md#24-json-schemas-for-structured-output) | Primary |
| `ACAD/claude-with-google-vertex/15` | Structured data exercise | Practice 2.4; homework Ex 3 | Primary |
| `ACAD/claude-with-google-vertex/32` | Introducing tool use | [2.1](../README.md#21-what-is-tool_use) | Primary |
| `ACAD/claude-with-google-vertex/33` | Project overview | Practice running example and mini-project (the course project's role) | Supporting |
| `ACAD/claude-with-google-vertex/34` | Tool functions | Practice running example; [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) error messages | Primary |
| `ACAD/claude-with-google-vertex/35` | Tool schemas | [2.2](../README.md#22-tool-definition) | Primary |
| `ACAD/claude-with-google-vertex/36` | Handling message blocks | [2.1](../README.md#21-what-is-tool_use), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) | Primary |
| `ACAD/claude-with-google-vertex/37` | Sending tool results | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide); homework Ex 5 | Primary |
| `ACAD/claude-with-google-vertex/38` | Multi-turn conversations with tools | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) | Primary |
| `ACAD/claude-with-google-vertex/39` | Implementing multiple turns | [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide); homework Ex 6 | Primary |
| `ACAD/claude-with-google-vertex/40` | Using multiple tools | [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide) parallel calls | Primary |
| `ACAD/claude-with-google-vertex/41` | The batch tool | [The "batch tool" pattern (legacy)](../README.md#the-batch-tool-pattern-legacy); practice 2.7 | Primary |
| `ACAD/claude-with-google-vertex/42` | Tools for structured data | [2.4](../README.md#24-json-schemas-for-structured-output) | Primary |
| `ACAD/claude-with-google-vertex/43` | The text edit tool | [Anthropic-schema client tools in brief](../README.md#anthropic-schema-client-tools-in-brief); practice 2.7 | Primary |
| `ACAD/claude-with-google-vertex/44` | The web search tool | [Server tools: what changes in the loop](../README.md#server-tools-what-changes-in-the-loop) (Google-managed Google Cloud, i.e. Vertex AI, offers only the basic `web_search_20250305`); practice 2.7 | Primary |
| `ACAD/claude-with-google-vertex/45` | Quiz on tool use with Claude | [Self-check](../README.md#self-check), [More self-check questions](#more-self-check-questions) and homework Part A; the Academy quiz itself is taken on the Academy site | Supporting |
| `ACAD/claude-with-google-vertex/82` | Computer use | [Anthropic-schema client tools in brief](../README.md#anthropic-schema-client-tools-in-brief) (toolset GA on Claude API and Google Cloud) | Primary |
| `ACAD/claude-with-google-vertex/83` | How computer use works | Same section; practice 2.7 batch action | Primary |
| `ROLE/PROMPT/3` | Structured outputs and schema enforcement with validation and retry | [2.4](../README.md#24-json-schemas-for-structured-output), [2.5](../README.md#25-syntax-vs-semantic-errors) (`extract_with_retry`); practice 2.5; homework Ex 3–4 | Primary |
| `ROLE/AGENT/2` | Tool / function-calling design, tool errors, tool-result flow | [2.2](../README.md#22-tool-definition), [2.6](../README.md#26-the-client-side-tool-loop-and-tool_result-rules-expanded-beyond-the-guide), [2.7](../README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide); mini-project | Primary |

## More self-check questions

**Q1. (Multi-agent system, tool naming)** An internal help desk has a wiki agent and a ticketing agent. Questions such as "where is the runbook for the VPN outage?" land on the ticketing agent about one time in three. The ticketing agent's tool is `search_records`, described as "searches records and returns matching entries". The wiki agent's tool is `search_pages`, described as "searches pages and returns matching entries". What is the best fix?

- A) Rename the ticketing tool to `find_support_tickets` and describe it as searching open and closed support tickets by ticket ID, requester or keyword, and not wiki pages or runbooks
- B) Merge both tools into one `search` tool that queries the wiki and the ticket system together and returns both result sets
- C) Add a dozen few-shot routing examples to the coordinator prompt, half wiki questions and half ticket questions
- D) Add a line to the coordinator's system prompt: "Prefer the wiki agent for documentation questions"

<details><summary>Answer</summary>

**A.** The root cause is that the two names and descriptions say almost the same thing, so neither tells the model what it covers. Renaming and re-scoping one tool, with an explicit boundary, removes the overlap at the source (the same move as renaming `analyze_content` to `extract_web_results`). B hides two different data sources behind one vague tool. C and D add layers on top of a tool interface that is still ambiguous, and D is a keyword-style rule that misfires on tickets about documentation.
</details>

**Q2. (Structured data extraction, exam-blueprint semantics)** Documents arrive as invoices, receipts or contracts, and you can't tell which beforehand. You defined one extraction tool per type and you must always get structured output, never a prose answer. On a model that supports forced tool use, which `tool_choice` fits best?

- A) `{"type": "auto"}`
- B) `{"type": "any"}`
- C) `{"type": "tool", "name": "extract_invoice"}`
- D) `{"type": "none"}`

<details><summary>Answer</summary>

**B.** `any` guarantees that *some* tool is called while letting the model choose the right schema. A may return text. C forces the invoice schema onto receipts and contracts. D forbids tools entirely. (On Opus 5.5 / Sonnet 5.5 / Fable 5.1 / Mythos 5.1, which reject `any`, you would use `auto` + `strict: true` + a check that a tool was called, or a single `output_config.format` object schema with a `document_type` enum plus one nullable section per document type.)
</details>

**Q3. (Migration, current API)** A pipeline that sends `tool_choice={"type": "tool", "name": "extract_metadata"}` starts returning HTTP 400 after you switch the model to `claude-sonnet-5-5`. The tool exists only to get a metadata JSON object back. What is the best migration?

- A) Retry the request with exponential backoff
- B) Remove `tools` and ask for JSON in the prompt, then parse the text with a regex
- C) Replace the extraction tool with `output_config.format` (or `messages.parse()` with a Pydantic model) for the metadata schema
- D) Keep forced `tool_choice` and switch `thinking` to `{"type": "enabled"}`

<details><summary>Answer</summary>

**C.** Sonnet 5.5 rejects forced tool use, so a 400 is deterministic and retries (A) won't help. When the forced call only existed to extract JSON, structured outputs are the documented replacement and give a schema guarantee. B gives up all guarantees. D makes things worse: manual extended thinking also blocks forced tool use, and Sonnet 5.5 rejects `{"type": "enabled"}` thinking with a 400 anyway (it uses adaptive thinking).
</details>

**Q4. (Tool error handling)** Your logs show a pattern: when `lookup_order` returns `{"is_error": true, "content": "Not found"}`, Claude calls `lookup_order` again with the **same** order ID two or three times before it tells the customer anything. The backend answered correctly each time; the ID simply does not exist. What is the best fix?

- A) Drop the `is_error` flag on not-found results, so Claude reads "Not found" as ordinary data and stops retrying
- B) Lower the loop's `max_turns` to 2, so the repeated calls are cut off before they waste any more requests
- C) Wrap the backend call in exponential backoff inside `lookup_order`, so the tool itself retries before it answers
- D) Rewrite the error text: say the ID was checked and does not exist, that repeating the same call will not help, and what to do instead (ask the customer to confirm the ID)

<details><summary>Answer</summary>

**D.** Claude retries because "Not found" doesn't say whether the failure is temporary. An error message that states the failure is permanent and names the next step lets the model recover in one turn. A hides a real failure as if it were a normal answer. B cuts off legitimate multi-step work as well as the bad retries. C adds retries for an error that no retry can fix; backoff is for transient failures such as timeouts.
</details>

**Q5. (Agent harness, server tools)** Your research agent has the server `web_search` tool and a client tool `save_note`. One response ends with `stop_reason: "tool_use"` and contains a `server_tool_use` block (`web_search`, id `srvtoolu_01…`) with **no** result block, plus a `tool_use` block for `save_note`. What should the harness send next?

- A) Run `save_note`, then send a user message with only its `tool_result`, keeping the same `tools` array (including `web_search`)
- B) Run `save_note`, then send a user message with two `tool_result` blocks: one for `save_note` and an empty one for the web search
- C) Treat it as `pause_turn`: resend the assistant content unchanged, with no user message and no `tool_result` blocks
- D) Run the web search yourself with another search API, then return both results as `tool_result` blocks

<details><summary>Answer</summary>

**A.** When Claude calls a server tool and a client tool in the same parallel group, the API returns early so you can run the client tool first. The pending server call has no result block yet, and the API runs it after you send the client `tool_result` blocks. The resume request must still define `web_search`, or it fails with a 400. B answers a server tool, which the API does itself. C confuses this with `pause_turn` (which never leaves a client `tool_use` waiting). D replaces a tool Anthropic runs for you.
</details>

## Share your progress

```text
AI Solution Architect journey: Chapter 2, Claude tool use.

The model never runs your code. It asks, your code executes, and you report back.

3 takeaways:
1. Tool descriptions are the router. Vague descriptions = wrong tool.
2. strict: true fixes syntax, not truth. Totals can still be wrong, so validate.
3. Make fields nullable, or the model will invent data to fill them.

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #Anthropic #AIArchitecture #LLM #BuildInPublic
```
