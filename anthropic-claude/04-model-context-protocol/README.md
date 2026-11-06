# Chapter 4 — Model Context Protocol (MCP)

> **Exam domain(s):** Domain 2 — Tool Design & MCP Integration (**18%**, primary) · Domain 3 — Claude Code Configuration & Workflows (20%, `.mcp.json` and scopes) · Domain 1 — Agentic Architecture & Orchestration (27%, MCP inside agents) · Domain 5 — Context Management & Reliability (15%, error propagation)
> **Est. time:** 6–8 hours (reading + notebooks) · **Status:** [ ] not started

<a id="why-this-matters-for-a-solution-architect"></a>

MCP is the standard plug that lets you write an integration with an outside system (ticketing, CRM, database, code host) **once** and reuse it in Claude Code, the Agent SDK, Claude Desktop, the Messages API, and other vendors' clients. The architect's job is to pick the right **primitive** (tool, resource, or prompt), **transport** (local or remote), **configuration scope** (personal or team), and **error contract**. Those four choices decide whether the agent is reliable, secure, and cheap to run.

## What you'll learn

- What MCP solves, how hosts, clients, and servers relate, and how tools, resources, and prompts differ by *who controls them*.
- stdio vs Streamable HTTP, and how to configure servers in Claude Code with the right scope and `${VAR}` expansion.
- Structured errors with `isError: true`, a category, and a retry flag, and why an empty result is not an error.
- How to build, test, and connect a Python MCP server (`MCPServer`) from Claude Code, the Agent SDK, and the Messages API.

## Prerequisites

[00-prerequisites](../../00-prerequisites/README.md) (Python, `.env`, Jupyter, async/await) · [Chapter 2 — Tool use](../02-tool-use/README.md) (MCP tools are those same tools, delivered by a server) · [Chapter 3 — Agent SDK](../03-agent-sdk/README.md) (agent loop, `allowed_tools`, hooks). Install: `pip install "mcp>=2.3" anthropic claude-agent-sdk python-dotenv` (in the root [`requirements.txt`](../../requirements.txt)). Node.js 22.19+ only for the MCP Inspector.

## Concepts

### 4.1 What MCP is

Before MCP, every AI app wrote its own adapter for every system: N apps × M systems = N×M integrations. MCP makes it N + M. Each system ships one **MCP server**, each AI app embeds one **MCP client**, and they speak the same JSON-RPC protocol. A server exposes three primitives. Tell them apart by asking *who decides to use it*:

| Primitive | Controlled by | What it is | Example |
|---|---|---|---|
| **Tool** | **The model** — Claude decides to call it | A function with a JSON input schema; may have side effects | `lookup_order`, `create_issue` |
| **Resource** | **The application / user** — the host reads and attaches it | Read-only data addressed by a URI | `schema://orders`, `tickets://open` |
| **Prompt** | **The user** — a person picks it by name | A reusable, parameterized message template | `/review-pr` |

A server with one of each, using the official Python SDK v2 (`server.py`):

```python
from mcp.server import MCPServer

mcp = MCPServer("Bookshop")
BOOKS = {"978-0441172719": {"title": "Dune", "author": "Frank Herbert"}}

@mcp.tool()
def search_books(query: str) -> list[dict]:
    """Search the catalog by title or author. Empty list means no match."""
    q = query.lower()
    return [{"isbn": isbn, **b} for isbn, b in BOOKS.items()
            if q in b["title"].lower() or q in b["author"].lower()]

@mcp.resource("books://{isbn}", mime_type="application/json")
def get_book(isbn: str) -> dict:
    """A single book record, addressed by ISBN."""
    return BOOKS[isbn]  # 4.5 shows the proper error for an unknown id

@mcp.prompt()
def recommend(genre: str) -> str:
    """Ask for three recommendations in a genre."""
    return f"Recommend three {genre} books from our catalog."

if __name__ == "__main__":
    mcp.run()  # stdio by default
```

