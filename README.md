# Smart-Fit (Minimal)

Quick start (Windows PowerShell):

1) Create venv and install

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

2) Run API (from repo root)

```
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend
```

3) Environment variables (PowerShell example)

```
$env:DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/smartfit"
$env:API_BASE = "http://127.0.0.1:8000"
```

4) Run Streamlit app (in a second shell)

```
streamlit run frontend/app.py
```

API highlights:
- POST /auth/register
- POST /auth/login
- GET /auth/user/{user_id}
- CRUD: /exercises, /workouts, /nutrition, /progress
- Chat: POST /chat/ask, GET /chat/history/{user_id}

This build stores data in PostgreSQL (see `DATABASE_URL`) and uses a tiny in-memory retrieval for chat. The API auto-creates tables at startup. If the target database doesn't exist and the user has privileges, it will attempt to create it.

use proper files structure and modular and should implement everything as i mentioned