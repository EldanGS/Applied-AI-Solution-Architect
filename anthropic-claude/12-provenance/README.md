# Chapter 12 — Preserving Provenance

> **Exam domain(s):** Domain 5 — Context Management & Reliability (**15%**, task 5.6 in full; supports 5.3 coverage annotations and 5.1 structured upstream output) · Domain 1 — Agentic Architecture & Orchestration (**27%**, what flows between coordinator and subagents) · Domain 4 — Prompt Engineering & Structured Output (**20%**, schemas and citation formats, 4.2 / 4.3)
> **Est. time:** 5–7 hours (reading + 2 notebooks) · **Status:** [ ] not started

Provenance means every claim in a report can answer "who said this, when, and how did they measure it?" In a multi-agent system, every hop (search, analysis, coordinator, synthesis, report) is a chance to compress a finding and drop that link. As an architect you design provenance into the data contracts between agents, let the API produce verifiable citations where it can, and check it in code before anything reaches a reader.

## What you'll learn

- Why attribution is lost across hops, and the claim record that stops it
- How to handle conflicting values: classify, annotate both, let the coordinator reconcile
- Why data period, publication date and retrieval date must stay separate
- How to render by content type and report coverage gaps honestly
- How to use the Citations API, `search_result` blocks and web citations, and their limits
- How to audit provenance in code before publishing

## Prerequisites

- [00 — Prerequisites](../../00-prerequisites/README.md), [Chapter 2 — Tool Use](../02-tool-use/README.md), [Chapter 3 — Agent SDK](../03-agent-sdk/README.md), [Chapter 6 — Prompt Engineering](../06-prompt-engineering/README.md), [Chapter 10 — Multi-Agent Error Handling](../10-multi-agent-error-handling/README.md), [Chapter 11 — Context Management](../11-context-management/README.md)
- Snippets assume `client = anthropic.Anthropic()`, `MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")` and `import json`.

## Concepts

The whole chapter is one idea: **a claim and its evidence travel together, as data, from the first agent that reads a source to the last line of the report.** Sections 12.5–12.10 are marked *expanded beyond the guide*: they go further than the official exam guide's task statements, into current API detail and practice.

### 12.1 The attribution loss problem

