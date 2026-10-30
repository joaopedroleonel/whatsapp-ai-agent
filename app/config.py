import json
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


def optional(name, default):
    return os.getenv(name, "").strip() or default


AI_BASE_URL = require("AI_BASE_URL")
AI_MODEL = require("AI_MODEL")
AI_API_KEY = optional("AI_API_KEY", "none")
AI_TEMPERATURE = float(optional("AI_TEMPERATURE", "0.2"))
AI_MAX_TOKENS = int(optional("AI_MAX_TOKENS", "256"))
AI_TIMEOUT = float(optional("AI_TIMEOUT", "60"))
AI_EXTRA_BODY = json.loads(optional("AI_EXTRA_BODY", "{}"))
AI_HISTORY = optional("AI_HISTORY", "true").lower() in ("true", "1", "yes", "sim")

WHATSAPP_URL = optional("WHATSAPP_URL", "https://web.whatsapp.com")
BROWSER_PROFILE_DIR = ROOT / optional("BROWSER_PROFILE_DIR", "app/browser-profile")
BROWSER_PATH = optional("BROWSER_PATH", None)
if BROWSER_PATH and not Path(BROWSER_PATH).is_file():
    raise SystemExit(f"Navegador não encontrado em BROWSER_PATH: {BROWSER_PATH}")
LOGIN_TIMEOUT = float(optional("LOGIN_TIMEOUT", "300"))
CHECK_INTERVAL = float(optional("CHECK_INTERVAL", "5"))
OPEN_TIMEOUT = float(optional("OPEN_TIMEOUT", "5"))
SEND_WAIT = float(optional("SEND_WAIT", "2"))
SENDER_NAME = optional("SENDER_NAME", "")
MAX_TABS = int(optional("MAX_TABS", "60"))
MAX_ARROWS = int(optional("MAX_ARROWS", "50"))
KEY_DELAY_MIN = float(optional("KEY_DELAY_MIN", "0.25"))
KEY_DELAY_MAX = float(optional("KEY_DELAY_MAX", "0.6"))
TYPING_DELAY_MIN = float(optional("TYPING_DELAY_MIN", "0.03"))
TYPING_DELAY_MAX = float(optional("TYPING_DELAY_MAX", "0.1"))
