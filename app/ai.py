from pathlib import Path
from time import perf_counter

from openai import AsyncOpenAI

from config import (AI_API_KEY, AI_BASE_URL, AI_EXTRA_BODY, AI_HISTORY, AI_MAX_TOKENS, AI_MODEL, AI_TEMPERATURE, AI_TIMEOUT)
from log import elapsed_ms, get_logger

INSTRUCTIONS = (Path(__file__).parent / "prompts" / "instructions.md").read_text(encoding="utf-8")
client = AsyncOpenAI(base_url=AI_BASE_URL, api_key=AI_API_KEY, timeout=AI_TIMEOUT)

log = get_logger("ai")


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
    messages = build_messages(history, pending)
    log.debug("Chamando a IA", mensagens_enviadas=len(messages))
    start = perf_counter()
    response = await client.chat.completions.create(
        model=AI_MODEL,
        messages=messages,
        temperature=AI_TEMPERATURE,
        max_tokens=AI_MAX_TOKENS,
        extra_body=AI_EXTRA_BODY,
    )
    choice = response.choices[0]
    answer = (choice.message.content or "").strip()
    usage = response.usage
    log.info(
        "Resposta gerada", ms=elapsed_ms(start), chars=len(answer), fim=choice.finish_reason,
        tokens_in=usage.prompt_tokens if usage else None, tokens_out=usage.completion_tokens if usage else None,
    )
    if choice.finish_reason == "length":
        log.warning("Resposta cortada", detalhe=f"atingiu AI_MAX_TOKENS={AI_MAX_TOKENS}")
    if not answer:
        log.warning("Resposta vazia da IA")
    log.debug("Texto da resposta", texto=answer)
    return answer
