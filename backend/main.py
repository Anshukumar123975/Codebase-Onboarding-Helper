import os

from dotenv import load_dotenv

load_dotenv()  # loads .env
load_dotenv(".env.example")  # fallback if .env doesn't exist

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import run_pipeline
from services.redis import get_job, get_cached_result, close_redis

app = FastAPI(title="Codebase Onboarding Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    github_url: str


class AnalyzeResponse(BaseModel):
    job_id: str


class StatusResponse(BaseModel):
    status: str
    current_agent: str
    completed_agents: list[str]
    progress_percent: int


class ResultResponse(BaseModel):
    markdown: str


@app.on_event("shutdown")
async def shutdown():
    await close_redis()


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    url = req.github_url.strip()
    if not url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="URL must be a public GitHub repository")
    job_id = await run_pipeline(url)
    return AnalyzeResponse(job_id=job_id)


@app.get("/status/{job_id}", response_model=StatusResponse)
async def status(job_id: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] == "error":
        raise HTTPException(status_code=500, detail=job.get("error", "Unknown error"))
    return StatusResponse(
        status=job["status"],
        current_agent=job.get("current_agent", ""),
        completed_agents=job.get("completed_agents", []),
        progress_percent=job.get("progress_percent", 0),
    )


@app.get("/result/{job_id}", response_model=ResultResponse)
async def result(job_id: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "done":
        raise HTTPException(status_code=202, detail="Job is still processing")
    return ResultResponse(markdown=job.get("result", ""))
