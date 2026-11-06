# Lesson 7 · Prompt Engineering and Evals with Claude and OpenAI in Python: recording script

The same text lives in the deck's speaker notes. Open the deck with `?notes` (or press N) to get a teleprompter that highlights the line for the current step.
`→` means press the arrow key, once per line. `[FACE]` marks a good moment to cut to your face.
22 slides · 1288 spoken words · about 9:47 at ~150 words a minute, including about a second per key press.


## 0:00 · Measure a prompt

### 1. Cold open: the finished result  ·  0:00, ~27 s

Same twenty support emails, two versions of one prompt. The vague one passes thirteen of twenty on gpt-6-luna. The better one passes nineteen, and a check in code lets it ship. I'm Eldan: I built search ranking at Bing and AI features at Apple. By the end, you'll have a small eval that scores any prompt change on Claude and OpenAI. No more judging prompts by eye.

### 2. Stop judging prompts by eye  ·  0:27, ~6 s

[FACE] This is Lesson 7: prompt engineering, with evals. Every prompt change gets a score.

### 3. Lesson 7 of the Applied AI series  ·  0:33, ~22 s

Last lesson, coding agents worked in your repo. Today we go back to Lesson 3's Ticket and measure how often it's right.

→ You build twenty labeled emails, one harness that scores any prompt on both vendors, and a better prompt. It ships only if it matches or beats the old score.

### 4. An eval is a test suite for a prompt  ·  0:55, ~42 s

An eval is a test suite for a prompt. It starts with a dataset: twenty real emails, each labeled with the right ticket.

→ Run every email through the prompt and the model.

→ Grade in code: compare each field with the label. Exact match.

→ Score: a case passes only if all three fields match. Our vague prompt: thirteen of twenty.

→ Read the misses. They come in clusters. Change one thing, and run the same twenty again.

→ The gate: the new version ships only if the score doesn't drop. A unit test, for a prompt.

### 5. Same eval, different knobs  ·  1:37, ~38 s

Same eval on both vendors. Five things differ.

→ The prompt goes in system on Claude. On OpenAI, in instructions or a developer message.

→ House style: Anthropic's docs use XML tags for sections, OpenAI's use Markdown headers.

→ The typed ticket: Lesson 3's parse calls, with mirrored names. parsed_output, output_parsed.

→ temperature is gone. The Claude SDK raises a TypeError. gpt-6-luna returns a 400 while it reasons. Consistency comes from the eval.

→ What's left is effort, plus verbosity on OpenAI. Change one, then re-run the eval.

## 2:15 · Build the eval

### 6. Build the eval  ·  2:15, ~6 s

Chapter two: build the eval.

### 7. Twenty emails, each with the right ticket  ·  2:21, ~34 s

The shared file, cases.py: one list for both vendors.

→ Each case: an ID and a real email.

→ Plus want: the ticket you want back. You label it by hand, from your team's rules. That's the real work.

→ Add hard cases on purpose. A polite double charge is urgent.

→ Shouting with no deadline is not. Anger isn't urgency.

→ Twenty cases: everyday ones, plus the traps. Start with twenty to fifty from real traffic.

### 8. One email in, one ticket out  ·  2:55, ~35 s

The Claude file. Imports and client as in Lesson 3, plus the cases.

→ Lesson 3's Ticket, unchanged. The eval grades these three fields.

→ run takes a prompt and one email, and calls messages dot parse.

→ The prompt goes in system. It's the only thing we change between versions.

→ No ticket, for example after a refusal: run returns an empty dict. It counts as a miss, and the eval keeps going.

→ One email in, one ticket out.

### 9. Grade every field, count the passes  ·  3:30, ~31 s

Now the grader, score. Same code in both files.

→ For each case, run the prompt, and keep what we got and what we want.

→ bad lists the fields that don't match. Exact match, plain Python.

→ Print each wrong field next to the right value. You'll read these.

→ A case passes only if all three fields match. score returns the count.

→ Ten lines. That's the whole grader.

### 10. Score the prompt everyone writes first  ·  4:01, ~23 s

Version one: the prompt most of us write first. One vague sentence.

→ Score it, and print the result.

→ Run it on Claude. Each ✗ line is one wrong field, next to the value we wanted. The last line is the score: your baseline. Every new version has to match or beat it.

### 11. Same harness on gpt-6-luna  ·  4:24, ~24 s

OpenAI. Only one function differs: run.

→ responses dot parse, with text_format equals Ticket.

→ The prompt goes in instructions.

→ output_parsed, with the same empty-dict fallback. score is identical.

→ Run version one on gpt-6-luna.

