# Chapter 4 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

There is no OpenAI architect exam (see the [OpenAI path README](../../README.md#certification-status-read-this-first)). This table maps the chapter to the Academy, bootcamp, and developer-track items and to role competencies in this repo's requirement lists. Items that the requirement list marks **[INFERRED]** come from a related bootcamp session or developer track, not from the course page itself.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `OAI/tracks/building-agents/7` | Built-in tools run on OpenAI infrastructure (except computer use); use a built-in tool before a custom function | [4.1](../README.md#41-the-tool-landscape-hosted-client-executed-and-mcp) (tool landscape, exam trap); [Cheat-sheet](../README.md#cheat-sheet); practice 4.1 | Primary |
| `OAI/tracks/building-agents/8` | Web search tool for knowledge past the training cutoff | [4.2](../README.md#42-web-search); practice 4.2; homework Ex 4 | Primary |
| `OAI/tracks/building-agents/9` | File search tool and managed vector stores, and the custom RAG steps they replace | [4.3](../README.md#43-file-search-and-vector-stores-hosted-rag); practice 4.3; homework Ex 3 | Primary |
| `OAI/tracks/building-agents/10` | Code interpreter tool (Python sandbox, file input and output) | [4.4](../README.md#44-code-execution-hosted-shell-code-interpreter-local-shell-apply_patch) (tool table, containers, status note); practice 4.4 | Primary |
| `OAI/tracks/building-agents/11` | Computer use loop: suggested action, you execute it, send a screenshot, next action | [4.5](../README.md#45-computer-use-and-image-generation); practice 4.5 (action policy, `computer_call_output`) | Primary |
| `OAI/tracks/building-agents/13` | MCP tool (hosted MCP servers) | [4.7](../README.md#47-remote-mcp-servers-in-the-responses-api), [4.8](../README.md#48-mcp-in-the-agents-sdk-and-the-agents-api), [4.10](../README.md#410-security-trust-approvals-and-prompt-injection); practice 4.7–4.8 and mini-project; homework Ex 1, 2, 6 (Ex 6: local MCP via the Agents SDK) | Primary |
| `OAI/api/build-with-rag/16` **[INFERRED]** | Embed chunks into a vector store; create and use OpenAI managed vector stores | [4.3](../README.md#43-file-search-and-vector-stores-hosted-rag) (Files → vector store, chunking, limits, cost); practice 4.3 | Primary |
| `OAI/api/build-with-rag/18` **[INFERRED]** | Retrieval optimization: process the query, rank and re-rank results | [4.3 Ranking and metadata](../README.md#ranking-and-metadata) (query processing, `ranking_options`, custom re-ranking); practice 4.3b (threshold vs recall, `rewrite_query`); homework Ex 7, Q11 | Primary |
| `OAI/api/build-with-rag/19` **[INFERRED]** | Use metadata in retrieval | [4.3 Ranking and metadata](../README.md#ranking-and-metadata) (attribute design, comparison and compound filters); practice 4.3 and 4.3b (filter evaluator); homework Ex 3 | Primary |
| `OAI/api/build-with-rag/21` **[INFERRED]** | Grounded answers with the Responses API plus File Search | [4.3](../README.md#43-file-search-and-vector-stores-hosted-rag) (code sample, `file_citation`, grounded answers); practice 4.3 (live answer with citations) and 4.3b (grounding check) | Primary |
| `OAI/bootcamp/api-builder/23` | RAG: vector stores and File Search | [4.3](../README.md#43-file-search-and-vector-stores-hosted-rag); practice 4.3 | Primary |
| `OAI/bootcamp/api-builder/24` | RAG: ranking and metadata | [4.3 Ranking and metadata](../README.md#ranking-and-metadata); practice 4.3b; homework Ex 3, Ex 7, Q11; [Self-check](../README.md#self-check) Q4 | Primary |
| `OAI/bootcamp/api-builder/26` | RAG: grounded answers using the Responses API and File Search | [4.3](../README.md#43-file-search-and-vector-stores-hosted-rag) (grounded answers); practice 4.3 and 4.3b (grounding check) | Primary |
| `ROLE/AGENT/11` | Computer use, browser, and sandboxed execution | [4.4](../README.md#44-code-execution-hosted-shell-code-interpreter-local-shell-apply_patch) (hosted containers, network policy, local shell sandboxing), [4.5](../README.md#45-computer-use-and-image-generation) (computer use safety); practice 4.4–4.5 | Primary |
| `OAI/api/build-with-rag/17` **[INFERRED]** | Choose between built-in File Search and a custom RAG pipeline | [4.3 Ranking and metadata](../README.md#ranking-and-metadata) (custom re-ranking path); [Cheat-sheet](../README.md#cheat-sheet) rows on `file_search` vs own retrieval | Supporting |
| `OAI/api/build-with-rag/20` **[INFERRED]** | Keep knowledge fresh | [4.3 Ranking and metadata](../README.md#ranking-and-metadata) ("Keep knowledge fresh"); [Self-check](../README.md#self-check) Q4; practice 4.3b (sync plan, live refresh); homework Q12 | Supporting |
| `OAI/bootcamp/api-builder/25` | RAG: keeping knowledge fresh | [4.3 Ranking and metadata](../README.md#ranking-and-metadata) ("Keep knowledge fresh"); [Self-check](../README.md#self-check) Q4; practice 4.3b; homework Q12 | Supporting |
| `OAI/tracks/building-agents/12` | Image generation tool (GPT Image) | [4.5](../README.md#45-computer-use-and-image-generation) (image generation); practice 4.5 | Supporting |
| `ROLE/AGENT/3` | MCP servers, clients, and connectors | [4.7](../README.md#47-remote-mcp-servers-in-the-responses-api)–[4.9](../README.md#49-secure-mcp-tunnel-private-servers-without-inbound-ports) (OpenAI as MCP client, Agents SDK, tunnels, legacy connectors); protocol basics live in the Claude chapter | Supporting |
| `ROLE/SAFE/10` | Securing agent and tool access | [4.4](../README.md#44-code-execution-hosted-shell-code-interpreter-local-shell-apply_patch) (network allowlists, `domain_secrets`), [4.7](../README.md#47-remote-mcp-servers-in-the-responses-api) (`authorization`, approvals), [4.10](../README.md#410-security-trust-approvals-and-prompt-injection); practice 4.10 (fingerprinting); homework Ex 5, Q10 | Supporting |

## More self-check questions

**Q1.** An Agents SDK service must use an MCP server that runs inside the company VPC and is not reachable from the internet. The service itself runs in the same VPC. Which option fits best?

- A) `HostedMCPTool` with the server's internal URL.
- B) `MCPServerStreamableHttp` pointed at the internal URL, passed in `mcp_servers`.
- C) A legacy `connector_id`.
- D) Copy the server's tools into function tools by hand.

<details><summary>Answer</summary>

**B.** With a local MCP server class, your runtime opens the connection, so it can reach anything your runtime can. A fails because OpenAI makes hosted MCP connections and cannot reach the VPC. C only covers a fixed list of SaaS services. D throws away MCP's automatic discovery and doubles maintenance.
</details>

**Q2.** ChatGPT and the Responses API must call an on-premises MCP server. Security forbids inbound firewall rules and public endpoints. What do you propose?

- A) A public reverse proxy with IP allowlisting.
- B) Secure MCP Tunnel: run `tunnel-client` next to the server and reference the tunnel with `tunnel_id` in the `mcp` tool.
- C) Rebuild the server as a set of function tools.
- D) Pass the tunnel's OpenAI-hosted endpoint URL as `server_url`.

<details><summary>Answer</summary>

**B.** The tunnel is outbound-only and keeps the server private, which matches both constraints. A creates the public ingress security refused. C does not help ChatGPT reach the system. D is explicitly wrong in the docs: use `tunnel_id`, not the hosted endpoint as `server_url`.
</details>

**Q3.** An agent has access to 120 functions across billing, CRM, shipping, and HR. Tool selection errors and input-token costs are rising. What is the most effective first change?

- A) Split the functions into namespaces with clear descriptions, mark rarely used ones `defer_loading: true`, and add `tool_search`.
- B) Shorten every function description to save tokens.
- C) Increase `max_output_tokens`.
- D) Merge everything into one `do_anything(action, payload)` function.

<details><summary>Answer</summary>

**A.** Tool search loads only what the task needs and namespaces give the model a clear map. B makes selection worse. C does not affect input tokens or selection. D destroys schema validation and makes errors harder to diagnose.
</details>

**Q4.** A reporting agent fetches 200 order records through a function, filters them by status, sums totals per region, and returns a 5-row table. Each step is predictable, nothing is written, and latency is too high. What helps most?

- A) Programmatic tool calling: allow the function to be called from a program so the model writes JavaScript that loops, filters, and aggregates, then returns the small table.
- B) Ask the model to call the function 200 times with `parallel_tool_calls=True`.
- C) Put all 200 records in the system prompt.
- D) Use `web_search` to find the totals.

<details><summary>Answer</summary>

**A.** This is PTC's sweet spot: predictable data flow, large intermediate results, a small structured output, and no writes. PTC needs a model that supports it (see [4.6](../README.md#46-large-tool-catalogs-tool-search-and-programmatic-tool-calling)); otherwise do the same reduction in your own code or in one function that returns the small table. B still pushes every record through the model's context. C does not scale and goes stale. D is unrelated.
</details>

**Q5.** A product team wants the model to use a code container that can `pip install` from PyPI and call a partner API with a bearer token. Which configuration is right?

- A) Hosted `shell` with an org-approved allowlist, a request `network_policy` listing only the PyPI domains and the partner domain, and `domain_secrets` for the partner token.
- B) Hosted `shell` with the token pasted into the user prompt.
- C) `code_interpreter` with no network policy; containers have internet access by default.
- D) Local shell on a developer laptop.

<details><summary>Answer</summary>

**A.** Network is off by default, the org allowlist bounds what requests may enable, and `domain_secrets` keeps the raw token out of the model's context. B leaks the secret into context and logs. C is wrong about the default. D moves risk onto a laptop with no isolation.
</details>

## Share your progress

```text
Week 4 on the OpenAI side: built-in tools + MCP.

3 takeaways:
1. Ask "who executes it?": hosted tools run at OpenAI, local shell/apply_patch/computer run in my sandbox, MCP runs on someone else's server
2. Remote MCP = one tool entry. Keep allowed_tools small and require approval for every write
3. Private server? Secure MCP Tunnel (outbound only) or connect from my own runtime

Same MCP server worked in Claude and OpenAI agents.
#OpenAI #MCP #AIArchitecture #LearningInPublic
```
