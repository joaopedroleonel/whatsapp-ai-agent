from browser import run_js


async def get_unread_chats(tab):
    return await run_js(tab, "unread_chats.js")
