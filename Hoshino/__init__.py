import logging
from pyrogram import Client
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from Helpo import Helpo
from config import BOT_TOKEN, API_ID, API_HASH, CHAT_ID

logging.basicConfig(
    format="%(asctime)s - [HOSHINO] - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
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

print(f"Helpo Initialized with Modules: {', '.join(pagination.modules.keys())}")


class TelegramLogHandler(logging.Handler):
    def __init__(self, chat_id, client: Client):
        super().__init__()
        self.chat_id = chat_id
        self.client = client

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.client.send_message(chat_id=self.chat_id, text=f"`{log_entry}`")
        except Exception as e:
            hoshi.error(f"Failed to send log to Telegram: {e}")

CHAT_ID = 123456789
telegram_handler = TelegramLogHandler(chat_id=CHAT_ID, client=pyrohoshi)
telegram_handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - [HOSHINO] - %(levelname)s - %(name)s - %(message)s")
telegram_handler.setFormatter(formatter)
hoshi.addHandler(telegram_handler)
