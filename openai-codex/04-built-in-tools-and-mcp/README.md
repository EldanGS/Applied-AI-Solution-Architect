# Chapter 4 — Built-in Tools and MCP

> Claude counterpart: [Chapter 4 — Model Context Protocol (MCP)](../../anthropic-claude/04-model-context-protocol/README.md) · Academy course(s): Build with Retrieval-Augmented Generation, Design and Build Agentic Systems · **Est. time:** 7–9 hours (reading + notebooks) · **Status:** [ ] not started

On the OpenAI platform, web search, retrieval over your documents, a sandboxed shell, image generation, and a full MCP client run on OpenAI's side when you add one entry to the `tools` array. The architect's job is to decide which work runs on OpenAI's infrastructure, which stays in your runtime, and which needs a human approval in between. MCP itself is the same open protocol on both platforms, so its fundamentals stay in the [Claude chapter](../../anthropic-claude/04-model-context-protocol/README.md); this chapter covers the OpenAI side.

## What you'll learn

- Classify every tool as **hosted**, **client-executed**, or **MCP** (plus programmatic tool calling, a hosted program that calls your client-executed functions), and know who runs the code.
- Use `web_search` with filters and citations, and build hosted RAG with vector stores and `file_search`.
- Choose between hosted `shell`, `code_interpreter`, local `shell`, and `apply_patch`, and lock down network access.
- Connect MCP servers through the `mcp` tool or the Agents SDK, handle approvals, and reach private servers with Secure MCP Tunnel.
- Apply the MCP trust model: least-privilege tools, approvals for writes, logging.

## Prerequisites

- [Chapter 3 — Agents SDK and Agents API](../03-agents-sdk-and-agents-api/README.md) — `Agent`, `Runner`, function tools, human review.
- [00-prerequisites](../../00-prerequisites/README.md) — venv and `.env` with `OPENAI_API_KEY`. Install: `pip install "openai>=3.24" "openai-agents>=0.23" "mcp>=2.3" python-dotenv`.
- Optional: the [Claude chapter](../../anthropic-claude/04-model-context-protocol/README.md) for MCP primitives and transports.

---

## Concepts

All examples use `client = OpenAI()` and `MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")`. The `gpt-6-luna` model page lists web search, file search, code interpreter, hosted shell, apply patch, computer use, image generation, MCP, and tool search as supported (not programmatic tool calling, see 4.6).

### 4.1 The tool landscape: hosted, client-executed, and MCP

Every entry in the `tools` array falls into one group. The group tells you **who runs the code**, which tells you where data goes and who owns safety.

| Group | Who executes | Tools (`type`) | Your loop |
|---|---|---|---|
| **Hosted** | OpenAI | `web_search`, `file_search`, `code_interpreter`, hosted `shell`, `image_generation`, `tool_search` | Nothing to run; call and result come back as output items |
| **Hosted program, client tools** | OpenAI runs the JavaScript; you run the functions it calls | `programmatic_tool_calling` | Return each `function_call_output` with the same `call_id` and unchanged `caller` (4.6) |
| **Client-executed** | Your application | `function`, local `shell`, `apply_patch`, `computer`, client `tool_search` | Run the call, return the matching `*_output` item with the same `call_id` |
| **MCP** | A remote MCP server, called by OpenAI's MCP client | `mcp` (`server_url`, `tunnel_id`, or legacy `connector_id`) | Usually nothing, except approvals |

You observe what happened through output items in `response.output`, such as `web_search_call`, `file_search_call`, `shell_call`, `computer_call`, `mcp_call`, and the final `message`. **Pricing** (tokens are always billed on top): web search $10.00 per 1k calls; file search $2.50 per 1k calls plus storage $0.10/GB/day after 1 GB free; hosted containers $0.03 (1 GB) to $1.92 (64 GB) per 20-minute session; remote MCP has no per-call fee.

