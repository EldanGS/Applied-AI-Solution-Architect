# Chapter 06 — RAG pipelines

> **Serves:** CCAR-P Domain 3 — Integration (task 3.5: chunking and indexing strategies) · OpenAI Academy *Build with RAG* · the RAG modules of the Anthropic Academy courses *Claude with the Anthropic API*, *Claude with Amazon Bedrock* and *Claude on Google Cloud* · role area **RAG**
> **Est. time:** 5–7 hours (reading + 2 notebooks) · **Status:** [ ] not started

Retrieval-augmented generation (**RAG**) finds the right passages in your own documents and puts them in front of the model before it answers. This chapter builds a RAG pipeline one stage at a time: ingestion, chunking, embeddings, BM25, hybrid search, reranking, query transformation, contextual retrieval and grounded generation. It shows each stage for Claude and for OpenAI, and it ends with the decision customers ask about most: a managed File Search service or your own pipeline? Measuring retrieval quality, finding the failing stage and keeping indexes fresh are chapter 07 (planned).

## What you'll learn

- Decide whether a use case needs RAG at all, and ingest documents into clean records with the metadata that filters and citations need.
- Choose a chunking strategy and an indexing strategy for a given corpus and query pattern.
- Combine **BM25** and **embeddings** with reciprocal rank fusion, then **rerank** the fused candidates.
- Apply **contextual retrieval** and keep its cost down with prompt caching.
- Generate grounded answers with citations on Claude (`search_result` blocks) and OpenAI (File Search), and say when the documents do not cover the question.
- Recommend managed File Search or a custom pipeline, and explain why.

## Prerequisites

