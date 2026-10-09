# Lesson 2 · Call Claude and OpenAI from Python in 15 Minutes: recording script

The same text lives in the deck's speaker notes. Open the deck with `?notes` (or press N) to get a teleprompter that highlights the line for the current step.
`→` means press the arrow key, once per line. `[FACE]` marks a good moment to cut to your face.
22 slides · 1696 spoken words · about 13:04 at ~150 words a minute, including about a second per key press.


## 0:00 · Map one model call

### 1. Cold open: the finished result  ·  0:00, ~25 s

One script. Two models. The same question. I'm Eldan: I built search ranking at Bing and AI features at Apple. Claude and OpenAI both priced a thirty-day API bill: twenty thousand, seven hundred thirty-six dollars. And under each answer, the script prints why the model stopped, how many tokens it used, and what that exact call cost.

### 2. Call Claude and OpenAI from Python  ·  0:25, ~13 s

This is Lesson 2: call Claude and OpenAI from Python. In fifteen minutes you'll make the call, read the reply safely, catch a cut-off answer, keep a conversation going, and price every request.

### 3. Lesson 2 of the Applied AI series  ·  0:38, ~26 s

Lesson 1 mapped the architect role. This lesson is the floor everything else stands on.

→ Tool use in Lesson 3, agent SDKs in Lesson 4, MCP after that: all of it runs on this one call.

→ Today you build three things. The same call on both vendors. A guard that catches cut-off answers. And a two-turn chat with its real bill.

### 4. One stateless call, five fundamentals  ·  1:05, ~74 s

One idea runs this whole lesson.

→ A model call is one stateless HTTP request. One POST: v1/messages on Claude, v1/responses on OpenAI. Inside: a model, a token budget, your messages. Tools, structured output, effort: later, they're just more fields on this same request.

→ The reply is not a string. It's a typed list: thinking and text blocks on Claude, reasoning and message items on OpenAI. Read it by type, never by position.

→ Next to it, the stop signal. HTTP 200 means the request worked. It does not mean the answer is complete. Real failures, a 429 or a 500, get two automatic retries from both SDKs, then raise.

→ The API remembers nothing. For turn two, you append the reply and resend the whole history. You own the memory.

→ And usage is the bill: tokens in plus tokens out, times the price. Every call. Resent history included.

→ Call, typed reply, stop signal, memory, bill. Draw this for a customer, and you can debug almost any LLM integration they show you.

### 5. Same call, two vendors  ·  2:19, ~54 s

Same call, two vendors. Screenshot this table: learn one vendor, and the other becomes a lookup.

→ The call. Claude's messages.create requires model, max_tokens and messages. OpenAI's responses.create needs only model and input.

→ Your rules. Claude takes a top-level system field. OpenAI takes instructions, for this request only.

→ The reply. Claude returns content, a list of blocks. OpenAI returns output, a list of items, plus output_text, which joins the text for you.

→ Why it stopped. stop_reason on Claude. On OpenAI: status first, then incomplete_details.reason.

→ Memory. On Claude, you always resend. On OpenAI, resend, or chain with previous_response_id, because OpenAI stores responses for thirty days by default.

→ The bill. Both return usage, and hidden thinking is billed as output on both.

## 3:13 · Call Claude and OpenAI from Python

### 6. Call Claude and OpenAI from Python  ·  3:13, ~6 s

Chapter one: make the call, on both vendors.

### 7. Your first Claude call  ·  3:19, ~64 s

Here's the Claude file.

→ Import Anthropic, create a client. No arguments: it reads ANTHROPIC_API_KEY from your environment. Keys never live in code.

→ Two constants. A system prompt: you're a cloud architect, one sentence. And the question: twelve hundred requests a minute, four hundredths of a cent each. What's the thirty-day bill?

→ The call: messages.create, with the model ID as a plain string. In production, keep it in config, so a model swap isn't a deploy.

