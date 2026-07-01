import re
from typing import List, Optional


def split_terms(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    parts = re.split(r"[\n,;；，]+", raw)
    return [part.strip().lower() for part in parts if part.strip()]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_term(text: str, term: str) -> bool:
    if not term:
        return False
    return re.search(rf"(?<!\w){re.escape(term.lower())}(?!\w)", text.lower()) is not None
