import asyncio

from openai import APIError

from ai import reply
from browser import start_whatsapp
from chat_list import get_unread_chats
from config import CHECK_INTERVAL, SEND_WAIT, SENDER_NAME
from conversation import read_messages, unanswered
from keyboard import press, type_text
from navigation import close_chat, open_chat


async def handle_chat(tab, chat):
    await open_chat(tab, chat)
    messages = await read_messages(tab)
    pending = unanswered(messages)
    answer = await reply(messages[:len(messages) - len(pending)], pending)
    if answer:
        await type_text(tab, f"*[{SENDER_NAME}]*\n{answer}" if SENDER_NAME else answer)
        await press(tab, "Enter")
        await asyncio.sleep(SEND_WAIT)
    await close_chat(tab)


async def stop_browser(browser):
    process = browser._process
    if not browser.stopped:
        browser.stop()
    if process:
        await process.wait()


async def main():
    browser, tab = await start_whatsapp()
    print("WhatsApp Web pronto. Feche o navegador ou aperte Ctrl+C para sair.")
    try:
        while not browser.stopped:
            chats = await get_unread_chats(tab)
            if chats:
                try:
                    await handle_chat(tab, chats[0])
                except (RuntimeError, APIError) as e:
                    print(f"Falha em {chats[0]['name']}: {e}")
            await asyncio.sleep(CHECK_INTERVAL)
    finally:
        await stop_browser(browser)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