- The decorators are factories: write `@mcp.tool()` with parentheses. The SDK builds `inputSchema` from the type hints, and the docstring becomes the tool description Claude reads. Write it with the same care as a hand-written tool from Chapter 2.
- To describe one argument, wrap its hint: `Annotated[str, Field(description="Id of the document to edit, for example 'plan.md'.")]` (pydantic `Field`). Arguments without a default are `required`.
- SDK v2 renamed `FastMCP` to **`MCPServer`** (`from mcp.server import MCPServer`). Old `from mcp.server.fastmcp import FastMCP` code does not run on `mcp>=2.0`. The PyPI package `fastmcp` is a different project.

### 4.2 MCP servers, clients, and transports

**Roles.** The **host** is the app the user works in (Claude Code, Claude Desktop, your Agent SDK app). It creates **one client per server**. A **server** is a local process or a remote web service.

**On connection** the client asks each server for `tools/list`, `resources/list`, and `prompts/list`. Discovery is automatic: the host gets names, descriptions, and schemas from the server. **All tools from all connected servers are available at once.** Five servers with ten tools each means fifty tools, and selection gets less reliable, so connect only what the role needs, restrict with `allowed_tools`, and use tool search for large catalogs. **The server's descriptions decide behavior**, and you may not be able to edit a third-party one.

> **Exam trap:** If an agent keeps using a built-in tool (for example `Grep`) instead of a more capable MCP tool, strengthen the MCP tool's **description** (what unique data or capability it offers). Do not remove the built-in tool or add a routing classifier.

**One request, end to end.** The model never talks to the server; the host relays. The host gets `tools/list` on connect → sends messages plus tool definitions to Claude → Claude returns `tool_use` → the host sends `tools/call` to the server → the server calls the external system and returns a `CallToolResult` (content, `isError`) → the host sends a `tool_result` to Claude → Claude answers. Tool definitions and execution both live in the server.

**Transports.** A transport is how JSON-RPC messages travel. The semantics are the same on every transport. Each message is a **request** (has an `id`, expects a reply, for example `tools/call`), a **response** to that `id` (`result` or `error`), or a **notification** (no `id`, no reply, for example `notifications/tools/list_changed`).

| Transport | How it works | Use when | Watch out for |
|---|---|---|---|
| **stdio** | Client launches the server as a subprocess; JSON-RPC over stdin/stdout | Local tools, local files or credentials | One user. Never `print()` to stdout; log to stderr |
| **Streamable HTTP** | Each message is an HTTP POST to one endpoint (for example `/mcp`) | Shared, remote, multi-user servers; the Messages API connector | Needs auth (OAuth or bearer), TLS, normal operations |
| ~~HTTP+SSE~~ | Older two-endpoint design | Legacy only | **Deprecated** since `2025-03-26`; migrate |

Spec revision **2026-07-28** made MCP **stateless**: no `initialize` handshake and no `Mcp-Session-Id`. It also deprecated Roots, Sampling, and Logging. SDK v2 speaks both `2025-11-25` and `2026-07-28`.

Serve over HTTP with `mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)`. Connect with the v2 `Client` (Python attributes are snake_case, such as `result.is_error`; the wire JSON stays `isError`):

```python
# Top-level await works in a notebook; in a .py file, wrap this in async def main() + asyncio.run(main()).
import sys
from mcp import Client, StdioServerParameters

# 1) In-memory: pass the server object (server.py from 4.1). Ideal for notebooks and tests.
from server import mcp
async with Client(mcp) as client:
    tools = await client.list_tools()
    print([t.name for t in tools.tools])
# 2) stdio: the client starts the server as a subprocess.
params = StdioServerParameters(command=sys.executable, args=["server.py"])  # same venv as the client
async with Client(params) as client:
    result = await client.call_tool("search_books", {"query": "Herbert"})
    print(result.is_error, result.structured_content)
# 3) Streamable HTTP: pass the endpoint URL.
async with Client("http://127.0.0.1:8000/mcp") as client:
    print(client.server_info, client.protocol_version)
```

