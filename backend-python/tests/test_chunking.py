from app.services.chunking import chunk_text

def test_chunking():
    chunks = chunk_text("Enterprise RAG " * 300)
    assert len(chunks) > 1

def test_empty():
    assert chunk_text("") == []
