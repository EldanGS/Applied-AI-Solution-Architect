import time
from anthropic import Anthropic
from emails import EMAILS, POLICY, SCHEMA, Ticket

client = Anthropic()
SYSTEM = [{
    "type": "text", "text": POLICY,
    "cache_control": {"type": "ephemeral", "ttl": "1h"},
}]
FORMAT = {"format": {"type": "json_schema", "schema": SCHEMA}}

requests = [{"custom_id": cid, "params": {
    "model": "claude-sonnet-5-5", "max_tokens": 1024,
    "system": SYSTEM, "output_config": FORMAT,
    "messages": [{"role": "user", "content": email}],
}} for cid, email in EMAILS.items()]

batch = client.messages.batches.create(requests=requests)
print(batch.id, batch.processing_status)

while batch.processing_status != "ended":
    time.sleep(60)
    batch = client.messages.batches.retrieve(batch.id)
    print(batch.processing_status)
print(batch.request_counts)

tickets, usage, failed = {}, [], []
for r in client.messages.batches.results(batch.id):
    if r.result.type != "succeeded":
        failed.append(r.custom_id)
        continue
    msg = r.result.message
    ticket = Ticket.model_validate_json(msg.content[-1].text)
    tickets[r.custom_id] = ticket
    usage.append(msg.usage)

print(list(tickets)[:3])
print(tickets.get("email-008"))

inp = sum(u.input_tokens for u in usage)
write = sum(u.cache_creation_input_tokens or 0 for u in usage)
read = sum(u.cache_read_input_tokens or 0 for u in usage)
out = sum(u.output_tokens for u in usage)
print(f"in={inp} write={write} read={read} out={out}")

# $ per 1M tokens, Oct 2026: in 2, 1h write 4, read 0.20, out 10
std = ((inp + write + read) * 2 + out * 10) / 1e6
cost = (inp * 2 + write * 4 + read * 0.2 + out * 10) / 2e6
print(f"standard, no cache  ${std:.4f}")
print(f"batch, no cache     ${std / 2:.4f}")
print(f"batch + cache       ${cost:.4f}")

retry = [q for q in requests if q["custom_id"] in failed]
if retry:
    batch = client.messages.batches.create(requests=retry)
print(len(retry), "to resubmit")
