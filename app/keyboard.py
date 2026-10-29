import asyncio
import random

import nodriver as uc

from config import KEY_DELAY_MAX, KEY_DELAY_MIN

KEYS = {
    "Tab": ("Tab", 9, None),
    "Enter": ("Enter", 13, "\r"),
    "Escape": ("Escape", 27, None),
    "ArrowUp": ("ArrowUp", 38, None),
    "ArrowDown": ("ArrowDown", 40, None),
}


async def press(tab, key, times=1):
    code, vk, text = KEYS[key]
    for _ in range(times):
        for type_ in ("keyDown", "keyUp"):
            await tab.send(uc.cdp.input_.dispatch_key_event(
                type_=type_, key=key, code=code, windows_virtual_key_code=vk,
                text=text if type_ == "keyDown" else None,
            ))
        await asyncio.sleep(random.uniform(KEY_DELAY_MIN, KEY_DELAY_MAX))
