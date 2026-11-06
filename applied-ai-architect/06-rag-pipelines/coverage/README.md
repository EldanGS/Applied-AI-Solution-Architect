# Chapter 06 — certification coverage and extras

[↑ Chapter README](../README.md)

## Certification coverage

This table feeds the repo coverage matrix. IDs come from the official CCAR-P and CCAR-F guides, the OpenAI Academy course and bootcamp pages, the Anthropic Academy course outlines (`ACAD/<course>/<lesson number>`) and the role competency matrix. **Primary** means this chapter is where the item is taught in depth; **Supporting** means it is applied or reinforced here and taught more fully elsewhere.

| Requirement ID | What it asks (short) | Where in this chapter | Depth |
|---|---|---|---|
| `CCAR-P/D3/3.5/S1` | Design a RAG pipeline with appropriate chunking and indexing strategies | Whole chapter: the two-pipeline table in [Concepts](../README.md#concepts), [6.3](../README.md#63-chunking-strategies), [6.5](../README.md#65-indexing-strategies), Self-check 4; practice mini-project; homework Part C | Primary |
| `CCAR-P/D3/3.5/K1` | Chunking strategies | [6.3](../README.md#63-chunking-strategies) (strategy table, `chunk_markdown`), [6.10](../README.md#610-contextual-retrieval); practice §6.3; homework Q2, exercise 1 | Primary |
| `CCAR-P/D3/3.5/K2` | Indexing strategies | [6.4](../README.md#64-embeddings-and-vector-indexes) (flat, HNSW, IVF), [6.5](../README.md#65-indexing-strategies) (what, how many, partitioning, updates), [6.7](../README.md#67-hybrid-search-a-multi-index-pipeline-with-rank-fusion); homework Q6, Q8 | Primary |
| `CCAR-P/D3/3.6/S1` | Retrieval strategies matched to data shape and query pattern | [6.7](../README.md#67-hybrid-search-a-multi-index-pipeline-with-rank-fusion), [6.9](../README.md#69-query-transformation), [cheat-sheet](../README.md#cheat-sheet); taught fully in chapter 07 (planned) | Supporting |
| `CCAR-F/APPX/OUT/7` | Embedding models and vector database internals (out of scope for CCAR-F) | [6.4](../README.md#64-embeddings-and-vector-indexes): taught here for CCAR-P and the job; not tested in CCAR-F | Supporting |
| `OAI/api/build-with-rag/1` | How RAG finds the right source material before answering | [6.1](../README.md#61-what-rag-is-and-when-you-need-it) | Primary |
| `OAI/api/build-with-rag/2` | Build a retrieval pipeline | [6.3](../README.md#63-chunking-strategies)–[6.8](../README.md#68-reranking); practice §6.3–6.8 and mini-project | Primary |
| `OAI/api/build-with-rag/9` | Build applications that produce relevant, grounded answers from your data | [6.11](../README.md#611-grounded-generation-with-citations); practice §6.11 and mini-project (`RagPipeline.answer`); homework Q3 | Primary |
| `OAI/api/build-with-rag/15` | Knowledge ingestion: structure source content, pre-process and chunk it | [6.2](../README.md#62-ingestion-parse-clean-add-metadata), [6.3](../README.md#63-chunking-strategies); practice §6.1–6.3 | Primary |
| `OAI/api/build-with-rag/16` | Embed chunks and store them in a vector store | [6.4](../README.md#64-embeddings-and-vector-indexes), [6.12](../README.md#612-managed-file-search-or-a-custom-pipeline) (taught fully in [OpenAI 04 §4.3](../../../openai-codex/04-built-in-tools-and-mcp/README.md#43-file-search-and-vector-stores-hosted-rag)) | Supporting |
| `OAI/api/build-with-rag/17` | Decide between built-in File Search and a custom RAG pipeline | [6.12](../README.md#612-managed-file-search-or-a-custom-pipeline), Self-check 4; homework Q7, Part C | Primary |
| `OAI/api/build-with-rag/18` | Retrieval optimization: process the query, rank and re-rank results | [6.7](../README.md#67-hybrid-search-a-multi-index-pipeline-with-rank-fusion)–[6.9](../README.md#69-query-transformation), Self-check 3; homework Q5 | Primary |
| `OAI/api/build-with-rag/19` | Use metadata in retrieval | [6.2](../README.md#62-ingestion-parse-clean-add-metadata), [6.5](../README.md#65-indexing-strategies) (filter inside the search); practice §6.5 | Supporting |
| `OAI/api/build-with-rag/21` | Grounded answers with the Responses API plus File Search | [6.12](../README.md#612-managed-file-search-or-a-custom-pipeline) (taught fully in [OpenAI 04 §4.3](../../../openai-codex/04-built-in-tools-and-mcp/README.md#43-file-search-and-vector-stores-hosted-rag)) | Supporting |
| `OAI/bootcamp/api-builder/22` | RAG: knowledge ingestion and structuring source content | [6.2](../README.md#62-ingestion-parse-clean-add-metadata), [6.3](../README.md#63-chunking-strategies) | Primary |
| `OAI/bootcamp/api-builder/24` | RAG: ranking and metadata | [6.5](../README.md#65-indexing-strategies), [6.7](../README.md#67-hybrid-search-a-multi-index-pipeline-with-rank-fusion), [6.8](../README.md#68-reranking) | Supporting |
| `ACAD/claude-with-the-anthropic-api/LO7` | Build RAG with chunking, embeddings, BM25 search and contextual retrieval | [6.3](../README.md#63-chunking-strategies), [6.4](../README.md#64-embeddings-and-vector-indexes), [6.6](../README.md#66-bm25-lexical-search), [6.10](../README.md#610-contextual-retrieval) | Primary |
| `ACAD/claude-with-the-anthropic-api/44` | Lesson: introducing retrieval augmented generation | [6.1](../README.md#61-what-rag-is-and-when-you-need-it) | Primary |
| `ACAD/claude-with-the-anthropic-api/45` | Lesson: text chunking strategies | [6.3](../README.md#63-chunking-strategies) | Primary |
| `ACAD/claude-with-the-anthropic-api/46` | Lesson: text embeddings | [6.4](../README.md#64-embeddings-and-vector-indexes) | Primary |
| `ACAD/claude-with-the-anthropic-api/47` | Lesson: the full RAG flow | Two-pipeline table in [Concepts](../README.md#concepts), [6.1](../README.md#61-what-rag-is-and-when-you-need-it) | Primary |
| `ACAD/claude-with-the-anthropic-api/48` | Lesson: implementing the RAG flow | [6.11](../README.md#611-grounded-generation-with-citations); practice mini-project | Primary |
| `ACAD/claude-with-the-anthropic-api/49` | Lesson: BM25 lexical search | [6.6](../README.md#66-bm25-lexical-search) | Primary |
| `ACAD/claude-with-the-anthropic-api/50` | Lesson: a multi-index RAG pipeline | [6.7](../README.md#67-hybrid-search-a-multi-index-pipeline-with-rank-fusion) | Primary |
| `ACAD/claude-in-amazon-bedrock/LO4` | RAG pipelines with chunking, embeddings, BM25 and contextual retrieval (Bedrock edition) | [6.3](../README.md#63-chunking-strategies)–[6.10](../README.md#610-contextual-retrieval); Bedrock Knowledge Bases in [6.12](../README.md#612-managed-file-search-or-a-custom-pipeline) | Primary |
| `ACAD/claude-in-amazon-bedrock/43` | Lesson: introducing retrieval augmented generation | [6.1](../README.md#61-what-rag-is-and-when-you-need-it) | Primary |
| `ACAD/claude-in-amazon-bedrock/44` | Lesson: text chunking strategies | [6.3](../README.md#63-chunking-strategies) | Primary |
| `ACAD/claude-in-amazon-bedrock/45` | Lesson: text embeddings | [6.4](../README.md#64-embeddings-and-vector-indexes) | Primary |
| `ACAD/claude-in-amazon-bedrock/46` | Lesson: the full RAG flow | Two-pipeline table in [Concepts](../README.md#concepts), [6.1](../README.md#61-what-rag-is-and-when-you-need-it) | Primary |
| `ACAD/claude-in-amazon-bedrock/47` | Lesson: implementing the RAG flow | [6.11](../README.md#611-grounded-generation-with-citations); practice mini-project | Primary |
| `ACAD/claude-in-amazon-bedrock/48` | Lesson: BM25 lexical search | [6.6](../README.md#66-bm25-lexical-search) | Primary |
| `ACAD/claude-in-amazon-bedrock/49` | Lesson: a multi-search RAG pipeline | [6.7](../README.md#67-hybrid-search-a-multi-index-pipeline-with-rank-fusion) | Primary |
| `ACAD/claude-in-amazon-bedrock/50` | Lesson: reranking results | [6.8](../README.md#68-reranking) | Primary |
| `ACAD/claude-in-amazon-bedrock/51` | Lesson: contextual retrieval | [6.10](../README.md#610-contextual-retrieval) | Primary |
| `ACAD/claude-in-amazon-bedrock/52` | Quiz on retrieval augmented generation | [Self-check](../README.md#self-check), [More self-check questions](#more-self-check-questions), homework Part A | Supporting |
| `ACAD/claude-with-google-vertex/LO6` | RAG pipelines with chunking, embeddings, BM25 and contextual retrieval (Vertex edition) | [6.3](../README.md#63-chunking-strategies)–[6.10](../README.md#610-contextual-retrieval); Vertex AI RAG Engine in [6.12](../README.md#612-managed-file-search-or-a-custom-pipeline) | Primary |
| `ACAD/claude-with-google-vertex/46` | Lesson: introducing retrieval augmented generation | [6.1](../README.md#61-what-rag-is-and-when-you-need-it) | Primary |
| `ACAD/claude-with-google-vertex/47` | Lesson: text chunking strategies | [6.3](../README.md#63-chunking-strategies) | Primary |
| `ACAD/claude-with-google-vertex/48` | Lesson: text embeddings | [6.4](../README.md#64-embeddings-and-vector-indexes) | Primary |
| `ACAD/claude-with-google-vertex/49` | Lesson: the full RAG flow | Two-pipeline table in [Concepts](../README.md#concepts), [6.1](../README.md#61-what-rag-is-and-when-you-need-it) | Primary |
| `ACAD/claude-with-google-vertex/50` | Lesson: implementing the RAG flow | [6.11](../README.md#611-grounded-generation-with-citations); practice mini-project | Primary |
| `ACAD/claude-with-google-vertex/51` | Lesson: BM25 lexical search | [6.6](../README.md#66-bm25-lexical-search) | Primary |
| `ACAD/claude-with-google-vertex/52` | Lesson: a multi-index RAG pipeline | [6.7](../README.md#67-hybrid-search-a-multi-index-pipeline-with-rank-fusion) | Primary |
| `ACAD/claude-with-google-vertex/53` | Lesson: reranking results | [6.8](../README.md#68-reranking) | Primary |
| `ACAD/claude-with-google-vertex/54` | Lesson: contextual retrieval | [6.10](../README.md#610-contextual-retrieval) | Primary |
| `ACAD/claude-with-google-vertex/55` | Quiz on retrieval augmented generation | [Self-check](../README.md#self-check), [More self-check questions](#more-self-check-questions), homework Part A | Supporting |
| `ROLE/RAG/1` | RAG architecture and grounding against enterprise data | [6.1](../README.md#61-what-rag-is-and-when-you-need-it), [6.11](../README.md#611-grounded-generation-with-citations), [6.12](../README.md#612-managed-file-search-or-a-custom-pipeline) | Primary |
| `ROLE/RAG/2` | Document ingestion, parsing and chunking | [6.2](../README.md#62-ingestion-parse-clean-add-metadata), [6.3](../README.md#63-chunking-strategies), [6.10](../README.md#610-contextual-retrieval) | Primary |
| `ROLE/RAG/3` | Select embedding models; design and operate vector indexes | [6.4](../README.md#64-embeddings-and-vector-indexes), [6.5](../README.md#65-indexing-strategies); homework Q8 | Primary |
| `ROLE/RAG/4` | Hybrid search, reranking and query transformation | [6.6](../README.md#66-bm25-lexical-search)–[6.9](../README.md#69-query-transformation); homework Q5, exercise 2 | Primary |
| `ROLE/RAG/5` | Index freshness, metadata and source sync | [6.2](../README.md#62-ingestion-parse-clean-add-metadata) (`content_hash`, versions), [6.5](../README.md#65-indexing-strategies) (update strategies); taught fully in chapter 07 (planned) | Supporting |

## More self-check questions

**1. (Knowledge assistant)** Your retriever uses Voyage `voyage-4`. Retrieval quality on short user questions is noticeably worse than in the vendor's demo. You find that both the documents and the queries are embedded without `input_type`. What do you change?

- A) Embed documents with `input_type="document"` and queries with `input_type="query"`, then re-run the retrieval eval
- B) Switch to `voyage-4-large`, which ignores `input_type`
- C) Append "this is a question" to every query before embedding it
- D) Lower the embedding dimension to 256 so short queries carry more weight

<details><summary>Answer</summary>

**A.** For retrieval, Voyage's docs say to set `input_type` so that queries and documents get the right prompt before embedding. Documents must be re-embedded with `"document"` as well, which means a rebuild of the index. B is wrong: the larger model also expects `input_type`. C is an ad-hoc version of what `input_type` does properly. D reduces quality and does not touch the cause.
</details>

**2. (Customer support assistant)** In a chat, the user first asks "what is the return window for opened items?" and then "and in Germany?". Retrieval for the second message returns shipping pages. What is the best fix?

- A) Embed the whole conversation as one query
- B) Rewrite the last message into a standalone query (for example, "return window for opened items for EU customers") with a fast model before retrieval
- C) Raise top-k so the EU page is more likely to appear
- D) Add "Germany" as a synonym of "EU" in the BM25 index

<details><summary>Answer</summary>

**B.** Follow-ups are not usable queries on their own; a standalone rewrite restores the missing subject. A dilutes the query with old turns and gets worse as the chat grows. C sends more irrelevant chunks. D patches one word and misses the main problem, which is that the follow-up has no subject.
</details>

**3. (Solution design)** A customer's corpus is 1,500 short FAQ entries (about 60 tokens each, about 90,000 tokens in total), the same for every user and updated weekly. They ask whether they should set up contextual retrieval. What do you say?

- A) Yes: contextual retrieval always improves recall
- B) Yes, and use the largest model so the contexts are high quality
- C) Probably neither contextual retrieval nor RAG: the whole FAQ fits in the prompt with prompt caching; if they still use RAG, each FAQ entry is already self-contained, so contextualizing it adds cost but little information
- D) No: contextual retrieval only works with OpenAI embeddings

<details><summary>Answer</summary>

**C.** Contextual retrieval helps when chunks lose context from a longer document. Self-contained FAQ entries have no lost context, and a 90,000-token corpus that every user may read is a candidate for the whole-corpus prompt in [6.1](../README.md#61-what-rag-is-and-when-you-need-it). A and B ignore the data shape. D is false: the technique works with any embedding model and with BM25.
</details>

**4. (Enterprise RAG)** Contract chunks are 150 tokens, which makes search precise, but answers often miss conditions stated in the surrounding paragraphs of the same clause. What indexing change fits best?

- A) Parent-child retrieval: search on the small chunks, but return the parent clause or section to the generator
- B) Raise the chunk size to 2,000 tokens everywhere
- C) Add more overlap between the 150-token chunks
- D) Send the top 40 small chunks instead of the top 8

<details><summary>Answer</summary>

**A.** Parent-child keeps precise matching and gives the generator the full clause ([6.3](../README.md#63-chunking-strategies), [6.5](../README.md#65-indexing-strategies)). B makes search less precise for every query. C adds a little context and a lot of duplication. D fills the prompt with fragments from unrelated clauses.
</details>

**5. (Enterprise RAG)** After a re-index with a new chunking strategy, users report worse answers. There is no labeled question set, and the old index has already been deleted. Which practice would have prevented this?

- A) Asking the model to rate its own answers after each change
- B) Building the new index next to the old one, comparing recall@k and answer checks on a labeled question set, then switching traffic with the old index kept for rollback
- C) Re-indexing only at night
- D) Increasing top-k after every re-index to compensate

<details><summary>Answer</summary>

**B.** A chunking or embedding change is a release: compare on labeled questions, then do a blue/green swap with a way back. Measuring retrieval in detail is chapter 07 (planned). A is not a measurement. C changes the timing, not the risk. D hides the regression and adds cost.
</details>

## Share your progress

```text
Chapter 06 of my Applied AI Architect journey: RAG pipelines, built one stage at a time.

3 takeaways:
1. Embeddings catch paraphrases and blur exact codes; BM25 does the opposite. Fuse ranks with RRF, then rerank.
2. Chunks forget which document they came from. Contextual retrieval (or a title + section prefix) puts that back.
3. Access rules are filters inside the search, never prompt instructions and never filters applied after top-k.

Same pipeline, two generators: Claude with search_result citations, OpenAI with File Search.
Notes + notebooks: https://github.com/EldanGS/Applied-AI-Solution-Architect
#RAG #AIArchitecture #ClaudeAI #OpenAI #LearningInPublic
```
