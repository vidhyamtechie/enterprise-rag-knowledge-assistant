from app.config import settings
from app.services.ollama_client import OllamaClient
from app.services.vector_store import VectorStore

class RagService:
    def __init__(self):
        self.ollama = OllamaClient()
        self.store = VectorStore()

    def ask(self, question: str, top_k: int | None = None) -> dict:
        k = top_k or settings.top_k
        query_embedding = self.ollama.embed([question])[0]
        matches = self.store.query(query_embedding, k)

        if not matches:
            return {
                "answer": "I could not find enough information in the indexed documents.",
                "sources": []
            }

        context_parts = []
        sources = []

        for index, match in enumerate(matches, start=1):
            meta = match["metadata"]
            source = meta.get("source", "unknown")
            page = meta.get("page")

            context_parts.append(
                f"[Context {index} | Source: {source} | Page: {page}]\n"
                f"{match['document']}"
            )

            sources.append({
                "source": source,
                "page": page,
                "chunk_id": match["id"],
                "distance": match["distance"]
            })

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an enterprise knowledge assistant.

Follow these rules:
1. Answer only from the supplied context.
2. If the context does not support the answer, say you could not find enough information.
3. Never invent names, dates, numbers, policies or facts.
4. Cite the source filename/page naturally when useful.
5. Keep the answer concise and professional.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

        return {
            "answer": self.ollama.generate(prompt),
            "sources": sources
        }
