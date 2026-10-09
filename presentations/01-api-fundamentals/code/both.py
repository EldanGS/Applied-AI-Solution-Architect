from anthropic import Anthropic
from openai import OpenAI

SYS = "You are a cloud architect. One sentence, no markdown."
Q = "We get 1,200 req/min at $0.0004 each. 30-day bill?"

c = Anthropic().messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2048,
    system=SYS,
    messages=[{"role": "user", "content": Q}],
)
o = OpenAI().responses.create(
    model="gpt-6-luna",
    instructions=SYS,
    input=Q,
    max_output_tokens=1000,
    store=False,
)


def report(name, text, why, u, p_in, p_out):
    cost = (u.input_tokens * p_in + u.output_tokens * p_out) / 1e6
    print(f"{name}: {text}")
    print(f"  stop={why}  in={u.input_tokens}  out={u.output_tokens}  ${cost:.6f}")


report("Claude", "".join(b.text for b in c.content if b.type == "text"),
       c.stop_reason, c.usage, 2.00, 10.00)
report("OpenAI", o.output_text, o.status, o.usage, 0.10, 0.50)