[00-prerequisites §2.7](../../00-prerequisites/README.md#27-embeddings-at-a-glance) (embeddings at a glance) · [Claude 01](../../anthropic-claude/01-claude-api-fundamentals/README.md) or [OpenAI 01](../../openai-codex/01-responses-api-fundamentals/README.md) · [Claude 12 §12.7–12.8](../../anthropic-claude/12-provenance/README.md#127-the-citations-api-document-blocks-expanded-beyond-the-guide) (citations) · [OpenAI 04 §4.3](../../openai-codex/04-built-in-tools-and-mcp/README.md#43-file-search-and-vector-stores-hosted-rag) (vector stores and `file_search`)

## Concepts

Snippets use a small `Chunk` record (`id`, `doc_id`, `text`, `meta`), `tokenize()` (lowercase words) and `slug()` helpers, `claude = anthropic.Anthropic()` and `oai = openai.OpenAI()`. The notebooks define all of these.

A RAG system has two pipelines. Most quality problems come from the first one.

| Pipeline | When it runs | Stages |
|---|---|---|
| **Indexing** (offline) | When documents are added or changed | Parse → clean → chunk → (contextualize) → embed + BM25 index → store with metadata |
| **Query** (online) | On every question | (Rewrite) → filter → retrieve from each index → fuse → rerank → generate with citations |

### 6.1 What RAG is and when you need it

A model only knows what it was trained on and what is in its context window. RAG adds a search step: find the few passages that answer the question, then ask the model to answer **from those passages** and cite them. You get answers grounded in private, current data without retraining the model, and every claim can be traced back to a source.

**First, check whether you need RAG at all.** Anthropic's contextual retrieval write-up suggests that a knowledge base under about **200,000 tokens** (roughly 500 pages) can go into the prompt whole. Prompt caching then makes repeated questions much cheaper and faster. Use RAG when the corpus is too large for the prompt, changes often, or must be filtered per user.

| Situation | Choose |
|---|---|
| Small, stable corpus (well under the context window), same for every user | The whole corpus in the prompt, with prompt caching |
| Large or growing corpus, or questions that need only a small part of it | RAG |
| Different users may see different documents | RAG with metadata filters applied **before** ranking (6.5) |

### 6.2 Ingestion: parse, clean, add metadata

Retrieval can only find what ingestion kept. Every document goes through four steps:

1. **Parse** to text while keeping the structure. Headings, lists and tables matter. For PDFs, use a layout-aware parser, and use OCR for scanned pages. Turn each table into rows with their column headers, because a table cell such as "2 years" means nothing without its header.
2. **Clean** away boilerplate (navigation, footers, repeated disclaimers) that would match many queries without answering any.
3. **Add metadata** to every record: `source_id`, `title`, `section` path, `version`, `effective_at`, `content_hash`, and the access fields (`tenant`, `region`, `allowed_groups`). Filters, citations and freshness checks all depend on these fields, so plan them at ingestion time. Adding a field later means re-ingesting everything.
4. **Deduplicate and version.** A content hash tells you which documents changed, so a re-sync only re-embeds those. Mark superseded versions `is_current=False` instead of leaving two "truths" in the index. Ask for real sample documents on day one: scanned PDFs and two-column layouts change the design more than any model choice.

### 6.3 Chunking strategies

A **chunk** is the unit you index, retrieve and cite. If chunks are too large, one embedding has to stand for several topics, and the prompt fills with text that does not help. If chunks are too small, a passage loses the context it needs ("it is covered for 2 years": what is?).

| Strategy | How it splits | Good for | Watch out for |
|---|---|---|---|
| **Fixed size + overlap** | Every N tokens, with M tokens of overlap | Unstructured text, a quick baseline | Cuts sentences and clauses in half |
| **Sentence / paragraph** | At natural boundaries, packed up to a size cap | Articles, support answers | Uneven sizes |
| **Structure-aware** | At headings, sections or clauses, with the heading path kept | Manuals, policies, contracts, Markdown or HTML | Needs a parser that keeps the structure |
| **Semantic** | Where the embedding similarity between neighboring sentences drops | Long, loosely structured text | One embedding call per sentence; harder to debug |
| **Parent-child** | Small child chunks for search, the larger parent section returned for the answer | Precise matching that still needs surrounding context | Two levels to keep in sync |

Start with **structure-aware chunks of about 200–800 tokens** and 10–20% overlap only where a split falls inside a passage. Then tune the size on your own questions (chapter 07). OpenAI's vector stores default to 800-token chunks with 400 tokens of overlap, which you can change through `chunking_strategy`. On Claude, the chunk is also the **citation unit**, because Claude cites whole text blocks ([Claude 12 §12.8](../../anthropic-claude/12-provenance/README.md#128-search_result-blocks-citations-for-your-own-retrieval-expanded-beyond-the-guide)).

```python
def chunk_markdown(doc_id: str, text: str, max_words: int = 150):
    """One chunk per section; split long sections with 20% overlap."""
    chunks, title, section = [], "", ""
    for block in re.split(r"\n(?=#)", text.strip()):
        heading, _, body = block.partition("\n")
        if heading.startswith("# "):
            title = heading[2:]
        section = heading.lstrip("# ")
        words, step = body.split(), int(max_words * 0.8)
        for n, start in enumerate(range(0, len(words), step)):
            chunks.append(Chunk(
                id=f"{doc_id}#{slug(section)}-{n}", doc_id=doc_id,
                text=" ".join(words[start:start + max_words]),
                meta={"title": title, "section": section}))
            if start + max_words >= len(words):
                break               # this window reached the section's end
    return chunks
```

### 6.4 Embeddings and vector indexes

An **embedding model** turns text into a vector, and texts with similar meaning get nearby vectors. Dense retrieval embeds the question and returns the chunks whose vectors are closest by cosine similarity. It finds paraphrases ("money back" matches "refund"), but it is weak on exact identifiers such as part numbers and error codes.

**Choosing a model.** Anthropic does not offer an embedding model; its docs point to **Voyage AI** (`voyage-4-large`, `voyage-4`, `voyage-4-lite`, plus domain models such as `voyage-code-4` and `voyage-law-2`). OpenAI offers `text-embedding-3-small` (1,536 dimensions) and `text-embedding-3-large` (3,072). Open models can run locally (the repo's extras use `fastembed`). Compare models on your own labeled questions, not on public leaderboards.

| Decision | Rule of thumb |
|---|---|
| Query vs document | Voyage takes `input_type="query"` or `"document"`; always set it for retrieval |
| Dimensions | Both can return shorter vectors (`output_dimension` on Voyage, `dimensions` on OpenAI): cheaper storage, small quality loss. Compare by cosine (dot product on normalized vectors) |
| Changing models | Vectors from different models cannot be compared, so re-embed the whole corpus into a new index and switch after an eval |

Voyage is a plain HTTP call (`POST https://ai.mongodb.com/v1/embeddings` with `model`, `input` and `input_type`); the practice notebook has both.

```python
def embed_openai(texts: list[str], dims: int = 512) -> list[list[float]]:
    r = oai.embeddings.create(model="text-embedding-3-small",
                              input=texts, dimensions=dims)
    return [d.embedding for d in r.data]
```

**Vector indexes.** A **flat** index compares the query with every vector: exact, and fine up to roughly 100,000 vectors. Larger corpora use approximate nearest-neighbor (ANN) indexes. **HNSW** (a navigable graph) is fast and accurate but uses a lot of memory. **IVF** (clustered lists) uses less memory but recall drops when too few lists are probed. Quantization (int8 or binary vectors) cuts memory further. Where the vectors live matters more than the algorithm: **pgvector** if the customer already runs Postgres, **OpenSearch** or Elasticsearch if they already run keyword search, or a managed vector database (or a managed File Search, 6.12) if nobody wants to run one.

### 6.5 Indexing strategies

An indexing strategy decides **what** you index, **how many** indexes you keep, and **how** you partition them.

| Question | Options | Choose by |
|---|---|---|
| What is indexed | Raw chunk · chunk + generated context (6.10) · section summaries · likely questions per chunk | Query style: summaries for broad questions, raw chunks for precise ones |
| How many indexes | Dense only · dense + BM25 (6.7) · one index per content type (manuals, tickets, code) | Mixed query types need dense + BM25; very different content types each need their own chunking |
| Partitioning | One index with metadata filters · one namespace or index per tenant | Hard isolation or per-tenant deletion → namespace per tenant; many small tenants → filters |
| Granularity | Flat chunks · parent-child · document-level index first, then chunks within the top documents | Long documents with many similar sections → parent-child or two-level |
| Updates | Full rebuild · incremental upsert by `content_hash` · blue/green index swap | Model or chunking change → blue/green; content edits → incremental |

**Filter before you rank.** Access rules, tenant, region and `is_current` are **filters applied inside the search**, never instructions in the prompt. If you rank first and filter afterwards, a top 20 full of forbidden chunks becomes a top 2. That is a quality problem, and a security problem if anything skips the filter. Chapter 07 (planned) and chapter 13 (planned) cover permission-aware retrieval in depth.

```python
def search(index, query: str, user, k: int = 20):
    allowed = lambda c: (c.meta["tenant"] == user.tenant
                         and c.meta["is_current"]
                         and c.meta["group"] in user.groups)
    return index.search(query, k=k, where=allowed)   # filter inside search
```

### 6.6 BM25 lexical search

**BM25** is the standard keyword ranking. A chunk scores high when it contains the query's terms often (with diminishing returns), when those terms are rare in the corpus, and when the chunk is not padded with other text. It finds what embeddings blur: `E-305`, `HX-40`, product names, clause numbers and acronyms. It costs no model calls, runs in milliseconds, and its results are easy to explain. It does not understand paraphrases.

For each query term t: `idf(t) · tf·(k1+1) / (tf + k1·(1 − b + b·len/avg_len))`, summed over the terms. Here `tf` is the term's count in the chunk, `idf(t) = ln(1 + (N − n_t + 0.5)/(n_t + 0.5))` for N chunks of which n_t contain t, and the usual settings are `k1 ≈ 1.2–2.0` (how fast repeated terms stop adding score) and `b = 0.75` (how much long chunks are penalized).

```python
class BM25:
    def __init__(self, chunks, k1=1.5, b=0.75):
        self.chunks, self.k1, self.b = chunks, k1, b
        self.docs = [tokenize(c.text) for c in chunks]
        self.avg = sum(map(len, self.docs)) / len(self.docs)
        n = Counter(t for d in self.docs for t in set(d))
        N = len(self.docs)
        self.idf = {t: math.log(1 + (N - f + 0.5) / (f + 0.5))
                    for t, f in n.items()}

    def search(self, query: str, k: int = 20):
        q = tokenize(query)
        def score(d):
            tf = Counter(d)
            norm = self.k1 * (1 - self.b + self.b * len(d) / self.avg)
            return sum(self.idf.get(t, 0) * tf[t] * (self.k1 + 1)
                       / (tf[t] + norm) for t in q if tf[t])
        ranked = sorted(zip(self.chunks, map(score, self.docs)),
                        key=lambda p: -p[1])
        return [c for c, s in ranked[:k] if s > 0]
```

### 6.7 Hybrid search: a multi-index pipeline with rank fusion

Real questions mix both kinds of need: "is the Ember stove's E-305 error covered by warranty?" contains an exact code and a paraphrased concept. A **multi-index pipeline** runs the question against the dense index and the BM25 index (and any others), then **fuses** the ranked lists.

Scores from different retrievers use different scales, so do not add them directly. **Reciprocal rank fusion (RRF)** uses only the ranks: each list gives a chunk `1 / (k + rank)`, and the sums decide the order. `k = 60` is the common default; per-retriever weights let you lean toward one side. OpenAI's `file_search` uses the same idea: its `ranking_options.hybrid_search` sets `embedding_weight` and `text_weight` for its RRF.

```python
def rrf(rankings: list[list[str]], k: int = 60,
        weights: list[float] | None = None) -> list[str]:
    """Fuse ranked lists of chunk ids; higher fused score ranks first."""
    weights = weights or [1.0] * len(rankings)
    scores: dict[str, float] = {}
    for w, ranking in zip(weights, rankings):
        for rank, cid in enumerate(ranking, start=1):
            scores[cid] = scores.get(cid, 0.0) + w / (k + rank)
    return sorted(scores, key=lambda cid: -scores[cid])

fused = rrf([[c.id for c in dense.search(q, k=50)],
             [c.id for c in bm25.search(q, k=50)]])
```

### 6.8 Reranking

Embedding and BM25 retrievers score the query and each chunk **separately**, which makes them fast enough for millions of chunks. A **reranker** (a cross-encoder) reads the query and a chunk **together** and scores how well that chunk answers it. That is much more accurate, but too slow to run on the whole corpus. So you **retrieve wide, then rerank narrow**: fuse the top 50–150 candidates, rerank them, and send the top 5–20 to the model.

| Reranker | Example | Trade-off |
|---|---|---|
| Hosted cross-encoder | Voyage `rerank-3` / `rerank-3-lite`, Cohere Rerank | Accurate, adds one API call and about 100–500 ms |
| LLM as reranker | A fast model (`claude-haiku-4-5`) scores candidates with structured output | Flexible (you can add business rules), but slower and more expensive per candidate |
| Built into a managed service | `file_search` `ranking_options.ranker` | No extra work; little control. Add business-rule boosts (recency, official sources) in code |

```python
def rerank_voyage(query: str, chunks: list[Chunk], top_k: int = 8):
    r = httpx2.post("https://ai.mongodb.com/v1/rerank", headers={
        "Authorization": f"Bearer {os.environ['VOYAGE_API_KEY']}"},
        json={"query": query, "documents": [c.text for c in chunks],
              "model": "rerank-3", "top_k": top_k})
    r.raise_for_status()
    return [(chunks[d["index"]], d["relevance_score"])
            for d in r.json()["data"]]     # sorted, best first
```

The reranker's top score also gives you a **"not found" signal**: if even the best candidate scores low, say that the documents do not cover the question instead of letting the model guess. Set the threshold from labeled questions.

### 6.9 Query transformation

Users rarely type good search queries. Fix the query before retrieval, and measure that the fix helps:

| Technique | What it does | Use when |
|---|---|---|
| **Rewrite to standalone** | Turns "and for the EU?" into "EU return policy for opened items" using the conversation | Multi-turn chat (almost always needed) |
| **Multi-query expansion** | A fast model writes 2–4 paraphrases; retrieve for each and fuse with RRF | Short or vague questions, vocabulary mismatch |
| **Decomposition** | Splits a compound question into sub-questions, retrieves for each; can also pull out filters ("for the Summit 40") | "Compare X and Y", multi-part questions |
| **HyDE** | Embeds a hypothetical answer instead of the question | Questions phrased very differently from the documents |

On OpenAI, `vector_stores.search(..., rewrite_query=True)` rewrites the query for you, and `file_search` lets the model write its own queries. On Claude, make retrieval a tool ([Claude 02](../../anthropic-claude/02-tool-use/README.md)), and Claude writes the query arguments itself. That is the step from a fixed RAG pipeline toward **agentic search**, where the model decides what to search for, reads the results and searches again.

### 6.10 Contextual retrieval

Chunking cuts a passage off from its document. "The frame is covered for 2 years" could come from any product manual, so neither BM25 nor embeddings can tell which product it belongs to. **Contextual retrieval** (Anthropic, 2024) fixes this at indexing time. For each chunk, a fast model reads the whole document and writes 50–100 tokens that place the chunk in it ("From the Summit 40 backpack owner's guide, warranty section."). You prepend that text to the chunk before building **both** the embedding index and the BM25 index.

Anthropic measured the effect as the share of questions whose relevant chunk was missing from the top 20 retrieved chunks. Contextual embeddings cut that failure rate by **35%**, adding contextual BM25 cut it by **49%**, and adding reranking cut it by **67%** (from 5.7% to 1.9%). Your numbers will differ, so measure on your own questions.

**Cost control.** Each document is sent once per chunk, so put it first in the prompt with `cache_control`. The first call writes the cache and the later calls read it. Remember the minimum cacheable length: 4,096 tokens on Haiku 4.5, so documents shorter than that are simply not cached. Run the job through the Message Batches API ([Claude 07](../../anthropic-claude/07-message-batches/README.md)) at half price, and re-run it only for changed documents. A rough estimate at Haiku 4.5 list prices, for an 8,000-token document with ten 800-token chunks: about **$0.03 per document**, or roughly $4 per million document tokens before the Batch discount.

```python
CONTEXT_PROMPT = ("Here is a chunk from the document above:\n"
    "<chunk>{chunk}</chunk>\nWrite one or two sentences that situate "
    "this chunk within the document, to improve search retrieval. "
    "Answer with only those sentences.")

def contextualize(doc_text: str, chunk: Chunk) -> str:
    r = claude.messages.create(
        model="claude-haiku-4-5", max_tokens=150,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": f"<document>{doc_text}</document>",
             "cache_control": {"type": "ephemeral"}},  # same prefix
            {"type": "text",                           # for every chunk
             "text": CONTEXT_PROMPT.format(chunk=chunk.text)}]}])
    context = "".join(b.text for b in r.content if b.type == "text")
    return f"{context.strip()}\n\n{chunk.text}"   # index THIS text
```

A free first step: prepend the document title and section path (from 6.2) to every chunk; it fixes many "which product?" failures. An alternative is a **contextualized chunk embedding model** (Voyage `voyage-context-4`), which embeds each chunk with the whole document in view.

### 6.11 Grounded generation with citations

Retrieval is only half the job. The answer must stay within the retrieved passages and show where each claim came from. Instruct the model to answer only from the sources, to say when they do not contain the answer, and never to fill gaps from general knowledge.

- **Claude:** send each retrieved chunk as a `search_result` block (with `source`, `title` and text `content`, citations enabled), either directly in the user message or inside a `tool_result`. The response's text blocks then carry `search_result_location` citations with `source`, `cited_text` and the block indices ([Claude 12 §12.8](../../anthropic-claude/12-provenance/README.md#128-search_result-blocks-citations-for-your-own-retrieval-expanded-beyond-the-guide)).
- **OpenAI:** with `file_search` the answer carries `file_citation` annotations. With your own retrieval, number the sources in the input, ask for `[S1]`-style markers, and **check in code** that every marker exists ([OpenAI 04 §4.3](../../openai-codex/04-built-in-tools-and-mcp/README.md#43-file-search-and-vector-stores-hosted-rag)).
- **Gate in code:** if the reranker found nothing good enough, return "not covered" without calling the model. If a policy answer comes back without a citation, do not show it.

```python
def claude_answer(question: str, hits: list[Chunk]):
    blocks = [{"type": "search_result",
               "source": f"kb://{c.doc_id}?v={c.meta['version']}",
               "title": f"{c.meta['title']} — {c.meta['section']}",
               "content": [{"type": "text", "text": c.text}],
               "citations": {"enabled": True}} for c in hits]
    r = claude.messages.create(
        model="claude-sonnet-5-5", max_tokens=1024, system=GROUNDED,
        messages=[{"role": "user", "content": blocks + [
            {"type": "text", "text": question}]}])
    cited = {cit.source for b in r.content if b.type == "text"
             for cit in (b.citations or [])}
    return r, cited          # no citations on a policy answer → block it
```

### 6.12 Managed File Search or a custom pipeline

A **managed** service does ingestion, chunking, embedding, hybrid search and reranking for you: OpenAI vector stores with `file_search`, Amazon Bedrock Knowledge Bases (which can answer with Claude models on Bedrock), or Google Cloud's managed retrieval (Vertex AI RAG Engine, Vertex AI Search), whose results your code can pass to Claude. A **custom** pipeline means you own every stage from 6.2 to 6.11.

| Criterion | Managed File Search | Custom pipeline |
|---|---|---|
| Time to first answer | Hours | Days to weeks |
| Chunking, embeddings, reranking | Few settings (chunk size, filters, score threshold, hybrid weights) | Anything: structure-aware chunks, contextual retrieval, any reranker |
| Model choice | Tied to the provider's platform | Any model, including both vendors behind one interface |
| Data location and access control | The provider's store, attribute filters (OpenAI: up to 16 attributes per file) | Your database (pgvector, OpenSearch) and your existing access model |
| Debugging | Inspect what was retrieved (`include=["file_search_call.results"]`, `vector_stores.search`) | Every stage can be logged and tested on its own |
| Cost model | Storage per GB-day plus tool calls | Infrastructure plus engineering time |

**Claude vs OpenAI.** OpenAI gives you a first-party hosted RAG (Files → vector store → `file_search` with citations). On the Claude API, you bring your own retrieval: embeddings from Voyage AI, OpenAI or a local model, a vector store you run, and `search_result` blocks for citations. On AWS and Google Cloud, the clouds' managed retrieval services above fill the same role for Claude, with chapter 14 (planned) covering the platform choice. A sensible path for many customers: **prototype on managed File Search to prove the value, and move to a custom pipeline when evals show a specific retrieval limit**, such as exact-code lookups, per-user permissions or the need for contextual retrieval.

```python
response = oai.responses.create(
    model="gpt-6-luna",
    input="Can an EU customer return opened headphones?",
    tools=[{"type": "file_search", "vector_store_ids": [store_id],
            "max_num_results": 8,
            "filters": {"type": "eq", "key": "region", "value": "EU"},
            "ranking_options": {"hybrid_search": {
                "embedding_weight": 0.5, "text_weight": 0.5}}}],
    include=["file_search_call.results"])   # see what was retrieved
```

## Notebooks

| Notebook | What you do |
|---|---|
| [`01_practice.ipynb`](01_practice.ipynb) | Build every stage from 6.2–6.12 offline on a small product-policy corpus. Measure recall@k and MRR for dense, BM25, hybrid, reranked and contextual retrieval. Then build the mini-project: one RAG pipeline that answers through Claude or OpenAI behind the same interface, with citations and a "not covered" gate. Optional live cells call Voyage, OpenAI and Claude. |
| [`02_homework.ipynb`](02_homework.ipynb) | An 8-question scenario quiz, 5 auto-checked offline exercises (chunking, RRF, retrieval metrics, a cited Claude request, cached contextualizer requests), an architecture scenario with a rubric, and a scorecard (pass mark 72%) |

## Cheat-sheet

| Situation | Choose | Over |
|---|---|---|
| Corpus well under the context window and stable | The whole corpus in the prompt, with prompt caching | A RAG pipeline |
| Manuals, policies, contracts | Structure-aware chunks with the heading path in metadata | Fixed-size splits |
| Queries contain codes, SKUs, names | BM25 + embeddings fused with RRF | Embeddings only |
| Answer is in the top 50 but not in the top 5 | Rerank the top 50, then send the top 5–20 | Sending 50 chunks, or a bigger generation model |
| Chunks lose their document ("which product?") | Contextual retrieval (or at least title + section prefix) | Larger chunks |
| Users see different documents | Metadata filters inside the search (or per-tenant namespaces) | "Do not reveal X" in the prompt |
| Changing the embedding model | Re-embed into a new index, evaluate, then swap | Mixing old and new vectors |
| Claude, own data store, strict access rules | Custom pipeline with `search_result` citations | Copying data into a third-party store |

<a id="common-mistakes-and-anti-patterns"></a>

## Common mistakes

- **RAG by default.** Building a pipeline for a 60-page handbook that would fit in a cached prompt.
- **Ignoring ingestion.** Tables flattened into number soup, scanned pages with no OCR, footers in every chunk.
- **Embeddings only, or raw scores added together.** Exact codes get lost; BM25 and cosine scores live on different scales, so fuse ranks.
- **Ranking first, filtering later.** Permission rules applied after top-k, or written into the prompt.
- **Stuffing the prompt.** Sending 50 chunks instead of reranking down to the best 5–20.
- **No "not covered" path.** The model always answers, even when retrieval found nothing relevant.

## Self-check

**1. (Customer support assistant)** A support assistant for a camping-gear retailer answers "how do I fix error E-305 on the Ember stove?" with steps for E-217. The retriever uses `text-embedding-3-small` vectors only. The E-305 passage exists and is chunked correctly. What change fixes this most directly?

- A) Switch to `text-embedding-3-large` for more dimensions
- B) Add a BM25 index over the same chunks and fuse it with the dense results using reciprocal rank fusion
- C) Tell the model in the system prompt to pay close attention to error codes
- D) Double the chunk size so each chunk holds more error codes

