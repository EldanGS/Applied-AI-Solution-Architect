import asyncio
import sys
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

SYSTEM = "You are Acme Shop support. Reply in under 12 words."
SERVER = str(Path(__file__).with_name("shop_server.py"))

async def ask(q):
    async with MCPServerStdio(
        name="shop",
        params={"command": sys.executable, "args": [SERVER]},
    ) as shop:
        agent = Agent(name="Acme support", instructions=SYSTEM,
                      model="gpt-6-luna", mcp_servers=[shop])
        result = await Runner.run(agent, q, max_turns=5)
    for item in result.new_items:
        if item.type == "tool_call_item":
            print("→", item.raw_item.name, item.raw_item.arguments)
    print(result.final_output)

asyncio.run(ask("Cancel my orders A-1001 and A-1002."))

from openai import OpenAI

client = OpenAI()
Q = ("Which transports does modelcontextprotocol/python-sdk "
     "support? One short sentence.")

r = client.responses.create(
    model="gpt-6-luna",
    tools=[{"type": "mcp", "server_label": "deepwiki",
            "server_url": "https://mcp.deepwiki.com/mcp",
            "allowed_tools": ["ask_wiki_question"],
            "require_approval": "never"}],
    input=Q,
)
for item in r.output:
    if item.type == "mcp_call":
        print("→", item.name, item.arguments)
print(r.output_text)
