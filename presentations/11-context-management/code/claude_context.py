import json
from typing import Literal
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()
MODEL = "claude-sonnet-5-5"
SYSTEM = ("You are Acme Shop support. If a case_facts block is present, it "
          "is the source of truth: copy amounts and IDs from it exactly.")

# what the order API really returns: 5 useful fields buried in noise
RAW = {"order_id": "A-2291", "status": "delivered", "total": "84.00 USD",
       "charges": ["84.00 USD card *4417", "84.00 USD card *4417"],
       "return_eligible": True}
RAW |= {f"warehouse_field_{i}": f"WH-{i:04d}-OK" for i in range(40)}
RAW["scan_events"] = [{"time": f"2026-10-{1 + i // 24:02d}T{i % 24:02d}:00",
                       "hub": f"HUB-{i % 7}", "event": "in transit"}
                      for i in range(150)]

FIRST = ("Order A-2291: you charged my card twice, 84.00 USD each. Refund "
         "the duplicate to my card, NOT store credit. - Dana")
SMALL_TALK = [("Does the rain jacket come in blue?", "Yes, navy and sky."),
              ("Is it machine washable?", "Yes, cold, no dryer."),
              ("Do you ship to Canada?", "Yes, in 5-7 days."),
              ("Can I add a gift note?", "Yes, at checkout.")] * 5
QUESTION = "Dana again. What exactly are you refunding, on which order, how?"

class Refund(BaseModel):
    order_id: str
    amount: str
    to: Literal["original card", "store credit"]

def turns(pairs):
    return [{"role": r, "content": c} for u, a in pairs
            for r, c in (("user", u), ("assistant", a))]

# before: every turn verbatim, the full tool result early in the history
before = turns([(FIRST, "Sorry, Dana! Checking the order."),
                (f"<tool_result>{json.dumps(RAW)}</tool_result>",
                 "I see two charges.")] + SMALL_TALK)

# after: summary + trimmed tool result, the last 2 turns, then one new
# user turn: the facts block first, the question last
KEEP = ("order_id", "status", "total", "charges", "return_eligible")
slim = {k: RAW[k] for k in KEEP}  # trim before it enters the context
FACTS = {"customer": "Dana Kim", "order_id": RAW["order_id"],
         "amount": RAW["total"], "problem": "charged twice",
         "customer_request": "refund to card, NOT store credit (turn 1)"}
facts = "\n".join(f"{k}: {v}" for k, v in FACTS.items())
# a prose summary drops exact values; the facts block keeps them
SUMMARY = "Older turns: a billing problem; the customer wants it fixed."
after = turns([(f"{SUMMARY}\n<tool_result>{json.dumps(slim)}</tool_result>",
                "Understood.")] + SMALL_TALK[-2:])

def ask(history, question):
    r = client.messages.parse(
        model=MODEL, max_tokens=4096, system=SYSTEM, output_format=Refund,
        messages=history + [{"role": "user", "content": question}])
    return r.parsed_output, r.usage

print(f"tool result: {len(RAW)} fields -> {len(slim)} fields")
print(f"amount in summary: {FACTS['amount'] in SUMMARY}, "
      f"in facts block: {FACTS['amount'] in facts}")
a0, u0 = ask(before, QUESTION)
a1, u1 = ask(after, f"<case_facts>\n{facts}\n</case_facts>\n{QUESTION}")
for name, msgs, a, u in (("before", before, a0, u0),
                         ("after", after, a1, u1)):
    print(f"{name:6} {len(msgs) + 1:2} messages, in={u.input_tokens:5}: "
          f"{a.order_id}, {a.amount}, to {a.to}")

saved = 1 - u1.input_tokens / u0.input_tokens
exact = a1.order_id == FACTS["order_id"] and a1.amount == FACTS["amount"]
print(f"input tokens {u0.input_tokens} -> {u1.input_tokens} "
      f"({saved:.0%} less); answer matches facts block: {exact}")

inp = u0.input_tokens + u1.input_tokens
out = u0.output_tokens + u1.output_tokens
cost = (inp * 2 + out * 10) / 1e6  # Sonnet 5.5: $2 in, $10 out per million
print(f"2 calls, in={inp} out={out}, ${cost:.4f}")
