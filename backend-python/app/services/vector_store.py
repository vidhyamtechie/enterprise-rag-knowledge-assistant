import chromadb
from app.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_path)
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name
        )

    def upsert(self, ids, documents, embeddings, metadatas):
        if ids:
            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )

    def query(self, embedding: list[float], top_k: int) -> list[dict]:
        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        metadata = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        return [
            {
                "id": chunk_id,
                "document": doc,
                "metadata": meta or {},
                "distance": distance
            }
            for chunk_id, doc, meta, distance
            in zip(ids, docs, metadata, distances)
        ]

    def count(self) -> int:
        return self.collection.count()

    def clear(self):
        data = self.collection.get()
        ids = data.get("ids", [])
        if ids:
            self.collection.delete(ids=ids)
