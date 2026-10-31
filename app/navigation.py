import asyncio
from time import perf_counter

from browser import run_js
from config import MAX_ARROWS, MAX_TABS, OPEN_TIMEOUT
from keyboard import press
from log import elapsed_ms, get_logger

log = get_logger("navigation")


async def focus_state(tab, name):
    return await run_js(tab, "focus_state.js", name=name)


async def open_chat(tab, chat):
    name = chat["name"]
    start = perf_counter()
    tabs = arrows = 0

    state = await focus_state(tab, name)
    for _ in range(MAX_TABS):
        if state["focused"] is not None:
            break
        await press(tab, "Tab")
        tabs += 1
        state = await focus_state(tab, name)
    else:
        raise RuntimeError("Não foi possível chegar na lista de conversas com TAB")

    for _ in range(MAX_ARROWS):
        if state["target"] is None:
            raise RuntimeError(f"Conversa não encontrada na lista: {name}")
        if state["focused"] == state["target"]:
            break
        await press(tab, "ArrowDown" if state["target"] > state["focused"] else "ArrowUp")
        arrows += 1
        state = await focus_state(tab, name)
    else:
        raise RuntimeError(f"Não foi possível chegar na conversa com as setas: {name}")

    await press(tab, "Enter")
    for _ in range(int(OPEN_TIMEOUT * 4)):
        state = await focus_state(tab, name)
        if state["chatOpen"] and state["selectedName"] == name:
            await asyncio.sleep(1)
            log.info("Conversa aberta", tabs=tabs, setas=arrows, ms=elapsed_ms(start))
            return
        await asyncio.sleep(0.25)
    raise RuntimeError(f"A conversa não abriu: {name}")


async def close_chat(tab):
    for presses in range(3):
        if not (await focus_state(tab, None))["chatOpen"]:
            log.debug("Conversa fechada", esc=presses)
            return
        await press(tab, "Escape")
        await asyncio.sleep(0.5)
    raise RuntimeError("A conversa não fechou com Esc")