<details><summary>Answer</summary>

**B.** Exact identifiers are where dense embeddings are weakest. BM25 treats `e-305` as a rare, high-value term, and RRF combines the two rankings without comparing their scores. A may help a little but does not change how embeddings handle codes. C cannot help, because the generator never received the E-305 chunk. D mixes several codes into one chunk and makes ranking worse.
</details>

**2. (Knowledge assistant)** Product manuals are chunked by section. Questions such as "how long is the Summit 40 frame covered?" often return the warranty section of a different product. Every warranty section says something like "The frame is covered for N years" without naming the product. What is the best fix?

- A) Contextual retrieval: prepend a short document-level context (product and section) to each chunk before building the embedding and BM25 indexes
- B) Put whole manuals into each chunk so the product name is always included
- C) Raise top-k from 5 to 30 so the right warranty section is more likely to be included
- D) Ask users to always include the product's SKU

<details><summary>Answer</summary>

**A.** The chunks lost the one fact that tells them apart: which document they come from. Contextual retrieval (or at least a title and section prefix) puts it back into both indexes. B removes the precision that chunking gives and floods the prompt. C sends more near-identical, wrong sections and still relies on luck. D pushes the problem onto users.
</details>

**3. (Enterprise RAG)** Your retrieval eval shows the right chunk appears in the top 50 hybrid results for 96% of questions, but only in the top 5 for 61%. The generator receives the top 5. Latency budget allows about 300 ms more. What should you do?

