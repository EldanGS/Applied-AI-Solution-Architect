# Lesson 5 · Build an MCP Server for Claude and OpenAI in Python: recording script

The same text lives in the deck's speaker notes. Open the deck with `?notes` (or press N) to get a teleprompter that highlights the line for the current step.
`→` means press the arrow key, once per line. `[FACE]` marks a good moment to cut to your face.
22 slides · 1241 spoken words · about 9:26 at ~150 words a minute, including about a second per key press.


## 0:00 · Understand how MCP works

### 1. Cold open: the finished result  ·  0:00, ~25 s

Claude and OpenAI just used the same order tools, from one server, and neither agent file defines a tool. I'm Eldan: I built search ranking at Bing and AI features at Apple. Today you move the shop tools into an MCP server, plug that one server into both agents, and then let both APIs call a remote server. No glue code.

### 2. Write your tools once  ·  0:25, ~7 s

[FACE] This is Lesson 5: the Model Context Protocol. Write your tools once, and plug them into any agent.

### 3. Lesson 5 of the Applied AI series  ·  0:32, ~22 s

In Lesson 4, the shop tools lived inside each agent script: the tool decorator on Claude, function_tool on OpenAI. The same tools, written twice.

→ Today you write them once, in an MCP server. Both agents plug into it, and both APIs call a remote server with no client code at all.

### 4. One protocol instead of every wire  ·  0:53, ~35 s

Here's the problem MCP solves. Picture three AI apps and three systems they need.

→ Without a standard, every app wires every system by hand. Nine integrations, each with its own glue code. One more app means three more.

→ MCP puts one protocol in the middle.

→ Each system ships one MCP server. Each app embeds one MCP client. Nine becomes three plus three.

→ Anthropic created MCP, and OpenAI supports it too. So the server you write today plugs into both.

### 5. Who decides what gets used  ·  1:29, ~46 s

Three roles. The host is the app you run: Claude Code, or your agent script.

→ Inside it, one MCP client per server. On connect, the client asks: what do you have? The server answers with names, descriptions and schemas.

→ A server offers three kinds of things. Tools: the model decides when to call them.

→ Resources: read-only data your app decides to attach.

→ Prompts: templates a user picks, like a slash command.

→ Two transports. stdio, standard in and out: the host starts the server as a local subprocess. Streamable HTTP: a remote server at one URL. The old HTTP plus SSE is deprecated.

### 6. Same server, different knobs  ·  2:14, ~38 s

Same protocol, different knobs.

→ A local server: Claude takes a dict in its options, shaped like an mcp.json file. OpenAI takes an MCPServerStdio object.

→ Tool names: Claude prefixes them, mcp, server, tool. OpenAI keeps the plain name.

→ Least privilege: allowed_tools on Claude, a tool filter on OpenAI.

→ Remote servers: both APIs can call one for you. Claude's MCP connector is in beta. OpenAI adds a tool of type mcp.

→ Approvals: OpenAI has require_approval. On Claude, they live in your agent, as hooks.

## 2:52 · Build an MCP server

### 7. Build an MCP server  ·  2:52, ~6 s

Chapter two: build an MCP server.

### 8. A server is a decorated module  ·  2:58, ~35 s

The server file. Both vendors use it as is.

→ Two imports from the official MCP Python SDK. MCPServer is what older tutorials call FastMCP. We name it shop.

→ Same orders as every lesson.

→ A tool is a plain function with one decorator. The type hints become its JSON schema.

→ The docstring becomes the description, so it's still the router.

→ Unknown order? Raise ToolError. The model gets your message, flagged isError.

→ One server, one tool.

### 9. A guarded write, a read-only resource  ·  3:34, ~28 s

The second tool, cancel_order.

→ Its description says: only when the customer asks. That's guidance, not a rule.

→ The rule is Lesson 3's guard. Shipped? Raise ToolError. It lives in Python.

→ And one resource: the policy, at a URI. Read-only data for the app, not the model. In Claude Code you attach it with an at-mention.

→ Two tools, one resource.

### 10. Test it before any model does  ·  4:01, ~28 s

The last two lines.

→ mcp dot run. No arguments means stdio, so stdout is now the protocol channel. Never print to it; log to stderr.

→ Before any model touches it, test it with the MCP Inspector. Its CLI calls cancel_order on the shipped order.

→ isError: true, with our message. Exactly what the model will read. Drop the cli flag for a web UI.

## 4:29 · Plug it into both agents

### 11. Plug it into both agents  ·  4:29, ~6 s

Chapter three: plug it into both agents.