- With the Python SDK's stdio client, a server gets only a small safe list of environment variables (`HOME`, `PATH`, `USER`, ...) plus what you pass in `env`. Other hosts differ: Claude Code passes your shell environment unless `CLAUDE_CODE_MCP_ALLOWLIST_ENV=1` is set. Either way, pass a server's secret on purpose, for example `env={"CRM_TOKEN": os.environ["CRM_TOKEN"]}`.
- **Test with the MCP Inspector** before wiring a server into Claude: `npx @modelcontextprotocol/inspector python server.py` opens a web UI that lists every tool, resource, and prompt, lets you call them, and shows raw JSON-RPC. Add `--cli ... --method tools/list` for CI. Check descriptions, error paths, MIME types, and a clean stdout.
- **Build or reuse?** For GitHub, Jira, Slack, Postgres, or Sentry, prefer an existing, well-maintained server (ideally the vendor's). Build your own for team-specific workflows or a narrower, safer surface (`get_refund_eligibility` instead of raw SQL).

### 4.3 Configuring MCP servers

Claude Code stores each server in one of three scopes:

| Scope | Stored in | Shared with team? | Loads in |
|---|---|---|---|
| **local** (default) | `~/.claude.json`, under this project | No | This project only |
| **project** | `.mcp.json` at the repo root, committed | **Yes** | This project, for everyone |
| **user** | `~/.claude.json`, top level | No | All your projects |

The most specific scope wins: **local > project > user**. The whole winning entry is used; fields are not merged. Add servers with `claude mcp add --transport http github <url>`, share one with `--scope project`, and check them with `claude mcp list` or `/mcp` inside a session.

The team file, `.mcp.json`, is committed and must never contain a secret:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_PAT}" }
    },
    "orders": {
      "type": "stdio",
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/servers/orders_server.py"],
      "env": {
        "ORDERS_DB_URL":
          "${ORDERS_DB_URL:-postgres://localhost:5432/orders_dev}"
      }
    }
  }
}
```

- `${VAR}` takes the developer's environment variable at load time; `${VAR:-default}` adds a fallback. Expansion works in `command`, `args`, `env`, `url`, and `headers`. Each developer supplies their **own** token; the README lists the required variables.
- Always set `type` for remote servers (`"http"`). An entry with a `url` but no `type` is read as stdio and fails.
- Claude Code asks each developer to **approve** project servers once. Headless runs load them without asking, so review `.mcp.json` changes like code.
- **Reuse before you build.** For a standard integration such as an issue tracker, add the vendor's server or a well-maintained community server to `.mcp.json`. Write a custom server only for workflows specific to your team (see "Build or reuse?" in 4.2).
- **Vet a community server before the team uses it.** Check who maintains it and how actively, what it can read, write or delete, and which credentials it needs. An entry in `.mcp.json` loads for every teammate, so review it like a new dependency.

> **Exam trap:** One server for the whole team, but a personal token for each person. Commit the entry to `.mcp.json`, write the token as `${VAR}`, and name the variable in the README. A design that puts a real token in the file, or gives each developer a separate copy of the entry, misses one of the two goals.

**Inside Claude Code**, tools appear as `mcp__<server>__<tool>` (the same name used in permissions and `allowed_tools`). Resources attach with `@<server>:<protocol>://<path>`. Prompts become slash commands such as `/mcp__github__pr_review 456`. Output is capped (warning at 10,000 tokens, default limit 25,000, raise with `MAX_MCP_OUTPUT_TOKENS`), so return focused results.

### 4.4 The `isError` flag and structured errors

MCP has two kinds of failure:

