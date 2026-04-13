from services.llm import call_llm

SYSTEM_PROMPT = """You are an expert software architect. Given a repository's file tree and selected file contents, produce a concise analysis covering:

1. **Languages & Frameworks** — list every programming language, framework, and major library you can identify from file extensions, import statements, and config files.
2. **Project Type** — classify the project (web app, CLI tool, library, mobile app, API service, etc.).
3. **Directory Structure** — describe each top-level directory and its purpose.
4. **Architecture Pattern** — identify the architectural pattern (MVC, microservices, monorepo, serverless, etc.) if discernible.
5. **Key Configuration Files** — note important config files (package.json, pyproject.toml, Dockerfile, CI configs, etc.) and what they tell you.

Output well-structured Markdown. Be factual — only state what you can confirm from the provided data."""


async def run(repo_data: dict) -> str:
    tree_str = "\n".join(repo_data["tree"])
    sample_files = ""
    for path, content in list(repo_data["file_contents"].items())[:15]:
        sample_files += f"\n--- {path} ---\n{content[:3000]}\n"

    user_prompt = (
        f"Repository: {repo_data['owner']}/{repo_data['repo']}\n\n"
        f"File tree:\n{tree_str}\n\n"
        f"Sample file contents:\n{sample_files}"
    )
    return await call_llm(SYSTEM_PROMPT, user_prompt)
