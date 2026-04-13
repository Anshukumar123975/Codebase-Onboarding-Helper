from services.llm import call_llm

SYSTEM_PROMPT = """You are a developer experience expert. Given a repository's file tree and selected file contents, produce a clear setup guide covering:

1. **Prerequisites** — runtime versions, system dependencies, tools that must be installed.
2. **Installation Steps** — exact commands to install dependencies (npm install, pip install, etc.).
3. **Environment Variables** — list every env var referenced in the code or .env files, with a description and whether it's required or optional.
4. **How to Run** — commands to start the application in development mode.
5. **How to Build** — commands for production builds, if applicable.
6. **How to Test** — commands to run the test suite, if tests exist.
7. **Docker** — if Dockerfiles or docker-compose files exist, explain how to use them.

Output well-structured Markdown. Only include sections for which you find evidence in the provided data."""


async def run(repo_data: dict) -> str:
    # Focus on setup-relevant files
    setup_keywords = {
        "readme", "dockerfile", "docker-compose", "makefile", "procfile",
        "package.json", "requirements.txt", "pyproject.toml", "cargo.toml",
        "go.mod", "gemfile", ".env", "setup.py", "setup.cfg",
        "build.gradle", "pom.xml", "justfile",
    }

    relevant_files = ""
    for path, content in repo_data["file_contents"].items():
        name = path.split("/")[-1].lower()
        if any(kw in name for kw in setup_keywords):
            relevant_files += f"\n--- {path} ---\n{content[:4000]}\n"

    tree_str = "\n".join(repo_data["tree"])

    user_prompt = (
        f"Repository: {repo_data['owner']}/{repo_data['repo']}\n\n"
        f"File tree:\n{tree_str}\n\n"
        f"Setup-relevant files:\n{relevant_files}"
    )
    return await call_llm(SYSTEM_PROMPT, user_prompt)