| Failure | How it is reported | Who sees it |
|---|---|---|
| Malformed JSON-RPC, unknown method, `MCPError` raised by the server | JSON-RPC error (for example `-32602`, `-32603`) | The host; usually not the model |
| The tool ran but the operation failed | A normal result with **`isError: true`** | **The model**, which can retry, fix, or escalate |

Arguments that fail the input schema also come back as `isError` results, and SDK v2 reports an unknown tool name the same way. `isError` keeps the failure inside the conversation. A message that says only "Operation failed" wastes it: the agent cannot tell whether a retry will help. Give it a category, a retry flag, and a message:

| `errorCategory` | Example | `isRetryable` | Agent should |
|---|---|---|---|
| `transient` | Upstream timeout, 503 | `true` | Retry (bounded, with backoff) |
| `validation` | Order ID has the wrong format | `false` (until input is fixed) | Fix the arguments and call again |
| `business` | Refund exceeds policy limit | `false` | Explain to the user; offer escalation |
| `permission` | Token lacks scope | `false` | Escalate or ask for access; do not loop |

For a simple argument mistake, a `ToolError` with a fix-it message is enough (as in the example below); use the structured payload when the agent must act on the category. `content` is always an **array of content blocks**, so put the JSON in a text block and, optionally, in `structuredContent`. In SDK v2, raise **`ToolError`** for expected failures (your message reaches the model) or return a `CallToolResult` yourself. Any other exception reaches the model only as a generic `Error executing tool <name>`. That is the "Operation failed" anti-pattern.

```python
import json
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, TextContent

def tool_error(category: str, message: str, retryable: bool) -> CallToolResult:
    payload = {"errorCategory": category, "isRetryable": retryable,
               "message": message}
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(payload))],
        structured_content=payload, is_error=True)

@mcp.tool()
async def lookup_order(order_id: str) -> CallToolResult:
    """Fetch one order by ID (format: ORD-12345)."""
    if not order_id.startswith("ORD-"):
        raise ToolError("order_id must look like 'ORD-12345'.")
    try:
        order = await orders_api.get(order_id)  # your client
    except TimeoutError:
        return tool_error("transient", "Orders API timed out after 5s.", True)
    if order is None:  # NOT an error: the lookup worked and found nothing
        return CallToolResult(content=[TextContent(
            type="text", text=f"No order {order_id} exists.")])
    return CallToolResult(content=[TextContent(
        type="text", text=json.dumps(order))])
```

> **Exam trap:** "No matching records" is a **successful** call with an empty result. Flag it with `isError` and the agent retries pointlessly. Report a timeout as an empty result and the agent tells the user "you have no orders".

- In multi-agent systems ([Chapter 10](../10-multi-agent-error-handling/README.md)), a subagent retries `transient` errors locally once or twice and passes the rest up with the category and partial results. Never loop on `isRetryable: false`.
- If servers you cannot change return the same kind of value in different shapes, convert their results to one shape in a **`PostToolUse` hook**. Code runs on every result; an instruction to the model can be missed.

### 4.5 Resources: give the agent a map

<a id="resource-templates-mime-types-and-argument-completion"></a>

A resource is read-only context the agent should *know* before it starts *doing*: content catalogs, schemas, documentation, summaries. Without one, an agent explores (`list_tables` → `describe_table` × N → query), and every step is a model turn. A `schema://orders` resource attached up front replaces that exploration with one read.

- A **direct** resource has a fixed URI (`docs://documents`) and appears in `resources/list`. A **templated** one has parameters (`docs://documents/{doc_id}`), appears in `resources/templates/list`, and the client reads a concrete URI. `{+path}` matches several segments; `{?status,limit}` takes query values converted to the annotated types.
- **MIME types:** a `str` is sent as text, `bytes` as a base64 `blob`, anything else as **JSON text**. `mime_type` is only a label. It defaults to `text/plain`, so label every resource and decode on the client by type (blob → base64, `application/json` → `json.loads`, else text).
- For a missing id, raise `ResourceNotFoundError` (the client gets `-32602`). Resource reads are protocol requests, so failures are JSON-RPC errors, never `isError`.