> **Exam trap:** "We need the model to search the web, so we must build a search function." No: `web_search` is hosted, and so are retrieval (`file_search`) and code execution. Build your own function only when the hosted tool cannot meet a requirement (an internal index, a data-residency rule, a custom ranking).

### 4.2 Web search

`{"type": "web_search"}` lets the model decide when to search. Reasoning models can search, open pages, and search within pages, so one request may hold several `web_search_call` items.

```python
response = client.responses.create(
    model=MODEL,
    tools=[{
        "type": "web_search",
        "filters": {"allowed_domains": [
            "modelcontextprotocol.io", "developers.openai.com"]},
        "user_location": {"type": "approximate",
                          "country": "DE", "city": "Berlin"},
        "search_context_size": "medium",   # low | medium | high
    }],
    tool_choice="auto",          # "required" forces at least one call
    include=["web_search_call.action.sources"],  # every URL consulted
    input="Summarize the transports in the current MCP spec, with citations.",
)
```

`filters` takes up to 100 `allowed_domains` or up to 100 `blocked_domains`, without `https://` (subdomains are included). `blocked_domains` is documented but not yet in the Python SDK's typed params, so pass it as a plain dict key. **Citations** arrive as `url_citation` annotations on the `message`. When you show web results to users, the docs require citations to be **clearly visible and clickable**.

> **Gotcha:** With `tool_choice: "auto"` the model may answer from memory. If an answer must be grounded in a fresh search, set `"required"` and check that a `web_search_call` item exists.

### 4.3 File search and vector stores (hosted RAG)

`file_search` is OpenAI's hosted retrieval: semantic plus keyword search over files in one or more **vector stores**. The flow is Files API → vector store (chunk, embed, index) → `file_search` tool → answer with `file_citation` annotations. On the Claude side you bring your own vector database.

```python
vector_store = client.vector_stores.create(
    name="support-policies",
    expires_after={"anchor": "last_active_at", "days": 7},
)
with open("refund_policy.md", "rb") as f:
    client.vector_stores.files.upload_and_poll(  # upload + wait
        vector_store_id=vector_store.id,
        file=f,
        attributes={"region": "EU", "doc_type": "policy"},
    )

response = client.responses.create(
    model=MODEL,
    input="Can an EU customer return opened headphones?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store.id],
        "max_num_results": 4,
        "filters": {"type": "eq", "key": "region", "value": "EU"},
    }],
    include=["file_search_call.results"],  # return retrieved chunks
)
```

**Chunking** defaults to 800-token chunks with 400-token overlap (change it with `chunking_strategy`). Limits are 512 MB and 5,000,000 tokens per file. Indexing is asynchronous, so use the `*_and_poll` helpers. Storage is billed daily, so set `expires_after` on short-lived stores. `client.vector_stores.search(...)` returns raw retrieval without a model call, which helps you evaluate retrieval on its own.

#### Ranking and metadata

**Design attributes up front.** Each file holds an `attributes` map (at most 16 keys). Plan keys for every rule you must enforce: `tenant`, `region`, `doc_type`, `effective_at` (a Unix timestamp), `is_current`, `source_id`, `version`. Use numbers for dates, because range operators work on numbers.