- A) Send the top 50 chunks to the generator instead
- B) Switch the generator to a larger model
- C) Rerank the top 50 with a cross-encoder reranker and send its top 5–8
- D) Lower the chunk size so more chunks fit in the top 5

<details><summary>Answer</summary>

**C.** The candidates are good; the ordering is the problem. That is exactly what a reranker fixes, within the latency budget. A raises cost, dilutes attention and makes citations noisier. B cannot use a chunk it never receives. D changes the index without any evidence that chunk size is the cause.
</details>

**4. (Solution design)** A bank wants an internal policy assistant on Claude. Documents live in SharePoint with per-department permissions, the security team will not allow data in a vendor-hosted store, and the policies contain many clause numbers. The team asks whether to use a managed File Search service. What do you recommend?

- A) OpenAI vector stores with `file_search`, with a system prompt that tells the model which departments the user belongs to
- B) A custom pipeline in the bank's own store (for example pgvector): structure-aware chunks with clause metadata, BM25 + embeddings, permission filters applied inside the search, and `search_result` blocks for Claude citations
- C) Put all policies in the prompt for every question and rely on prompt caching
- D) Fine-tune Claude on the policy documents

<details><summary>Answer</summary>

**B.** Each constraint points to a custom pipeline: the data must stay in the bank's store, permissions must be enforced as filters before ranking, clause numbers need BM25, and Claude cites `search_result` blocks. A breaks the data-location rule and turns access control into a prompt instruction. C ignores per-department permissions. D does not give citations or permission checks, and every policy change would need retraining.
</details>

