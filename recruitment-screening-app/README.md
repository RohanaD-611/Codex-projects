# Overseas Candidate Screening

Local web app for JD-based resume screening in overseas hiring scenarios.

## Run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SCREENING_STORAGE_ROOT = "D:\Codex\Web"
uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
```

Open `http://127.0.0.1:8010/`.

## Storage

Uploaded resumes and exports are stored under `D:\Codex\Web` by default:

```text
D:\Codex\Web\
  uploads\
  outputs\
```

Set `SCREENING_STORAGE_ROOT` to override this path.
