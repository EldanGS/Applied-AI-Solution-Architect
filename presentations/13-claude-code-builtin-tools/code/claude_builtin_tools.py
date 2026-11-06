import asyncio
from pathlib import Path
from claude_agent_sdk import (
    AssistantMessage, ClaudeAgentOptions, ResultMessage, SystemMessage,
    ToolUseBlock, query)

REPO = (Path(__file__).parent
        / "../../05-claude-code-and-codex/code/acme-shop").resolve()
TASK = ("Support ticket: a customer cancelled order A-1001 after it shipped, "
        "and the cancel went through. Find the line that should have "
        "refused it and explain why it did not. Search first, then read "
        "only what you need. Answer in 3 lines with file:line.")

options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    cwd=str(REPO),
    tools=["Grep", "Glob", "Read"],          # the ONLY built-in tools it has
    allowed_tools=["Grep", "Glob", "Read"],  # pre-approved: no prompts
    permission_mode="dontAsk",               # anything else: denied
    setting_sources=[],  # ignore acme-shop's .claude/settings.json
    max_turns=10, max_budget_usd=0.10,
)

async def main():
    async for msg in query(prompt=TASK, options=options):
        if isinstance(msg, SystemMessage) and msg.subtype == "init":
            tools = msg.data["tools"]
            print("tools:", tools)
            print("not available:",
                  [t for t in ("Edit", "Write", "Bash") if t not in tools])
        elif isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, ToolUseBlock):
                    # show the key input: a pattern or a file path
                    key = b.input.get("pattern") or b.input.get("file_path")
                    key = key.replace(f"{REPO}/", "")  # shorter paths
                    print(f"→ {b.name}({key!r})")
        elif isinstance(msg, ResultMessage):
            print(msg.result)
            u = msg.usage
            inp, out = u["input_tokens"], u["output_tokens"]
            write = u["cache_creation_input_tokens"]
            read = u["cache_read_input_tokens"]
            # $ per 1M: in 2, 5-min cache write 2.50, read 0.20, out 10
            cost = (inp * 2 + write * 2.5 + read * 0.2 + out * 10) / 1e6
            print(f"{msg.num_turns} turns, in={inp} write={write} "
                  f"read={read} out={out}")
            print(f"${cost:.4f} (SDK reports ${msg.total_cost_usd:.4f})")

asyncio.run(main())
