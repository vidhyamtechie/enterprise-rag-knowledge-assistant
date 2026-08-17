# Enterprise RAG Knowledge Assistant

A portfolio-ready, fully local Retrieval-Augmented Generation application.

## Stack

- Python + FastAPI for the RAG service
- Ollama for local LLM inference and embeddings
- ChromaDB for persistent vector storage
- Java 17 + Spring Boot for the enterprise REST facade
- Angular frontend
- PDF/TXT/Markdown ingestion
- Source/page attribution

## Architecture

```text
Documents -> Loader -> Chunking -> Embeddings -> ChromaDB
                                                |
User -> Angular -> Spring Boot -> FastAPI -> Retrieval
                                      |           |
                                      +------ Context
                                                |
                                                v
                                           Ollama LLM
                                                |
                                                v
                                        Answer + Sources
```

## 1. Install prerequisites

Install Git, Python 3.11+, Java 17+, Maven, Node.js, Angular CLI and Ollama.

## 2. Pull free local models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
ollama list
```

## 3. Start Python RAG service

Windows PowerShell:

```powershell
cd backend-python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## 4. Add documents

Put public/sample PDF, TXT or Markdown files in:

```text
data/documents/
```

Then run:

```bash
curl -X POST http://localhost:8000/api/ingest/directory
```

Or upload a single file from Swagger using:

```text
POST /api/ingest/upload
```

## 5. Test RAG

```bash
curl -X POST http://localhost:8000/api/chat   -H "Content-Type: application/json"   -d "{\"question\":\"Summarize the indexed document\",\"top_k\":5}"
```

## 6. Start Spring Boot gateway

```bash
cd backend-spring
mvn spring-boot:run
```

Test:

```text
GET  http://localhost:8080/api/rag/health
POST http://localhost:8080/api/rag/chat
```

Request:

```json
{
  "question": "What are the main points?",
  "topK": 5
}
```

## 7. Start Angular frontend

```bash
cd frontend
npm install
npm start
```

Open:

```text
http://localhost:4200
```

## Core API flow

### Ingestion
1. Load PDF/TXT/MD.
2. Extract text page by page.
3. Split into overlapping chunks.
4. Generate embeddings with Ollama.
5. Store chunks, embeddings and metadata in ChromaDB.

### Question answering
1. Receive question.
2. Generate query embedding.
3. Run top-K vector similarity search.
4. Build context only from retrieved chunks.
5. Ask local Ollama model to answer from context.
6. Return answer plus source filename/page/chunk.

## Recommended GitHub commits

```text
1. initial project structure
2. add document ingestion and chunking
3. add ollama embedding integration
4. add chromadb vector persistence
5. add semantic retrieval and grounded generation
6. add source attribution
7. add spring boot rag gateway
8. add angular chat interface
9. add tests and documentation
```

## Important portfolio rule

Never upload proprietary client/company PDFs. Use public documents or your own sample documents.
