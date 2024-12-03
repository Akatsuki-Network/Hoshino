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

async def send_as_document(client, chat_id, content, file_name="output.txt"):
    with io.BytesIO(str.encode(content)) as out_file:
        out_file.name = file_name
        await client.send_document(chat_id, out_file)

@Client.on_inline_query()
async def handle_inline(client: Client, inline_query: InlineQuery):
    query = inline_query.query

    if query.startswith("py "):
        code = query[3:].strip()
        await execute_code(client, inline_query, code)

    elif query.startswith("sh "):
        command = query[3:].strip()
        await execute_shell(client, inline_query, command)

async def execute_code(client, inline_query: InlineQuery, code: str):
    start = datetime.now()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        exec(code)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = exc or stderr or stdout or "Success"
    end = datetime.now()
    ping = (end - start).microseconds / 1000

    if len(evaluation) > 4096:
        await send_as_document(client, inline_query.from_user.id, evaluation, "evaluation.txt")
    else:
        result = InlineQueryResultArticle(
            title="Execution Result",
            description=f"Executed in {ping} ms",
            input_message_content=InputTextMessageContent(
                f"<b>📎 Input:</b>\n<code>{code}</code>\n\n"
                f"<b>📒 Output:</b>\n<code>{evaluation.strip()}</code>\n\n"
                f"<b>✨ Time:</b> {ping}ms",
                parse_mode=ParseMode.HTML,
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Retry", switch_inline_query_current_chat="py ")]]
            ),
        )
        await inline_query.answer([result], is_personal=True, cache_time=0)

async def execute_shell(client, inline_query: InlineQuery, command: str):
    start = datetime.now()

    try:
        process = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = process.stdout
        stderr = process.stderr
        result = stderr if stderr else stdout
    except Exception as e:
        result = str(e)

    end = datetime.now()
    ping = (end - start).microseconds / 1000

    if len(result) > 4096:
        await send_as_document(client, inline_query.from_user.id, result, "shell_output.txt")
    else:
        inline_result = InlineQueryResultArticle(
            title="Shell Execution Result",
            description=f"Executed in {ping} ms",
            input_message_content=InputTextMessageContent(
                f"<b>📎 Command:</b>\n<code>{command}</code>\n\n"
                f"<b>📒 Output:</b>\n<code>{result.strip()}</code>\n\n"
                f"<b>✨ Time:</b> {ping}ms",
                parse_mode=ParseMode.HTML,
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Retry", switch_inline_query_current_chat="sh ")]]
            ),
        )
        await inline_query.answer([inline_result], is_personal=True, cache_time=0)

@Client.on_message()
async def eval_command(client: Client, m: Message):
    if m.text and m.text.startswith("/eval"):
        code = m.text[5:].strip()
        try:
            result = eval(code)
            await m.reply_text(f"<b>📒 Output:</b>\n<code>{result}</code>", parse_mode=ParseMode.HTML)
        except Exception as e:
            await m.reply_text(f"<b>Error:</b>\n<code>{e}</code>", parse_mode=ParseMode.HTML)

@Client.on_message()
async def sh_command(client: Client, m: Message):
    if m.text and m.text.startswith("/sh"):
        command = m.text[4:].strip()
        try:
            process = subprocess.run(
                command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout = process.stdout
            stderr = process.stderr
            result = stderr if stderr else stdout

            if len(result) > 4096:
                await send_as_document(client, m.chat.id, result, "command_output.txt")
            else:
                await m.reply_text(f"<b>📒 Output:</b>\n<code>{result}</code>", parse_mode=ParseMode.HTML)
        except Exception as e:
            await m.reply_text(f"<b>Error:</b>\n<code>{e}</code>", parse_mode=ParseMode.HTML)

__HELP__ = "INLINE"
__MODULE__ = "INLINE"
