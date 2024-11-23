from pyrogram import Client as app
from pyrogram import filters
from pyrogram.types import ForceReply, InlineKeyboardMarkup, InlineKeyboardButton

OWNER_ID = 6312693124

@app.on_message(filters.command("contact"))
async def contact(_, message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Chat With Creator", callback_data="live_chat")]])
    await message.reply_text("Click this button to contact my creator", reply_markup=keyboard)

@app.on_callback_query(filters.regex("live_chat"))
async def live_chat(_, query):
    await query.message.delete()
    string = """TO CONTACT MY CREATOR, JUST REPLY TO THIS MESSAGE"""
    await query.message.reply_text(text=string, reply_markup=ForceReply(True))

@app.on_message(filters.reply & filters.private)
async def live_chat_forward(_, message):
    reply = message.reply_to_message
    if reply and reply.reply_markup and isinstance(reply.reply_markup, ForceReply):
        await message.forward(chat_id=OWNER_ID) # put your id here if need
        await message.reply_text("Message successfully sent to my creator. ✅")
        await reply.delete()


__MODULE__ = "chat"

__HELP__ = "KELA"