## Official documentation

- [Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings) (Claude docs): no first-party model, Voyage AI models, `input_type`
- [Search results](https://platform.claude.com/docs/en/build-with-claude/search-results) (Claude docs): `search_result` blocks and `search_result_location` citations for your own retrieval
- [Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) (Anthropic Engineering): the method, the failure-rate results, cost with prompt caching
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) (Claude docs): cache breakpoints and minimum lengths for contextualizer jobs
- [Embedding and reranking models](https://www.mongodb.com/docs/voyageai/models/) (Voyage AI on MongoDB): model families and rerankers
- [Embeddings](https://developers.openai.com/api/docs/guides/embeddings) (OpenAI docs): `text-embedding-3-small` and `-large`, the `dimensions` parameter
- [Retrieval](https://developers.openai.com/api/docs/guides/retrieval) (OpenAI docs): vector stores, chunking defaults, attribute filters, `rewrite_query`, ranking options
- [File search](https://developers.openai.com/api/docs/guides/tools-file-search) (OpenAI docs): the hosted `file_search` tool in the Responses API

[← Chapter 05 — Model strategy and customization trade-offs](../05-model-strategy-and-customization/README.md) | [↑ Applied AI Architect track](../README.md) | Chapter 07 — Retrieval strategy and knowledge operations (planned)

Certification coverage, more self-check questions and share text: [coverage/README.md](coverage/README.md)
