import requests
from pyrogram import filters, Client as app
from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.enums import *
from config import BOT_UNAME as BOT_USERNAME

url_nsfw = "https://api.waifu.pics/nsfw/"

@app.on_message(filters.command("cosplay"))
async def cosplay(_,msg):
    img = requests.get("https://waifu-api.vercel.app").json()
    await msg.reply_photo(img, caption=f"Cosplay By {BOT_USERNAME}")



@app.on_message(filters.command("ncosplay"))
async def ncosplay(_,msg):
    if msg.chat.type != ChatType.PRIVATE:
      await msg.reply_text("Sorry you can use this command only in private chat with bot",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Go PM",url=f"https://t.me/{BOT_USERNAME}?start=True")]
            ]
        ))
    else:
       ncosplay = requests.get("https://waifu-api.vercel.app/items/1").json()

       await msg.reply_photo(ncosplay, caption=f"Ncosplay By {BOT_USERNAME}")
      
__MODULE__ = "cosplay"

__HELP__ = "bokya"
