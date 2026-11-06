import asyncio
from typing import Literal
from anthropic import AsyncAnthropic
from pydantic import BaseModel

client = AsyncAnthropic()
MODEL = "claude-sonnet-5-5"
EMAIL = ("Where is my order A-2291? And did the refund for order A-1980, "
         "which I sent back, go through? - Dana")

# three data sources in plain code: one works, one hangs, one has no match
async def orders(q):
    return [{"order": "A-2291", "status": "shipped", "date": "2026-11-02",
             "carrier": "ParcelGo"}]
async def tracking(q):
    await asyncio.sleep(30)  # the carrier API hangs: every call times out
async def refunds(q):
    return []  # the query ran fine: there is no refund for A-1980

class Facts(BaseModel):
    facts: list[str]
class Answer(BaseModel):
    reply: str
# what a subagent hands back: never a bare exception, never a fake empty
class Result(BaseModel):
    source: str
    status: Literal["ok", "empty", "failed"]
    attempted: str
    attempts: int
    facts: list[str] = []  # on failure: the partial results, if any
    error: str | None = None
    retryable: bool | None = None

async def ask(system, user, schema):
    r = await client.messages.parse(
        model=MODEL, max_tokens=2048, system=system,
        messages=[{"role": "user", "content": user}], output_format=schema)
    if r.stop_reason != "end_turn":
        raise RuntimeError(r.stop_reason)
    return r.parsed_output, r.usage

async def subagent(source, fetch, query):
    for attempt in (1, 2, 3):
        try:
            rows = await asyncio.wait_for(fetch(query), timeout=1.0)
            break
        except Exception as e:  # any failure becomes an envelope
            retryable = isinstance(e, TimeoutError)  # retry transient only
            if not retryable or attempt == 3:
                return Result(source=source, status="failed", attempted=query,
                              attempts=attempt, error=type(e).__name__,
                              retryable=retryable), None
            await asyncio.sleep(0.5 * attempt)  # back off before retrying
    if not rows:  # the source answered "nothing": a finding, not an error
        return Result(source=source, status="empty", attempted=query,
                      attempts=attempt), None
    f, u = await ask("List the facts in these records that answer the "
                     "question. Short, one fact per item.",
                     f"<question>{query}</question>\n<records>{rows}</records>",
                     Facts)
    return Result(source=source, status="ok", attempted=query,
                  attempts=attempt, facts=f.facts), u

async def main():
    jobs = [("orders", orders, "status of order A-2291"),
            ("tracking", tracking, "carrier tracking for A-2291"),
            ("refunds", refunds, "refund for order A-1980")]
    done = await asyncio.gather(*(subagent(*j) for j in jobs))
    results = [r for r, _ in done]
    for r in results:
        print(f"{r.source}: {r.status} after {r.attempts} attempt(s)"
              + (f", {r.error}, retryable={r.retryable}" if r.error else ""))

    answer, u = await ask(
        "You are the Acme Shop support coordinator. Answer the email from the "
        "subagent results only. status empty: the source was searched and "
        "nothing matched, say so as a fact. status failed: we do not know, "
        "say what you could not check; never claim it does not exist.",
        f"<email>{EMAIL}</email>\n<results>{[r.model_dump() for r in results]}"
        "</results>", Answer)
    print(answer.reply)
    # the coverage gap is computed in code, from the envelopes
    gaps = [f"{r.source} ({r.error})" for r in results if r.status == "failed"]
    print(f"coverage: {len(results) - len(gaps)}/{len(results)} sources, "
          f"gap: {', '.join(gaps) or 'none'}")

    usage = [x for _, x in done if x] + [u]
    inp = sum(x.input_tokens for x in usage)
    out = sum(x.output_tokens for x in usage)
    cost = (inp * 2 + out * 10) / 1e6  # Sonnet 5.5: $2 in, $10 out per 1M
    print(f"{len(usage)} calls, in={inp} out={out}, ${cost:.4f}")

asyncio.run(main())
