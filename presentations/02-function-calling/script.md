# Lesson 3 · Function Calling with Claude and OpenAI from Python in 15 Minutes: recording script

The same text lives in the deck's speaker notes. Open the deck with `?notes` (or press N) to get a teleprompter that highlights the line for the current step.
`→` means press the arrow key, once per line. `[FACE]` marks a good moment to cut to your face.
27 slides · 1784 spoken words · about 13:50 at ~150 words a minute, including about a second per key press.


## 0:00 · Understand how tool calling works

### 1. Cold open: the finished result  ·  0:00, ~29 s

Claude and OpenAI just called my Python function. I'm Eldan: I built search ranking at Bing and AI features at Apple. Neither model can see my order database. So each one asked my code to look up order A-1001, then answered with the real status. Both also turned an angry email into a typed Python object. The model asks. Python acts.

### 2. Let the model call your Python  ·  0:29, ~7 s

[FACE] This is Lesson 3: function calling on Claude and OpenAI. One loop, written by hand. No framework.

### 3. Lesson 3 of the Applied AI series  ·  0:36, ~25 s

Lesson 2 skipped one stop reason: tool_use. Today it runs the show.

→ You build a small support bot for an online shop. It looks up orders through your Python, runs one loop on both vendors, and turns emails into typed tickets. In Lesson 4, an agent SDK runs this loop for you. Today you learn exactly what it hides.

### 4. The model never runs your code  ·  1:01, ~56 s

One idea: the model never runs your code.

→ Your app sends the question plus a menu of tools. Each tool: a name, a description, a JSON schema.

→ The model doesn't answer. It asks: call get_order with A-1001. And that request carries an ID.

→ Your Python runs the function against your systems: database, CRM, payments. That's why permissions, limits and approvals live here, in code. Not in the prompt.

→ You send the result back, tagged with the same ID, plus the history.

→ Now the model has facts, and it answers.

→ Needs more data? It asks again. So in code this is a loop, not one call. Anthropic calls it tool use, OpenAI calls it function calling. Same loop. Every agent you ship runs on it.

### 5. Same loop, different names  ·  1:56, ~58 s

Same loop, different names. That's exactly where the bugs hide.

→ Claude asks with a tool_use block in content. OpenAI asks with a function_call item in output.

→ Arguments. Claude hands you a dict, input. OpenAI hands you a JSON string, arguments: json.loads it first.

→ The ID you answer. Claude: the block's id. OpenAI gives every call two IDs: id starts with fc, call_id starts with call. Answer with call_id.

→ Results. On Claude, all tool_result blocks in one user message. On OpenAI, one function_call_output per call.

→ Keep looping while stop_reason is tool_use, or while OpenAI's output still holds function calls.

→ And tool_choice. auto lets the model decide. none blocks tools. any, or required on OpenAI, forces a call. Sonnet 5.5 rejects forced calls with a 400, so we stay on auto.

## 2:54 · Define a tool

### 6. Define a tool  ·  2:54, ~6 s

Chapter two: define a tool.

### 7. Your data, your function  ·  3:00, ~40 s

The Claude file. Imports and client from Lesson 2, plus a system prompt: under twelve words.

→ The data the model has never seen: our orders. In a real project, your database or an internal API.

→ The tool: a plain Python function. No AI inside.

→ Unknown order? It raises, with a message that says what to do next: check the ID. The model will read that message.

→ The OpenAI file is identical, except lines two and four: import OpenAI, create an OpenAI client.

→ Plain Python. That's the whole tool.

### 8. The description is the router  ·  3:40, ~45 s

Now describe it. The description is how the model picks a tool, so it's the most important text here. Say what it does: look up one order, by ID.

→ What it returns: status and eta.

→ When to use it, and when not: any order question, but no ID means ask first. Wrong tool in production? Fix the description before you buy a bigger model.

→ Under it, a plain JSON schema: one string, order_id, required.

→ additionalProperties false: no extra keys. Strict mode needs this line on both vendors.

