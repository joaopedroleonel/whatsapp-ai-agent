from browser import load_js, run_js


async def get_unread_chats(tab):
    return await run_js(tab, load_js("unread_chats.js"))
