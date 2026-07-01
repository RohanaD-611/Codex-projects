from pathlib import Path
from typing import List, Optional
from uuid import uuid4
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import OUTPUTS_DIR, UPLOADS_DIR, ensure_storage_dirs
from app.schemas import AnalysisRecord, AnalyzeResponse, SalaryBudget
from app.services.jd_parser import split_terms
from app.services.report_generator import write_exports
from app.services.resume_parser import parse_resume_file
from app.services.scoring import rank_candidates, score_candidate

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    mode: str = Form("batch"),
    job_title: str = Form(...),
    job_description: str = Form(...),
    target_market: str = Form(""),
    top_n: int = Form(10),
    salary_currency: str = Form("SGD"),
    salary_period: str = Form("year"),
    salary_min: Optional[float] = Form(None),
    salary_max: Optional[float] = Form(None),
    hard_requirements: str = Form(""),
    must_have_skills: str = Form(""),
    nice_to_have_skills: str = Form(""),
    resumes: List[UploadFile] = File(...),
) -> AnalyzeResponse:
    ensure_storage_dirs()
    if mode not in {"single", "batch"}:
        raise HTTPException(status_code=400, detail="mode must be single or batch")
    if mode == "single" and len(resumes) > 1:
        resumes = resumes[:1]

    analysis_id = f"analysis_{uuid4().hex[:12]}"
    analysis_upload_dir = UPLOADS_DIR / analysis_id
    analysis_output_dir = OUTPUTS_DIR / analysis_id
    analysis_upload_dir.mkdir(parents=True, exist_ok=True)

    budget = SalaryBudget(
        currency=salary_currency.upper(),
        period=salary_period,
        min=salary_min,
        max=salary_max,
    )
    parsed_candidates = []
    scored = []
    errors = []

    for index, upload in enumerate(resumes, start=1):
        original_name = Path(upload.filename or f"resume_{index}.txt").name
        candidate_id = f"{analysis_id}_candidate_{index:03d}"
        stored_name = f"{candidate_id}_{original_name}"
        stored_path = analysis_upload_dir / stored_name
        with stored_path.open("wb") as target:
            shutil.copyfileobj(upload.file, target)

        try:
            candidate = parse_resume_file(
                stored_path,
                candidate_id=candidate_id,
                resume_url=f"/api/candidates/{candidate_id}/resume",
            )
            parsed_candidates.append(candidate)
            scored.append(
                score_candidate(
                    analysis_id=analysis_id,
                    job_title=job_title,
                    job_description=job_description,
                    target_market=target_market,
                    hard_requirements=split_terms(hard_requirements),
                    must_have_skills=split_terms(must_have_skills),
                    nice_to_have_skills=split_terms(nice_to_have_skills),
                    salary_budget=budget,
                    candidate=candidate,
                )
            )
        except Exception as exc:
            errors.append({"file": original_name, "error": str(exc)})

    ranked = rank_candidates(scored, top_n)
    average = round(sum(item.total_score for item in ranked) / len(ranked), 2) if ranked else 0
    record = AnalysisRecord(
        analysis_id=analysis_id,
        mode=mode,
        job={
            "title": job_title,
            "description": job_description,
            "target_market": target_market,
            "top_n": top_n,
            "candidate_count": len(parsed_candidates),
            "salary_budget": budget.dict(),
            "hard_requirements": split_terms(hard_requirements),
            "must_have_skills": split_terms(must_have_skills),
            "nice_to_have_skills": split_terms(nice_to_have_skills),
            "parse_errors": errors,
        },
        summary={"average_score": average},
        candidates=ranked,
    )
    write_exports(record, analysis_output_dir)
    return AnalyzeResponse(
        analysis_id=analysis_id,
        mode=mode,
        candidate_count=len(parsed_candidates),
        top_n=top_n,
        redirect_url=f"/results/{analysis_id}",
    )


@router.get("/analysis/{analysis_id}", response_model=AnalysisRecord)
def get_analysis(analysis_id: str) -> AnalysisRecord:
    return _load_record(analysis_id)


def _load_record(analysis_id: str) -> AnalysisRecord:
    path = OUTPUTS_DIR / analysis_id / "analysis.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisRecord.parse_raw(path.read_text(encoding="utf-8"))
