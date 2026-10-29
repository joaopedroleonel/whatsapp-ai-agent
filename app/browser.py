import json
from pathlib import Path

import nodriver as uc

from config import CHROME_PROFILE_DIR, LOGIN_TIMEOUT, WHATSAPP_URL

JS_DIR = Path(__file__).parent / "js"
CHAT_LIST_ITEM = '[data-testid="cell-frame-title"]'


async def start_whatsapp():
    browser = await uc.start(user_data_dir=str(CHROME_PROFILE_DIR))
    tab = await browser.get(WHATSAPP_URL)
    print("Waiting for WhatsApp Web to load (scan the QR code if asked)...")
    await tab.select(CHAT_LIST_ITEM, timeout=LOGIN_TIMEOUT)
    return browser, tab


def load_js(name):
    return (JS_DIR / name).read_text(encoding="utf-8")


async def run_js(tab, code, **args):
    wrapped = f"(() => {{ const ARGS = {json.dumps(args)};\n{code}\n}})()"
    result = await tab.evaluate(wrapped, return_by_value=True)
    if not isinstance(result, str):
        raise RuntimeError(f"JS failed: {result}")
    return json.loads(result)
