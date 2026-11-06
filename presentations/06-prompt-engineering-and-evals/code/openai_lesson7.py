from typing import Literal
from openai import OpenAI
from pydantic import BaseModel
from cases import CASES

client = OpenAI()

class Ticket(BaseModel):
    category: Literal["shipping", "billing", "other"]
    order_id: str | None
    urgent: bool

def run(prompt: str, email: str) -> dict:
    r = client.responses.parse(
        model="gpt-6-luna", instructions=prompt,
        text_format=Ticket, input=email)
    t = r.output_parsed
    return t.model_dump() if t else {}

def score(prompt: str) -> int:
    passed = 0
    for case in CASES:
        got, want = run(prompt, case["email"]), case["want"]
        bad = [k for k in want if got.get(k) != want[k]]
        for k in bad:
            print(f"✗ {case['id']} {k}: {got.get(k)!r},",
                  f"want {want[k]!r}")
        passed += not bad
    return passed

V1 = "Turn this customer email into a support ticket."
v1 = score(V1)
print(f"v1: {v1}/{len(CASES)} cases pass")

V2 = """# Identity
You sort Acme Shop support email into tickets.
# Instructions
* category is billing for money: charges, refunds, invoices,
  promo codes. Money and delivery in one email? billing.
* shipping: delivery, tracking, address changes, cancels,
  returns, exchanges and items damaged in transit.
* other: everything else, like logins, questions, praise.
* order_id: Acme IDs look like A-1234, so a1042 is A-1042.
  Tracking and invoice numbers are not order IDs. None? null.
* urgent: true only for a double or unknown charge, or a date
  the customer needs it by. Anger, capitals, ASAP: not urgent.
# Examples
<email id="1">WHY IS a1042 STILL NOT HERE?!</email>
<ticket id="1">shipping, A-1042, urgent: false</ticket>
<email id="2">A-1050 came late. I want my fee back!</email>
<ticket id="2">billing, A-1050, urgent: false</ticket>
<email id="3">Parcel 94001112 stuck. I fly Friday!</email>
<ticket id="3">shipping, null, urgent: true</ticket>"""
v2 = score(V2)
print(f"v2: {v2}/{len(CASES)} cases pass")
assert v2 >= v1, "v2 scores lower than v1: don't ship it"
print("gate passed: v2 >= v1")

V3 = V2.replace("ASAP:", "ASAP or lateness alone:")
v3 = score(V3)
print(f"v3: {v3}/{len(CASES)} cases pass")
assert v3 >= v2, "v3 scores lower than v2: don't ship it"
