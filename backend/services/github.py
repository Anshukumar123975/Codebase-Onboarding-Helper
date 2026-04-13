import os
from typing import Any

import httpx

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

MAX_FILES = 50
PRIORITY_DIRS = {"src", "app", "lib", "pkg", "cmd", "internal", "core", "server", "client"}


def _headers() -> dict[str, str]:
    h = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


def parse_repo_url(url: str) -> tuple[str, str]:
    """Return (owner, repo) from a GitHub URL."""
    url = url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    parts = url.replace("https://github.com/", "").split("/")
    if len(parts) < 2:
        raise ValueError(f"Invalid GitHub URL: {url}")
    return parts[0], parts[1]


async def fetch_repo_tree(owner: str, repo: str) -> list[dict[str, Any]]:
    """Fetch the full file tree using the Git Trees API (recursive)."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url, headers=_headers())
        resp.raise_for_status()
        data = resp.json()
    all_items = [item for item in data.get("tree", []) if item["type"] == "blob"]
    return _prioritize(all_items)


def _prioritize(items: list[dict]) -> list[dict]:
    """Pick up to MAX_FILES, prioritising root-level and key directories."""
    root_files: list[dict] = []
    priority_files: list[dict] = []
    other_files: list[dict] = []

    for item in items:
        path: str = item["path"]
        depth = path.count("/")
        if depth == 0:
            root_files.append(item)
        elif path.split("/")[0] in PRIORITY_DIRS:
            priority_files.append(item)
        else:
            other_files.append(item)

    selected = root_files + priority_files + other_files
    return selected[:MAX_FILES]


async def fetch_file_content(owner: str, repo: str, path: str) -> str:
    """Fetch raw file content from GitHub."""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url, headers=_headers())
        if resp.status_code != 200:
            return ""
        return resp.text


async def fetch_repo_contents(owner: str, repo: str) -> dict[str, Any]:
    """Return a dict with the tree and contents of key files."""
    tree = await fetch_repo_tree(owner, repo)
    paths = [item["path"] for item in tree]

    # Fetch content for important files (limit to keep context manageable)
    important_exts = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java",
        ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini",
        ".md", ".txt", ".sh", ".dockerfile",
    }
    important_names = {
        "Dockerfile", "Makefile", "Procfile", "docker-compose.yml",
        "docker-compose.yaml", ".env.example",
    }

    files_to_fetch: list[str] = []
    for p in paths:
        name = p.split("/")[-1].lower()
        ext = "." + name.rsplit(".", 1)[-1] if "." in name else ""
        original_name = p.split("/")[-1]
        if ext in important_exts or original_name in important_names:
            files_to_fetch.append(p)
        if len(files_to_fetch) >= MAX_FILES:
            break

    contents: dict[str, str] = {}
    for p in files_to_fetch:
        text = await fetch_file_content(owner, repo, p)
        if text:
            # Truncate very large files
            contents[p] = text[:8000]

    return {
        "owner": owner,
        "repo": repo,
        "tree": paths,
        "file_contents": contents,
    }
