# Ep. 01 publish kit: Claude and OpenAI API Fundamentals

Replace before posting:

- `<YOUTUBE_LINK>`: the video URL, once it's uploaded.
- `<INTRO_VIDEO_LINK>`: the Ep. 00 video URL.

Links used below:

- Repo: https://github.com/EldanGS/Applied-AI-Solution-Architect
- Claude chapter: https://github.com/EldanGS/Applied-AI-Solution-Architect/tree/main/anthropic-claude/01-claude-api-fundamentals
- OpenAI chapter: https://github.com/EldanGS/Applied-AI-Solution-Architect/tree/main/openai-codex/01-responses-api-fundamentals

---

## 1. YouTube

### Title (pick one, max 100 chars, under ~70 so it isn't cut)

1. **Claude API vs OpenAI API: Fundamentals + Live Python Demo** (recommended)
2. Claude & OpenAI API Tutorial for Beginners (Python)
3. Messages API vs Responses API: How Claude and OpenAI Differ

Optional series suffix: ` | AI Architect Ep. 01`. Use it only if the title stays under ~70 chars.

### Description

```
Every Claude or OpenAI feature (tools, agents, MCP, coding agents) runs on one HTTP call. This episode covers that call on both platforms side by side, the Claude Messages API and the OpenAI Responses API, then runs everything live in Python (about 1 hour).

WHAT YOU'LL LEARN
• Why the reply is a typed list, not a string, and why content[0].text breaks
• How to tell why the model stopped: Claude's stop_reason vs OpenAI's status
• Who owns conversation state: stateless replay, previous_response_id or the Conversations API
• How to count tokens before a call and read usage after it
• Why the same workload costs 100x more on one model than another
• Effort settings, non-determinism, and how to test output that changes every run

FIVE RULES FOR THIS LAYER
1. Filter output by type, never by position.
2. Branch on the stop signal, never on prose.
3. Know who owns state and what it stores.
4. Count tokens. Budget for thinking.
5. Choose model and effort with an eval.

CHAPTERS
0:00 Intro: one HTTP call under everything
0:54 Why most incidents start at the API layer
2:36 Part 1: Request, response and roles
7:15 Part 2: Why the model stopped (stop_reason vs status)
10:48 Part 3: Conversation state
14:58 Part 4: Context window, tokens, cost and effort
19:48 Part 5: Non-determinism and production
21:18 Recap: same concepts, different names
23:00 Claude demo: setup
26:55 Inside the Anthropic Python SDK client
30:48 Claude: first call
31:54 Claude: the reply is a typed list
33:15 Claude: system prompts
34:45 Claude: max_tokens and stop_sequence
37:00 Claude: tool_use round trip
39:20 Claude: one handler for all seven stop reasons
40:42 Claude: stateless, your app owns the history
43:05 Claude: count_tokens vs usage
44:03 Claude: same workload, different model cost
44:39 Claude: low vs high effort
45:36 Claude: same request, different answer
47:18 Claude: streaming and async
51:30 OpenAI demo: setup
52:09 OpenAI: first call, typed output, incomplete responses
53:21 OpenAI: store=False, your app owns the state
54:48 OpenAI: previous_response_id and the Conversations API
59:51 Wrap-up and what's next

CODE, SLIDES AND NOTEBOOKS (free, open source)
Repo: https://github.com/EldanGS/Applied-AI-Solution-Architect
Claude chapter: https://github.com/EldanGS/Applied-AI-Solution-Architect/tree/main/anthropic-claude/01-claude-api-fundamentals
OpenAI chapter: https://github.com/EldanGS/Applied-AI-Solution-Architect/tree/main/openai-codex/01-responses-api-fundamentals
Demo from this video: 00_session_demo.ipynb in each chapter folder
Practice and homework: 01_practice.ipynb and 02_homework.ipynb

SERIES
Ep. 00 Intro: <INTRO_VIDEO_LINK>
Next: Ep. 02 Tool use and function calling

Prices shown were checked on 2026-10-03. Check the vendor pricing pages before any real estimate.

ABOUT THE SERIES
I'm learning in public on the way to Claude Certified Architect and the OpenAI API and Codex pathways. Every chapter has a theory page, a guided notebook and a self-test.

FOLLOW
LinkedIn: https://linkedin.com/in/eldan-abdrashim
X: https://x.com/eldan_nomad
Instagram and Threads: @eldan.nomad

#ClaudeAI #OpenAI #AIArchitect
```

### Tags (under 500 chars total)

```
Claude API, OpenAI API, Anthropic API, Claude Messages API, OpenAI Responses API, Claude API tutorial, OpenAI API tutorial, LLM API, Python, AI solution architect, Claude Certified Architect, AI engineering, GPT-6, Claude Sonnet, stop_reason, token counting, LLM cost, learning in public
```

