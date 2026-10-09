from anthropic import Anthropic

SYS = "You are a cloud architect. One sentence, no markdown."
Q = "We get 1,200 req/min at $0.0004 each. 30-day bill?"

client = Anthropic()
resp = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2048,
    system=SYS,
    messages=[{"role": "user", "content": Q}],
)
print([b.type for b in resp.content])

def text_of(resp):
    return "".join(
        b.text for b in resp.content if b.type == "text"
    )

print(text_of(resp))

cut = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=20,
    system=SYS,
    messages=[{"role": "user", "content": Q}],
)
print(cut.stop_reason)
print(repr(text_of(cut)), cut.usage.output_tokens)

def ask(messages, max_tokens=2048):
    r = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=max_tokens,
        system=SYS,
        messages=messages,
    )
    if r.stop_reason != "end_turn":
        raise RuntimeError(r.stop_reason)
    return r

F = "Does that fit a $25,000 budget?"
history = [{"role": "user", "content": Q},
           {"role": "assistant", "content": resp.content},
           {"role": "user", "content": F}]
for msgs in ([history[-1]], history):
    r = ask(msgs)
    print(r.usage.input_tokens, text_of(r))

n = client.messages.count_tokens(
    model="claude-sonnet-5-5", system=SYS, messages=history
)
print(n.input_tokens)

u = r.usage
cost = (u.input_tokens * 2 + u.output_tokens * 10) / 1e6
print(u.input_tokens, u.output_tokens, f"${cost:.6f}")
