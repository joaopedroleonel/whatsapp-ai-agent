import asyncio
from time import perf_counter
from urllib.parse import urlparse

from openai import APIError

from ai import reply
from browser import start_whatsapp
from chat_list import get_unread_chats
from config import AI_BASE_URL, AI_HISTORY, AI_MODEL, CHECK_INTERVAL, SEND_WAIT, SENDER_NAME
from conversation import read_messages, unanswered
from keyboard import press, type_text
from log import chat_context, elapsed_ms, get_logger, setup_logging
from navigation import close_chat, open_chat

log = get_logger("main")


async def handle_chat(tab, chat):
    await open_chat(tab, chat)
    messages = await read_messages(tab)
    pending = unanswered(messages)
    answer = await reply(messages[:len(messages) - len(pending)], pending)
    text = (f"*[{SENDER_NAME}]*\n{answer}" if SENDER_NAME else answer) if answer else ""
    if text:
        await type_text(tab, text)
        await press(tab, "Enter")
        await asyncio.sleep(SEND_WAIT)
    else:
        log.info("Nothing sent", reason="empty reply")
    await close_chat(tab)
    return len(pending), len(text)


async def attend(tab, chat):
    with chat_context(chat["name"]):
        start = perf_counter()
        log.info("Chat started", unread=chat["unread"])
        try:
            pending, sent = await handle_chat(tab, chat)
        except (RuntimeError, APIError) as e:
            log.error("Chat failed", error=type(e).__name__, detail=str(e), ms=elapsed_ms(start))
        else:
            log.info("Chat finished", pending=pending, chars_sent=sent, ms=elapsed_ms(start))


async def stop_browser(browser):
    process = browser._process
    if not browser.stopped:
        browser.stop()
    if process:
        await process.wait()


async def main():
    setup_logging()
    log.info("Starting", model=AI_MODEL, api=urlparse(AI_BASE_URL).netloc, history=AI_HISTORY, interval_s=CHECK_INTERVAL)
    browser, tab = await start_whatsapp()
    log.info("WhatsApp Web ready", hint="close the browser or press Ctrl+C to exit")
    try:
        while not browser.stopped:
            chats = await get_unread_chats(tab)
            log.debug("Check", unread=len(chats))
            if chats:
                log.info("Unread chats", total=len(chats), queue=[c["name"] for c in chats])
                await attend(tab, chats[0])
            await asyncio.sleep(CHECK_INTERVAL)
    except Exception:
        log.exception("Fatal error")
        raise SystemExit(1)
    finally:
        log.info("Shutting down")
        await stop_browser(browser)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
