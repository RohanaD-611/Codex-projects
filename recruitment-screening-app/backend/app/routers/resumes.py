from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.routers.candidates import find_candidate

router = APIRouter(prefix="/api", tags=["resumes"])


@router.get("/candidates/{candidate_id}/resume")
def get_resume(candidate_id: str):
    candidate = find_candidate(candidate_id)
    path = Path(candidate.resume_url)
    # resume_url is public; file path is stored in the detail record only in V1 exports.
    record_path = _extract_path(candidate)
    if not record_path.exists():
        raise HTTPException(status_code=404, detail="Resume file not found")
    return FileResponse(
        record_path,
        filename=candidate.resume_file_name,
        media_type="application/octet-stream",
    )


def _extract_path(candidate):
    # Stored file name begins with candidate_id inside the analysis upload directory.
    from app.config import UPLOADS_DIR

    matches = list(UPLOADS_DIR.glob(f"{candidate.analysis_id}/{candidate.candidate_id}_*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Resume file not found")
    return matches[0]
