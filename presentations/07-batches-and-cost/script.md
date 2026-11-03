# Lesson 8 · Batch API with Claude and OpenAI in Python: recording script

The same text lives in the deck's speaker notes. Open the deck with `?notes` (or press N) to get a teleprompter that highlights the line for the current step.
`→` means press the arrow key, once per line. `[FACE]` marks a good moment to cut to your face.
22 slides · 1281 spoken words · about 9:53 at ~150 words a minute, including about a second per key press.


## 0:00 · See where the money goes

### 1. Cold open: the finished result  ·  0:00, ~25 s

A hundred support emails, triaged into tickets by Claude and by OpenAI. Same tokens, three prices: list price, half price through the batch API, and less again with prompt caching. I'm Eldan: I built search ranking at Bing and AI features at Apple. By the end, you'll run a whole job at half price on both APIs, then stack caching on top.

### 2. Pay half price for the same tokens  ·  0:25, ~7 s

[FACE] This is Lesson 8: batch APIs and prompt caching. Same tokens, half the price, then less.

### 3. Lesson 8 of the Applied AI series  ·  0:31, ~18 s

In Lesson 7 you wrote a prompt that turns support emails into tickets, and scored it with an eval.

→ Today you run it on a whole inbox: a hundred emails in one batch job, on Claude and OpenAI. Then you add prompt caching.

### 4. Where the money goes  ·  0:49, ~38 s

Every LLM bill is one formula: requests, times tokens, times price, times a tier multiplier.

→ Our hundred emails on Luna, real tokens, at list price: 1.4 cents.

→ Through the batch API, the tier multiplier is one half, on input and output: 0.71 of a cent.

→ Now cache the policy that every request repeats. On Luna, a cached read costs a tenth of the input price: 0.23 of a cent.

→ At a hundred thousand emails a month, that's $14.12 versus $2.26. Same model, same prompt.

### 5. A batch is a job, not a call  ·  1:27, ~42 s

A batch is a job, not a call.

→ One create call sends all hundred requests, each with a custom_id you choose.

→ The batch waits in a queue, so you poll its status, about once a minute.

→ Workers run your requests in parallel, in any order. Most finish within an hour. The limit is 24, with no latency guarantee.

→ Then you get one results file, and neither API promises its order.

→ So you match each result by custom_id, never by position.

→ The reward: half price on every token, on both vendors.

### 6. Same batch, different plumbing  ·  2:09, ~31 s

Same idea on both vendors. Different plumbing.

→ Claude takes a list: custom_id plus params. OpenAI takes a JSONL file.

→ Claude submits in one call. OpenAI uploads the file, then creates the batch.

→ Claude is done at ended. OpenAI at completed, or failed, expired, cancelled.

→ Claude streams the results. OpenAI gives you two files: outputs and errors.

→ Same deal on both: half price, within 24 hours.

## 2:40 · Batch it on Claude

### 7. Batch it on Claude  ·  2:40, ~6 s

Chapter two: batch it on Claude.

### 8. One request = custom_id + params  ·  2:46, ~41 s

emails.py holds the job for both files: Lesson 3's Ticket, its schema, an 1,100-token triage policy, and a hundred emails.

→ The policy is the system prompt. Every request repeats it, so it gets a cache marker: chapter four.

→ A batch has no parse helper, so the schema goes in raw, in output_config.

→ Each request has two keys. custom_id: a name you choose. Here, the email's key.

→ And params: exactly what you'd pass to messages dot create.

→ One request per email. A hundred.

→ No API call yet. Only data.

### 9. Submit once, then poll  ·  3:28, ~36 s

Submit it.

→ One call sends the whole list. You get an ID back at once, in_progress. Save that ID: after a crash, you poll it again instead of paying twice.

→ Then poll every minute, until it says ended.

→ Run it. [PENDING real Claude run: minutes until ended] Most finish within an hour, but plan for 24.

→ The four outcome counts stay at zero until the batch ends. [PENDING real Claude run: final counts]

→ One call, one loop.

### 10. Read results by custom_id  ·  4:04, ~35 s

Now the results.

→ batches dot results streams them back, one per request.

→ Check the type. Errored, canceled or expired: no message, and not billed. Keep the custom_id to resend it.

→ Succeeded: thinking comes first, so the JSON is the last block. Validate it into a Ticket, under its custom_id.

→ Keep the usage for the bill.

