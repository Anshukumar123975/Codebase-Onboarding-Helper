import os

import httpx

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


async def call_chat(messages: list[dict[str, str]], max_tokens: int = 4096) -> str:
    """Send a chat completion request to OpenRouter and return the text."""
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set — check your .env file")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        if not resp.is_success:
            body = resp.text
            raise RuntimeError(f"OpenRouter {resp.status_code}: {body}")
        data = resp.json()
    return data["choices"][0]["message"]["content"]


async def call_llm(system_prompt: str, user_prompt: str) -> str:
    return await call_chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
