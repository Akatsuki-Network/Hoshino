from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram import enums

__MODULE__ = "json"
__HELP__ = "Send the JSON representation of a message or the replied-to message."

@Client.on_message(filters.command("json"))
async def json_command(client, message: Message):
    msg = message.reply_to_message if message.reply_to_message else message
    await message.reply_text(f"`{msg}`")