**Attribution loss** happens when a step compresses findings into prose. It keeps the *what* and drops the *who, when and how*. Source identity goes first, then verbatim excerpts, qualifiers ("estimated", "up to"), dates and methods. After two or three hops nobody downstream can recover the link. The fix is a **claim record**: one finding with its evidence attached, passed on as data. Sources live in a registry keyed by `source_id`. Fields that may be missing in the source are **required but nullable**, so the model writes `null` instead of inventing a date or URL ([Chapter 2](../02-tool-use/README.md#24-json-schemas-for-structured-output)):

```python
from pydantic import BaseModel, Field

class Source(BaseModel):
    source_id: str              # stable key: "S3", a URL, "kb://faq#v12"
    title: str
    url: str | None             # null for internal documents
    published: str | None       # ISO 8601; null if unknown, never guessed
    retrieved_at: str | None    # when our system fetched it
    methodology: str | None     # "phone survey, n=1,200"
    derived_from: str | None    # source_id of the original it re-reports

class Evidence(BaseModel):
    source_id: str
    excerpt: str                # verbatim quote, not a paraphrase
    location: str | None        # "p. 12", "chars 1040-1188", "block 3"

class Claim(BaseModel):
    claim_id: str
    statement: str              # keeps qualifiers: "estimated", "projected"
    subject: str
    metric: str | None
    value: float | None
    unit: str | None            # "%", "USD bn"
    period: str | None          # the period the value describes
    evidence: list[Evidence] = Field(min_length=1)  # no evidence, no claim
    confidence: float | None    # optional evidence strength 0-1; null if not rated

class ClaimBatch(BaseModel):    # what one subagent returns
    claims: list[Claim]
```

Tell each subagent: one finding per record, a verbatim excerpt, the page or section, and `null` for any date the source does not state. A finding without a source is not reported. Sources cite their own sources in different ways. Few-shot examples ([Chapter 6](../06-prompt-engineering/README.md#61-few-shot-prompting)) teach the mapping for inline citations ("(Smith, 2023)") vs numbered bibliographies ("[1]"), and for methods in a dedicated section vs a footnote. Two or three examples also reduce hallucinated fields, because the model sees what "not stated, so `null`" looks like. `confidence` is optional: a self-reported score is not calibrated, so measure it against labeled data before anyone routes claims on it (12.6).

> **Exam trap:** "Ask the final report writer to add citations at the end" cannot fix attribution loss: the links were dropped upstream. Subagents must output structured claim-source mappings, and every later step must preserve them. Likewise, when synthesis input is too large, an intermediate *summarization agent* is wrong: it saves tokens by destroying attribution. Have upstream agents return **structured data (key facts, citations, relevance scores)** instead (task 5.1; see [Chapter 11](../11-context-management/README.md)).

### 12.2 Handling conflicting data

Two credible sources give different values. Picking the "more credible" one, averaging, dropping the outlier, or stopping the analysis are all wrong. The exam's answer: **finish the analysis, include both values, annotate the conflict with full attribution, and let the coordinator reconcile before synthesis.** The coordinator sees the whole task and can request verification, so the decision belongs there. Many "conflicts" are two correct numbers about different things. Classify in code before you call it a conflict. The order of checks matters: if you test agreement before periods, 1.9 for 2023 and 1.9 for 2024 merge into one claim and a time series disappears.

```python
def classify(a: Claim, b: Claim, sources: dict[str, Source],
             rel_tol: float = 0.05) -> str:
    ka = (a.subject.lower(), (a.metric or "").lower(), (a.unit or "").lower())
    kb = (b.subject.lower(), (b.metric or "").lower(), (b.unit or "").lower())
    if ka != kb:
        return "different_quantity"     # report both, explain
    if a.value is None or b.value is None:
        return "not_numeric"            # keep both statements as they are
    if a.period is None or b.period is None:
        return "undetermined"           # cannot tell trend from conflict
    if a.period != b.period:
        return "temporal_difference"    # a time series, not a contradiction
    if abs(a.value - b.value) <= rel_tol * max(abs(a.value), abs(b.value)):
        return "agree"                  # corroborating: report together
    methods = {sources[e.source_id].methodology
               for e in a.evidence + b.evidence}
    if None not in methods and len(methods) > 1:
        return "methodology_difference" # show both with methods
    return "conflict"                   # same thing, same period: escalate
```

The conflict record holds both values with `claim_id`, `source_id`, `published`, `period`, `methodology` and `excerpt`. `conflict_detected` records that the sources *appear* to disagree. `conflict_type` records what classification found. `status` and `reconciliation` stay `unresolved` / `null` until the coordinator decides. Roles: the **analysis subagent** completes its analysis, records both values, sets `conflict_detected` and proposes an explanation. The **coordinator** presents both, requests verification, or escalates to a human, and writes `reconciliation`. **Synthesis** shows the conflict in a "contested" section with sources, dates and methods, never one smoothed number.

> **Exam trap:** "A regulator's filing puts market share at 24%, a trade-body survey puts it at 31% for the same year": **complete the analysis with both numbers, annotate the conflict with source attribution, let the coordinator reconcile before synthesis**. Any option that settles on one number early, or hides that the two disagree, is wrong.

### 12.3 Include dates for correct interpretation

Without dates, a **temporal difference looks exactly like a contradiction**. "Source A says 18%, source B says 26%" reads as a conflict; with "data for 2022" and "data for 2025" attached, it reads as growth. Keep three dates apart:

| Date | Field | Answers |
|---|---|---|
| **Data period** | `Claim.period` | "What time does this number describe?" |
| **Publication date** | `Source.published` | "How recent is this source?" |
| **Retrieval date** | `Source.retrieved_at` | "When did *we* read it?" (pages change) |

**Require nullable date fields** in every subagent schema: "unknown" is valid, an invented date is a defect. Resolve relative dates ("last quarter") against the source's publication date, not today. Give the model today's date when it must judge recency. Group by period before comparing, and apply a per-domain freshness policy in code. Web search results carry `page_age` (when the site was last updated) and web fetch results carry `retrieved_at`. Dates also make failures diagnosable: if a RAG system gives confident wrong answers right after a document refresh, chunk metadata (document version, published date, indexed-at time) shows answers citing a stale version. That points at retrieval and indexing, not the prompt.

> **Exam trap:** When numbers "contradict" and the sources are from different years, **require publication or data-collection dates in the subagents' structured output**. "Prefer the most recent source" is wrong: it hides the trend.

### 12.4 Render by content type

Converting everything into one format loses information. Match the form to the content:

| Content | Render as |
|---|---|
| Financial and statistical data | **Table** with value, unit, period, source and method columns |
| News and analysis | **Prose** with inline citations |
| Technical findings | **Structured list** (finding, evidence, implication) |
| Time series | **Chronological** table or timeline |
| Conflicts | **Contested** section with both values side by side |

A report for task 5.6 has a summary (each sentence ends in claim refs such as [C1][C4]), **well-established findings** (>= 2 independent, dated sources agree), **contested findings** (both values, sources, dates, methods), a key-figures table, coverage and limitations (12.6), and numbered sources. **Keep the sources' own characterizations.** "Up to 30%" must not become "30%", and "projected for 2027" must not become "is". Sample size and method belong next to the number. **Let code render, let the model write:** the model writes narrative and picks claim IDs; code builds tables and references from the claim records, so numbers cannot drift. For Claude app users (the Claude Certified Associate exam, CCAO-F): use structured data or an artifact for content people will reuse or compare, and inline answers for short explanations.

### 12.5 Carrying mappings through every hop *(expanded beyond the guide)*

Four rules keep claim records intact:

1. **Pass by reference, not by retelling.** The coordinator forwards the subagents' complete claim records (or the file they wrote) to synthesis. It does not re-summarize them. Anthropic's research-system post calls this avoiding the "game of telephone".
2. **Merge, never replace.** Claims about the same subject, metric, unit and period are merged, and their **evidence lists are unioned**.
3. **Check independence.** Two articles quoting one analyst report are one source. Count origins via `derived_from`, not URLs.
4. **Synthesis output references claim IDs**, so code can audit it (12.10).

```python
def key(c: Claim) -> tuple:
    return (c.subject.lower(), (c.metric or "").lower(),
            (c.unit or "").lower(), c.period)

def merge_claims(claims: list[Claim]) -> list[Claim]:
    merged: dict[tuple, Claim] = {}
    for c in claims:
        k = key(c) + (c.value,)
        if k in merged:
            seen = {(e.source_id, e.excerpt) for e in merged[k].evidence}
            merged[k].evidence += [e for e in c.evidence
                                   if (e.source_id, e.excerpt) not in seen]
        else:
            merged[k] = c.model_copy(deep=True)
    return list(merged.values())  # different values stay apart: 12.2
```

Getting claim records out of each hop:

- **Messages API:** `client.messages.parse(..., output_format=ClaimBatch)` with the Pydantic class, or `client.messages.create(..., output_config={"format": {"type": "json_schema", "schema": ...}})` with a raw JSON-schema dict. Neither can be combined with citations in the same request (12.7).
- **Agent SDK subagent:** put the claim schema in `AgentDefinition.prompt` and validate the returned text with Pydantic in the coordinator.
- **Final Agent SDK result:** `ClaudeAgentOptions(output_format=...)`, then read `ResultMessage.structured_output`.

> **Note: changed since the guide.** The official exam guide says the coordinator's `allowedTools` must include `"Task"`. The subagent tool is now called `Agent` ([Chapter 3](../03-agent-sdk/README.md#34-the-subagent-tool-agent-formerly-task)). On the exam, read `Task` as "the subagent-spawning tool".
>
> **Exam trap:** "Let the analysis agent hand its results straight to synthesis and skip the coordinator" is a false speed-up. The coordinator is the hub: it reconciles conflicts and tracks coverage. Pass large payloads *by reference* through it.

### 12.6 Coverage and uncertainty reporting *(expanded beyond the guide)*

A report can mislead through what it **leaves out**. Track coverage per sub-question as data (task 5.3, [Chapter 10](../10-multi-agent-error-handling/README.md)). `empty` and `failed` must stay distinct: "no results" is information, "could not look" is a gap.

| State | Meaning | In the report |
|---|---|---|
| `covered` | Searched, relevant results used | Normal findings with citations |
| `empty` | Searched successfully, **no matching results** (a valid answer) | "No sources found on X" |
| `failed` | Access failure: timeout, error, blocked | "News archives were unavailable; findings on X may be incomplete" |
| `not_searched` | Out of scope or never assigned | Listed under limitations |

**Derive support levels from evidence**, not from the model's self-rating: *well established* (>= 2 independent origins agree), *single source* ("According to [S3] ..."), *contested* (12.2), *no evidence found* (`empty` coverage, reported as an answer), *gap* (`failed` coverage). A self-reported confidence such as "0.8" (the optional 12.1 field) is not calibrated. Until you have measured it against labeled data, use it at most as a hint for a human reviewer ([Chapter 9](../09-escalation-human-in-the-loop/README.md)). This section is also how you communicate limits to stakeholders.

> **Exam trap:** When some sources time out, the synthesis **annotates coverage**: which conclusions are well supported and where gaps exist. Silent omission, failing the task, and one number ("80% of sources answered") are all wrong; the last hides *which* sub-question is affected.

### 12.7 The Citations API: document blocks *(expanded beyond the guide)*

With **Citations**, you send documents and Claude's answer comes back as text blocks whose `citations` point at exact locations. Citations are **guaranteed to contain valid pointers** to the provided documents, and `cited_text` does not count toward output tokens. Document citations work on all active models and on the Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud and Microsoft Foundry.

```python
doc = {
    "type": "document",
    "source": {"type": "text", "media_type": "text/plain",
               "data": "...full text..."},
    "title": "AI Music Market Review 2024",
    # context reaches the model but is never cited: put metadata here
    "context": json.dumps({"source_id": "S1", "published": "2024-03"}),
    "citations": {"enabled": True},
}
content = [doc]   # one block per source, in your registry's order
content.append({"type": "text", "text": "How large was the AI-generated "
                "music market in 2024? Report each source's figure, "
                "period and method separately."})
response = client.messages.create(
    model=MODEL, max_tokens=4096,
    messages=[{"role": "user", "content": content}])
```

| Document type | Citation `type` | Location fields |
|---|---|---|
| Plain text (chunked into sentences) | `char_location` | `start_char_index`, `end_char_index`: 0-indexed, end exclusive |
| PDF | `page_location` | `start_page_number`, `end_page_number`: **1-indexed**, end exclusive |
| Custom content (your blocks, no further chunking) | `content_block_location` | `start_block_index`, `end_block_index`: 0-indexed, end exclusive |

Every citation carries `cited_text`, `document_index` (over **all** document blocks in the request) and `document_title`. Code converts each cited block into a claim record, so the model never retypes a quote or URL. Confirm `document_title` when mapping `document_index` to your `source_id`. Custom content lets you control granularity (RAG chunks that must not be split).

- **All or none:** enable citations on every document in a request, or on none.
- **Only `source` text is citable.** `title` and `context` are never cited. Images are not citable.
- **Structured outputs are incompatible.** Citations plus `output_config.format` returns a **400**. Use two steps: a cited answer, then code converts it (optionally a second structured call over the cited excerpts).
- **Cost:** slightly more input tokens. Put `cache_control` on document blocks to cache them. Works with token counting and the Message Batches API. When streaming, citations arrive as `citations_delta` events.

> **Exam trap:** "Ask Claude to output each quote and source URL in JSON" works, but the quotes are generated text that can be wrong. For documents you supply, Citations gives **valid pointers by construction**. Prompt-based mappings stay necessary where no API citations exist (subagent to coordinator).

### 12.8 `search_result` blocks: citations for your own retrieval *(expanded beyond the guide)*

For RAG you usually have chunks with a URL or internal ID. **Search result blocks** let Claude cite your chunks the way it cites web results. No beta header is needed.

```python
def kb_search(query: str) -> list[dict]:
    hits = retriever.search(query, k=3)   # vector, keyword or hybrid
    if not hits:
        return [{"type": "text", "text": "No results found."}]
    return [
        {
            "type": "search_result",
            "source": f"kb://{h.doc_id}#v{h.version}",  # include version
            "title": f"{h.title} (published {h.published})",
            "content": [{"type": "text", "text": p}
                        for p in h.paragraphs],   # one block per paragraph
            "citations": {"enabled": True},
        }
        for h in hits
    ]
# Inside the Chapter 2 tool loop: {"type": "tool_result", ...,
#   "content": kb_search(block.input["query"])}
```

**Citation shape:** `search_result_location` with `source`, `title`, `cited_text`, `search_result_index`, `start_block_index`, `end_block_index`. **Mixing rule:** in a `tool_result`, if any block is a `search_result`, all must be. All search results in a request have citations enabled, or all disabled. **Granularity:** Claude cites whole text blocks, never substrings. Your chunking strategy now sets citation granularity, so it is a provenance decision too. **Availability:** all active models; Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud and Microsoft Foundry.

### 12.9 Web search and web fetch citations *(expanded beyond the guide)*

The two server tools from [Chapter 2](../02-tool-use/README.md#27-client-tools-anthropic-schema-tools-and-server-tools-beyond-the-guide) bring their own provenance:

| | Web search | Web fetch |
|---|---|---|
| Citations | **Always on** | **Optional, off by default** |
| Citation type | `web_search_result_location` (`cited_text` up to 150 characters) | `char_location` or `page_location` (the page arrives as a `document` block) |
| Empty vs failed | Empty `content` list vs `web_search_tool_result_error` | `web_fetch_tool_result_error` |
| Price | $10 per 1,000 searches plus tokens | No additional charge beyond tokens |
| Not available on | Amazon Bedrock | Amazon Bedrock, Google Cloud (Google managed / Vertex AI) |

Two platforms get only the basic versions, without dynamic filtering: Vertex AI (Google managed) supports only `web_search_20250305`, and Microsoft Foundry hosted on Azure supports only `web_search_20250305` and `web_fetch_20250910`. Turn on fetch citations with `"citations": {"enabled": True}` in the web fetch tool definition; it works the same on every version (the latest is `web_fetch_20260318`; `use_cache` needs `web_fetch_20260309` or later). On `stop_reason == "pause_turn"`, send the assistant content back unchanged. `cited_text`, `title` and `url` of web search citations do not count toward input or output tokens. **Empty is not failed:** map an empty `content` list to `empty` and a `*_tool_result_error` to `failed` (12.6). **Display obligation:** when you show API output directly to end users, Anthropic's docs require the citations to the original source. **Retrieved content is untrusted:** a page can contain injected instructions, so keep it in tool results, never in the system prompt, and never let it trigger sensitive actions. Search results carry `page_age` and fetch results carry `retrieved_at` (12.3).

In the Claude apps, the **Research** feature runs several searches across the web and connected sources and returns a cited answer. It is on paid plans and needs web search turned on. Open those citations and check them before reusing the content.

### 12.10 Verifying provenance before you publish *(expanded beyond the guide)*

Citations make claims *checkable*; something must still *check* them. Run cheap deterministic checks in code first: every sentence has claim IDs, every claim exists and has evidence, every number appears in its evidence, every excerpt really is in the source, dates are present or marked unknown, contested claims are not in the established section, and every `failed` or `empty` sub-question appears in the coverage section.

```python
import re
CLAIM_REF = re.compile(r"\[(C\d+)\]")
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")        # "3.2", "3,200", "1,250.5"

def numbers(text: str) -> set[str]:
    return {n.replace(",", "") for n in NUMBER.findall(text)}

def audit(sentences: list[str], claims: dict[str, Claim]) -> list[str]:
    problems = []
    for s in sentences:
        refs = CLAIM_REF.findall(s)
        if not refs:
            problems.append(f"no claim reference: {s[:60]}")
            continue
        missing = [r for r in refs if r not in claims]
        if missing:
            problems.append(f"unknown claims {missing}: {s[:60]}")
            continue
        found = numbers(" ".join(e.excerpt for r in refs
                                 for e in claims[r].evidence))
        for num in numbers(CLAIM_REF.sub("", s)):
            if num not in found:               # whole-token match
                problems.append(
                    f"number {num} not found in evidence: {s[:60]}")
    return problems   # empty = publishable; else back to synthesis
```

The number check is deliberately strict: digits in a label such as Q4 or a report ID also count as numbers, so a false alarm sends the draft back for review instead of letting a wrong figure through.

Model-side checks: after drafting, have Claude find a supporting quote for each claim and **retract any claim it cannot support**. For an independent check, use a **fresh** instance that sees only the draft and the evidence ([Chapter 6](../06-prompt-engineering/README.md#66-self-correction)). For frequent simple fact checks during synthesis, give a narrowly scoped `verify_fact` tool; complex investigations still go through the coordinator. Prefer purpose-specific tools (`extract_data_points`, `verify_claim_against_source`) over a generic `analyze_document` ([Chapter 2](../02-tool-use/README.md)).

**Humans review** legal, medical, financial and regulatory outputs, contested findings that drive a decision, and high-impact single-source claims. A well-formatted citation can still point to a passage that does not say what the summary claims. When a confident summary cites a regulation subsection, **verify the citation against the official text** before sharing. The model's confidence is not evidence.

## Lesson code

Code from the video lesson: [../../presentations/12-provenance/code/](../../presentations/12-provenance/code/)

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Walk through 12.1–12.10 offline on stub responses, then build a multi-source research synthesizer (extract, merge, classify, reconcile, render, audit) with an optional live Citations API path |
| [`02_homework.ipynb`](02_homework.ipynb) | Self-test: a 10-question quiz, 6 auto-checked coding exercises plus an optional live one, an architecture scenario, and a scorecard |

## Cheat-sheet

| Situation | Choose | Over | Why |
|---|---|---|---|
| Final reports contain unattributed numbers | Subagents output structured claim-source records; every hop preserves them | "Add citations at the end", a citation-reminder prompt | Attribution lost upstream cannot be recovered downstream |
| Two credible sources disagree | Annotate both with attribution; coordinator reconciles | Pick by credibility, average, drop one, or block | Keeps information and puts the decision where the context is |
| Values differ across years | Carry data period and publication date; present as a trend | "Prefer the most recent source" | A temporal difference is not a contradiction |
| Answering over documents you supply | Citations API (`document` blocks, `citations.enabled`) | Asking the model to copy quotes and URLs into JSON | Valid pointers by construction; `cited_text` costs no output tokens |
| You need both citations and typed JSON | Two steps: cited answer, then convert in code (optionally a structured call over the cited excerpts) | Citations plus `output_config.format` in one call | That combination returns a 400 |
| RAG over your own chunks | `search_result` blocks with citations, one text block per citable unit | Plain text tool results | Claude cites your `source` and `title`; block granularity controls citation granularity |
| Some sources failed | Coverage annotations by sub-question; `empty` vs `failed` kept apart | Silent omission, one coverage percentage, failing the task | The reader must know where the gaps are |
| High-stakes report (legal, financial, regulatory) | Code audit, fresh-instance review, then human review | Publishing after one model pass | Valid-looking citations can still be misread |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **Prose hand-offs between agents.** "Here is a summary of what I found" with no records is where provenance dies.
- **Silently picking a winner** in a conflict, or averaging two incompatible numbers into one that no source reported.
- **Inventing metadata.** Required, non-nullable `published` or `url` fields push the model to make them up.
- **Counting URLs instead of origins.** Five articles repeating one press release are one source.
- **Combining citations with structured outputs** in one request (400), or enabling citations on only some documents (all or none).
- **Reporting "no results" and "timeout" the same way.** One is an answer, the other is a gap.

## Self-check

**1. (Multi-agent research system)** The coordinator receives two claim records about public EV fast chargers installed in 2025, both with `conflict_detected: true`. A national energy agency report counts 9,400; an industry association tally counts 13,100 for the same year and the same charger definition. The gap would change the report's recommendation. What should the coordinator do before synthesis?

- A) Send synthesis the average, 11,250, so the report shows one clear figure
- B) Keep only the figure from whichever source was published most recently
- C) Keep both values with their sources, dates and methods; ask a subagent to check how each source counts "installed" (or escalate to a human); record the outcome in `reconciliation`, and have synthesis show both in a contested section
- D) Forward both records to synthesis and tell it to use the more plausible number

<details><summary>Answer</summary>

**C.** Reconciliation is the coordinator's job: it sees the whole task and can request verification. Whatever it finds, both values and their attribution stay in the report until the conflict is explained. A invents a number that no source reported. B uses recency as a tie-breaker for two figures about the same year, which hides the conflict. D pushes the decision to synthesis, which has less context than the coordinator.
</details>

**2. (Multi-agent research system)** Final reports read well, but reviewers keep finding statistics with no source, and some figures cannot be traced to any document. Subagents currently return a few paragraphs of summary each. What fixes the root cause?

- A) Tell the report-writing agent to cite sources wherever possible
- B) Require subagents to return structured claim records (statement, verbatim excerpt, source URL or document name, location, dates) and have every later step preserve and merge them
- C) Add a final agent that searches the web for a source for each sentence in the finished report
- D) Raise the synthesis agent's `max_tokens` so it has room to include citations

