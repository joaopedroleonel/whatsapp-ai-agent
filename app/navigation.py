import asyncio

from browser import load_js, run_js
from config import MAX_ARROWS, MAX_TABS, OPEN_TIMEOUT
from keyboard import press


async def focus_state(tab, name):
    return await run_js(tab, load_js("focus_state.js"), name=name)


async def open_chat(tab, chat):
    name = chat["name"]

    state = await focus_state(tab, name)
    for _ in range(MAX_TABS):
        if state["focused"] is not None:
            break
        await press(tab, "Tab")
        state = await focus_state(tab, name)
    else:
        raise RuntimeError("Could not reach the chat list with TAB")

    for _ in range(MAX_ARROWS):
        if state["target"] is None:
            raise RuntimeError(f"Chat not found in the list: {name}")
        if state["focused"] == state["target"]:
            break
        await press(tab, "ArrowDown" if state["target"] > state["focused"] else "ArrowUp")
        state = await focus_state(tab, name)
    else:
        raise RuntimeError(f"Could not reach chat with arrows: {name}")

    await press(tab, "Enter")
    for _ in range(int(OPEN_TIMEOUT * 4)):
        state = await focus_state(tab, name)
        if state["chatOpen"] and state["selectedName"] == name:
            await asyncio.sleep(1)
            return
        await asyncio.sleep(0.25)
    raise RuntimeError(f"Chat did not open: {name}")


async def close_chat(tab):
    for _ in range(3):
        if not (await focus_state(tab, None))["chatOpen"]:
            return
        await press(tab, "Escape")
        await asyncio.sleep(0.5)
    raise RuntimeError("Chat did not close with Escape")
