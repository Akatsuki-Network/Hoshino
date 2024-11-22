from Hoshino import ptbhoshi
from config import Config
from telegram import ChatMemberOwner, ChatMemberAdministrator, constants, CallbackQuery
from telegram.ext import CommandHandler, MessageHandler, PrefixHandler, CallbackQueryHandler, filters
import sys
from typing import Union
from functools import wraps

PREFIX = ["/", ".", "!", "", "?", "\""]

BOT_USERNAME = Config.BOT_UNAME

def command(command, filters=None, block=False):
    def decorator(func):
        if PREFIX:
            def convert(cmd: Union[str, list]):
                if isinstance(cmd, tuple):
                    cmd = list(cmd)
                if not isinstance(cmd, (str, list)):
                    print(f"Wrong command data type detected: {cmd} and ignored!!")
                    return
                commands = [cmd] if isinstance(cmd, str) else cmd
                return [f"{c}{BOT_USERNAME}" for c in commands] + commands

            handler = PrefixHandler(
                prefix=PREFIX,
                command=convert(command),
                callback=func,
                filters=filters,
                block=block
            )
        else:
            handler = CommandHandler(
                command=command,
                callback=func,
                filters=filters,
                block=block
            )
        application.add_handler(handler)
        return func
    return decorator

def send_action(action):
    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            bot = context.bot
            chat = update.message.chat
            await bot.send_chat_action(
                chat_id=chat.id,
                action=action
            )
            return await func(update, context, *args, **kwargs)
        return command_func
    return decorator
