import re
from pathlib import Path

from src.config import DOCUMENTS_DIR


def clean_text(text: str) -> str:
    """Remove HTML artifacts and normalize whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[dict]:
    """Load all .txt files from documents/."""
    docs = []
    for path in sorted(documents_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        cleaned = clean_text(raw)
        if cleaned:
            docs.append(
                {
                    "source": path.name,
                    "text": cleaned,
                }
            )
    return docs