### Pinned comment

```
Slides, the demo notebooks and practice exercises are free here: https://github.com/EldanGS/Applied-AI-Solution-Architect

Question for you: which API do you run in production, and what bit you first? Forgotten history, a loop that never stopped, or the bill?
```

### Upload settings

| Setting | Value |
|---|---|
| Thumbnail | Test & compare with all 3 variants. Metric: watch time share |
| Playlist | "Applied AI Solution Architect" (add Ep. 00 too) |
| Audience | No, it's not made for kids |
| Altered or synthetic content | No. The video is real footage; an AI-made thumbnail doesn't need the label |
| Paid promotion | No |
| Category | Education |
| Video language / caption language | English / English |
| Captions | Auto-captions, then review them: they mangle `stop_reason`, `max_tokens`, `previous_response_id`, "Claude" |
| Chapters | Manual chapters from the description. Turn off automatic chapters |
| License | Standard YouTube License |
| Embedding | Allow |
| Shorts remixing | Allow video and audio |
| Comments | On, sorted by Top |
| End screen (last 20 s) | Subscribe element + "Best for viewer" video or the series playlist |
| Cards | Link Ep. 00 near 0:30. Link the playlist at the recap |
| Visibility | Schedule for a time when you can reply to comments in the first hour |

---

## 2. LinkedIn

LinkedIn tends to show posts with outbound links to fewer people. You can post without the two link lines and put them in the first comment instead.

```
The bot forgot.
The agent never stopped.
The bill doubled.

None of these is a model problem. All three start at the same HTTP call.

Episode 01 of my Applied AI Solution Architect series is out: the Claude Messages API and the OpenAI Responses API side by side, then a live Python demo.

5 rules for this layer:

1. Filter output by type, never by position.
content[0].text breaks once thinking blocks show up.

2. Branch on the stop signal, never on prose.
stop_reason on Claude. status and incomplete_details on OpenAI.

3. Know who owns state and what it stores.
Claude: your app. OpenAI: your app, 30 days, or until you delete it.

4. Count tokens. Budget for thinking.
Thinking tokens are billed as output.

5. Choose model and effort with an eval.
Same workload: $0.45 to $45 per 1,000 requests.

Slides, demo notebooks and exercises are free on GitHub.

Video: <YOUTUBE_LINK>
Code: https://github.com/EldanGS/Applied-AI-Solution-Architect

Next episode: tool use and function calling.

Which API do you run in production, and what bit you first?

#ClaudeAI #OpenAI #AISolutionArchitect #LearningInPublic #BuildInPublic
```

---

## 3. X (thread, each post 280 chars or less)

Links cut reach on X, so the links go in the last post.

**Post 1**
```
The bot forgot. The agent never stopped. The bill doubled.

None of these is a model problem. All three start at one HTTP call.

New video: Claude Messages API vs OpenAI Responses API, side by side, with a live Python demo 🧵
```

**Post 2**
```
1/ The reply is a typed list, not a string.

Claude: thinking, text, tool_use blocks.
OpenAI: reasoning, message, function_call items.

content[0].text and output[0] break once reasoning shows up. Filter by type.
```

**Post 3**
```
2/ Branch on the stop signal, never on prose.

Claude: stop_reason, 7 values.
OpenAI: status + incomplete_details.reason.

A reasoning model can spend the whole output budget thinking and come back "incomplete" with empty text.
```

**Post 4**
```
3/ Know who owns state.

Claude is stateless: your app resends history every turn.
OpenAI: store=False replay, previous_response_id (30 days) or Conversations (until deleted).

Gotcha: previous_response_id does not carry your instructions.
```

**Post 5**
```
4/ Same workload, 100x price spread.

1,000 requests x (2K in + 500 out):
GPT-6 Luna $0.45
Sonnet 5.5 / GPT-6.1 Sol $9
Fable 5.1 / GPT-6 Astra $45

Thinking bills as output. Count tokens before, read usage after.
```

**Post 6**
```
5/ Same request, different answer.

On the newest Claude models a non-default temperature returns 400. Test properties, run 3-5 times, report a pass rate.

Video: <YOUTUBE_LINK>
Slides + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
```

---

## 4. Threads (500 chars per post)

**Main post**
```
The bot forgot. The agent never stopped. The bill doubled.

All three start at the API call, not the model.

Ep. 01 is out: Claude Messages API vs OpenAI Responses API, side by side, plus a live Python demo.

5 rules:
1. Filter output by type, never by position
2. Branch on the stop signal, never on prose
3. Know who owns state
4. Count tokens, budget for thinking
5. Pick model and effort with an eval

<YOUTUBE_LINK>
```

**Reply**
```
Slides, demo notebooks and exercises, free: https://github.com/EldanGS/Applied-AI-Solution-Architect

Next: tool use and function calling.
```
