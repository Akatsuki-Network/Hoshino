from Hoshino.helpers.pdecorators import command
from pyrogram import Client, filters, types as t, enums

@Client.on_message(filters.command(["start", "help", "repo", "source"]))
async def start(_: Client, m: t.Message):
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

