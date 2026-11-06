from typing import Literal
from anthropic import Anthropic
from pydantic import BaseModel, ConfigDict

client = Anthropic()
MODEL = "claude-sonnet-5-5"
ORDERS = {"A-3101": {"item": "mug", "total": 18.0},
          "A-3102": {"item": "espresso machine", "total": 240.0}}
LIMIT = 100.0  # never shown to the model: the code enforces it
SYSTEM = (f"You are Acme Shop support. Orders: {ORDERS}. A damaged item gets "
          "a full refund with issue_refund. Call escalate_to_human only if "
          "the customer asks for a person, the policy does not cover the "
          "request, you cannot make progress, or a tool says a human must "
          "decide. Being upset is not a reason. Reply in under 25 words.")

class Handoff(BaseModel):  # the human reads only this, never the chat
    model_config = ConfigDict(extra="forbid")
    # no "customer_angry": being upset is not a trigger
    reason: Literal["customer_requested_human", "policy_gap",
                    "no_progress", "over_limit"]
    order_id: str
    amount_usd: float
    issue: str
    tried: list[str]
    recommended_action: str

REFUND = {"type": "object", "additionalProperties": False,
          "required": ["order_id", "amount_usd"],
          "properties": {"order_id": {"type": "string"},
                         "amount_usd": {"type": "number"}}}
TOOLS = [{"name": "issue_refund", "description": "Refund one order.",
          "input_schema": REFUND, "strict": True},
         {"name": "escalate_to_human", "strict": True,
          "description": "Hand the case to a human specialist, who "
                         "never sees this chat.",
          "input_schema": Handoff.model_json_schema()}]
usage = []

def run(name, args):
    if name == "escalate_to_human":
        handoff = Handoff.model_validate(args)
        print("→", name, handoff.model_dump_json(indent=2))
        return "ticket H-1 filed, a specialist replies within 24h"
    print("→", name, args)
    ok = 0 < args["amount_usd"] <= LIMIT  # a hard rule lives in code
    print("  gate:", "allow" if ok else f"block, over ${LIMIT:.0f}")
    return "refunded" if ok else ("BLOCKED: over the refund limit, a "
                                  "human must approve. Escalate.")

def ask(text):
    print("\ncustomer:", text)
    msgs = [{"role": "user", "content": text}]
    for _ in range(5):
        r = client.messages.create(model=MODEL, max_tokens=1024,
                                   system=SYSTEM, tools=TOOLS, messages=msgs)
        usage.append(r.usage)
        msgs.append({"role": "assistant", "content": r.content})
        if r.stop_reason != "tool_use":
            break
        msgs.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": b.id,
             "content": run(b.name, b.input)}
            for b in r.content if b.type == "tool_use"]})
    print("agent:", "".join(b.text for b in r.content if b.type == "text"))

ask("Order A-3101: the mug arrived smashed. Third time! I'm furious. Refund!")
ask("Hi, my espresso machine (order A-3102) arrived cracked. Refund, please?")

inp = sum(u.input_tokens for u in usage)
out = sum(u.output_tokens for u in usage)
cost = (inp * 2 + out * 10) / 1e6  # Sonnet 5.5: $2 in, $10 out per 1M
print(f"\n{len(usage)} calls, in={inp} out={out}, ${cost:.4f}")
