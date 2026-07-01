from fastapi import APIRouter, HTTPException

from app.config import OUTPUTS_DIR
from app.schemas import AnalysisRecord, CandidateAnalysisResult

router = APIRouter(prefix="/api", tags=["candidates"])


@router.get("/candidates/{candidate_id}", response_model=CandidateAnalysisResult)
def get_candidate(candidate_id: str) -> CandidateAnalysisResult:
    for record in _iter_records():
        for candidate in record.candidates:
            if candidate.candidate_id == candidate_id:
                return candidate
    raise HTTPException(status_code=404, detail="Candidate not found")


def find_candidate(candidate_id: str) -> CandidateAnalysisResult:
    return get_candidate(candidate_id)


def _iter_records():
    if not OUTPUTS_DIR.exists():
        return
    for path in OUTPUTS_DIR.glob("analysis_*/analysis.json"):
        yield AnalysisRecord.parse_raw(path.read_text(encoding="utf-8"))
