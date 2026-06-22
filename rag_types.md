# Retrieval-Augmented Generation (RAG) Systems

## What is RAG?
Retrieval-Augmented Generation combines a retriever with a generative model. The retriever finds relevant documents or passages, and the generator uses those retrieved texts to produce answers, summaries, or conversational responses.

## Why use RAG?
- Enables models to answer from large, external knowledge sources.
- Keeps responses up to date without retraining the generator.
- Reduces hallucination by grounding output in real documents.

## Common RAG Types

### 1. Sparse Retrieval
Sparse retrieval uses traditional text search methods.
- Examples: BM25, TF-IDF, Elasticsearch.
- Works with exact keyword matches and document terms.
- Best for well-defined terminology and low-latency search.

### 2. Dense Retrieval
Dense retrieval uses vector embeddings.
- Examples: sentence-transformers, OpenAI embeddings, semantic search.
- Maps queries and documents to numeric vectors.
- Retrieves semantically similar content, even without exact keywords.

### 3. Hybrid Retrieval
Hybrid retrieval combines sparse and dense methods.
- Uses both keyword matching and embedding similarity.
- Improves accuracy across broad query types.
- Common in production search systems.

## RAG Architectures

### RAG-Sequence
- Retrieves documents once for a query.
- The generator processes retrieved text in sequence.
- Simple and effective for many tasks.

### RAG-Token
- Retrieves documents repeatedly while generating tokens.
- Each token may use a different set of retrieved information.
- More computationally expensive but can be more accurate.

### End-to-end RAG
- Combines retriever and generator into a single trainable system.
- The retriever and generator are trained together on the task.
- Common in research but harder to build from scratch.

## Application-Based RAG Types

### Open-domain Question Answering
- Answers questions using a broad document collection.
- Useful for knowledge bases, wikis, or enterprise data.

### Conversational Assistants
- Uses RAG to ground chatbot responses in documents.
- Keeps dialogue consistent with external knowledge.

### Document Summarization
- Retrieves key passages before generating a summary.
- Ensures summaries reflect the actual source content.

### Knowledge-Grounded Generation
- Produces responses grounded in product specs, manuals, or policies.
- Helps maintain correctness in regulated or technical domains.

## Deployment and Data Patterns

### Local RAG
- Uses documents stored on disk or in local databases.
- Great for prototyping and private data.

### Cloud RAG
- Uses managed embedding services and cloud indexes.
- Scales to very large collections.

### Hybrid Deployment
- Stores static data locally and dynamic data in the cloud.
- Balances performance, cost, and privacy.

## Key RAG Components

### Retriever
- Finds relevant information from a knowledge store.
- Can be sparse, dense, or hybrid.

### Index
- Stores document representations for fast search.
- Examples: inverted index, vector index, Faiss, Elasticsearch.

### Generator
- Produces the final answer or response.
- Usually a language model or an LLM API.

### Reranker
- Reorders retrieved results to improve precision.
- Often a smaller model or scoring function.

## Example RAG System Types

- **BM25 + GPT**: sparse retrieval from documents and generative answer generation.
- **Vector Search + LLM**: semantic retrieval using embeddings and a language model.
- **Knowledge Graph + LLM**: structured data retrieval combined with generative text.

## How to Read This Document
Use the chatbot script (`rag.py`) to query this document interactively. The script treats the sections as knowledge passages and lets you ask questions about RAG system types.
