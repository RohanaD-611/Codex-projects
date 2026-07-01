from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import FRONTEND_DIR, ensure_storage_dirs
from app.routers import analysis, candidates, exports, interview, resumes


app = FastAPI(title="Overseas Candidate Screening")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
app.include_router(candidates.router)
app.include_router(resumes.router)
app.include_router(interview.router)
app.include_router(exports.router)


@app.on_event("startup")
def startup() -> None:
    ensure_storage_dirs()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/results/{analysis_id}")
def results_page(analysis_id: str):
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/candidates/{candidate_id}")
def candidate_page(candidate_id: str):
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