<details><summary>Answer</summary>

**B.** Attribution is lost when subagents compress findings into prose; the claim-source link must be created at the source and carried through every hop. A asks for something the writer no longer has. C searches for sources *after* the claims were written, which can attach a source to a claim that never came from it. D addresses length, not missing data.
</details>

**3. (Multi-agent research system)** The synthesis agent flags a "contradiction": one source says 18% of employees work fully remote, another says 26%. On inspection, the first measures 2022 and the second 2025, but neither year appears in the subagents' output. What is the best fix?

- A) Tell the synthesis agent to always keep the newest source and drop the other
- B) Have the synthesis agent report the midpoint, 22%
- C) Require subagents to put the data period and publication date in their structured output, so synthesis can tell a trend from a conflict
- D) Remove older reports from the search scope

<details><summary>Answer</summary>

**C.** Without dates, a change over time looks exactly like a contradiction. With them, synthesis can report a rise from 18% to 26% between 2022 and 2025. A throws away valid history and hides the trend. B invents a number no source reported. D discards the evidence for the trend.
</details>

**4. (Structured data extraction, current API)** A team wants answers grounded in uploaded contract PDFs with page-level citations, and also wants the answer as a strict JSON object. They enable `"citations": {"enabled": true}` on the documents and set `output_config.format`, and the request returns a 400. What is the right design?

