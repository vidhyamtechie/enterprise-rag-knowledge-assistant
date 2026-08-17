from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import ChatRequest, ChatResponse, IngestResponse
from app.services.ingestion_service import IngestionService
from app.services.rag_service import RagService
from app.services.ollama_client import OllamaClient
from app.services.vector_store import VectorStore

app = FastAPI(
    title="Enterprise RAG Knowledge Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

ingestion = IngestionService()
rag = RagService()
ollama = OllamaClient()
store = VectorStore()

@app.get("/api/health")
def health():
    return {
        "status": "UP",
        "ollama": "UP" if ollama.healthy() else "DOWN",
        "indexed_chunks": store.count()
    }

@app.post("/api/ingest/directory", response_model=IngestResponse)
def ingest_directory():
    files, chunks = ingestion.ingest_directory(Path("../data/documents"))
    return IngestResponse(
        files_processed=files,
        chunks_created=chunks,
        message="Directory ingestion completed"
    )

@app.post("/api/ingest/upload", response_model=IngestResponse)
async def ingest_upload(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in {".pdf", ".txt", ".md"}:
        raise HTTPException(400, "Only PDF, TXT and MD are supported")

    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir) / (file.filename or f"upload{suffix}")
        with target.open("wb") as output:
            shutil.copyfileobj(file.file, output)
        chunks = ingestion.ingest_file(target)

    return IngestResponse(
        files_processed=1,
        chunks_created=chunks,
        message=f"{file.filename} ingested successfully"
    )

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return ChatResponse(**rag.ask(request.question, request.top_k))
    except Exception as exc:
        raise HTTPException(500, f"RAG processing failed: {exc}") from exc

@app.delete("/api/index")
def clear_index():
    store.clear()
    return {"message": "Index cleared"}