→ Run it. [PENDING real Claude run: first three IDs and email-008's ticket]

→ Every answer under its own ID.

## 4:39 · Batch it on OpenAI

### 11. Batch it on OpenAI  ·  4:39, ~6 s

Chapter three: batch it on OpenAI.

### 12. One JSON line per request  ·  4:45, ~28 s

OpenAI. Same emails, same policy, same schema.

→ The format is raw JSON schema here too: a name, the schema, strict.

→ Each line: the custom_id, method POST, and the endpoint URL.

→ The body is exactly what responses dot create takes. One model per file.

→ Join the lines with newlines: that's a JSONL file, as bytes.

→ Still no API call.

### 13. Upload, create, poll  ·  5:13, ~29 s

Upload, then submit.

→ files dot create, with purpose batch.

→ batches dot create points at the file. The endpoint must match every line's url, and 24 hours is the only window.

→ Then poll until one of four final statuses.

→ Run it. Validating first: OpenAI checks the whole file before it starts. Then in_progress, and completed after 12 minutes.

→ Upload, create, poll.

### 14. Two files back, joined by custom_id  ·  5:42, ~32 s

Two files come back.

→ Outputs and errors. read_jsonl turns one into a list of dicts.

→ Each body is a normal Responses API response. Response dot model_validate turns it back into the object from Lesson 2.

→ output_text works again. Validate the Ticket, keyed by custom_id.

→ Run it. First three: 000, 001, 002. In order, this time. And email-008, the double charge: billing, A-1009, urgent.

→ Two files, joined by ID.

## 6:14 · Stack prompt caching

### 15. Stack prompt caching  ·  6:14, ~6 s

Chapter four: stack prompt caching.

### 16. Pay for the shared prefix once  ·  6:20, ~50 s

All hundred requests start with the same 1,100-token policy. Only the email changes.

→ The first request writes that prefix to a cache. That costs extra: double the input price on Claude's one-hour cache, a quarter more on OpenAI.

→ Later requests read it: five percent of the input price on Sonnet 5.5, ten on Luna. Only the email pays full price.

→ On Claude, cache_control marks where the prefix ends, with a one-hour TTL, because batches outlive five minutes. OpenAI caches automatically above 1,024 tokens. Keep the prefix identical, and first.

→ In a batch, hits are best-effort, because requests run in parallel. Ours: 98 of a hundred on OpenAI. [PENDING real Claude run: Claude hit count]

### 17. Read the hits, price the bill  ·  7:10, ~32 s

Every result carries its usage. Add it up.

→ Claude calls writes cache_creation_input_tokens, and hits cache_read_input_tokens.

→ input_tokens is only what comes after the cache marker. The full input is all three.

→ List price: two dollars per million tokens in, ten out.

→ Batch plus cache: writes at double, reads at a tenth, all halved. Run it: [PENDING real Claude run: the three prices]

→ Priced from what the API reported.

### 18. Same bill, one trap  ·  7:42, ~34 s

OpenAI calls them cache_write_tokens and cached_tokens.

→ The trap: OpenAI's input_tokens already includes them. Claude's doesn't. Subtract them to get the fresh input, or your cost report is wrong.

→ List price: ten cents per million tokens in, fifty out.

→ Batch plus cache. Run it: 1.4 cents, 0.71 of a cent, 0.23 of a cent. Zero errors.

→ Luna costs a twentieth of Sonnet per token. Model choice is the next lever, once an eval says it's good enough.

### 19. Batch only when nobody is waiting.  ·  8:16, ~19 s

[FACE] One rule before you batch everything: batch only when nobody is waiting. A blocking pre-merge check, a chat reply, live triage: someone is stuck, and a batch can take 24 hours. Call the API directly there, with caching. Nightly reports, evals, backfills, yesterday's inbox: batch them.

### 20. Three of your 100 requests came back errored. Send those three again, and nothing else. Why not rerun all 100?  ·  8:35, ~32 s

Your turn. Three requests came back errored. Resend those three, nothing else. And predict: why not rerun all hundred? Pause and try it.

→ Here's mine.

→ Keep the requests whose custom_id is in failed.

→ Submit only those. When nothing failed, it prints zero to resubmit.

→ A full rerun pays again for ninety-seven good answers, and can file duplicate tickets. On OpenAI, write only the failed lines to a new file.

### 21. Matching batch results by position.  ·  9:07, ~23 s

[FACE] The most common batch mistake: matching results by position.

→ Our OpenAI file came back in order this time, so zipping by position would pass your test. The docs promise no order, so it breaks on a later run, with no error. Only wrong tickets. [PENDING real Claude run: Claude's first result ID] Key everything by custom_id.

### 22. Name every request with a custom_id, batch the job for half price, match results by ID, and cache the shared prefix.  ·  9:30, ~23 s

[FACE] Name every request with a custom_id, batch the job for half price, match results by ID, and cache the shared prefix.

→ Today's code is in the free hub, linked below.

→ In Lesson 9, one job gets too big for one prompt. You break it into subtasks, and orchestrate agents to run them.