- A) Retry with exponential backoff
- B) Enable citations on only one of the documents
- C) Keep citations enabled and drop `output_config.format`; convert the cited text blocks (`page_location`, `cited_text`, `document_index`) into JSON records in code, and if extra fields are needed, run a second structured-output call over the cited excerpts
- D) Disable citations and ask the model to type page numbers into the JSON

<details><summary>Answer</summary>

**C.** Citations and structured outputs are incompatible by design, so the 400 is deterministic (A cannot help). B breaks the all-or-none rule for documents in a request. D gives up valid pointers for generated page numbers that can be wrong. The two-step design keeps verifiable citations and still produces typed records.
</details>

## Official documentation

- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations): document types, citation indices, token costs, the structured-outputs incompatibility, streaming `citations_delta`
- [Search results](https://platform.claude.com/docs/en/build-with-claude/search-results): `search_result` blocks for RAG, `search_result_location`, mixing rules, limitations
- [Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool): versions, `web_search_result_location`, `page_age`, pricing, display requirement
- [Web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool): optional citations, `retrieved_at`, `use_cache`, URL validation and exfiltration risks
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations): "I don't know", direct quotes, verify with citations and retract unsupported claims
- Engineering post: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (lead researcher, parallel subagents, a final citation step, filesystem outputs to avoid a "game of telephone")

[← Chapter 11 — Context Management](../11-context-management/README.md) | [↑ Claude path overview](../README.md) | [Chapter 13 — Claude Code Built-in Tools →](../13-claude-code-builtin-tools/README.md)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
