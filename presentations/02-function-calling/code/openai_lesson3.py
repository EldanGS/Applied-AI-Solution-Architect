import json
from openai import OpenAI

client = OpenAI()
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
    "type": "function",
    "name": "get_order",
    "description": DESC,
    "parameters": SCHEMA,
    "strict": True,
}]

TOOLS = {"get_order": get_order}

def run_tool(call):
    args = json.loads(call.arguments)
    try:
        out = json.dumps(TOOLS[call.name](**args))
    except Exception as e:
        out = json.dumps({"error": str(e)})
    print("→", call.name, args, "←", out)
    return {"type": "function_call_output",
            "call_id": call.call_id, "output": out}

def ask(q):
    items = [{"role": "user", "content": q}]
    for turn in range(5):
        r = client.responses.create(
            model="gpt-6-luna", instructions=SYSTEM,
            tools=tools, input=items)
        items += r.output
        calls = [i for i in r.output
                 if i.type == "function_call"]
        if not calls:
            return r
        items += [run_tool(c) for c in calls]

print(ask("Where is my order A-1001?").output_text)
print(ask("Where is my order Z-999?").output_text)

from typing import Literal
from pydantic import BaseModel

class Ticket(BaseModel):
    category: Literal["shipping", "billing", "other"]
    order_id: str | None
    urgent: bool

EMAIL = "Charged twice for order A-1001. Fix it today!"

r = client.responses.parse(
    model="gpt-6-luna",
    text_format=Ticket,
    input=EMAIL,
)
print(r.output_parsed)

def cancel_order(order_id: str) -> dict:
    if get_order(order_id)["status"] == "shipped":
        raise ValueError("Shipped. Offer a return.")
    ORDERS[order_id]["status"] = "cancelled"
    return {"cancelled": order_id}

TOOLS["cancel_order"] = cancel_order
tools.append({**tools[0], "name": "cancel_order",
              "description": "Cancel ONE order by its ID. "
                             "Only when the customer asks."})
print(ask("Cancel my orders A-1001 and A-1002.").output_text)