→ One description, one schema, shared by both files. Fix it once, fixed everywhere.

### 9. One tool, two shapes  ·  4:25, ~37 s

One tool, two shapes.

→ Both take a name and the description.

→ OpenAI adds type: function, because it also has built-in tools.

→ The schema key differs: input_schema on Claude, parameters on OpenAI.

→ And strict: true on both. Arguments are generated against your schema, so they always parse and always match. OpenAI adds one rule: every property must be required. Optional means required and nullable.

→ Migration trap: Chat Completions nests all this under a function key. The Responses API is flat, like here.

## 5:02 · Run the tool loop

### 10. Run the tool loop  ·  5:02, ~6 s

Chapter three: run the tool loop.

### 11. Run the call, return data  ·  5:08, ~49 s

TOOLS maps each tool name to a real function. Never eval a name a model gave you. Look it up in a table you control.

→ run_tool gets one tool_use block. input is already a dict: unpack it, call the function, JSON-encode the result.

→ If the function raises, don't crash, and don't skip the call. Keep the error text as the output, and flag the error.

→ A trace line. Arrow right: the model asked. Arrow left: we answered.

→ Return a tool_result. tool_use_id must be this block's id. And is_error tells the model this is an error, so it decides what to do next.

→ Every call gets an answer. Even a failed one.

### 12. The loop, on Claude  ·  5:58, ~66 s

The loop.

→ History starts with the question, and we loop at most five times. Always bound a tool loop: a confused model can't spin forever and burn tokens. Out of turns, ask returns None. In production, raise or hand off to a human right there.

→ Each turn: Lesson 2's create call, plus tools.

→ The line people get wrong: append the model's whole reply, r.content. Not the text. It holds the tool_use blocks, sometimes thinking too, and the API checks every result against them.

→ The exit. stop_reason isn't tool_use? Done. Return the whole response, so you can still check why it stopped.

→ Otherwise, collect every tool_use block. One reply can hold several: parallel calls. Run them all, and send every result back in one user message. Text before the results is a 400. Split them across messages, and Claude learns to stop calling in parallel.

→ Twelve lines. That's an agent loop.

### 13. Run it: real and missing  ·  7:04, ~35 s

Let's run it.

→ To print, read by type with text_of, the helper from Lesson 2.

→ Two questions: a real order, and one that doesn't exist. Run it.

→ A-1001: the model asked, our function said shipped, October 12, and the answer uses exactly that.

→ Z-999: our function raised. The error went back as data, and the model asked the customer to check the ID.

→ No crash. No invented status.

### 14. Same job, three differences  ·  7:38, ~32 s

OpenAI. Same job, three differences.

→ One: arguments is a JSON string. json.loads it first.

→ Two: there's no is_error flag. The error goes inside the output, as a small JSON object.

→ Three: return a function_call_output linked by call_id. Not id. The fc id names the item; call_id links your answer to the question. Mix them up, and the next request fails.

→ The table, the try-except, the trace: same as Claude.

### 15. The loop, on OpenAI  ·  8:10, ~41 s

The OpenAI loop.

→ A list of input items instead of messages. Same five-turn bound, same None when it runs out.

→ Each turn: responses.create with instructions, tools and the items so far.

→ Append all of r.output, reasoning items included. They travel with the function calls they produced.

→ No stop_reason on this API, so we look for function_call items. None? Done. Return the response.

→ Otherwise, run every call: one output per call.

→ We resend the full list instead of chaining previous_response_id, so you see exactly what the model gets.

### 16. Run it on gpt-6-luna  ·  8:51, ~24 s

Run it on gpt-6-luna.

→ output_text joins the text by type for you.

→ Same two questions. The real order: shipped, with its date.

→ Z-999: our error JSON went back as plain output, and Luna asked for the right ID.

→ Two vendors. One loop. No framework.

## 9:15 · Get guaranteed JSON

### 17. Get guaranteed JSON  ·  9:15, ~6 s

Chapter four: get guaranteed JSON.

### 18. Describe the shape once  ·  9:21, ~47 s

