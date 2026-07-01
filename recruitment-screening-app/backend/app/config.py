from pathlib import Path
import os


APP_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = APP_DIR.parents[1] / "frontend"
STORAGE_ROOT = Path(os.getenv("SCREENING_STORAGE_ROOT", r"D:\Codex\Web"))
UPLOADS_DIR = STORAGE_ROOT / "uploads"
OUTPUTS_DIR = STORAGE_ROOT / "outputs"


def ensure_storage_dirs() -> None:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