**Filter on metadata.** `filters` is a comparison filter (`eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `nin`) or a compound filter (`and`, `or`) that nests others. Filters run *before* ranking, so they are a hard boundary, not a hint. Use them for tenancy and region rules instead of prompt instructions.

**Tune ranking** with `ranking_options`. Keep `ranker` on `"auto"`. A higher `score_threshold` (0.0–1.0) gives fewer, more relevant chunks, but can drop the chunk that held the answer, so tune it on a labeled question set. In `hybrid_search`, raise `text_weight` for part numbers and exact names and `embedding_weight` for paraphrased questions. More `max_num_results` (1–50) costs more tokens.

**Query processing.** With `file_search`, the model writes its own queries (see `file_search_call.queries`). With `vector_stores.search`, set `rewrite_query=True` to turn a chatty question into a search query. For your own re-ranking (business rules, recency boosts), retrieve with `vector_stores.search`, re-rank in code, and pass the chunks to `responses.create` yourself. You then own citation rendering.

**Keep knowledge fresh.** Files cannot be edited in place. Refresh like this:

1. Upload the new version with `version`, `effective_at`, and `is_current=True`; wait until it is `completed`.
2. Set `is_current: False` on the old file with `client.vector_stores.files.update(...)` (metadata only).
3. Remove the old file. Removal is eventually consistent, so the `is_current` filter covers the gap.
4. Run this from a scheduled sync that compares a content hash per document, so unchanged documents are skipped.

**Grounded answers.** Scope retrieval with filters, tell the model to answer only from retrieved content and to say when the documents do not cover the question, and check that the final `message` has at least one `file_citation` before you show a policy answer.

### 4.4 Code execution: hosted shell, code interpreter, local shell, apply_patch

Pick by **where commands run** and **what kind of change** you need.

| Tool | Runs where | Best for |
|---|---|---|
| `shell` + `environment: {"type": "container_auto"}` | OpenAI-hosted container | General terminal work, multi-language scripts, skills |
| `code_interpreter` + `container: {"type": "auto"}` | OpenAI-hosted container | Python data analysis, charts, file transforms (files return as `container_file_citation`) |
| `shell` + `environment: {"type": "local"}` | **Your** machine or sandbox | Your repo and internal tooling; you run `shell_call` and return `shell_call_output` |
| `apply_patch` | **Your** filesystem | Structured file edits (create, update, delete) as V4A diffs |

**Hosted containers** come in `1g` (default), `4g`, `16g`, and `64g`. A container expires after 20 minutes without activity and its data is deleted, so download files from `/mnt/data` first. **Network access is off by default.** An org admin sets an allowlist in the dashboard, and a request can only narrow it with `network_policy`. `domain_secrets` inject credentials: the model sees a placeholder such as `$API_KEY`, never the raw value.

```python
tools = [{"type": "shell", "environment": {
    "type": "container_auto",
    "network_policy": {"type": "allowlist", "allowed_domains": [
        "pypi.org", "files.pythonhosted.org"]},
}}]
```

**Local shell and apply_patch.** You return `stdout`, `stderr`, and an `outcome` for each `shell_call`, and `status: "completed"` or `"failed"` for each `apply_patch_call`. Keep non-zero exit output so the model can recover. Setting `cwd` confines nothing: **always sandbox** model-generated commands in a container or VM that mounts only the workspace, and reject paths that leave it. Never allowlist a domain an attacker can write to (a paste site, a public bucket): that turns prompt injection into data exfiltration.

> **Note:** `code_interpreter` is still documented and supported on current model pages, but the "Using tools" page now lists `shell` instead (checked 2026-10-03; no deprecation announced). Prefer `shell` for new general work; `code_interpreter` is fine for Python-only analysis that returns charts and files.

### 4.5 Computer use and image generation

**Computer use** lets a model operate a browser or desktop. You always provide the environment and execute the actions. There are two paths:

- **Code execution** (the computer-use guide recommends it for the flagship `gpt-6-astra`; the `computer` tool below also works on `gpt-6-luna`): a function tool accepts a script (for example Playwright); your sandbox runs it and returns output and screenshots.
- **The `computer` tool**: the model returns a `computer_call` with an ordered `actions` list (`click`, `type`, `scroll`, `screenshot`, and more). You execute them and return a `computer_call_output` with a screenshot. The model then suggests the next action.

Safety checklist: run in an **isolated browser or VM** with a site allowlist; treat **screen content as untrusted**; **confirm consequential actions** (purchases, sending data, destructive changes); and **bound the run** with step, time, and cost limits.

**Image generation** (`{"type": "image_generation", "model": "gpt-image-2.5-flare"}`) creates or edits images mid-conversation. The result arrives base64-encoded in an `image_generation_call` item. Use `gpt-image-2.5-sunburst` for precise edits and `gpt-image-2.5-flare` for fast generation.

### 4.6 Large tool catalogs: tool search and programmatic tool calling

**Tool search** (`{"type": "tool_search"}`) fixes **too many tools**. Mark functions `defer_loading: true`, ideally inside a **namespace** with a clear description (fewer than 10 functions each), or defer a whole MCP server. The model first sees only names and descriptions and loads details through `tool_search_call` → `tool_search_output`.

```python
crm = {
    "type": "namespace",
    "name": "crm",
    "description": "CRM tools for customer lookup and order management.",
    "tools": [{
        "type": "function", "name": "list_open_orders",
        "description": "List open orders for a customer ID.",
        "defer_loading": True,
        "parameters": {"type": "object",
            "properties": {"customer_id": {"type": "string"}},
            "required": ["customer_id"], "additionalProperties": False},
    }],
}
tools = [crm, {"type": "tool_search"}]   # hosted tool search
```

**Programmatic tool calling (PTC)** fixes **too many round trips**. Add `{"type": "programmatic_tool_calling"}` and set `allowed_callers` on each eligible tool. The model writes JavaScript that calls your tools in loops and returns one reduced result. Programs run in an isolated V8 runtime with no network or filesystem.

Your loop: run each client-owned `function_call`, return its output with the same `call_id` **and the `caller` copied unchanged**, and repeat until the response holds the final `message`. Use PTC when many results must be filtered or aggregated in code. Use direct calls when each result needs fresh model judgment or the call writes data. When checked on 2026-11-06, no model page (including `gpt-6-luna`) listed PTC as supported, so confirm it with a small test request first. Without PTC, do the same reduction in your own code or in one function that returns the small result.

### 4.7 Remote MCP servers in the Responses API

The `mcp` tool turns the Responses API into an **MCP client**. OpenAI connects to a remote server (Streamable HTTP or HTTP/SSE), imports its tools, and calls them. You write no client code. The example uses the public DeepWiki server, which needs no authentication.

```python
mcp_tool = {
    "type": "mcp",
    "server_label": "deepwiki",            # your name for this server
    "server_url": "https://mcp.deepwiki.com/mcp",
    "allowed_tools": ["read_wiki_structure", "ask_wiki_question"],
    "require_approval": "always",          # the default behavior
}
response = client.responses.create(
    model=MODEL, tools=[mcp_tool],
    input="What transports does modelcontextprotocol/python-sdk support?",
)
# Answer the mcp_approval_request item in a new request
# (present because require_approval="always")
request_item = next(i for i in response.output if i.type == "mcp_approval_request")
approval = {"type": "mcp_approval_response",
            "approval_request_id": request_item.id,
            "approve": True}   # False to deny; optional "reason"
followup = client.responses.create(
    model=MODEL, previous_response_id=response.id,
    tools=[mcp_tool],   # send the tool config (and authorization) again
    input=[approval],
)
```

| Field | Purpose |
|---|---|
| `server_url` / `tunnel_id` / `connector_id` | A public server, a [Secure MCP Tunnel](#49-secure-mcp-tunnel-private-servers-without-inbound-ports), or a legacy connector |
| `allowed_tools` | Tool names, or `{"tool_names": [...], "read_only": true}` |
| `require_approval` | `"always"`, `"never"`, or per tool: `{"always": {"tool_names": [...]}, "never": {"tool_names": [...]}}` |
| `authorization` | OAuth token. Not stored, so send it on **every** request |
| `defer_loading` | Load this server's tools only through tool search (4.6) |

**The item flow.** `mcp_list_tools` records the imported tools; keep it in context so the list is not fetched each turn. `mcp_approval_request` (`id`, `name`, `arguments`, `server_label`) asks for your decision; if you auto-approve in code, key on `(server_label, name)`, never the name alone. `mcp_call` shows the arguments, the `output`, and any `error`. **Reduce approvals safely.** Skip approvals only for a trusted server's read-only tools, keep writes on approval, and keep `allowed_tools` small, because every imported definition costs input tokens on every turn.

**Legacy connectors** (`connector_id`, such as `connector_gmail`) are **deprecated for models released after September 1, 2026**. Use the vendor's official MCP server via `server_url`, or `tunnel_id` for a private one.

**Reuse before you build.** For a standard integration such as an issue tracker, connect the vendor's server or a well-maintained community server. Write a custom server only for workflows specific to your team. **Vet a community server first:** check who maintains it and how actively, which tools it exposes (reads, writes, deletes), and what credentials and data it receives (4.10).

> **Gotcha:** The `mcp` tool imports **tools only**. MCP resources and prompts are not surfaced. Expose a read-only tool instead, or connect the server from your own runtime (4.8).

### 4.8 MCP in the Agents SDK (and the Agents API)

The Agents SDK offers MCP in two ways. The difference is **who opens the connection**.

| Class | Connection made by | Use for |
|---|---|---|
| `HostedMCPTool(tool_config={...})` in `tools=[...]` | OpenAI (the `mcp` tool from 4.7) | Public remote servers |
| `MCPServerStdio(params={...})` in `mcp_servers=[...]` | Your process, as a subprocess | Local tools, local files or credentials |
| `MCPServerStreamableHttp(params={"url": ...})` | Your process | Private or internal HTTP servers your runtime can reach |

```python
# Run in a notebook (top-level await) or wrap in async def main() + asyncio.run(main()).
# orders_server.py is the server written in 01_practice.ipynb, section 4.8.
import sys
from agents import Agent, Runner
from agents.mcp import MCPServerStdio, create_static_tool_filter

async with MCPServerStdio(
    name="orders",
    params={"command": sys.executable, "args": ["orders_server.py"]},
    cache_tools_list=True,  # skip tools/list; only if the list is fixed
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["lookup_order", "cancel_order"]),
    require_approval={"always": {"tool_names": ["cancel_order"]}},
) as orders:
    agent = Agent(name="Support", model=MODEL, mcp_servers=[orders],
                  instructions="Look up orders before answering.")
    result = await Runner.run(agent, "Cancel ORD-1001, it was a duplicate.")
    while result.interruptions:     # a resumed run can pause again
        state = result.to_state()
        for item in result.interruptions:
            print("Needs approval:", item.name, item.arguments)
            state.approve(item)     # or state.reject(item)
        result = await Runner.run(agent, state)
    print(result.final_output)
