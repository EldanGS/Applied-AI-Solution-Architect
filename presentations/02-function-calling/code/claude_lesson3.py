import json
from anthropic import Anthropic

client = Anthropic()
SYSTEM = "You are Acme Shop support. Reply in under 12 words."
ORDERS = {"A-1001": {"status": "shipped", "eta": "Oct 12"},
          "A-1002": {"status": "packing", "eta": "Oct 15"}}

def get_order(order_id: str) -> dict:
    if order_id not in ORDERS:
        raise ValueError(f"No order {order_id}. Check the ID.")
    return ORDERS[order_id]

DESC = ("Look up ONE order by its ID, e.g. A-1001. "
        "Returns its status and eta. Use it for any "
        "order question; if no ID is given, ask first.")
SCHEMA = {
    "type": "object",
    "properties": {"order_id": {"type": "string"}},
    "required": ["order_id"],
    "additionalProperties": False,
}

tools = [{
    "name": "get_order",
    "description": DESC,
    "input_schema": SCHEMA,
    "strict": True,
}]

TOOLS = {"get_order": get_order}

def run_tool(call):
    try:
        out = json.dumps(TOOLS[call.name](**call.input))
        error = False
    except Exception as e:
        out, error = str(e), True
    print("→", call.name, call.input, "←", out)
    return {"type": "tool_result", "tool_use_id": call.id,
            "content": out, "is_error": error}

def ask(q):
    msgs = [{"role": "user", "content": q}]
    for turn in range(5):
        r = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=1024,
            system=SYSTEM, tools=tools, messages=msgs)
        msgs.append({"role": "assistant", "content": r.content})
        if r.stop_reason != "tool_use":
            return r
        calls = [b for b in r.content if b.type == "tool_use"]
        results = [run_tool(c) for c in calls]
        msgs.append({"role": "user", "content": results})

def text_of(resp):
    return "".join(
        b.text for b in resp.content if b.type == "text"
    )

print(text_of(ask("Where is my order A-1001?")))
print(text_of(ask("Where is my order Z-999?")))

from typing import Literal
from pydantic import BaseModel

class Ticket(BaseModel):
    category: Literal["shipping", "billing", "other"]
    order_id: str | None
    urgent: bool

EMAIL = "Charged twice for order A-1001. Fix it today!"

r = client.messages.parse(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    output_format=Ticket,
    messages=[{"role": "user", "content": EMAIL}],
)
print(r.parsed_output)

def cancel_order(order_id: str) -> dict:
    if get_order(order_id)["status"] == "shipped":
        raise ValueError("Shipped. Offer a return.")
    ORDERS[order_id]["status"] = "cancelled"
    return {"cancelled": order_id}

TOOLS["cancel_order"] = cancel_order
tools.append({**tools[0], "name": "cancel_order",
              "description": "Cancel ONE order by its ID. "
                             "Only when the customer asks."})
print(text_of(ask("Cancel my orders A-1001 and A-1002.")))
