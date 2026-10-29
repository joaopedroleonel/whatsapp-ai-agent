import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")


def require(name):
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Faltando {name} no .env (veja o .env.example)")
    return value


WHATSAPP_URL = require("WHATSAPP_URL")
CHROME_PROFILE_DIR = ROOT / require("CHROME_PROFILE_DIR")
LOGIN_TIMEOUT = float(require("LOGIN_TIMEOUT"))
CHECK_INTERVAL = float(require("CHECK_INTERVAL"))
OPEN_TIMEOUT = float(require("OPEN_TIMEOUT"))
SEND_WAIT = float(require("SEND_WAIT"))
MAX_TABS = int(require("MAX_TABS"))
MAX_ARROWS = int(require("MAX_ARROWS"))
KEY_DELAY_MIN = float(require("KEY_DELAY_MIN"))
KEY_DELAY_MAX = float(require("KEY_DELAY_MAX"))
TYPING_DELAY_MIN = float(require("TYPING_DELAY_MIN"))
TYPING_DELAY_MAX = float(require("TYPING_DELAY_MAX"))
OLLAMA_HOST = require("OLLAMA_HOST")
OLLAMA_MODEL = require("OLLAMA_MODEL")
OLLAMA_TEMPERATURE = float(require("OLLAMA_TEMPERATURE"))
OLLAMA_NUM_CTX = int(require("OLLAMA_NUM_CTX"))
OLLAMA_NUM_BATCH = int(require("OLLAMA_NUM_BATCH"))
OLLAMA_NUM_PREDICT = int(require("OLLAMA_NUM_PREDICT"))
OLLAMA_KEEP_ALIVE = require("OLLAMA_KEEP_ALIVE")
if OLLAMA_KEEP_ALIVE.lstrip("-").isdigit():
    OLLAMA_KEEP_ALIVE = int(OLLAMA_KEEP_ALIVE)
