from telegram import Update
from telegram.ext import ContextTypes
from config import DEV_LIST, SUDO
from functools import wraps

def devsonly(func):
    async def decorator(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.message.from_user.id
        if user_id in DEV_LIST:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("🚫 This command is restricted to developers!")
            return None
    return decorator

def sudoonly(func):
    async def decorator(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.message.from_user.id
        if user_id in (DEV_LIST + SUDO):
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("⚠️ This command is for sudo users only!")
            return None
    return decorator

def devplus(func):
    async def decorator(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.message.from_user.id
        if user_id in (DEV_LIST + SUDO):
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("🔒 Only developers and sudo users can use this command!")
            return None
    return decorator

def group_only(func):
    async def decorator(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        chat_type = update.message.chat.type
        if chat_type == 'private':
            await update.message.reply_text("🚫 This command works only in groups!")
            return None
        else:
            return await func(update, context, *args, **kwargs)
    return decorator

def private_only(func):
    async def decorator(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        chat_type = update.message.chat.type
        if chat_type != 'private':
            await update.message.reply_text("📩 This command works only in private chat!")
            return None
        else:
            return await func(update, context, *args, **kwargs)
    return decorator

def no_bot(func):
    async def decorator(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.message.reply_to_message.from_user
        is_replied = update.message.reply_to_message
        if is_replied and user.is_bot:
            await update.message.reply_text("🤖 Can't perform this action on a bot!")
            return None
        else:
            return await func(update, context, *args, **kwargs)
    return decorator