→ Thirteen of twenty. Seven emails fail, some on two fields. Next chapter, we read them.

## 4:48 · Improve the prompt

### 12. Improve the prompt  ·  4:48, ~6 s

Chapter three: improve the prompt.

### 13. Read the misses, not just the score  ·  4:54, ~36 s

Version one on gpt-6-luna. Twenty emails, one cell each.

→ Thirteen pass, seven fail. Don't fix them one by one. Group them.

→ Three clusters. Urgency read from tone: anger looks urgent, a quiet double charge doesn't. IDs copied as typed. And category boundaries: an exchange lands in other, praise for the driver in shipping.

→ Each cluster points to a lever. Vague judgment: explicit criteria. A format: a rule plus an example. Fuzzy categories: say what goes where. All three go into version two.

### 14. v2: a role, then explicit rules  ·  5:30, ~41 s

Version two opens with a role. One line: what this model does, for whom.

→ The rules sit in rules tags, so Claude can tell instructions from the email.

→ Categories, spelled out. Money is billing, even when delivery is late. Cancels, returns and exchanges are shipping. Praise is other.

→ order_id: the format, one fix as an example, and what is not an ID.

→ urgent: a checklist, not a feeling. A double or unknown charge, or a date the customer needs. Anger alone isn't urgent.

→ Calm, plain sentences. No capitals, no MUST.

### 15. Show the rules with three examples  ·  6:11, ~31 s

Then three examples, each in example tags. They show the rules instead of telling them.

→ Shouting, but not urgent, and the ID rewritten as A-1042.

→ A late delivery plus money: billing.

→ A tracking number is not an order ID, and a named day makes it urgent.

→ None of these emails is in the test set. If they were, the score would measure memory, not the prompt.

### 16. Same words, OpenAI’s house style  ·  6:41, ~23 s

On OpenAI: the same words, in OpenAI's house style.

→ Markdown sections. Identity first: the role.

→ Instructions as bullets. The same rules, word for word.

→ Examples get their own header, still in XML tags, with ids. The format follows each vendor's docs. The gain comes from the rules and examples.

### 17. Score v2, gate it, run both  ·  7:04, ~31 s

Same score function for version two. The prompt changed. The harness didn't.

→ Then a gate. If v2 scores lower than v1, the assert stops the release.

→ Run it. Claude first: the misses, the score, and the gate.

→ gpt-6-luna: nineteen of twenty. Gate passed.

→ One miss in this run: c01. The order was due Monday, and the model read that date as a deadline. Keep it in mind.

### 18. v1 vs v2, scored  ·  7:35, ~23 s

Before and after, on all twenty emails.

→ Version one: Claude, then gpt-6-luna at thirteen of twenty.

→ Version two: gpt-6-luna at nineteen.

→ I ran each version six times. On Luna, v1 scored twelve to fifteen, v2 nineteen or twenty. Models aren't deterministic, so run more than once before you trust a gain.

## 7:58 · Gate every change

### 19. A prompt change ships with a score, or it doesn’t ship.  ·  7:58, ~26 s

[FACE] The rule: a prompt change ships with a score, or it doesn't ship.

→ Exact match works for labels. For free text, like a reply's tone, use an LLM judge: a second model grades against a pass-or-fail rubric. Check it against your own labels first. On OpenAI, the Evals platform is deprecated; Promptfoo is the documented path. The Claude Console has an Evaluate tool.

### 20. Your turn: fix the last miss  ·  8:25, ~46 s

Your turn. Version two failed c01 in one of six runs: due Monday read as urgent. One run in six is a bug in production. Fix it with one change. Predict first: which number must not go down? Pause the video.

→ Here's mine. One rule: lateness alone isn't urgent.

→ Score it. The gate compares v3 with v2. That's the number.

→ gpt-6-luna: twenty of twenty in five of six runs. In the sixth, another email flaked, and the gate blocked v3. That's why one run is never proof.

→ One caveat: you tuned on these twenty. Keep a few fresh emails aside for a final check.

### 21. Judging a prompt on two hand-picked emails.  ·  9:10, ~19 s

[FACE] The most common mistake: judging a prompt on two emails you picked.

→ Same version one. On two hand-picked emails: two out of two. Looks perfect. On all twenty: thirteen. The emails you remember are the ones it already gets right. Score the whole set, every time.

### 22. Label real cases, score every prompt, and ship a change only if the score holds.  ·  9:29, ~17 s

[FACE] Label real cases, score every prompt, and ship a change only if the score holds.

→ Today's code is in the free hub, linked below.

→ In Lesson 8, you run this whole eval set at half price with batch APIs.
