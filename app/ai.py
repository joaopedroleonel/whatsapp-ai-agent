from pathlib import Path

from openai import AsyncOpenAI

from config import (AI_API_KEY, AI_BASE_URL, AI_EXTRA_BODY, AI_HISTORY, AI_MAX_TOKENS, AI_MODEL,
                    AI_TEMPERATURE, AI_TIMEOUT)

INSTRUCTIONS = (Path(__file__).parent / "prompts" / "instructions.md").read_text(encoding="utf-8")
client = AsyncOpenAI(base_url=AI_BASE_URL, api_key=AI_API_KEY, timeout=AI_TIMEOUT)


def build_messages(history, pending):
    messages = [{"role": "system", "content": INSTRUCTIONS}]
    turns = [("assistant" if m["fromMe"] else "user", m["text"]) for m in history] if AI_HISTORY else []
    turns += [("user", m["text"]) for m in pending]
    for role, text in turns:
        if messages[-1]["role"] == role:
            messages[-1]["content"] += f"\n{text}"
        else:
            messages.append({"role": role, "content": text})
    return messages


async def reply(history, pending):
    response = await client.chat.completions.create(
        model=AI_MODEL,
        messages=build_messages(history, pending),
        temperature=AI_TEMPERATURE,
        max_tokens=AI_MAX_TOKENS,
        extra_body=AI_EXTRA_BODY,
    )
    return (response.choices[0].message.content or "").strip()
