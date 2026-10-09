from openai import OpenAI

SYS = "You are a cloud architect. One sentence, no markdown."
Q = "We get 1,200 req/min at $0.0004 each. 30-day bill?"

client = OpenAI()
resp = client.responses.create(
    model="gpt-6-luna",
    instructions=SYS,
    input=Q,
    max_output_tokens=1000,
)
print([i.type for i in resp.output])
print(resp.output_text)

cut = client.responses.create(
    model="gpt-6-luna",
    instructions=SYS,
    input=Q,
    max_output_tokens=32,
)
print(cut.status, cut.incomplete_details.reason)
print(repr(cut.output_text), cut.usage.output_tokens)

r2 = client.responses.create(
    model="gpt-6-luna",
    instructions=SYS,
    input="Does that fit a $25,000 budget?",
    previous_response_id=resp.id,
)
print(r2.usage.input_tokens, r2.output_text)
for x in (resp, cut, r2): client.responses.delete(x.id)

n = client.responses.input_tokens.count(
    model="gpt-6-luna", instructions=SYS, input=Q
)
u = resp.usage
print(n.input_tokens, u.input_tokens, u.output_tokens)
print(u.output_tokens_details.reasoning_tokens)
cost = (u.input_tokens * 0.1 + u.output_tokens * 0.5) / 1e6
print(f"${cost:.6f}")