### 12. Point the Agent SDK at the server  ·  4:35, ~42 s

The Claude file starts like Lesson 4. SERVER is the path to shop_server.py.

→ mcp_servers: a name, shop, and how to start it: this same Python, plus the server path. The SDK launches it over stdio, in the same shape as an mcp.json file.

→ allowed_tools: mcp, shop, tool. The same names as Lesson 4.

→ dontAsk denies anything not allowed. Empty tools turns off built-ins like Bash.

→ In Claude Code, it's one command: claude mcp add. Scope project writes mcp.json for your team, so never put a secret in it.

→ One server, any Claude host.

### 13. Trace the calls from the client  ·  5:17, ~25 s

Running it is Lesson 4's query loop.

→ One change: we print each tool call here, in the client. In a stdio server, stdout belongs to the protocol.

→ And the final result.

→ Run it. Claude called cancel_order twice, through the server.

→ The server refused A-1001 with our ToolError message, so Claude offered a return.

### 14. Same server, as an MCPServerStdio  ·  5:43, ~31 s

The OpenAI file starts the same: imports, SYSTEM, SERVER.

→ MCPServerStdio, with the same command and path. async with starts the server and stops it after.

→ Pass it to the Agent in mcp_servers. The SDK lists the tools itself.

→ Runner dot run, awaited this time, because the server connection is async.

→ Then print the tool calls from new_items, and the final answer.

→ Same server, no changes.

### 15. Run it on gpt-6-luna  ·  6:14, ~19 s

Same server, now on gpt-6-luna.

→ Run it. Luna checked both orders, then tried both cancels. A-1002 is cancelled, and A-1001 gets a return.

→ The first line is our server's own log, on stderr: the ToolError. Not one line of shop_server.py changed.

## 6:32 · Go remote, safely

### 16. Go remote, safely  ·  6:32, ~6 s

Chapter four: go remote, safely.

### 17. The MCP connector calls it for you  ·  6:38, ~37 s

Now remote. To share your server, you'd run it with transport streamable-http, behind a public URL. To try it today, we use a public server: DeepWiki, which answers questions about GitHub repos.

→ On Claude, that's the MCP connector, in beta: beta dot messages, plus a beta flag.

→ mcp_servers: a name and a public URL. Anthropic connects for you. No MCP client in your code.

→ An mcp_toolset: every tool off, then one on. Least privilege.

→ Run it, and Claude answers from DeepWiki.

### 18. A tool of type mcp  ·  7:15, ~30 s

On OpenAI, a remote server is one more entry in tools, next to hosted tools like web_search and file_search. Those run on OpenAI; MCP runs on someone else's server.

→ Type mcp, a label, the URL.

→ allowed_tools: import only the tool you need.

→ require_approval never, because this tool only reads data. The default is always.

→ Run it. DeepWiki says: stdio, Streamable HTTP, and the older SSE.

### 19. A remote server is someone else’s code in your agent’s loop.  ·  7:45, ~20 s

[FACE] One rule before you connect anything remote. A remote server is someone else's code in your agent's loop. Allow only the tools you need. Put an approval on anything that writes. And treat every tool result as untrusted input: a web page or a ticket can hide instructions for your model.

### 20. Let the agent look up orders but never cancel, with one change per file. Then ask: “Cancel my order A-1002.” What does each model answer?  ·  8:05, ~33 s

Your turn. Make the agent read-only: it can look up orders, never cancel. One change per file. Then ask it to cancel A-1002, and predict each answer. Pause and try it.

→ Claude: keep only get_order in allowed_tools. Claude still sees cancel_order, but dontAsk denies the call. In my run, Claude said permission was denied.

→ OpenAI: a tool filter, plus its import. Luna never sees cancel_order. In my run, Luna said it can't cancel here; A-1002 is still packing.

### 21. Raising a plain exception in an MCP tool.  ·  8:38, ~25 s

[FACE] The most common mistake when you move tools into a server: raising a plain exception.

→ Lesson 3 raised ValueError. The MCP SDK hides that message, so the model sees only: error executing tool cancel_order.

→ Claude retried, then reported an error. Luna couldn't say why. Neither offered a return.

→ Raise ToolError, and your reason reaches the model.

### 22. Write tools once in an MCP server. Agents plug in over stdio, APIs over Streamable HTTP.  ·  9:04, ~22 s

[FACE] Write your tools once in an MCP server. Agents plug in over stdio, and APIs over Streamable HTTP.

→ Today's code is in the free hub, linked below.

→ In Lesson 6: Claude Code and Codex, two coding agents that plug into MCP servers like this one, set up for a real repo.