```

- **The server** is an ordinary MCP server built with the MCP Python SDK, as in the [Claude chapter, 4.1–4.4](../../anthropic-claude/04-model-context-protocol/README.md#41-what-mcp-is). The class is `MCPServer`; the old `from mcp.server.fastmcp import FastMCP` import fails on every mcp 2.x release (FastMCP was renamed to `MCPServer` in 2.0).
- **Hosted MCP approvals** use `HostedMCPTool(..., on_approval_request=fn)`, where `fn` returns `{"approve": bool, "reason": str}`.
- **The managed Agents API (beta)** configures MCP per agent with a `transport` and a separate `connection_origin`. The default `"service"` connects from OpenAI; `"environment"` connects from the session's environment (type `self_hosted` or `openai_hosted`), so a server on a private network can be reached.

> **Exam trap:** "Our agent must call an MCP server on the developer's laptop or inside our VPC." `HostedMCPTool` and the `mcp` tool cannot reach it, because OpenAI makes that connection. Use `MCPServerStdio` or `MCPServerStreamableHttp` from your runtime, or Secure MCP Tunnel (4.9) if OpenAI-hosted surfaces must call it.

### 4.9 Secure MCP Tunnel: private servers without inbound ports

Secure MCP Tunnel connects a **private, on-premises, or firewalled** MCP server to ChatGPT, Codex, the Responses API, and other OpenAI surfaces without exposing it to the internet.

- Create a tunnel in Platform settings and run `tunnel-client` **inside** the network that can reach the server. It needs only **outbound** HTTPS to `api.openai.com:443`, with no inbound firewall rule. It long-polls for MCP work, forwards each JSON-RPC request to the server (stdio or an internal URL), and posts the response back.
- In the `mcp` tool you pass **`tunnel_id`**, **not** `server_url`: `{"type": "mcp", "server_label": "private_orders", "tunnel_id": "tunnel_0123..."}`.
- It is not for public plugin distribution, it does not tunnel your OAuth authorization server, and it does not make an untrusted server safe.

> **Exam trap:** "Security will not open an inbound port, but the Responses API must call our on-prem MCP server." The answer is Secure MCP Tunnel with `tunnel_id`. If the caller is your own backend, the simpler answer is `MCPServerStreamableHttp` from your runtime.

### 4.10 Security: trust, approvals, and prompt injection

A malicious remote server can **exfiltrate anything that enters the model's context**. Every tool that reads outside content (web pages, files, MCP outputs, screens) is also a prompt-injection channel.

| Risk | Control |
|---|---|
| Untrusted or aggregator MCP servers | Prefer official servers hosted by the vendor; keep approvals on and log every `mcp_call`'s arguments while you evaluate |
| Harmful action after injected text | Minimal `allowed_tools`; `require_approval` for every write |
| Server changes tools later ("rug pull") | Hash and diff `mcp_list_tools` between deployments; alert on changes |
| Data residency | Data sent to an MCP server follows **that server's** policies |
| Annotations treated as enforcement | `read_only` filters trust the server's own hints; enforce limits server-side |

---

## Lesson code

Video-lesson code: [../../presentations/04-mcp/code/](../../presentations/04-mcp/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Work through 4.1–4.10 live and offline, then build an orders support agent over MCP with a tool filter and an approval-gated `cancel_order`. |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: a 12-question quiz, 7 auto-checked exercises, an architecture scenario, and a scorecard. |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Need fresh public information | `web_search` (with `allowed_domains` if sources matter) | A custom scraping function |
| Answers must come from our documents | `file_search` + vector store with attributes and filters | Stuffing documents into the prompt |
| Must keep documents in our own store or region | Your own retrieval as a function tool or MCP server | `file_search` |
| Source documents change weekly | Scheduled sync: new version + `is_current`, then remove the old file | Never removing old versions |
| Python analysis with charts/files | `code_interpreter` or hosted `shell` | Local execution |
| Work on our repo or internal tools | Local `shell` / `apply_patch` in your sandbox | Hosted containers |
| Public SaaS with an official MCP server | Responses `mcp` tool or `HostedMCPTool` | A bespoke integration |
| Server on a laptop or in the VPC, called by your backend | `MCPServerStdio` / `MCPServerStreamableHttp` | Hosted MCP |
| Private server, called by ChatGPT, Codex, or the Responses API | Secure MCP Tunnel (`tunnel_id`) | Opening an inbound port |
| Write or destructive MCP tools | `require_approval` for those tools; read-only on `never` | `"never"` for the whole server |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Building what is hosted:** a custom search, RAG, or sandbox when `web_search`, `file_search`, or `shell` would do.
- **Relying on prompts for data scoping** instead of attributes plus `filters`.
- **Never retiring old document versions,** so the model quotes both; mark and filter `is_current`.
- **`require_approval: "never"` on a whole server** that has write tools.
- **Forgetting `authorization` on follow-up requests** (it is never stored).
- **Using `HostedMCPTool` for a server OpenAI cannot reach** (localhost, VPC) instead of a local MCP server class or a tunnel.

## Self-check

**Q1.** A support assistant must answer from 4,000 internal policy PDFs in two regions (EU and US). Testers find EU customers sometimes get US rules. What is the best fix?

- A) Add "Only use EU documents for EU customers" to the instructions.
- B) Put the EU and US PDFs in one vector store, add a `region` attribute to every file, and pass a `filters` clause on `file_search` based on the customer's region.
- C) Raise `max_num_results` so the model sees both versions and can choose.
- D) Switch to `web_search` restricted to the company domain.

<details><summary>Answer</summary>

**B.** Attribute filters stop the wrong chunks from ever reaching the model. A depends on the model obeying an instruction while wrong content is in context. C makes the mix-up more likely. D searches the public web, not the internal policies.
</details>

**Q2.** Your backend uses the Responses API `mcp` tool with a CRM server that requires OAuth. The first request returns an `mcp_approval_request`. The follow-up request with `previous_response_id` and an `mcp_approval_response` fails with an authentication error from the MCP server. Why?

- A) Approval responses cannot be combined with `previous_response_id`.
- B) The `authorization` token is not stored by the API, so the follow-up must include the MCP tool config with the token again.
- C) The approval must be sent to the MCP server directly, not to the Responses API.
- D) OAuth tokens only work with `connector_id`.

<details><summary>Answer</summary>

**B.** OpenAI does not store or echo the `authorization` value, so every request that may call the server must carry it. A is how the docs chain approvals. C is wrong: the API calls the server after your approval. D is wrong: `authorization` works with `server_url` too.
</details>

**Q3.** A team connects a third-party CRM MCP server and sets `"require_approval": "never"` to remove latency. The server exposes `search_contacts`, `get_contact`, `update_contact`, and `delete_contact`. What should the architect change?

- A) Nothing; approvals are only for debugging.
- B) Set `"require_approval": "always"` and approve everything automatically in code.
- C) Use `allowed_tools` to import only the tools the use case needs and `{"never": {"tool_names": ["search_contacts", "get_contact"]}}` so writes still require approval.
- D) Move the server behind Secure MCP Tunnel.

<details><summary>Answer</summary>

**C.** Least privilege plus approvals exactly where the risk is. A ignores the docs' advice to keep sensitive actions behind approval. B keeps the latency and removes the protection. D changes the network path, not what the model may do.
</details>

**Q4.** A policy assistant uses `file_search` over a vector store. Policies are revised every week. After each revision, answers sometimes quote the old rule and the new rule side by side. What should the architect do?

- A) Raise `ranking_options.score_threshold` to 0.9 so only the best chunk survives.
- B) Add "always prefer the newest policy" to the instructions.
- C) Give every file `version`, `effective_at`, and `is_current` attributes, filter on `is_current`, and run a scheduled sync that attaches new versions, marks the old file not current, and then removes it.
- D) Create a new vector store for every revision and delete the old store.

<details><summary>Answer</summary>

**C.** The two versions are both relevant, so ranking cannot separate them; metadata plus a lifecycle can. The `is_current` filter also covers the short window in which a removed file can still appear (removal is eventually consistent). A risks dropping the right chunk and does not tell old from new. B leaves both versions in context and hopes. D re-indexes the whole corpus for every small change, and requests that still reference the deleted store fail.
</details>

## Official documentation

- Using tools (overview) — https://developers.openai.com/api/docs/guides/tools
- Web search — https://developers.openai.com/api/docs/guides/tools-web-search
- File search — https://developers.openai.com/api/docs/guides/tools-file-search
- MCP servers (remote MCP tool, approvals, connectors, risks) — https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- Secure MCP Tunnel — https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
- Agents SDK reference: MCP — https://openai.github.io/openai-agents-python/mcp/

---

[← Chapter 3 — Agents SDK and Agents API](../03-agents-sdk-and-agents-api/README.md) | [↑ OpenAI path](../README.md) | [Chapter 5 — Codex →](../05-codex/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
