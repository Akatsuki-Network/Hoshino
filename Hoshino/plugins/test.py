from pyrogram import Client, filters, types as t
from Hoshino.helpers.pdecorators import command 


@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hi Pyro")


@command("pstart")
async def pstart(update, context):
    await update.message.reply_text("Hi PTB")


__MODULE__ = "START"

__HELP__ = "HI"

