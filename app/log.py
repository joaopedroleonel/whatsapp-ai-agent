import logging
import os
import re
import secrets
import sys
from contextlib import contextmanager
from contextvars import ContextVar
from time import perf_counter

from config import LOG_LEVEL

LOGGING_KWARGS = {"exc_info", "stack_info", "stacklevel", "extra"}
LEVEL_COLORS = {"DEBUG": "\033[90m", "INFO": "\033[32m", "WARNING": "\033[33m", "ERROR": "\033[31m", "CRITICAL": "\033[1;31m"}
DIM = "\033[2m"
RESET = "\033[0m"

_chat = ContextVar("chat", default=None)


class FieldsAdapter(logging.LoggerAdapter):
    """Aceita campos como kwargs: log.info("Conversa aberta", tabs=3, ms=812)."""

    def process(self, msg, kwargs):
        fields = {**(_chat.get() or {}), **{k: kwargs.pop(k) for k in list(kwargs) if k not in LOGGING_KWARGS}}
        kwargs["extra"] = {**kwargs.get("extra", {}), "fields": {k: v for k, v in fields.items() if v is not None}}
        return msg, kwargs


class ConsoleFormatter(logging.Formatter):
    def __init__(self, color):
        super().__init__(datefmt="%Y-%m-%d %H:%M:%S")
        self.color = color

    def paint(self, text, code):
        return f"{code}{text}{RESET}" if self.color and code else text

    def format(self, record):
        level = self.paint(f"{record.levelname:<7}", LEVEL_COLORS.get(record.levelname))
        name = record.name.removeprefix("agent.")
        line = f"{self.formatTime(record, self.datefmt)} {level} {name:<12} {record.getMessage():<24}"
        fields = " ".join(f"{k}={format_value(v)}" for k, v in getattr(record, "fields", {}).items())
        if fields:
            line += " " + self.paint(fields, DIM)
        line = line.rstrip()
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line


def format_value(value):
    text = ", ".join(map(str, value)) if isinstance(value, (list, tuple)) else str(value)
    if text and not re.search(r'[\s"=]', text):
        return text
    return '"' + text.replace('"', '\\"').replace("\r", "\\r").replace("\n", "\\n") + '"'


def enable_windows_ansi():
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-12)  # STD_ERROR_HANDLE
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    except Exception:
        return False


def use_color(stream):
    if os.getenv("NO_COLOR") or not stream.isatty():
        return False
    return sys.platform != "win32" or enable_windows_ansi()


def setup_logging():
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ConsoleFormatter(use_color(sys.stderr)))
    # Bibliotecas (httpx, nodriver...) só aparecem a partir de WARNING; o app segue o LOG_LEVEL
    logging.basicConfig(level=logging.WARNING, handlers=[handler], force=True)
    logging.getLogger("agent").setLevel(LOG_LEVEL)


def get_logger(name):
    return FieldsAdapter(logging.getLogger(f"agent.{name}"), None)


@contextmanager
def chat_context(name):
    """Adiciona chat e id do atendimento em todos os logs emitidos dentro do bloco."""
    token = _chat.set({"chat": name, "id": secrets.token_hex(2)})
    try:
        yield
    finally:
        _chat.reset(token)


def elapsed_ms(start):
    return round((perf_counter() - start) * 1000)
