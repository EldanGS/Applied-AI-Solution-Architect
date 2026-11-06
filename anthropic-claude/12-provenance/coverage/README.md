# Chapter 12 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

Requirement IDs come from the official exam guides (via the repo's requirements checklist) and the Applied AI architect role map. "Primary" means this chapter is the main place the item is taught; "supporting" means it is taught mainly in another chapter and reinforced here.

| Requirement ID | What it asks (short) | Where in this chapter | Depth (Primary/Supporting) |
|---|---|---|---|
| `CCAR-F/D5/5.6/K1` | How attribution is lost when findings are compressed without claim-source mappings | [12.1](../README.md#121-the-attribution-loss-problem) | Primary |
| `CCAR-F/D5/5.6/K2` | Structured claim-source mappings that synthesis must preserve and merge | [12.1](../README.md#121-the-attribution-loss-problem), [12.5](../README.md#125-carrying-mappings-through-every-hop-expanded-beyond-the-guide) | Primary |
| `CCAR-F/D5/5.6/K3` | Annotating conflicting statistics with attribution instead of picking one | [12.2](../README.md#122-handling-conflicting-data) | Primary |
| `CCAR-F/D5/5.6/K4` | Requiring dates so temporal differences are not read as contradictions | [12.3](../README.md#123-include-dates-for-correct-interpretation) | Primary |
| `CCAR-F/D5/5.6/S1` | Subagents output claim-source mappings (URLs, document names, excerpts) preserved downstream | [12.1](../README.md#121-the-attribution-loss-problem), [12.5](../README.md#125-carrying-mappings-through-every-hop-expanded-beyond-the-guide), [12.7](../README.md#127-the-citations-api-document-blocks-expanded-beyond-the-guide) | Primary |
| `CCAR-F/D5/5.6/S2` | Reports separating established from contested findings, keeping source characterizations and methods | [12.4](../README.md#124-render-by-content-type), [12.6](../README.md#126-coverage-and-uncertainty-reporting-expanded-beyond-the-guide) | Primary |
| `CCAR-F/D5/5.6/S3` | Completing analysis with conflicting values annotated; coordinator reconciles | [12.2](../README.md#122-handling-conflicting-data) | Primary |
| `CCAR-F/D5/5.6/S4` | Publication or collection dates in subagent output | [12.3](../README.md#123-include-dates-for-correct-interpretation) | Primary |
| `CCAR-F/D5/5.6/S5` | Rendering by content type (tables, prose, lists) | [12.4](../README.md#124-render-by-content-type) | Primary |
| `CCAR-F/APPX/IN/18` | Information provenance: claim-source mappings, temporal data, conflict annotation, coverage gaps | 12.1–12.6 | Primary |
| `CCAR-F/SC3` | Scenario: Multi-Agent Research System producing cited reports | Whole chapter, mini-project | Primary |
| `CCAR-F/EX4/3` | Subagent output separating content from metadata (claim, excerpt, source, date); synthesis preserves attribution | [12.1](../README.md#121-the-attribution-loss-problem), [12.5](../README.md#125-carrying-mappings-through-every-hop-expanded-beyond-the-guide), mini-project | Primary |
| `CCAR-F/EX4/5` | Conflicting source data: both values with attribution; established vs contested sections | [12.2](../README.md#122-handling-conflicting-data), [12.4](../README.md#124-render-by-content-type), mini-project | Primary |
| `CCAR-F/D1/1.3/S2` | Structured formats that separate content from metadata (source URLs, document names, page numbers) when passing context between agents, to preserve attribution | [12.1](../README.md#121-the-attribution-loss-problem), [12.5](../README.md#125-carrying-mappings-through-every-hop-expanded-beyond-the-guide) | Primary |
| `CCAR-F/D1/1.3/S1` | Passing complete prior findings (web search and document analysis outputs) to the synthesis subagent | [12.5](../README.md#125-carrying-mappings-through-every-hop-expanded-beyond-the-guide) | Supporting (primary: Chapter 3) |
| `CCAR-F/EX4/1` | Coordinator with 2+ subagents; `allowedTools` includes the subagent tool (`Task`, now `Agent`) | [12.5](../README.md#125-carrying-mappings-through-every-hop-expanded-beyond-the-guide) | Supporting (primary: Chapter 3) |
| `CCAR-F/D5/5.3/S4` | Coverage annotations in synthesis output | [12.6](../README.md#126-coverage-and-uncertainty-reporting-expanded-beyond-the-guide) | Supporting (primary: Chapter 10) |
| `CCAR-F/D5/5.3/K2` | Access failures vs valid empty results | [12.6](../README.md#126-coverage-and-uncertainty-reporting-expanded-beyond-the-guide) | Supporting (primary: Chapter 10) |
| `CCAR-F/D5/5.1/S6` | Upstream agents return structured data (key facts, citations) instead of verbose content | [12.1](../README.md#121-the-attribution-loss-problem), [12.5](../README.md#125-carrying-mappings-through-every-hop-expanded-beyond-the-guide) | Supporting (primary: Chapter 11) |
| `CCAR-F/D4/4.2/S4` | Few-shot for varied document structures (inline citations vs bibliographies) | [12.1](../README.md#121-the-attribution-loss-problem) | Supporting (primary: Chapter 6) |
| `CCAR-F/EX3/3` | Few-shot extraction from varied formats (inline citations vs bibliographies) | [12.1](../README.md#121-the-attribution-loss-problem) | Supporting (primary: Chapter 6) |
| `CCAR-F/D4/4.2/K4` | Few-shot examples reduce hallucination in extraction across varied document structures | [12.1](../README.md#121-the-attribution-loss-problem) | Supporting (primary: Chapter 6) |
| `CCAR-F/APPX/IN/13` | Nullable schema fields to prevent hallucinated values | [12.1](../README.md#121-the-attribution-loss-problem), [12.3](../README.md#123-include-dates-for-correct-interpretation) | Supporting (primary: Chapter 2) |
| `CCAR-F/SQ9`, `CCAR-F/D2/2.3/S3` | Scoped `verify_fact` tool for simple checks during synthesis; complex cases through the coordinator | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCAR-F/D2/2.1/S3` | Purpose-specific tools such as `verify_claim_against_source` instead of a generic `analyze_document` | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting (primary: Chapter 2) |
| `CCAR-F/D5/5.5/S4` | Routing ambiguous or contradictory source documents to human review | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting (primary: Chapter 9) |
| `CCAR-P/D3/3.5/S1` | RAG pipeline with appropriate chunking (chunk size as citation granularity) | [12.7](../README.md#127-the-citations-api-document-blocks-expanded-beyond-the-guide), [12.8](../README.md#128-search_result-blocks-citations-for-your-own-retrieval-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D4/4.4/S1`, `CCAR-P/D4/4.4/K2` | Diagnosing hallucinations (stale retrieval after a document refresh) | [12.3](../README.md#123-include-dates-for-correct-interpretation), [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D5/5.2/S1` | Risks and failure modes of LLM systems (attribution loss, conflict smoothing) | [12.1](../README.md#121-the-attribution-loss-problem), [12.2](../README.md#122-handling-conflicting-data) | Supporting |
| `CCAR-P/D5/5.3/S1` | Human-in-the-loop validation | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCAR-P/D5/5.5/K3` | Transparency | [12.6](../README.md#126-coverage-and-uncertainty-reporting-expanded-beyond-the-guide), [12.9](../README.md#129-web-search-and-web-fetch-citations-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D6/6.3/K2`, `CCDV-F/D6/6.3/K4` | Response validation; skepticism toward confident output | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D7/7.1/K1` | Prompt injection in untrusted (retrieved) content | [12.9](../README.md#129-web-search-and-web-fetch-citations-expanded-beyond-the-guide) | Supporting |
| `CCDV-F/D5/5.4/S1` | Token and cost management (`cited_text` not billed, caching documents) | [12.7](../README.md#127-the-citations-api-document-blocks-expanded-beyond-the-guide), [12.9](../README.md#129-web-search-and-web-fetch-citations-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/D2/2.1/S1` | Evaluate outputs for accuracy and completeness | [12.6](../README.md#126-coverage-and-uncertainty-reporting-expanded-beyond-the-guide), [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/D2/2.2/S1` (`K1`, `K2`), `CCAO-F/MQC/7` | Identify hallucinations and inconsistencies; practical understanding of AI limitations | [12.2](../README.md#122-handling-conflicting-data), [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/D2/2.3/S1` | Fact-checking and validation techniques | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/D2/2.4/S1` | When human review or extra verification is required | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/D2/2.6/S1` (K1–K3) | Output formats: artifacts, inline, structured data | [12.4](../README.md#124-render-by-content-type) | Supporting |
| `CCAO-F/SQ1` | Verify a cited regulation subsection against the official text | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide), More self-check questions 4 | Supporting |
| `CCAO-F/D3/3.1/S1` (`K2`), `CCAO-F/D4/4.2/S1` (`K1`), `ACAD/claude-101/10` | Research mode; using Claude for research | [12.9](../README.md#129-web-search-and-web-fetch-citations-expanded-beyond-the-guide) | Supporting |
| `CCAO-F/D4/4.5/S1` | Communicate Claude's value and limitations to stakeholders | [12.6](../README.md#126-coverage-and-uncertainty-reporting-expanded-beyond-the-guide) | Supporting |
| `ACAD/claude-with-the-anthropic-api/54`, `ACAD/claude-with-the-anthropic-api/LO8` | Academy lesson: Citations | [12.7](../README.md#127-the-citations-api-document-blocks-expanded-beyond-the-guide)–[12.9](../README.md#129-web-search-and-web-fetch-citations-expanded-beyond-the-guide) | Primary |
| `ACAD/claude-with-the-anthropic-api/42`, `ACAD/claude-with-the-anthropic-api/LO6` | Academy lesson: the web search tool | [12.9](../README.md#129-web-search-and-web-fetch-citations-expanded-beyond-the-guide) | Supporting (primary: Chapter 2) |
| `ACAD/claude-certified-associate-foundations/LO3`, `ACAD/claude-certified-associate-foundations/3/LO2`, `ACAD/claude-certified-associate-foundations/3/LO3` | CCAO-F prep: evaluate outputs, identify hallucinations, fact-check | [12.10](../README.md#1210-verifying-provenance-before-you-publish-expanded-beyond-the-guide), More self-check questions 4 | Supporting |
| `ACAD/claude-in-amazon-bedrock/56`, `ACAD/claude-with-google-vertex/59`, `ACAD/claude-with-google-vertex/LO7` | Academy lessons: Citations on Bedrock / Vertex | [12.7](../README.md#127-the-citations-api-document-blocks-expanded-beyond-the-guide), [12.8](../README.md#128-search_result-blocks-citations-for-your-own-retrieval-expanded-beyond-the-guide) (platform availability) | Supporting |
| `ROLE/SAFE/3` | Hallucination mitigation and citations | 12.7–12.10 | Primary |
| `ROLE/SAFE/7` | Auditability, logging and provenance metadata | 12.1, 12.3, 12.10 | Primary |
| `ROLE/RAG/1` | RAG architecture and grounding | 12.7, 12.8 | Supporting |
| `ROLE/RAG/5` | Index freshness and metadata | 12.3, 12.8 | Supporting |
| `ROLE/AGENT/4` | Multi-agent orchestration (what flows between agents) | 12.5 | Supporting |
| `ROLE/SAFE/1` | Prompt-injection defense for retrieved content | 12.9 | Supporting |
| `ROLE/EVAL/2` | Code-based graders (provenance audit) | 12.10 | Supporting |
| `ROLE/COMM/1` | Audience-tailored communication of findings and uncertainty | 12.4, 12.6 | Supporting |

## More self-check questions

**1. (Multi-agent research system)** A report combines quarterly revenue figures from five companies, recent news coverage, and technical benchmark results. The synthesis agent writes everything as uniform bullet points, and readers struggle to compare the revenue numbers. What should change?

- A) Render financial data as a table (value, period, source, method), news as prose with inline citations, and technical findings as a structured list
- B) Convert everything to prose so the report reads consistently
- C) Move all numbers into an appendix
- D) Ask the model to bold the most important numbers

<details><summary>Answer</summary>

**A.** Different content types need different forms: tables make numbers comparable and keep the source and period on the same row, prose carries narrative, and lists make technical findings scannable. B and D keep the comparison problem. C separates numbers from their context.
</details>

**2. (Multi-agent research system)** A market scan ends with these coverage records: Q1 pricing `covered`; Q2 patents `failed` (the patent database rejected an expired API key); Q3 lawsuits `empty` (two searches, zero results); Q4 non-English press `not_searched`. Which line belongs in the report for Q2?

- A) "Q2 (patents): no patents found."
- B) "Q2 (patents): the patent database could not be reached (expired API key); findings on patents may be incomplete."
- C) Nothing: the report should only list sub-questions that produced findings
- D) "Q2 (patents): searched; evidence is weak."

<details><summary>Answer</summary>

**B.** `failed` means the system could not look, so the report names the gap, the reason and its effect on the findings. A reports the failure as if it were Q3's kind of result (`empty`), and a reader would wrongly conclude there are no patents. C hides the gap. D says a search happened when none did, and "weak evidence" is a support level, not a coverage state.
</details>

**3. (RAG, current API)** Your knowledge-base tool returns each article as one `search_result` whose `content` is a single long text block. Users complain that every citation shows the whole article. What fixes this?

- A) Switch the citations to `char_location`
- B) Split each article's `content` into smaller text blocks (for example one per paragraph), because the block is the smallest citable unit
- C) Ask Claude in the system prompt to quote only one sentence
- D) Put the article text in the `title` field

<details><summary>Answer</summary>

**B.** For search results, Claude cites whole blocks, and `cited_text` is the full text of the cited blocks, so block size sets citation granularity. A is not a choice you make for search results; their citation type is `search_result_location`. C does not change what the API returns as `cited_text`. D misuses a field meant for a short title.
</details>

**4. (Claude in daily work, CCAO-F)** A colleague used Claude to summarize a new regulation. The summary is confident and cites "Article 14(3)" for a key obligation. The summary is about to go to the leadership team. What should happen first?

- A) Send it, because the citation shows the model checked the source
- B) Ask Claude to rate its confidence in the summary and send it if the rating is high
- C) Open the official regulation text and verify that Article 14(3) says what the summary claims before sharing
- D) Remove the citation so the summary reads more cleanly

<details><summary>Answer</summary>

**C.** A citation makes a claim checkable; it does not prove it. Verifying against the authoritative source is the fact-checking step that high-stakes outputs need. A confuses format with truth. B relies on self-rated confidence, which is not reliable evidence. D removes the one thing that made verification possible.
</details>

**5. (Multi-agent research system)** Your claim records now carry the optional `confidence` field from 12.1, filled in by the extraction subagent. A product manager wants to auto-publish every claim scored 0.85 or higher and send the rest to an analyst. Nobody has compared the scores with real outcomes yet. What should happen first?

- A) Ship the rule, because the model knows how sure it is about its own extractions
- B) Have analysts check a labeled sample of claims, measure accuracy for each score band, and set the threshold from that data, while keeping the evidence-based support levels from 12.6
- C) Ask the model to explain each score in one sentence, then route on the score
- D) Raise the threshold to 0.95 to be safe

<details><summary>Answer</summary>

**B.** A self-reported score is not calibrated until you measure it against labeled data, so nobody can route on it yet. Evidence-based support levels (how many independent sources agree) stay the main signal. A trusts a number nobody has checked. C adds text, not calibration. D picks a stricter number that is just as unmeasured.
</details>

## Share your progress

```text
Chapter 12 of my Claude Certified Architect journey: provenance is architecture, not citation style.

3 takeaways:
1. Every summarizing hop drops sources. Pass claim records (claim + quote + URL + dates), never prose.
2. Two credible numbers disagree? Annotate both with sources and dates and let the coordinator decide. Different years can mean a trend, not a conflict.
3. Claude's Citations API returns valid pointers by construction, but not alongside structured outputs (400).

Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#ClaudeAI #AIArchitecture #RAG #LearningInPublic
```

*Syllabus source: community study guide by paullarionov, [Chapter 12 and Domain 5.6](https://github.com/paullarionov/claude-certified-architect/blob/main/guide_en.md#chapter-12-preserving-provenance), restructured and expanded here in my own words.*
