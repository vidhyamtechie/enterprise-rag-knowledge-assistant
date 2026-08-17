from pathlib import Path
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

def load_document(path: Path) -> list[dict]:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        pages = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({
                    "text": text,
                    "source": path.name,
                    "page": page_number
                })
        return pages

    if suffix in {".txt", ".md"}:
        return [{
            "text": path.read_text(encoding="utf-8", errors="ignore"),
            "source": path.name,
            "page": 1
        }]

    raise ValueError(f"Unsupported extension: {suffix}")
