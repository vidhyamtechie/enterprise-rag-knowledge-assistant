import httpx
from app.config import settings

class OllamaClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url.rstrip("/")

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = httpx.post(
            f"{self.base_url}/api/embed",
            json={
                "model": settings.ollama_embed_model,
                "input": texts
            },
            timeout=120.0
        )
        response.raise_for_status()
        return response.json()["embeddings"]

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": settings.ollama_chat_model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            },
            timeout=120.0
        )
        response.raise_for_status()
        return response.json()["response"].strip()

    def healthy(self) -> bool:
        try:
            return httpx.get(
                f"{self.base_url}/api/tags",
                timeout=5.0
            ).is_success
        except Exception:
            return False
