from services.llm import call_llm

SYSTEM_PROMPT = """You are a senior software engineer helping a new developer understand a codebase. Given the file tree and key source files, produce an analysis covering:

1. **Entry Points** — identify the main entry points (main.py, index.js, app.py, cmd/main.go, etc.) and explain what each one does.
2. **Application Startup Flow** — describe step by step what happens when the application starts: what gets initialized, what services connect, what routes are registered, etc.
3. **Core Data Flow** — trace how data moves through the application for a typical request or operation. Identify controllers/handlers, services/business logic, and data access layers.
4. **Key Functions & Classes** — highlight the most important functions, classes, or modules a new developer should understand first.
5. **External Dependencies & Integrations** — note any external APIs, databases, message queues, or services the code interacts with.

Output well-structured Markdown. Reference specific file names and function names where possible."""


async def run(repo_data: dict) -> str:
    # Focus on source code files likely to contain entry points and core logic
    entry_point_names = {
        "main", "index", "app", "server", "cli", "run", "manage",
        "__main__", "handler", "lambda_function",
    }

    relevant_files = ""
    for path, content in repo_data["file_contents"].items():
        name = path.split("/")[-1].rsplit(".", 1)[0].lower()
        if name in entry_point_names or path.count("/") == 0:
            relevant_files += f"\n--- {path} ---\n{content[:4000]}\n"

    # Also include other source files (truncated)
    other_source = ""
    for path, content in repo_data["file_contents"].items():
        name = path.split("/")[-1].rsplit(".", 1)[0].lower()
        if name not in entry_point_names and path.count("/") > 0:
            other_source += f"\n--- {path} ---\n{content[:2000]}\n"

    tree_str = "\n".join(repo_data["tree"])

    user_prompt = (
        f"Repository: {repo_data['owner']}/{repo_data['repo']}\n\n"
        f"File tree:\n{tree_str}\n\n"
        f"Entry point & root files:\n{relevant_files}\n\n"
        f"Other source files:\n{other_source}"
    )
    return await call_llm(SYSTEM_PROMPT, user_prompt)
