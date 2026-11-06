# Chapter 4 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Every requirement mapped to this chapter, from the Claude certification exam guides (CCAR-F, CCDV-F), the Anthropic Academy courses, and the role profile. *Primary* means this chapter is where the topic is taught; *Supporting* means it is covered here but owned elsewhere or has no content of its own.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `CCAR-F/MQC/3` | Design MCP tool and resource interfaces for backend integration | [4.1](../README.md#41-what-mcp-is) · [4.4](../README.md#44-the-iserror-flag-and-structured-errors) · [4.5](../README.md#45-resources-give-the-agent-a-map) · practice mini-project | Primary |
| `CCAR-F/D2/2.2/K1` | The `isError` flag pattern | [4.4](../README.md#44-the-iserror-flag-and-structured-errors) · practice 4.4 | Primary |
| `CCAR-F/D2/2.2/K2` | Transient vs validation vs business vs permission errors | [4.4](../README.md#44-the-iserror-flag-and-structured-errors) (category table) | Primary |
| `CCAR-F/D2/2.2/K3` | Why generic "Operation failed" blocks recovery | [4.4](../README.md#44-the-iserror-flag-and-structured-errors) · [Self-check](../README.md#self-check) Q2 | Primary |
| `CCAR-F/D2/2.2/K4` | Retryable vs non-retryable; metadata prevents wasted retries | [4.4](../README.md#44-the-iserror-flag-and-structured-errors) · practice 4.4 live loop | Primary |
| `CCAR-F/D2/2.2/S1` | Return `errorCategory`, `isRetryable`, message | [4.4](../README.md#44-the-iserror-flag-and-structured-errors) (`tool_error`) · homework Ex 3 | Primary |
| `CCAR-F/D2/2.2/S2` | `isRetryable: false` + customer-friendly business errors | [4.4](../README.md#44-the-iserror-flag-and-structured-errors) (business row) · practice 4.4 `request_refund` | Primary |
| `CCAR-F/D2/2.2/S4` | Access failure vs valid empty result | [4.4](../README.md#44-the-iserror-flag-and-structured-errors) (exam trap) · [Self-check](../README.md#self-check) Q4 · homework Ex 4 | Primary |
| `CCAR-F/D2/2.4/K1` | Project `.mcp.json` vs user `~/.claude.json` scope | [4.3](../README.md#43-configuring-mcp-servers) (scopes) | Primary |
| `CCAR-F/D2/2.4/K2` | `${VAR}` expansion in `.mcp.json` | [4.3](../README.md#43-configuring-mcp-servers) · practice 4.3 | Primary |
| `CCAR-F/D2/2.4/K3` | All servers' tools discovered at connect, available together | [4.2](../README.md#42-mcp-servers-clients-and-transports) (on connection) · practice 4.2 one host, many clients | Primary |
| `CCAR-F/D2/2.4/K4` | Resources as content catalogs to cut exploratory calls | [4.5](../README.md#45-resources-give-the-agent-a-map) · practice 4.5 live comparison | Primary |
| `CCAR-F/D2/2.4/S1` | Shared servers in project `.mcp.json` with env expansion | [4.3](../README.md#43-configuring-mcp-servers) · homework Ex 2 | Primary |
| `CCAR-F/D2/2.4/S2` | Personal servers in `~/.claude.json` | [4.3](../README.md#43-configuring-mcp-servers) (local and user scopes) · [More self-check questions](#more-self-check-questions) 4 | Primary |
| `CCAR-F/D2/2.4/S3` | Better MCP tool descriptions beat built-ins like Grep | [4.2](../README.md#42-mcp-servers-clients-and-transports) (exam trap) · [More self-check questions](#more-self-check-questions) 1 | Primary |
| `CCAR-F/D2/2.4/S4` | Community servers for standard integrations | [4.2](../README.md#42-mcp-servers-clients-and-transports) (build or reuse) · [4.3](../README.md#43-configuring-mcp-servers) (reuse before you build, vet a community server) · [cheat-sheet](../README.md#cheat-sheet) · [More self-check questions](#more-self-check-questions) 7 | Primary |
| `CCAR-F/D2/2.4/S5` | Expose content catalogs as resources | [4.5](../README.md#45-resources-give-the-agent-a-map) · [Self-check](../README.md#self-check) Q3 | Primary |
| `CCAR-F/APPX/TECH/2` | MCP technology list: servers, tools, resources, `isError`, `.mcp.json`, env expansion | [4.1](../README.md#41-what-mcp-is)–[4.5](../README.md#45-resources-give-the-agent-a-map) | Primary |
| `CCAR-F/APPX/IN/5` | Resources for catalogs, tools for actions, description quality | [4.5](../README.md#45-resources-give-the-agent-a-map) (choosing the primitive) · [4.2](../README.md#42-mcp-servers-clients-and-transports) | Primary |
| `CCAR-F/APPX/IN/6` | Project vs user scope, env expansion, multi-server access | [4.3](../README.md#43-configuring-mcp-servers) · [4.2](../README.md#42-mcp-servers-clients-and-transports) | Primary |
| `CCDV-F/D8/8.1/K2` | Configuration for external system interaction | [4.3](../README.md#43-configuring-mcp-servers) · [4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) (Agent SDK and connector configs) | Primary |
| `CCDV-F/D8/8.2/K1` | MCP server authoring | [4.1](../README.md#41-what-mcp-is) · [4.4](../README.md#44-the-iserror-flag-and-structured-errors) · [4.5 templates, MIME, completion](../README.md#resource-templates-mime-types-and-argument-completion) · practice mini-project | Primary |
| `CCDV-F/D8/8.2/K3` | Integrating MCP with Claude applications | [4.3](../README.md#43-configuring-mcp-servers) · [4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) · [4.6 SDK helpers](../README.md#option-c-shortcut-the-anthropic-sdks-mcp-helpers) | Primary |
| `CCDV-F/D8/8.2/K4` | MCP resources, tools, and prompts | [4.1](../README.md#41-what-mcp-is) · [4.5](../README.md#45-resources-give-the-agent-a-map) · [4.5 prompts in the client](../README.md#prompts-in-the-client-and-context-injection) | Primary |
| `ACAD/claude-platform-101/9` | MCP (platform overview lesson) | [4.1](../README.md#41-what-mcp-is) · [4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) | Supporting |
| `ACAD/claude-with-the-anthropic-api/LO10` | Develop MCP servers and clients | [4.1](../README.md#41-what-mcp-is)–[4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) · [4.6 SDK helpers](../README.md#option-c-shortcut-the-anthropic-sdks-mcp-helpers) · practice mini-project | Primary |
| `ACAD/claude-with-the-anthropic-api/60`, `ACAD/introduction-to-model-context-protocol/2`, `ACAD/claude-in-amazon-bedrock/61`, `ACAD/claude-with-google-vertex/64` | What MCP is, N×M → N+M, the three primitives | [4.1](../README.md#41-what-mcp-is) · practice 4.1 | Primary |
| `ACAD/claude-with-the-anthropic-api/61`, `ACAD/introduction-to-model-context-protocol/3`, `ACAD/claude-in-amazon-bedrock/62`, `ACAD/claude-with-google-vertex/65` | Hosts, clients, servers; the request flow | [4.2](../README.md#42-mcp-servers-clients-and-transports) (roles, one request end to end) · practice 4.2 | Primary |
| `ACAD/claude-with-the-anthropic-api/62`, `ACAD/introduction-to-model-context-protocol/4`, `ACAD/claude-in-amazon-bedrock/63`, `ACAD/claude-with-google-vertex/66` | Installing the SDK and tooling | [Prerequisites](../README.md#prerequisites) · practice helpers | Supporting |
| `ACAD/claude-with-the-anthropic-api/63`, `ACAD/introduction-to-model-context-protocol/5`, `ACAD/claude-in-amazon-bedrock/64`, `ACAD/claude-with-google-vertex/67` | Tools from decorators, docstrings, type hints, `Field` | [4.1](../README.md#41-what-mcp-is) (`Field`) · practice 4.1 `DocumentMCP` | Primary |
| `ACAD/claude-with-the-anthropic-api/64`, `ACAD/introduction-to-model-context-protocol/6`, `ACAD/claude-in-amazon-bedrock/65`, `ACAD/claude-with-google-vertex/68` | Testing a server with the MCP Inspector | [4.2](../README.md#42-mcp-servers-clients-and-transports) (MCP Inspector) · practice 4.2 inventory + Inspector CLI | Primary |
| `ACAD/claude-with-the-anthropic-api/65`, `ACAD/introduction-to-model-context-protocol/8`, `ACAD/claude-in-amazon-bedrock/66`, `ACAD/claude-with-google-vertex/69` | Writing an MCP client | [4.2](../README.md#42-mcp-servers-clients-and-transports) (`Client`) · [4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) option C · practice 4.6 · homework Ex 6 | Primary |
| `ACAD/claude-with-the-anthropic-api/66`, `ACAD/introduction-to-model-context-protocol/9`, `ACAD/claude-in-amazon-bedrock/67`, `ACAD/claude-with-google-vertex/70` | Direct and templated resources | [4.5](../README.md#45-resources-give-the-agent-a-map) · [4.5 templates, MIME, completion](../README.md#resource-templates-mime-types-and-argument-completion) · practice 4.5 | Primary |
| `ACAD/claude-with-the-anthropic-api/67`, `ACAD/introduction-to-model-context-protocol/10`, `ACAD/claude-in-amazon-bedrock/68`, `ACAD/claude-with-google-vertex/71` | Reading resources, MIME handling | [4.5 templates, MIME, completion](../README.md#resource-templates-mime-types-and-argument-completion) · practice 4.5 `decode_contents` · homework Ex 7 | Primary |
| `ACAD/claude-with-the-anthropic-api/68`, `ACAD/introduction-to-model-context-protocol/11`, `ACAD/claude-in-amazon-bedrock/69`, `ACAD/claude-with-google-vertex/72` | Prompt templates on the server | [4.5 prompts in the client](../README.md#prompts-in-the-client-and-context-injection) · practice 4.5 `format_document` | Primary |
| `ACAD/claude-with-the-anthropic-api/69`, `ACAD/introduction-to-model-context-protocol/12`, `ACAD/claude-in-amazon-bedrock/70`, `ACAD/claude-with-google-vertex/73` | Fetching prompts and sending them to Claude | [4.5 prompts in the client](../README.md#prompts-in-the-client-and-context-injection) · practice 4.5 `prompt_to_messages` | Primary |
| `ACAD/claude-with-the-anthropic-api/70`, `ACAD/introduction-to-model-context-protocol/14`, `ACAD/claude-in-amazon-bedrock/71`, `ACAD/claude-with-google-vertex/74` | Course recap | [cheat-sheet](../README.md#cheat-sheet) · practice Recap | Supporting |
| `ACAD/claude-with-the-anthropic-api/71`, `ACAD/claude-in-amazon-bedrock/72`, `ACAD/claude-with-google-vertex/75` | Course quiz | [Self-check](../README.md#self-check) · homework Part A | Supporting |
| `ACAD/claude-with-the-anthropic-api/75`, `ACAD/claude-in-amazon-bedrock/76`, `ACAD/claude-with-google-vertex/79` | Adding MCP servers to Claude Code | [4.3](../README.md#43-configuring-mcp-servers) (`claude mcp add`, scopes); Chapter 5 goes deeper | Supporting |
| `ACAD/claude-code-101/LO9` | Connect external tools to Claude Code with MCP servers | [4.3](../README.md#43-configuring-mcp-servers) | Primary |
| `ACAD/claude-code-101/11` | MCP in Claude Code | [4.3](../README.md#43-configuring-mcp-servers) | Primary |
| `ACAD/introduction-to-model-context-protocol/LO1` | Architecture; tool definition and execution move to MCP servers | [4.1](../README.md#41-what-mcp-is) · [4.2](../README.md#42-mcp-servers-clients-and-transports) (one request, end to end) | Primary |
| `ACAD/introduction-to-model-context-protocol/LO2` | Transport-agnostic communication; message types | [4.2](../README.md#42-mcp-servers-clients-and-transports) (transports, requests/responses/notifications) | Primary |
| `ACAD/introduction-to-model-context-protocol/LO3` | Full request-response flow, user → server → Claude | [4.2](../README.md#42-mcp-servers-clients-and-transports) (one request, end to end) · [4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) option C | Primary |
| `ACAD/introduction-to-model-context-protocol/LO4` | Python SDK decorators instead of hand-written schemas | [4.1](../README.md#41-what-mcp-is) · practice 4.1 | Primary |
| `ACAD/introduction-to-model-context-protocol/LO5` | Document read/edit tools with `Field` descriptions | [4.1](../README.md#41-what-mcp-is) (`Field`) · practice 4.1 `DocumentMCP` | Primary |
| `ACAD/introduction-to-model-context-protocol/LO6` | Test and debug with the MCP Inspector | [4.2](../README.md#42-mcp-servers-clients-and-transports) (MCP Inspector) · practice 4.2 | Primary |
| `ACAD/introduction-to-model-context-protocol/LO7` | Direct and templated resources | [4.5 templates, MIME, completion](../README.md#resource-templates-mime-types-and-argument-completion) · practice 4.5 | Primary |
| `ACAD/introduction-to-model-context-protocol/LO8` | Client resource reads with MIME handling (JSON, text) | [4.5 templates, MIME, completion](../README.md#resource-templates-mime-types-and-argument-completion) · practice 4.5 · homework Ex 7, Q11 | Primary |
| `ACAD/introduction-to-model-context-protocol/LO9` | Prompts as pre-crafted workflow instructions | [4.5 prompts in the client](../README.md#prompts-in-the-client-and-context-injection) · practice 4.5 `format_document` | Primary |
| `ACAD/introduction-to-model-context-protocol/LO10` | Tools = model, resources = app, prompts = user | [4.1](../README.md#41-what-mcp-is) (primitives table) · [4.5](../README.md#45-resources-give-the-agent-a-map) (choosing the primitive) | Primary |
| `ACAD/introduction-to-model-context-protocol/LO11` | Autocomplete and context injection | [4.5 templates, MIME, completion](../README.md#resource-templates-mime-types-and-argument-completion) (completion) · [4.5 prompts in the client](../README.md#prompts-in-the-client-and-context-injection) · practice 4.5 · homework Ex 8, [More self-check questions](#more-self-check-questions) 5 | Primary |
| `ACAD/introduction-to-model-context-protocol/1` | Course introduction | [Chapter intro](../README.md#why-this-matters-for-a-solution-architect) | Supporting |
| `ACAD/introduction-to-model-context-protocol/7` | Course survey (no learning content) | Nothing to teach; complete it on the Academy site | Supporting |
| `ACAD/introduction-to-model-context-protocol/13` | Course final assessment | [Self-check](../README.md#self-check) · homework Part A | Supporting |
| `ACAD/claude-in-amazon-bedrock/LO7` | Define MCP tools, resources, prompts; use them from a client | [4.1](../README.md#41-what-mcp-is) · [4.5](../README.md#45-resources-give-the-agent-a-map) · [4.5 prompts in the client](../README.md#prompts-in-the-client-and-context-injection) · [4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) | Primary |
| `ACAD/claude-with-google-vertex/LO8` | Custom MCP tools, resources, and prompt templates | [4.1](../README.md#41-what-mcp-is) · [4.5](../README.md#45-resources-give-the-agent-a-map) · [4.5 prompts in the client](../README.md#prompts-in-the-client-and-context-injection) | Primary |
| `ROLE/AGENT/3` | Build and secure MCP servers, clients and connectors | [4.2](../README.md#42-mcp-servers-clients-and-transports) · [4.3](../README.md#43-configuring-mcp-servers) · [4.4](../README.md#44-the-iserror-flag-and-structured-errors) · [4.6](../README.md#46-beyond-claude-code-mcp-from-the-agent-sdk-and-the-messages-api) · [4.6 SDK helpers](../README.md#option-c-shortcut-the-anthropic-sdks-mcp-helpers) | Primary |

## More self-check questions

**Q1.** In a developer-productivity agent, you added an MCP `code_search` tool backed by a semantic index of the whole monorepo. The agent keeps using the built-in `Grep` tool instead and misses relevant results. What should you do first?

- A) Remove `Grep` from the agent's tools.
- B) Strengthen `code_search`'s description: say what it searches (the semantic index across all services), when to prefer it over `Grep`, and give example queries.
- C) Add a routing classifier that decides between `Grep` and `code_search`.
- D) Move `code_search` to a separate subagent.

<details><summary>Answer</summary>

**B.** Descriptions are the main signal the model uses to choose tools; the MCP tool must explain what it offers that the built-in tool does not. A removes a tool that is still the right choice for exact-string searches. C and D add architecture before the cheap, root-cause fix has been tried.
</details>

**Q2.** A travel-booking agent uses two vendor MCP servers that you cannot change. One returns fares as integer cents (`18950`), the other as strings with a currency sign (`"$189.50"`). One gives flight time in minutes, the other as an ISO 8601 duration (`"PT2H30M"`). The agent often picks the wrong "cheapest" or "shortest" option. What is the most maintainable fix?

- A) Ask both vendors to change their output format, and wait for their next release.
- B) Add a `PostToolUse` hook that converts every result to one format before the model sees it.
- C) Send every search result through a second, cheaper model call that rewrites it before the main agent reads it.
- D) Fork both servers and change their output.

<details><summary>Answer</summary>

**B.** A hook is plain code: it runs on every result, sits in one place, and works for servers you do not control. A leaves the agent broken until someone else acts, and you do not control their roadmap. C adds cost and latency, and a model can still misread a value. D leaves you two forks to keep in sync with upstream.
</details>

**Q3.** A product team wants a Messages API backend (no Claude Code, no Agent SDK) to call an internal MCP server that currently runs only as a local stdio process on a developer laptop. They plan to use the MCP connector (`mcp_servers` in the request). What is the issue?

- A) None; the connector can launch stdio servers by command.
- B) The connector only works with Claude Code.
- C) The connector only reaches servers over HTTP and supports tools only, so the server must run with Streamable HTTP (with auth), or the team must run its own MCP client bridge.
- D) The connector supports resources but not tools.

<details><summary>Answer</summary>

**C.** The Messages API cannot reach a stdio process on someone's laptop, and the connector exposes only tools. There are three routes: deploy the server publicly with Streamable HTTP; run it with Streamable HTTP inside the company network and reach it through **MCP tunnels** (research preview, Claude API only); or run an MCP `Client` in the backend and pass tools through a normal tool-use loop (section 4.6, option C).
</details>

**Q4.** A developer wants to try an experimental MCP server in one repository without affecting teammates or other projects. Which configuration fits best?

- A) Add it to the committed `.mcp.json`.
- B) Add it with `claude mcp add` at the default local scope.
- C) Add it at user scope.
- D) Ask the team lead to add it to managed settings.

<details><summary>Answer</summary>

**B.** Local scope is private to the developer and limited to the current project, which matches the request exactly. A affects every teammate. C is private but loads in every project. D is for organization-wide policy, not experiments.
</details>

**Q5.** In a chat app built on your own MCP client, users attach documents by typing `@` and a document id. They often mistype the id, and the agent then wastes a turn calling `read_document` with a wrong id before it can answer. Which change fixes the cause?

- A) Add a completion handler for the `doc_id` parameter of the `docs://documents/{doc_id}` template, call it as the user types, and inject the chosen document into the user turn.
- B) Annotate `read_document` with `read_only_hint=True`.
- C) Let the agent retry `read_document` with fuzzy-matched ids.
- D) Expose every document as its own tool.

<details><summary>Answer</summary>

**A.** Completion catches the mistake while the user is typing, and context injection hands Claude the document up front, so no exploratory tool call is needed. B changes a UI hint, not behavior. C keeps the wasted turns. D bloats the tool list, which hurts selection.
</details>

**Q6.** A Messages API backend runs its own MCP client against a local stdio server and uses the Anthropic SDK's `mcp_resource_to_content()` to attach resources to the user turn. Text and PDF resources work, but reading `schema://tables` (served as `application/json`) raises `UnsupportedMCPValueError`. What is the right fix?

- A) Switch to the MCP connector, which supports resources.
- B) Convert the JSON resource to a `text` content block in your own code (or upload it with `mcp_resource_to_file` and the Files API), and keep the helper for the types it supports.
- C) Remove the `mime_type` from the resource so it is served without a label.
- D) Expose the schema as a tool instead and let Claude call it.

<details><summary>Answer</summary>

**B.** The helper converts only what Claude accepts as a content block (`text/*`, PDF, four image types), so JSON needs your own conversion or a file upload. A is wrong twice: the connector is tools only and cannot reach a stdio server. C mislabels the data. The SDK would then advertise it as `text/plain`, and every other client that trusts the label loses the JSON type. D turns stable background context back into exploratory tool calls (4.5).
</details>

**Q7.** A team wants Claude Code to read and update tickets in their issue tracker, a widely used SaaS product. They also want it to run their own release checklist, which touches three internal services. An engineer proposes writing custom MCP servers for both. A popular community server for the tracker exists, but nobody on the team knows who maintains it. What is the best plan?

- A) Write custom servers for both, so the team controls all of the code.
- B) Add the most popular community tracker server to `.mcp.json` right away, and write a custom server for the release checklist.
- C) Use the tracker vendor's own server if there is one, or the community server after vetting it (maintainer, recent activity, what it can change, which token scopes it needs). Write a custom server only for the release checklist.
- D) Skip MCP and let Claude call the tracker's REST API with `curl` through Bash.

<details><summary>Answer</summary>

**C.** Standard integrations should reuse an existing server, and custom code is for the team-specific workflow. A community server is still code that runs with your credentials, so vet it first. A means owning and updating code that others already maintain. B gets the split right but skips the vetting, and popularity is not a review. D gives up named, described tools and turns every call into a raw shell command to approve and audit.
</details>

## Share your progress

```text
MCP finally clicked for me: it's one protocol so an integration is built once and works in every AI app.

3 takeaways from week 4 of my AI Solution Architect journey:
1. Tools = model decides, Resources = app decides, Prompts = user decides
2. Team config goes in .mcp.json, secrets come in through ${ENV_VARS}, never committed
3. "Operation failed" is a bug. Errors need a category + retryable flag

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#MCP #ClaudeAI #AIArchitecture #LearningInPublic
```
