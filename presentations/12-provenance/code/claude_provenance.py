import json
from typing import Literal
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()
MODEL = "claude-sonnet-5-5"
QUESTION = ("I'm on Acme Plus. How long do I have to return my headphones, "
            "and when do I get my money back? - Dana")
# the source registry: S1 and S2 disagree on the return window
SOURCES = {
    "S1": {"title": "Returns policy page", "published": "2026-09-01",
           "text": "Items can be returned within 30 days of delivery. "
                   "Refunds reach the original card within 7 business days."},
    "S2": {"title": "Support macro #12", "published": "2026-03-15",
           "text": "Customers have 14 days from delivery to return an "
                   "item. Refunds reach the card within 7 business days."},
    "S3": {"title": "Acme Plus FAQ", "published": "2026-08-10",
           "text": "Acme Plus members get free return shipping."},
}

class Claim(BaseModel):
    topic: Literal["return_window", "refund_time", "return_shipping"]
    value: str       # the bare value, e.g. "30 days" or "free"
    excerpt: str     # the source's own words, not a paraphrase
    source_id: str   # the link back to the registry
class Claims(BaseModel):
    claims: list[Claim]
class Line(BaseModel):
    text: str
    claim_ids: list[str]  # every sentence points at its evidence
class Draft(BaseModel):
    lines: list[Line]

usage, ids = [], {}

def ask(system, user, schema):
    r = client.messages.parse(
        model=MODEL, max_tokens=2048, system=system,
        messages=[{"role": "user", "content": user}], output_format=schema)
    usage.append(r.usage)
    return r.parsed_output

for sid, s in SOURCES.items():  # one subagent per source
    found = ask("Extract each policy fact as a claim. Copy the excerpt word "
                "for word. value is the bare value, e.g. '30 days' or 'free'.",
                f'<source id="{sid}">{s["text"]}</source>', Claims)
    for c in found.claims:
        ids[f"C{len(ids) + 1}"] = c

for cid, c in list(ids.items()):
    src = SOURCES.get(c.source_id, {})  # an unknown source id fails too
    ok = c.excerpt in src.get("text", "")  # is the quote really there?
    print(f"{cid} {c.topic} = {c.value}  [{c.source_id} "
          f"{src.get('title', '?')}, {src.get('published', '?')}] "
          + ("quote ok" if ok else "QUOTE NOT FOUND"))
    if not ok:
        del ids[cid]  # an unverified claim never reaches the synthesis

topics = {}
for cid, c in ids.items():
    topics.setdefault(c.topic, []).append(cid)
conflicts = []  # code finds conflicts; nobody silently picks a winner
for topic, cids in topics.items():
    if len({ids[i].value.lower() for i in cids}) > 1:
        conflicts.append(topic)
        print(f"CONFLICT {topic}: " + " vs ".join(
            f"{ids[i].value} ({ids[i].source_id}, "
            f"{SOURCES[ids[i].source_id]['published']})" for i in cids))

# synthesis gets the claim records themselves, not a summary of them
records = {i: c.model_dump() for i, c in ids.items()}
draft = ask("Answer the customer using only these claims. Every sentence "
            "lists the claim ids it relies on; no greeting. For a contested "
            "topic, do not choose a value: say a teammate will confirm it, "
            "and cite every claim on that topic.",
            f"<question>{QUESTION}</question>\n"
            f"<claims>{json.dumps(records)}</claims>\n"
            f"<contested>{json.dumps(conflicts)}</contested>", Draft)
for line in draft.lines:
    refs = [f"{i}->{ids[i].source_id}" if i in ids else f"{i}->UNKNOWN"
            for i in line.claim_ids]
    print(f"{line.text}  [{', '.join(refs) or 'NO SOURCE'}]")

inp = sum(u.input_tokens for u in usage)
out = sum(u.output_tokens for u in usage)
cost = (inp * 2 + out * 10) / 1e6  # Sonnet 5.5: $2 in, $10 out per million
print(f"{len(usage)} calls, in={inp} out={out}, ${cost:.4f}")
