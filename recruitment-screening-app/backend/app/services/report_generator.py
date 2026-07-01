import csv
import json
from pathlib import Path

from app.schemas import AnalysisRecord


def write_exports(record: AnalysisRecord, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "analysis.json").write_text(record.json(indent=2, ensure_ascii=False), encoding="utf-8")
    _write_csv(record, output_dir / "shortlist.csv")
    _write_html(record, output_dir / "shortlist.html")


def _write_csv(record: AnalysisRecord, path: Path) -> None:
    fields = [
        "rank", "name", "resume_file", "total_score", "recommendation", "summary",
        "hard_requirements", "skills_match", "experience_relevance", "overseas_market_fit",
        "language_communication", "salary_match", "risk", "strengths", "gaps", "risks",
        "salary_status", "salary_reason",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for c in record.candidates:
            writer.writerow({
                "rank": c.rank,
                "name": c.name,
                "resume_file": c.resume_file_name,
                "total_score": c.total_score,
                "recommendation": c.recommendation,
                "summary": c.summary,
                "hard_requirements": c.scores.hard_requirements,
                "skills_match": c.scores.skills_match,
                "experience_relevance": c.scores.experience_relevance,
                "overseas_market_fit": c.scores.overseas_market_fit,
                "language_communication": c.scores.language_communication,
                "salary_match": c.scores.salary_match,
                "risk": c.scores.risk,
                "strengths": " | ".join(c.strengths),
                "gaps": " | ".join(c.gaps),
                "risks": " | ".join(c.risks),
                "salary_status": c.salary_match.status,
                "salary_reason": c.salary_match.reason,
            })


def _write_html(record: AnalysisRecord, path: Path) -> None:
    candidates = "\n".join(
        f"<article><h2>#{c.rank} {c.name} - {c.total_score}</h2><p>{c.recommendation}</p><p>{c.summary}</p></article>"
        for c in record.candidates
    )
    html = f"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>{record.job.get('title', 'Shortlist')}</title></head>
<body>
<h1>{record.job.get('title', 'Shortlist')}</h1>
<pre>{json.dumps(record.job, ensure_ascii=False, indent=2)}</pre>
{candidates}
</body>
</html>"""
    path.write_text(html, encoding="utf-8")
