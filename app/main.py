import asyncio

import nodriver as uc
from ollama import ResponseError

from ai import reply, warm_up
from browser import start_whatsapp
from chat_list import get_unread_chats
from config import CHECK_INTERVAL
from conversation import read_messages, to_text, unanswered
from navigation import close_chat, open_chat


async def main():
    (browser, tab), _ = await asyncio.gather(start_whatsapp(), warm_up())
    print("WhatsApp Web ready. Close the browser or press Ctrl+C to quit.")

    while not browser.stopped:
        chats = await get_unread_chats(tab)
        if chats:
            chat = chats[0]
            try:
                await open_chat(tab, chat)
                messages = await read_messages(tab)
                pending = unanswered(messages)
                question = to_text(pending)
                answer = await reply(messages[:len(messages) - len(pending)], question)
                print(f"Q: {question}\nA: {answer}\n")
                await close_chat(tab)
            except (RuntimeError, ConnectionError, ResponseError) as e:
                print(f"Failed on {chat['name']}: {e}")
        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        uc.loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
