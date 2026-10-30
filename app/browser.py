import json
from pathlib import Path

import nodriver as uc

from config import BROWSER_PATH, BROWSER_PROFILE_DIR, LOGIN_TIMEOUT, WHATSAPP_URL

JS_DIR = Path(__file__).parent / "js"
CHAT_LIST_ITEM = '[data-testid="cell-frame-title"]'


async def start_whatsapp():
    browser = await uc.start(user_data_dir=str(BROWSER_PROFILE_DIR), browser_executable_path=BROWSER_PATH)
    tab = await browser.get(WHATSAPP_URL)
    print("Aguardando o WhatsApp Web carregar (leia o QR code se for pedido)...")
    await tab.select(CHAT_LIST_ITEM, timeout=LOGIN_TIMEOUT)
    return browser, tab


def load_js(name):
    return (JS_DIR / name).read_text(encoding="utf-8")


async def run_js(tab, code, **args):
    wrapped = f"(() => {{ const ARGS = {json.dumps(args)};\n{code}\n}})()"
    result = await tab.evaluate(wrapped, return_by_value=True)
    if not isinstance(result, str):
        raise RuntimeError(f"Falha ao executar JS: {result}")
    return json.loads(result)
