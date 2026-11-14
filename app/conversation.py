from browser import run_js
from log import get_logger

log = get_logger("conversation")


async def read_messages(tab):
    return await run_js(tab, "chat_messages.js")


def unanswered(messages):
    last_mine = max((i for i, m in enumerate(messages) if m["fromMe"]), default=-1)
    pending = messages[last_mine + 1:]
    log.debug("Messages read", messages=len(messages), pending=len(pending))
    for m in pending:
        if m["text"]:
            log.debug("Pending message", time=m["time"], text=m["text"])
        else:
            log.warning("Message without text", time=m["time"], detail="probably media; sent empty to the AI")
    return pending
