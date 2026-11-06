import asyncio, time
from typing import Literal
from openai import AsyncOpenAI
from pydantic import BaseModel

client = AsyncOpenAI()
MODEL = "gpt-6-luna"
EMAIL = ("Order A-2291: you charged my card twice. My code SPRING10 didn't "
         "apply either.\nAnd please cancel my Acme Plus membership, I won't "
         "need it anymore. - Dana")
# the shared context: fetched once, in plain code, for every worker
CUSTOMER = {"name": "Dana Kim", "plan": "Acme Plus", "renews": "2026-11-20",
            "A-2291": {"total": 84.0, "charges": [84.0, 84.0], "promo": None}}

class Concern(BaseModel):
    id: str
    brief: str  # one self-contained job for one worker
class Plan(BaseModel):
    concerns: list[Concern]
class Answer(BaseModel):
    status: Literal["resolved", "needs_human"]
    reply: str
class Review(BaseModel):
    approved: bool
    issues: list[str]

async def ask(system, user, schema):
    r = await client.responses.parse(
        model=MODEL, max_output_tokens=4096, instructions=system,
        input=user, text_format=schema)
    if r.status != "completed" or r.output_parsed is None:  # None = refusal
        raise RuntimeError(r.incomplete_details or "refused")
    return r.output_parsed, r.usage

async def worker(c, sem):
    async with sem:
        t = time.perf_counter()
        a, u = await ask(
            "Resolve one concern for Acme Shop support. Use only the customer "
            "record. A refund or cancellation needs approval: set status "
            "needs_human.",
            f"<customer>{CUSTOMER}</customer>\n<concern>{c.brief}</concern>",
            Answer)
        return c.id, a, u, time.perf_counter() - t

async def main():
    t0 = time.perf_counter()
    plan, u0 = await ask("Split the email into separate concerns, one per "
                         "issue, no overlap.", EMAIL, Plan)
    print([c.id for c in plan.concerns])
    sem = asyncio.Semaphore(4)
    done = await asyncio.gather(*(worker(c, sem) for c in plan.concerns))
    for cid, a, _, s in done:
        print(f"{cid}: {a.status} in {s:.1f}s")

    parts = [a.model_dump() for _, a, _, _ in done]
    draft, u1 = await ask("Write one reply to the customer from these answers.",
                          str(parts), Answer)
    review, u2 = await ask(
        "You did not write this reply. Check that it answers every concern in "
        "the email and promises nothing the record does not support.",
        f"<email>{EMAIL}</email>\n<record>{CUSTOMER}</record>\n"
        f"<reply>{draft.reply}</reply>", Review)
    print(draft.reply)
    print(f"review: approved={review.approved}, issues={len(review.issues)}")

    usage = [u0, u1, u2] + [u for _, _, u, _ in done]
    inp = sum(u.input_tokens for u in usage)
    out = sum(u.output_tokens for u in usage)
    cost = (inp * 0.1 + out * 0.5) / 1e6  # Luna: $0.10 in, $0.50 out per 1M
    print(f"{len(usage)} calls, in={inp} out={out}, ${cost:.4f}")
    wall, slow = time.perf_counter() - t0, max(s for *_, s in done)
    print(f"total {wall:.1f}s; workers {slow:.1f}s in parallel "
          f"vs {sum(s for *_, s in done):.1f}s one by one")

asyncio.run(main())
