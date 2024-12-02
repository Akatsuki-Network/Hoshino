import io
import sys
import traceback
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

@Client.on_inline_query()
async def handle_inline_python(client: Client, inline_query: InlineQuery):
    query = inline_query.query

    if query.startswith("py "):
        code = query[3:].strip()
        start = datetime.now()

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None

        try:
            exec(code)
        except Exception as e:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"

        end = datetime.now()
        ping = (end - start).microseconds / 1000

        if len(evaluation) > 4096:
            with io.BytesIO(str.encode(evaluation)) as out_file:
                out_file.name = "evaluation.txt"
                result = InlineQueryResultArticle(
                    title="Execution Result (File)",
                    description="Result is too long to display.",
                    input_message_content=InputTextMessageContent(
                        "The result of your code execution is too large to display inline. Please download the file."
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Retry", switch_inline_query_current_chat="py ")]]
                    ),
                )
                results = [result]
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
            results = [result]

        await inline_query.answer(
            results=results,
            is_personal=True,
            cache_time=0,
            )


__HELP__ = "INLINE"
__MODULE__ = "INLINE"
