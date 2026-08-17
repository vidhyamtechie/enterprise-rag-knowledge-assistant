from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(min_length=2)
    top_k: int | None = Field(default=None, ge=1, le=20)

class Source(BaseModel):
    source: str
    page: int | None = None
    chunk_id: str
    distance: float | None = None

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]

class IngestResponse(BaseModel):
    files_processed: int
    chunks_created: int
    message: str