```python
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ResourceNotFoundError

mcp = MCPServer("DocumentMCP")
DOCS = {"plan.md": "Q4 plan...", "report.pdf": "Q3 revenue grew 12%..."}

@mcp.resource("docs://documents", mime_type="application/json")
def list_documents() -> list[str]:
    """Ids of every document in the store."""
    return sorted(DOCS)

@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_document(doc_id: str) -> str:
    """The full text of one document."""
    if doc_id not in DOCS:
        raise ResourceNotFoundError(f"No document {doc_id!r}.")
    return DOCS[doc_id]
```

**Argument completion** lets a host autocomplete while the user types, for example document ids after `@`. It covers **prompt arguments** and **resource-template parameters**. Register one `@mcp.completion()` handler per server; it returns `Completion(values=..., total=..., has_more=...)`. The SDK does not filter for you, and returning `None` means an empty list.

<a id="prompts-in-the-client-and-context-injection"></a>**Prompts in the client and context injection.** A prompt is a pre-written instruction for a workflow users repeat. It can return several messages (`list[Message]` of `UserMessage(...)`). The host calls `prompts/get` with the user's arguments and sends the returned messages to Claude. **Context injection** is the resource counterpart: when the user writes `@plan.md`, the host reads `docs://documents/plan.md` and adds the text to the user turn, so Claude does not spend a tool call fetching it.

**Choosing the primitive.** Use a **tool** when the model must act or fetch something that depends on its reasoning. Use a **resource** for stable background context it needs *before* reasoning. Use a **prompt** when a human repeatedly starts the same workflow. Claude Code supports all three. The Messages API MCP connector supports **tools only**. Tool annotations such as `read_only_hint=True` are UI **hints**, not a security boundary; enforce real limits in server code or a hook.

### 4.6 Beyond Claude Code: MCP from the Agent SDK and the Messages API

| Option | How | Limits |
|---|---|---|
| **A — Agent SDK** | `ClaudeAgentOptions(mcp_servers={...}, allowed_tools=["mcp__orders__lookup_order"])`; same shape as `.mcp.json` | None beyond the SDK |
| **B — MCP connector (beta)** | `client.beta.messages.create(..., mcp_servers=[{"type": "url", "url": ..., "name": ..., "authorization_token": ...}], tools=[{"type": "mcp_toolset", "mcp_server_name": ...}], betas=["mcp-client-2025-11-20"])` | Tools only; server must be reachable over HTTP (public, or private through MCP tunnels, a Claude API research preview); no stdio. Beta on the Claude API, Claude Platform on AWS, Claude Models on Google Cloud (Anthropic managed) and Microsoft Foundry; not on Amazon Bedrock. Off the Claude API, only `mcp-client-2025-11-20` works |
| **C — your own bridge** | Run an MCP `Client` and translate MCP tools into Messages API tools | You own the loop |

Option C is the Chapter 2 agent loop with MCP underneath. It works with local stdio servers and any model:

```python
import json
from anthropic import AsyncAnthropic
from mcp import Client
from server import mcp  # or StdioServerParameters(...) / an HTTP URL

claude = AsyncAnthropic()
async with Client(mcp) as session:
    listing = await session.list_tools()
    tools = [{"name": t.name, "description": t.description or "",
              "input_schema": t.input_schema} for t in listing.tools]
    messages = [{"role": "user",
                 "content": "Do you have anything by Frank Herbert?"}]
    for _ in range(6):  # cap the turns
        resp = await claude.messages.create(model="claude-sonnet-5-5",
            max_tokens=1024, tools=tools, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            break
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                r = await session.call_tool(block.name, block.input)
                text = "\n".join(c.text for c in r.content if c.type == "text")
                if not text and r.structured_content is not None:
                    text = json.dumps(r.structured_content)  # e.g. {"result": []}
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": text, "is_error": bool(r.is_error)})
        messages.append({"role": "user", "content": results})
    print("".join(b.text for b in resp.content if b.type == "text"))
```

