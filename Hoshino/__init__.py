import logging
from pyrogram import Client
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from Helpo import Helpo
from config import BOT_TOKEN, API_ID, API_HASH

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