→ max_tokens is required. It's a hard cap on everything the model generates, hidden thinking included. Remember that for chapter two.

→ system is its own top-level field, not a message.

→ messages: a list of turns, each with a role and content.

→ Three required fields plus a system prompt. And no temperature: SDK 1.x removed it, and GPT-6 rejects it while it reasons. Porting old code? Delete it.

### 8. Read the reply by type  ·  4:22, ~44 s

What came back?

→ Print the type of every block in resp.content.

→ Run it. Thinking first, then text. A thinking block has no text attribute, so content[0].text would crash right here with an AttributeError. Ask something easy and you may get text only. Position is a trap.

→ So read by type. text_of joins every block whose type is text, and ignores the rest.

→ There's the answer: fifty-one point eight four million requests, about twenty thousand seven hundred thirty-six dollars. Correct.

→ This function is the first thing I add to every Claude codebase.

### 9. The same call on OpenAI  ·  5:06, ~54 s

Same question on OpenAI. The top of the file is identical: same SYS, same Q.

→ An OpenAI client. It reads OPENAI_API_KEY.

→ responses.create: OpenAI's recommended API for new projects. You'll still meet Chat Completions in older customer code.

→ instructions is your system prompt. input is a plain string, meaning one user message, or a list when you need history.

→ max_output_tokens is optional here, but it caps the same thing: reasoning plus answer. And store, which you don't see, defaults to true. OpenAI keeps this response for thirty days. Chapter three uses that.

→ Print the item types and output_text.

→ Run it. Reasoning, then message: the same shape as Claude. And output_text is OpenAI's built-in text_of.

## 6:00 · Check why the model stopped

### 10. Check why the model stopped  ·  6:00, ~6 s

Chapter two: check why the model stopped. A 200 is not done.

### 11. A 200 that isn’t done  ·  6:06, ~56 s

This bug ships empty answers to production.

→ Same request. max_tokens: twenty. Far too small, on purpose.

→ Print stop_reason, then the text and the output tokens.

→ Run it. stop_reason: max_tokens. Text: empty. Billed: twenty tokens. Claude spent the whole budget thinking and never reached the answer. No exception, HTTP 200. Without this check, your app shows a blank reply. On an easier question you'd get half a sentence, which is worse, because it looks real.

→ Claude has seven stop reasons. Today you need three. end_turn: finished. max_tokens: cut off. tool_use: the model wants your code. That's Lesson 3.

→ Branch on stop_reason in code, never on the prose. And fix max_tokens with a bigger budget or lower effort, not a reworded prompt.

### 12. Incomplete, empty, and still billed  ·  7:02, ~44 s

OpenAI. Same experiment.

→ max_output_tokens: thirty-two. The API minimum is sixteen, so this is as tight as it gets.

→ No stop_reason here. Check status. If it's incomplete, incomplete_details.reason tells you why. On a completed response that field is None, so status always comes first.

→ Then the text and the output tokens.

→ Run it. Incomplete, max_output_tokens. Empty text. Thirty-two tokens billed, all reasoning. Same lesson on both vendors: the budget includes thinking, and a tight budget can buy you nothing. On a customer project, this is the ticket that says the bot sometimes answers with nothing.

### 13. Wrap the Claude call in ask(messages). Return the response only when Claude finished; otherwise raise with the stop reason.  ·  7:46, ~46 s

Your turn. Wrap the call in a function, ask, that takes messages. Return the response only when Claude finished. Otherwise, raise with the stop reason. Pause the video and write it.

→ Here's mine. The same create call: messages passed in, max_tokens optional.

→ One check. stop_reason isn't end_turn? Raise, with the reason.

→ Otherwise return the whole response, not just the text. We still need its usage.

→ Test it with a budget of twenty.

→ Run it. RuntimeError: max_tokens. A loud failure instead of a silent empty answer. Delete the test line: ask runs the rest of this lesson.

## 8:32 · Keep a conversation going

