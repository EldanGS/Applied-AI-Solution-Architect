# Lesson 5 · Set Up Claude Code and Codex for Your Team and CI: recording script

The same text lives in the deck's speaker notes. Open the deck with `?notes` (or press N) to get a teleprompter that highlights the line for the current step.
`→` means press the arrow key, once per line. `[FACE]` marks a good moment to cut to your face.
14 slides · 881 spoken words · about 6:35 at ~150 words a minute, including about a second per key press.


## 0:00 · Map Claude Code to Codex

### 1. Cold open: the finished result  ·  0:00, ~25 s

Claude Code and Codex just fixed the same failing test in CI, and nobody touched the keyboard. I'm Eldan: I built search ranking at Bing and AI features at Apple. You already use these agents on your laptop. Today you set them up once for your whole team, and run them in CI with guardrails they can't talk their way past.

### 2. Set up Claude Code and Codex for your team  ·  0:25, ~7 s

[FACE] This is Lesson 5: Claude Code and Codex, set up once for your team and your CI.

### 3. Lesson 5 of the Applied AI series  ·  0:31, ~22 s

In Lesson 3, the Claude Agent SDK ran the agent loop for you. Under the hood, that's Claude Code. In Lesson 4, you built an MCP server.

→ Today is the architect's part: one memory file and one skill for both agents, guardrails that are enforced, and a CI job your tests judge.

### 4. Same job, different files  ·  0:53, ~32 s

You already know both tools. Here's the map an architect needs: the same pieces, in different files.

→ Memory: CLAUDE.md, or AGENTS.md.

→ Skills: the same SKILL.md, in two folders.

→ Guardrails: allow and deny rules, or a sandbox and an approval policy.

→ MCP servers: .mcp.json, or a table in config.toml. Your Lesson 4 server plugs in right there.

→ Headless: claude dash p, or codex exec. That's your CI job.

## 1:25 · Set it up once for the team

### 5. Set it up once for the team  ·  1:25, ~6 s

Chapter two: set it up once, for the whole team.

### 6. AGENTS.md: what the agent can't guess  ·  1:31, ~45 s

AGENTS.md: plain markdown the agent reads before every task. Codex reads it as is.

→ One line on what this repo is.

→ The commands it can't guess, like the exact test command, so it can check its own work.

→ Your rules: where the business logic lives, and the don'ts.

→ Claude Code reads CLAUDE.md. Make it one line: an import of AGENTS.md. One source of truth, so two copies never drift apart.

→ Commit both to the repo, never to your home folder, or the next hire and your CI never see them. And keep it short: every line loads into every session.

### 7. One SKILL.md, two folders  ·  2:16, ~35 s

Memory loads in every session. A skill loads only when the task needs it: a folder with one SKILL.md.

→ The description is the trigger, like a tool description in Lesson 2. Until it fires, that's all the agent sees.

→ Then the steps: fix the source, never the tests, stop after three tries, and reply in one line.

→ Same file, two folders. Slash fix-tests in Claude Code, dollar fix-tests in Codex.

→ Write the workflow once, and both agents follow it.

### 8. Guardrails are enforced, not requested  ·  2:51, ~50 s

AGENTS.md says never edit the tests. That's a request: a model can still do it. Guardrails are enforced.

→ Claude Code: allow rules run without asking. Here, the test command and edits to Python files.

→ Deny rules never run: no edits under tests, no .env, no git push. Deny beats allow.

→ Codex: sandbox_mode is what commands can do, and the operating system enforces it: write in this repo, no internet. approval_policy is when to ask.

→ Both files live in the repo. But line one says it: Codex loads this only in a trusted repo. And Claude ignores the allow list until someone trusts the folder.

→ A CI runner trusts nothing. Hold that thought.

## 3:41 · Run it in CI

### 9. Run it in CI  ·  3:41, ~6 s

Chapter three: run it in CI.

### 10. The CI script: claude -p  ·  3:47, ~40 s

The CI job is a plain shell script. Claude first.

→ claude dash p: print mode, nobody at the keyboard. The prompt is the skill, and the output is JSON.

→ Caps: a pinned model, ten turns, one dollar. A confused agent can't loop all night.

→ allowedTools puts the allow rules in the command, because the runner ignores the repo's list.

→ Then three checks: print the report, run the tests yourself, and fail if anything under tests changed.

→ The real run: five turns, about four cents, and three tests passed.

### 11. The CI script: codex exec  ·  4:27, ~32 s

Codex: same shape.

→ codex exec runs the same skill, dollar fix-tests, and streams JSON Lines.

→ sandbox workspace-write, said out loud: on the runner, config.toml never loads, and exec starts read-only. Stdin comes from dev null, so it never waits.

→ The same three checks. Your tests decide, not the agent.

→ The real run: the same fix, three passed. And give the API key to this one step, never to the whole job.

### 12. Add a reviewer that reports bugs but can never write a file. What changes in each command?  ·  4:59, ~44 s

Your turn. Add a second job: a reviewer. It reports bugs, but it can never write a file. What changes in each command? Pause the video and try it.

→ Here's mine.

→ Claude Code: dash dash tools with only Read, Grep and Glob. In that session, the edit tools don't exist.

→ Codex: sandbox read-only. It's exec's default, but in CI you say it anyway.

→ I ran both: both found the Shipped bug, and git status stayed clean. Keep the reviewer a separate session, never the one that wrote the fix. To post PR comments, add a JSON schema to either command.

### 13. Trusting the repo's guardrails in CI.  ·  5:43, ~29 s

[FACE] The most common mistake: trusting the repo's guardrails in CI.

→ I ran both scripts without their flags. Claude ignored the allow rules, so even pytest was denied. Codex skipped config.toml and stayed read-only. Both exited zero: a green job, and nothing fixed.

→ So put the allow rules and the sandbox in the command, and let your tests decide. And never skip permissions on a runner that holds secrets.

### 14. One memory file, one shared skill, enforced guardrails, and a CI job your tests judge.  ·  6:13, ~22 s

[FACE] One memory file, one shared skill, enforced guardrails, and a CI job your tests judge.

→ The repo is in the free hub, linked below. Copy acme-shop into its own git repo and run either script.

→ Next, in Lesson 6: stop judging prompts by eye, and measure them with an eval.
