from browser import load_js, run_js


async def read_messages(tab):
    return await run_js(tab, load_js("chat_messages.js"))


def unanswered(messages):
    last_mine = max((i for i, m in enumerate(messages) if m["fromMe"]), default=-1)
    return messages[last_mine + 1:]
