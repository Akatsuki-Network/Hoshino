from pyrogram import filters, Client
from pyrogram.types import Message
import json

__MODULE__ = "json"
__HELP__ = "Send the JSON representation of a message or the replied-to message."

@Client.on_message(filters.command("json"))
async def json_command(client, message: Message):
    msg = message.reply_to_message if message.reply_to_message else message
    json_data = json.dumps(msg, indent=4, default=str)
    await message.reply_text(f"```{json_data}```", parse_mode="Markdown")
