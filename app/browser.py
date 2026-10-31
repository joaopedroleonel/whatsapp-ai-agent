import json
from pathlib import Path
from time import perf_counter

import nodriver as uc

from config import BROWSER_PATH, BROWSER_PROFILE_DIR, LOGIN_TIMEOUT, WHATSAPP_URL
from log import elapsed_ms, get_logger

JS_DIR = Path(__file__).parent / "js"
CHAT_LIST_ITEM = '[data-testid="cell-frame-title"]'

log = get_logger("browser")


async def start_whatsapp():
    log.info("Abrindo navegador", navegador=BROWSER_PATH or "chrome automático", perfil=BROWSER_PROFILE_DIR)
    browser = await uc.start(user_data_dir=str(BROWSER_PROFILE_DIR), browser_executable_path=BROWSER_PATH)
    tab = await browser.get(WHATSAPP_URL)
    log.info("Aguardando o WhatsApp Web", dica="leia o QR code se for pedido", timeout_s=LOGIN_TIMEOUT)
    start = perf_counter()
    await tab.select(CHAT_LIST_ITEM, timeout=LOGIN_TIMEOUT)
    log.info("WhatsApp Web carregado", ms=elapsed_ms(start))
    return browser, tab


def load_js(name):
    return (JS_DIR / name).read_text(encoding="utf-8")


async def run_js(tab, name, **args):
    start = perf_counter()
    wrapped = f"(() => {{ const ARGS = {json.dumps(args)};\n{load_js(name)}\n}})()"
    result = await tab.evaluate(wrapped, return_by_value=True)
    if not isinstance(result, str):
        raise RuntimeError(f"Falha ao executar {name}: {result}")
    log.debug("JS executado", script=name, ms=elapsed_ms(start))
    return json.loads(result)
