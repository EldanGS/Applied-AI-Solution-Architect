import asyncio
import sys
from pathlib import Path
from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions,
                              ResultMessage, ToolUseBlock, query)

SYSTEM = "You are Acme Shop support. Reply in under 12 words."
SERVER = str(Path(__file__).with_name("shop_server.py"))

options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    system_prompt=SYSTEM,
    mcp_servers={"shop": {"command": sys.executable,
                          "args": [SERVER]}},
    allowed_tools=["mcp__shop__get_order",
                   "mcp__shop__cancel_order"],
    permission_mode="dontAsk",
    tools=[],
    setting_sources=[],
    max_turns=5,
)

async def ask(q):
    async for msg in query(prompt=q, options=options):
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, ToolUseBlock):
                    print("→", b.name, b.input)
        if isinstance(msg, ResultMessage):
            print(msg.result)

asyncio.run(ask("Cancel my orders A-1001 and A-1002."))

from anthropic import Anthropic

client = Anthropic()
Q = ("Which transports does modelcontextprotocol/python-sdk "
     "support? One short sentence.")

r = client.beta.messages.create(
    model="claude-sonnet-5-5", max_tokens=1024,
    betas=["mcp-client-2025-11-20"],
    mcp_servers=[{"type": "url", "name": "deepwiki",
                  "url": "https://mcp.deepwiki.com/mcp"}],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "deepwiki",
            "default_config": {"enabled": False},
            "configs": {"ask_wiki_question": {"enabled": True}}}],
    messages=[{"role": "user", "content": Q}],
)
for b in r.content:
    if b.type == "mcp_tool_use":
        print("→", b.name, b.input)
print(r.content[-1].text)
