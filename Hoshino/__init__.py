import logging, sys 
import os
from pyrogram import Client 
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from Helpo import Helpo
from config import BOT_TOKEN, API_ID, API_HASH

# bogging
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


class pyrohoshi(Client):
    def __init__(self):
        super().__init__(
            "AiHoshi",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Hoshino.plugins"),
        ) 
        self.helpo = Helpo(
          client=self,
          modules_path="Hoshino/plugins",
          buttons_per_page=15,
          texts=custom_texts,
        )
    async def start(self):
        await super().start()
        hoshi.info("AiHoshi The Trash Bot Started Successfully")
        print("Helpo Initialized with Modules: {', '.join(self.helpo.modules.keys())}")
      
    async def stop(self):
        await super().stop()
        hoshi.info("AiHoshino The Trash Bot Is Shutdown Now")

# dhoshi = AsyncIOMotorClient(mongo_url)
