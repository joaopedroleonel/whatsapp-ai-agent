from pathlib import Path

from ollama import AsyncClient

from config import (OLLAMA_HOST, OLLAMA_KEEP_ALIVE, OLLAMA_MODEL, OLLAMA_NUM_BATCH,
                    OLLAMA_NUM_CTX, OLLAMA_NUM_PREDICT, OLLAMA_TEMPERATURE)

INSTRUCTIONS = (Path(__file__).parent / "prompts" / "instructions.md").read_text(encoding="utf-8")
client = AsyncClient(host=OLLAMA_HOST)
OPTIONS = {
    "temperature": OLLAMA_TEMPERATURE,
    "num_ctx": OLLAMA_NUM_CTX,
    "num_batch": OLLAMA_NUM_BATCH,
    "num_predict": OLLAMA_NUM_PREDICT,
}


def history_text(messages):
    return "\n".join(f"{'Atendente' if m['fromMe'] else 'Cliente'}: {m['text']}" for m in messages)


async def chat(history_messages, question, **options):
    return await client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": INSTRUCTIONS.replace("{history}", history_text(history_messages))},
            {"role": "user", "content": question},
        ],
        think=False,
        options={**OPTIONS, **options},
        keep_alive=OLLAMA_KEEP_ALIVE,
    )


async def warm_up():
    await chat([], "Oi", num_predict=1)


async def reply(history, question):
    response = await chat(history, question)
    return response.message.content.strip()
