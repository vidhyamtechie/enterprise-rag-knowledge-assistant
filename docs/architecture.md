# Architecture

```text
Angular UI
   |
   v
Spring Boot REST API
   |
   v
FastAPI RAG Service
   |
   +--> PDF/TXT/MD Loader
   +--> Chunker
   +--> Ollama Embeddings
   +--> ChromaDB
   |
   +--> Query Embedding
   +--> Top-K Retrieval
   +--> Context Builder
   +--> Ollama LLM
   |
   v
Answer + Sources
```
