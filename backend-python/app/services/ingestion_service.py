from pathlib import Path
from app.services.document_loader import load_document, SUPPORTED_EXTENSIONS
from app.services.chunking import chunk_text
from app.services.ollama_client import OllamaClient
from app.services.vector_store import VectorStore

class IngestionService:
    def __init__(self):
        self.ollama = OllamaClient()
        self.store = VectorStore()

    def ingest_file(self, path: Path) -> int:
        ids = []
        documents = []
        metadatas = []

        for page in load_document(path):
            for chunk_index, chunk in enumerate(chunk_text(page["text"])):
                chunk_id = f"{path.name}-{page['page']}-{chunk_index}"
                ids.append(chunk_id)
                documents.append(chunk)
                metadatas.append({
                    "source": path.name,
                    "page": page["page"],
                    "chunk_index": chunk_index
                })

        if not documents:
            return 0

        embeddings = self.ollama.embed(documents)
        self.store.upsert(ids, documents, embeddings, metadatas)
        return len(documents)

    def ingest_directory(self, directory: Path) -> tuple[int, int]:
        directory.mkdir(parents=True, exist_ok=True)

        files_processed = 0
        chunks_created = 0

        for path in directory.iterdir():
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                chunks_created += self.ingest_file(path)
                files_processed += 1

        return files_processed, chunks_created