<a id="option-c-shortcut-the-anthropic-sdks-mcp-helpers"></a>**Shortcut: the Anthropic SDK's MCP helpers** (`pip install "anthropic[mcp]"`, module `anthropic.lib.tools.mcp`). `async_mcp_tool(tool, session)` turns an MCP tool into a runnable tool for `claude.beta.messages.tool_runner(...)`. `mcp_message` converts a `prompts/get` message, `mcp_resource_to_content` turns a resource into a `document` or `image` block, and `mcp_resource_to_file` prepares it for the Files API. An `isError: true` result reaches Claude as a `tool_result` with `is_error: true`. `mcp_resource_to_content` raises `UnsupportedMCPValueError` for `application/json`, so convert JSON to a `text` block yourself. Choose the helpers for local stdio servers, resources, or prompts. Choose the connector when a remote server's tools are all you need.

## Lesson code

Video-lesson code: [../../presentations/04-mcp/code/](../../presentations/04-mcp/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Build servers and clients for 4.1–4.6 step by step, then a mini-project: an "orders" stdio MCP server with structured errors, a policy resource and a prompt, plus a Claude support-agent loop |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: 12 auto-graded questions, 8 offline coding exercises, 1 architecture scenario, scorecard (pass mark 72%) |

<a id="architect-decision-cheat-sheet"></a>

## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Standard SaaS integration (GitHub, Jira, Slack) | Official or well-maintained community MCP server | Writing your own | Less code to own; vendors track their API changes |
| Whole team needs the same server | Project scope, `.mcp.json` committed | User or local scope on each laptop | Single source of truth, reviewed in PRs |
| Credentials in shared config | `${VAR}` expansion, documented in README | A real token in the committed file | Secrets stay out of git; each dev uses their own token |
| Server needs local files or runs on the dev's machine | stdio | Streamable HTTP | Simple, no network exposure |
| Shared, multi-user, or called from the Messages API | Streamable HTTP | stdio, HTTP+SSE | Remote-capable; SSE is deprecated |
| Agent wastes turns discovering what data exists | Resource catalog (schemas, indexes) | More exploratory tools | One read replaces several calls |
| Tool failure | `isError: true` + category + `isRetryable` + message | Generic "Operation failed" or a bare (non-`ToolError`) exception | Agent can choose retry / fix / escalate |
| Query found nothing | Successful result, empty payload | `isError: true` | Not a failure; avoids pointless retries |
| Normalizing outputs from servers you cannot modify | `PostToolUse` hook | Asking the model to convert values | Deterministic and centralized |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Committing secrets in `.mcp.json`.** Use `${VAR}` expansion and document the variables.
- **Using stdout for logs in a stdio server.** Any non-protocol byte on stdout corrupts the stream. Log to stderr.
- **Returning "Operation failed".** Or letting expected failures escape as bare exceptions, which SDK v2 turns into a generic message.
- **Marking empty results as errors** (or the reverse: hiding a timeout behind an empty list).
- **Connecting every server to every agent.** Fifty tools of which the agent needs four leads to misrouting and higher token cost.
- **Expecting resources or prompts through the MCP connector.** It is tools only.

## Self-check

**Q1.** A platform team of nine wants everyone in Claude Code to use the vendor's hosted MCP server for their issue tracker. Each engineer has a personal API key for the tracker. The team lead wants one reviewed server definition and no keys in git. What is the best approach?

- A) Commit `.mcp.json` with the server URL and `"Authorization": "Bearer ${TRACKER_API_KEY}"`, and list the variable in the README.
- B) Commit `.mcp.json` with the URL only, and have each engineer add the same server again at local scope with their key in `--header`.
- C) Commit `.mcp.json` with one shared service-account key so nobody has to set anything up.
- D) Have the team lead run `claude mcp add --scope project --header "Authorization: Bearer $TRACKER_API_KEY"` and commit the result.

