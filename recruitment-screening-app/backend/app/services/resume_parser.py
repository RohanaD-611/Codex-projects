from pathlib import Path
import re
from typing import List, Optional

from pypdf import PdfReader

from app.schemas import CandidateParsedData, SalaryExpectation


LANGUAGE_TERMS = ["english", "mandarin", "chinese", "cantonese", "thai", "vietnamese", "bahasa", "malay", "japanese", "korean"]
COMMON_SKILLS = [
    "sales", "channel sales", "enterprise sales", "business development", "team management",
    "saas", "crm", "marketing", "operations", "finance", "python", "fastapi", "react",
    "aws", "kubernetes", "sql", "data analysis", "project management",
]
MARKETS = ["singapore", "malaysia", "indonesia", "thailand", "vietnam", "philippines", "china", "hong kong", "taiwan", "japan", "korea", "us", "europe"]


def parse_resume_file(file_path: Path, candidate_id: str, resume_url: str) -> CandidateParsedData:
    text = _extract_text(file_path)
    return CandidateParsedData(
        candidate_id=candidate_id,
        name=_extract_name(text, file_path.name),
        resume_file_name=file_path.name,
        resume_file_path=str(file_path),
        resume_url=resume_url,
        resume_text=text,
        email=_extract_email(text),
        phone=_extract_phone(text),
        years_experience=_extract_years(text),
        languages=_find_terms(text, LANGUAGE_TERMS),
        skills=_find_terms(text, COMMON_SKILLS),
        markets=_find_terms(text, MARKETS),
        salary_expectation=_extract_salary(text),
    )


def _extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(file_path))
        return _clean(" ".join(page.extract_text() or "" for page in reader.pages))
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise ValueError("DOCX parsing requires optional dependency python-docx.") from exc
        document = Document(str(file_path))
        return _clean(" ".join(paragraph.text for paragraph in document.paragraphs))
    if suffix == ".txt":
        return _clean(file_path.read_text(encoding="utf-8", errors="ignore"))
    raise ValueError(f"Unsupported resume format: {suffix}")


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _extract_email(text: str) -> Optional[str]:
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0) if match else None


def _extract_phone(text: str) -> Optional[str]:
    match = re.search(r"(?:\+\d{1,3}[\s-]?)?(?:\d[\s-]?){8,14}", text)
    return match.group(0).strip() if match else None


def _extract_name(text: str, fallback: str) -> str:
    name_match = re.search(
        r"\b(?:name|full name)\s*[:\-]\s*([A-Za-z][A-Za-z\s.'-]{1,60}?)(?=\s+(?:email|phone|mobile|tel)\b|$)",
        text,
        re.I,
    )
    if name_match:
        return _title(name_match.group(1))
    if _extract_email(text):
        local = _extract_email(text).split("@")[0]
        return _title(re.sub(r"[\d._+-]+", " ", local))
    return _title(Path(fallback).stem.replace("_", " ").replace("-", " "))


def _title(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split() if part) or "Candidate"


def _extract_years(text: str) -> float:
    values = []
    for pattern in [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+(?:professional\s+)?experience",
        r"experience\s*[:\-]\s*(\d+(?:\.\d+)?)\+?\s*years?",
    ]:
        values.extend(float(value) for value in re.findall(pattern, text, re.I))
    return max(values) if values else 0


def _find_terms(text: str, terms: List[str]) -> List[str]:
    lowered = text.lower()
    return sorted({term for term in terms if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", lowered)})


def _extract_salary(text: str) -> SalaryExpectation:
    match = re.search(r"\b(CNY|RMB|USD|SGD|MYR|THB|IDR|VND|PHP)\s*([0-9][0-9,]*(?:\.\d+)?)\s*(?:-|to|~)?\s*([0-9][0-9,]*(?:\.\d+)?)?", text, re.I)
    if not match:
        return SalaryExpectation()
    currency = "CNY" if match.group(1).upper() == "RMB" else match.group(1).upper()
    amount_min = float(match.group(2).replace(",", ""))
    amount_max = float(match.group(3).replace(",", "")) if match.group(3) else amount_min
    period = "year" if re.search(r"annual|year|年", text, re.I) else "month"
    return SalaryExpectation(amount_min=amount_min, amount_max=amount_max, currency=currency, period=period, source="resume_text")
