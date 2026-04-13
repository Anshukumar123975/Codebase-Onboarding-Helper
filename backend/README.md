# Backend — Codebase Onboarding Agent

FastAPI server with a multi-agent pipeline that analyzes GitHub repositories.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | Yes | API key from openrouter.ai |
| `REDIS_URL` | No | Defaults to `redis://localhost:6379` |
| `GITHUB_TOKEN` | No | Optional GitHub PAT for higher rate limits |

## Run

```bash
# Make sure Redis is running
uvicorn main:app --reload --port 8000
```

## API Endpoints

- `POST /analyze` — Start analysis `{ "github_url": "..." }` → `{ "job_id": "..." }`
- `GET /status/{job_id}` — Poll job status
- `GET /result/{job_id}` — Get completed markdown result