<details><summary>Answer</summary>

**A.** A committed `.mcp.json` is the one reviewed definition, and `${VAR}` expansion lets each engineer supply their own key at load time. B keeps keys out of git, but each local entry wins whole over the project one, so nobody runs the reviewed definition. C puts a secret in git and hides who did what. D also commits a secret: the shell expands `$TRACKER_API_KEY` before Claude Code sees it, so the lead's real key is written into the file.
</details>

**Q2.** A customer-support agent calls an MCP `lookup_order` tool. When the orders API times out, the tool returns `isError: true` with the text "Operation failed". Logs show the agent sometimes apologizes and ends the conversation, and sometimes retries five times in a row. What is the most effective fix?

- A) Add a system prompt rule: "If a tool fails, retry exactly twice."
- B) Return a structured error with `errorCategory: "transient"`, `isRetryable: true`, and a clear message, and use distinct categories for validation, business, and permission failures.
- C) Remove `isError` so the agent treats the failure as a normal answer.
- D) Retry inside the MCP server indefinitely until the API responds.

<details><summary>Answer</summary>

**B.** The agent behaves inconsistently because the error carries no information it can act on. Category plus retryability lets it retry transient failures, fix validation errors, and escalate business or permission failures. A treats every failure the same. C hides the failure, so the agent may report wrong data. D can hang the agent and hides the problem from both the model and the user.
</details>

**Q3.** An analytics agent connected to a database MCP server spends 4–6 turns per question calling `list_tables` and `describe_table` before writing the real query. Latency and token cost are too high. What change gives the biggest improvement?

- A) Expose the schema and a table catalog as MCP resources and attach them as context up front.
- B) Merge `list_tables` and `describe_table` into a single `explore_database` tool.
- C) Raise `max_tokens` so the agent can explore in fewer turns.
- D) Add few-shot examples of good SQL queries to the system prompt.

<details><summary>Answer</summary>

**A.** Resources exist for this case: they give the agent a map of what data exists so it does not need exploratory calls. B still needs exploration calls, now through a vaguer tool. C does not change how many calls are made. D helps query style but not schema discovery.
</details>

**Q4.** A `search_customers` MCP tool queries a CRM. In one case the CRM returns zero rows for the given email. In another, the CRM rejects the call because the service account's token expired. How should the tool report these two cases?

- A) Both as `isError: true`, with different messages.
- B) Zero rows as a successful result with an empty list; expired token as `isError: true`, `errorCategory: "permission"`, `isRetryable: false`.
- C) Both as successful results with an empty list, to keep the agent from stopping.
- D) Zero rows as `isError: true`, `errorCategory: "validation"`; expired token as a JSON-RPC protocol error.

<details><summary>Answer</summary>

**B.** "No match" is a valid answer, not a failure, so the agent can tell the user that no customer exists. The expired token is a real failure that retrying will not fix, so it should be flagged as a non-retryable permission error and escalated. C makes the agent claim "no customer found" when the system was actually unreachable, which is the worst outcome.
</details>

## Official documentation

- MCP introduction — https://modelcontextprotocol.io/docs/getting-started/intro
- MCP architecture (hosts, clients, servers) — https://modelcontextprotocol.io/docs/learn/architecture
- MCP Inspector (debugging tool) — https://modelcontextprotocol.io/docs/tools/inspector
- MCP Python SDK docs — https://py.sdk.modelcontextprotocol.io/
- Claude Code: connect to tools via MCP — https://code.claude.com/docs/en/mcp
- Claude API: MCP connector — https://platform.claude.com/docs/en/agents-and-tools/mcp-connector

[← Chapter 3 — Agent SDK](../03-agent-sdk/README.md) | [↑ Claude path overview](../README.md) | [Chapter 5 — Claude Code →](../05-claude-code/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
