import logging
import uuid

from agents import architecture, setup, code_flow, writer
from services.github import parse_repo_url, fetch_repo_contents
from services.redis import (
    create_job,
    update_job,
    get_cached_result,
    set_cached_result,
)

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def run_pipeline(github_url: str) -> str:
    """Start a new analysis job and return the job_id."""
    job_id = uuid.uuid4().hex[:12]
    await create_job(job_id, github_url)

    # Check cache first
    cached = await get_cached_result(github_url)
    if cached:
        log.info("[%s] Cache hit — returning cached result", job_id)
        await update_job(
            job_id,
            status="done",
            current_agent="",
            completed_agents=["architecture", "setup", "code_flow", "writer"],
            progress_percent=100,
            result=cached,
        )
        return job_id

    # Run pipeline in background — caller gets job_id immediately
    import asyncio
    asyncio.create_task(_run(job_id, github_url))
    return job_id


async def _run(job_id: str, github_url: str):
    try:
        owner, repo = parse_repo_url(github_url)
        repo_name = f"{owner}/{repo}"

        # Fetch repo data
        log.info("[%s] Fetching repo: %s", job_id, repo_name)
        await update_job(job_id, current_agent="fetching", progress_percent=5)
        repo_data = await fetch_repo_contents(owner, repo)
        log.info("[%s] Fetched %d files from repo", job_id, len(repo_data.get("file_contents", {})))

        # Architecture agent
        log.info("[%s] Running architecture agent...", job_id)
        await update_job(job_id, current_agent="architecture", progress_percent=15)
        arch_output = await architecture.run(repo_data)
        log.info("[%s] Architecture agent done (%d chars)", job_id, len(arch_output))
        await update_job(
            job_id,
            completed_agents=["architecture"],
            progress_percent=35,
        )

        # Setup agent
        log.info("[%s] Running setup agent...", job_id)
        await update_job(job_id, current_agent="setup")
        setup_output = await setup.run(repo_data)
        log.info("[%s] Setup agent done (%d chars)", job_id, len(setup_output))
        await update_job(
            job_id,
            completed_agents=["architecture", "setup"],
            progress_percent=55,
        )

        # Code flow agent
        log.info("[%s] Running code flow agent...", job_id)
        await update_job(job_id, current_agent="code_flow")
        code_flow_output = await code_flow.run(repo_data)
        log.info("[%s] Code flow agent done (%d chars)", job_id, len(code_flow_output))
        await update_job(
            job_id,
            completed_agents=["architecture", "setup", "code_flow"],
            progress_percent=75,
        )

        # Writer agent
        log.info("[%s] Running writer agent...", job_id)
        await update_job(job_id, current_agent="writer")
        markdown = await writer.run(repo_name, arch_output, setup_output, code_flow_output)
        log.info("[%s] Writer agent done (%d chars)", job_id, len(markdown))
        await update_job(
            job_id,
            completed_agents=["architecture", "setup", "code_flow", "writer"],
            progress_percent=100,
            current_agent="",
            status="done",
            result=markdown,
        )

        # Cache the result
        await set_cached_result(github_url, markdown)
        log.info("[%s] Pipeline complete!", job_id)

    except Exception as e:
        log.error("[%s] Pipeline failed: %s", job_id, e, exc_info=True)
        await update_job(job_id, status="error", error=str(e))
