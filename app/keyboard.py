import asyncio
import random
from time import perf_counter

import nodriver as uc

from config import KEY_DELAY_MAX, KEY_DELAY_MIN, TYPING_DELAY_MAX, TYPING_DELAY_MIN
from log import elapsed_ms, get_logger

SHIFT = 8

log = get_logger("keyboard")

KEYS = {
    "Tab": ("Tab", 9, None),
    "Enter": ("Enter", 13, "\r"),
    "Escape": ("Escape", 27, None),
    "ArrowUp": ("ArrowUp", 38, None),
    "ArrowDown": ("ArrowDown", 40, None),
}


async def press(tab, key, times=1, modifiers=0):
    code, vk, text = KEYS[key]
    for _ in range(times):
        for type_ in ("keyDown", "keyUp"):
            await tab.send(uc.cdp.input_.dispatch_key_event(
                type_=type_, key=key, code=code, windows_virtual_key_code=vk, modifiers=modifiers,
                text=text if type_ == "keyDown" else None,
            ))
        await asyncio.sleep(random.uniform(KEY_DELAY_MIN, KEY_DELAY_MAX))


async def type_text(tab, text):
    start = perf_counter()
    for i, line in enumerate(text.split("\n")):
        if i:
            await press(tab, "Enter", modifiers=SHIFT)
        for char in line:
            await tab.send(uc.cdp.input_.insert_text(text=char))
            await asyncio.sleep(random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX))
    log.debug("Texto digitado", chars=len(text), ms=elapsed_ms(start))
