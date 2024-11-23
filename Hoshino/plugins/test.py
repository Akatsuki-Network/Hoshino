from Hoshino.helpers.pdecorators import command
from pyrogram import Client, filters, types as t, enums
from Hoshino import pyrohoshi as bot

@Client.on_message(filters.command(["start", "help", "repo", "source"]))
async def start(_: Client, m: t.Message):
    if len(m.text.split()) > 1:
        name = m.text.split(None, 1)[1]
        if name.startswith("help"):
            await bot.show_help_menu(m.chat.id, page=1)
    else:
        await m.reply_text(
            text="under maintenance",
            reply_markup=t.InlineKeyboardMarkup(
                [[t.InlineKeyboardButton(text="Source", url="https://github.com/Akatsuki-Network/Hoshino")]]
            ),
        )

@command("pstart")
async def pstart(update, context):
    await update.message.reply_text("Hi PTB")

__MODULE__ = "START"
__HELP__ = "HI"
