import logging
import sys
import traceback
from pyrogram import Client
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from Helpo import Helpo
from config import BOT_TOKEN, API_ID, API_HASH, CHAT_ID
import asyncio
from functools import wraps

logging.basicConfig(
    format="%(asctime)s - [HOSHINO] - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)

hoshi = logging.getLogger(__name__)

ptbhoshi = Application.builder().token(BOT_TOKEN).build()
pyrohoshi = Client(name="AiHoshi", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Hoshino"))

custom_texts = {
    "help_menu_title": "**🛠 Custom Help Menu**",
    "help_menu_intro": "Available modules ({count}):\n{modules}\n\nTap on a module to explore.",
    "module_help_title": "**🔍 Details for {module_name} Module**",
    "module_help_intro": "Description:\n{help_text}",
    "no_modules_loaded": "⚠️ No modules available at the moment.",
    "back_button": "◀️ Go Back",
    "prev_button": "⬅️ Previous Page",
    "next_button": "➡️ Next Page",
    "support_button": "💬 Contact Support",
    "support_url": "https://t.me/YourSupportBot",
}

pagination = Helpo(
    client=pyrohoshi,
    modules_path="Hoshino/plugins",
    buttons_per_page=15,
    texts=custom_texts,
)

class TelegramLogHandler(logging.Handler):
    def __init__(self, chat_id, client: Client):
        super().__init__()
        self.chat_id = chat_id
        self.client = client

    def emit(self, record):
        if record.levelno < logging.WARNING:
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(self._async_emit(record))
        else:
            loop.create_task(self._async_emit(record))

    async def _async_emit(self, record):
        try:
            log_entry = self.format(record)
            await self.client.send_message(chat_id=self.chat_id, text=f"`{log_entry}`")
        except Exception as e:
            hoshi.error(f"Failed to send log to Telegram: {e}")

def setup_telegram_logging():
    telegram_handler = TelegramLogHandler(chat_id=CHAT_ID, client=pyrohoshi)
    telegram_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - [HOSHINO] - %(levelname)s - %(name)s - %(message)s")
    telegram_handler.setFormatter(formatter)
    hoshi.addHandler(telegram_handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    hoshi.critical(f"Unhandled exception:\n{trace}")
    error_feedback = split_limits(trace)
    for x in error_feedback:
        pyrohoshi.send_message(CHAT_ID, f"**Unhandled Exception**: `{x}`")

sys.excepthook = handle_exception

hoshi.info("Application initialized. Logging is active for warnings and above.")


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb,
            )
            error_feedback = split_limits(
                '**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n'.format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    ''.join(errors),
                ),
            )
            for x in error_feedback:
                await pyrohoshi.send_message(
                    CHAT_ID,
                    x
                )
            raise err
    return capture

def split_limits(text):
    if len(text) < 2048:
        return [text]
    lines = text.splitlines(True)
    small_msg = ''
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    result.append(small_msg)
    return result
