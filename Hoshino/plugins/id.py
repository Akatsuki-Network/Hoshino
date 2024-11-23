from pyrogram import filters, Client 
from pyrogram.types import Message


__MODULE__ = "id"
__HELP__ = "Get the ID of stickers, photos, documents, chats, channels, users, or replies."

@Client.on_message(filters.command("id"))
async def id_command(client, message: Message):
    msg = message.reply_to_message if message.reply_to_message else message
    response = []

    # User ID
    if msg.from_user:
        response.append(f"**User ID:** `{msg.from_user.id}`")

    # Chat ID
    if msg.chat:
        response.append(f"**Chat ID:** `{msg.chat.id}`")

    # Message ID
    response.append(f"**Message ID:** `{msg.id}`")

    # Sticker ID
    if msg.sticker:
        response.append(f"**Sticker ID:** `{msg.sticker.file_id}`")

    # Photo ID
    if msg.photo:
        response.append(f"**Photo ID:** `{msg.photo.file_id}`")

    # Document ID
    if msg.document:
        response.append(f"**Document ID:** `{msg.document.file_id}`")

    # Channel/Chat Username
    if msg.chat.username:
        response.append(f"**Username:** `@{msg.chat.username}`")

    # Reply-specific information
    if message.reply_to_message:
        response.append(f"**This is a reply to message ID:** `{message.reply_to_message.id}`")

    await message.reply_text("\n".join(response))
