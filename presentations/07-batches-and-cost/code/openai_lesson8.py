import json
import time
from openai import OpenAI
from openai.types.responses import Response
from emails import EMAILS, POLICY, SCHEMA, Ticket

client = OpenAI()
FORMAT = {"format": {"type": "json_schema", "name": "ticket",
                     "schema": SCHEMA, "strict": True}}

jsonl = "\n".join(json.dumps({
    "custom_id": cid, "method": "POST", "url": "/v1/responses",
    "body": {"model": "gpt-6-luna", "instructions": POLICY,
             "input": email, "text": FORMAT},
}) for cid, email in EMAILS.items()).encode()

file = client.files.create(file=("emails.jsonl", jsonl),
                           purpose="batch")
batch = client.batches.create(input_file_id=file.id,
    endpoint="/v1/responses", completion_window="24h")
print(batch.id, batch.status)

DONE = ("completed", "failed", "expired", "cancelled")
while batch.status not in DONE:
    time.sleep(60)
    batch = client.batches.retrieve(batch.id)
    print(batch.status)
print(batch.request_counts)

def read_jsonl(file_id):
    text = client.files.content(file_id).text if file_id else ""
    return [json.loads(x) for x in text.splitlines()]

results = read_jsonl(batch.output_file_id)
errors = read_jsonl(batch.error_file_id)
tickets, usage = {}, []
for r in results:
    resp = Response.model_validate(r["response"]["body"])
    ticket = Ticket.model_validate_json(resp.output_text)
    tickets[r["custom_id"]] = ticket
    usage.append(resp.usage)

print(list(tickets)[:3])
print(tickets.get("email-008"))

details = [u.input_tokens_details for u in usage]
inp = sum(u.input_tokens for u in usage)
write = sum(d.cache_write_tokens for d in details)
read = sum(d.cached_tokens for d in details)
out = sum(u.output_tokens for u in usage)
print(f"in={inp} write={write} read={read} out={out}")

# $ per 1M, Oct 2026: in 0.10, write 0.125, read 0.01, out 0.50
std = (inp * 0.1 + out * 0.5) / 1e6
fresh = inp - write - read
cost = (fresh * 0.1 + write * 0.125 + read * 0.01
        + out * 0.5) / 2e6
print(f"standard, no cache  ${std:.4f}")
print(f"batch, no cache     ${std / 2:.4f}")
print(f"batch + cache       ${cost:.4f}")
print(len(errors), "errors")
