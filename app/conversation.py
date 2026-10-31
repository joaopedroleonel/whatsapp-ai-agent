from browser import run_js
from log import get_logger

log = get_logger("conversation")


async def read_messages(tab):
    return await run_js(tab, "chat_messages.js")


def unanswered(messages):
    last_mine = max((i for i, m in enumerate(messages) if m["fromMe"]), default=-1)
    pending = messages[last_mine + 1:]
    log.debug("Mensagens lidas", mensagens=len(messages), pendentes=len(pending))
    for m in pending:
        if m["text"]:
            log.debug("Mensagem pendente", hora=m["time"], texto=m["text"])
        else:
            log.warning("Mensagem sem texto", hora=m["time"], detalhe="provavelmente mídia; vai vazia para a IA")
    return pending