### 14. Keep a conversation going  ·  8:32, ~6 s

Chapter three: keep a conversation going. The API remembers nothing.

### 15. Claude remembers nothing  ·  8:38, ~52 s

Turn two.

→ The follow-up: does that fit a twenty-five-thousand-dollar budget? "That" only means something if the model remembers turn one.

→ Claude has no session. So we build the history: the question, Claude's reply, the follow-up.

→ Append resp.content: the whole list of blocks, thinking included. Not just the text you printed.

→ Now ask twice: the new message alone, then the full history. Print input tokens and the answer.

→ Run it. Alone: forty-two tokens, and Claude asks what "that" means. With history: two hundred five tokens, and a real answer, about forty-two hundred dollars of headroom. Memory works. And you pay for it on every turn: each turn resends every earlier token.

### 16. Let OpenAI keep the history  ·  9:29, ~56 s

OpenAI gives you a choice. Replay the history yourself, exactly like Claude, with store set to false. Or let OpenAI keep it.

→ store defaulted to true, so we can pass previous_response_id.

→ One trap: instructions don't carry over. Resend them every turn, or the second answer loses your rules.

→ input is only the new question.

→ Run it. It remembers the bill. Now look at input tokens: one hundred thirty. You sent one short sentence and paid for the whole chain. Server-side state is convenient. It is not free.

→ Then clean up: delete all three stored responses, the cut-off one from chapter two included.

→ Thirty days of stored customer data is your client's compliance decision. Not a default you forget.

## 10:25 · Price every call

### 17. Price every call  ·  10:25, ~6 s

Chapter four: price every call. Before you send it, and after.

### 18. Count before, bill after  ·  10:31, ~41 s

Count before you send.

→ messages.count_tokens takes the same model, system and messages. It's free, and it returns an input-token estimate. Counts are model-specific: never estimate Claude with an OpenAI tokenizer, or with characters divided by four.

→ After the call, usage is the bill. Sonnet 5.5: two dollars per million tokens in, ten out. Input times two, plus output times ten, over a million.

→ Print both.

→ Run it. Counted two hundred five. Billed two hundred five. And this turn cost about a fifth of a cent, thinking included.

### 19. Reasoning hides inside output  ·  11:13, ~36 s

Same on OpenAI.

→ responses.input_tokens.count takes the request without generation options, and returns the input count.

→ Then usage: input, output, and the reasoning tokens inside output.

→ Luna: ten cents per million in, fifty cents out.

→ Run it. Counted forty-three, billed forty-three. Seventy-one out, forty-four of them reasoning. Here's the trap: reasoning is already inside output_tokens. Add it twice, and every estimate you send a customer is wrong. Your two cost levers: model tier and effort.

### 20. What 1,000 calls cost  ·  11:49, ~31 s

Now scale it the way a customer asks. A thousand calls. Two thousand tokens in, five hundred out.

→ Sonnet 5.5 or GPT-6.1 Sol, the same tier: nine dollars.

→ GPT-6 Luna or the new Claude Haiku 5.5: forty-five cents.

→ A twenty-times gap. So compare vendors inside a tier, and ship the cheapest model that passes your eval. That's also why the two costs at the start differed thirty-fold: Sonnet versus Luna.

### 21. dark  ·  12:20, ~17 s

The crash I find most in customer code: content zero dot text.

→ When Claude thinks first: AttributeError. On OpenAI: IndexError. Filter by type, or use output_text. One line, and it's the first thing I search for in a code review.

### 22. One stateless call: read the reply by type, check why it stopped, resend the memory, multiply usage by price.  ·  12:37, ~27 s

One stateless call: read the reply by type, check why it stopped, resend the memory, multiply usage by price.

→ Both lesson files and the side-by-side script are in the free hub linked below. Each runs in under ten seconds, for less than a cent.

→ In Lesson 3, the stop reason we skipped takes over: tool_use. Claude and OpenAI start calling your Python.
