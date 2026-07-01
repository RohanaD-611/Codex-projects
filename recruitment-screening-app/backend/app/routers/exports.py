from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import OUTPUTS_DIR

router = APIRouter(prefix="/api", tags=["exports"])


@router.get("/analysis/{analysis_id}/export/{kind}")
def export_analysis(analysis_id: str, kind: str):
    file_map = {
        "html": "shortlist.html",
        "csv": "shortlist.csv",
        "json": "analysis.json",
    }
    if kind not in file_map:
        raise HTTPException(status_code=404, detail="Export type not found")
    path = OUTPUTS_DIR / analysis_id / file_map[kind]
    if not path.exists():
        raise HTTPException(status_code=404, detail="Export not found")
    return FileResponse(path, filename=file_map[kind])