Tools are for fetching data or taking action. But often you just want data out of text: classify this email, pull out these fields. That's structured output. Two imports.

→ Describe the shape once, as a Pydantic model. category is a Literal: one of three values. other is the escape hatch, so the model never forces a wrong label.

→ order_id: str or None. The key is always there, and it's null when the email has no order number. That's the portable optional field on both vendors.

→ urgent: a real boolean.

→ And the input: an angry email.

→ In the OpenAI file: the same code, lines sixty to sixty-eight.

### 19. Claude: messages.parse  ·  10:08, ~41 s

Claude.

→ messages.parse: the same arguments as create, plus one.

→ output_format equals Ticket. The SDK turns the class into a JSON schema, and the API constrains the answer to it.

→ You read a Ticket from parsed_output.

→ Run it. Billing, A-1001, urgent: True. A Python object you can route on. Older guides force a tool call to get JSON. On Sonnet 5.5, a forced tool_choice is a 400, so this is the way now. One catch: thinking counts toward max_tokens, and a cut-off reply makes parse raise. Give it room.

### 20. OpenAI: responses.parse  ·  10:50, ~34 s

OpenAI.

→ responses.parse, with text_format equals Ticket.

→ And you read output_parsed. Watch out: the names are mirrored. Claude: output_format, parsed_output. OpenAI: text_format, output_parsed. Classic exam trap. Easy bug.

→ Same email, same Ticket. The rule: if the model must fetch or change something, give it a tool. If you only need its answer in a shape, use structured output. And if the model refuses, output_parsed is None. Check it before you route.

## 11:23 · Add a second tool safely

### 21. Add a second tool safely  ·  11:23, ~6 s

Chapter five: add a second tool. Safely.

### 22. Strict guarantees the shape, never the truth.  ·  11:29, ~19 s

[FACE] Before we add a tool that changes things, one rule. Strict guarantees the shape, never the truth. A perfectly valid call can still cancel a shipped order, or refund the wrong customer. Business rules live in your tool's code, where the model can't talk its way past them.

### 23. Add cancel_order. It must refuse shipped orders. Then ask: “Cancel my orders A-1001 and A-1002.” Does the loop need to change?  ·  11:49, ~40 s

Your turn. Add cancel_order. It must refuse shipped orders. Then ask: cancel my orders A-1001 and A-1002. First, predict: does the loop need to change? Pause the video and try it.

→ Here's mine.

→ cancel_order reuses get_order. Shipped? It raises. That one if statement is the guard, and it lives in Python.

→ Register it in TOOLS.

→ Add the definition: copy the first tool, with a new name and a description that says what it does and when. Same schema. Still strict.

→ And the loop? Not one line changes.

### 24. Two calls, one guard  ·  12:28, ~23 s

Run it on Claude.

→ Two cancel calls in one turn: parallel calls, same loop. The guard refused A-1001. A-1002 got cancelled.

→ And the model offered a return on its own. It picked the tool twice and combined the results.

→ That's the seed of an agent.

### 25. Same guard on gpt-6-luna  ·  12:52, ~12 s

Same code on gpt-6-luna.

→ Two calls. One refusal, one cancellation, and a return on offer.

→ The loop never changed.

### 26. Answering a tool call with the wrong ID.  ·  13:04, ~24 s

[FACE] The most common mistake in tool calling: answering with the wrong ID.

→ On Claude: a tool_use_id that matches no call from the last turn. On OpenAI: sending the fc id instead of call_id. Both fail with a 400. These are the real errors. Every call gets exactly one result, with its own ID, in the very next turn.

### 27. The model asks, your Python runs it, you answer by ID in a loop, and parse() returns typed JSON.  ·  13:28, ~23 s

[FACE] The model asks, your Python runs it, you answer by ID in a loop, and parse returns typed JSON.

→ Today's code is in the free hub, linked below.

→ In Lesson 4, the Claude Agent SDK and the OpenAI Agents SDK run this exact loop for you, and you build your first agent.
