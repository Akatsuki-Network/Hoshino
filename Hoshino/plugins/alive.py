import random

from pyrogram import __version__ as pgram
from telegram import __version__ as tgram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Hoshino.helpers.pdecorators import command

photu = [
    "https://storage.codesman.tech/file/tikge",
    "https://storage.codesman.tech/file/rmurv",
]


@command("alive")
async def jinda(update, context):
    user = update.effective_user
    bot = context.bot

    text = (
        f"**ʜᴇʏ [{user.first_name}](tg://user?id={user.id}),**\n\n"
        f"ɪ ᴀᴍ {bot.first_name}\n━━━━━━━━━━━━━━━━━━━\n\n"
        f"» **ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [NITRO](https://t.me/BEINGCAT)** \n\n"
        f"» **ᴘʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `{tgram}` \n\n"
        f"» **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pgram}` \n━━━━━━━━━━━━━━━━━\n\n"
    )

    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ʜᴇʟᴘ", url=f"https://t.me/{bot.username}?start=help"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/Akatsuki_x_bot_support"),
            ]
        ]
    )

    ran = random.choice(photu)

    await bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=ran,
        caption=text,
        parse_mode="Markdown",
        reply_markup=button,
    )

__MODULE__ = "Aʟɪᴠᴇ"

__HELP__ = """

• `/alive` - ᴛᴏ ᴄʜᴇᴄᴋ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ɴᴏᴛ

"""
