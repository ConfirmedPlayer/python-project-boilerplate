import asyncio
import sys
from typing import Any

from aiogram.exceptions import TelegramRetryAfter
from loguru import logger

from core.config import logger_bot
from core.env import env

lock = asyncio.Lock()


async def send_message_to_admins_chat(text: str) -> None:
    async with lock:
        try:
            await logger_bot.send_message(
                chat_id=env.TELEGRAM_LOGGING_CHAT_ID, text=text
            )
        except TelegramRetryAfter as _ex:
            await asyncio.sleep(_ex.retry_after + 1)
            await logger_bot.send_message(
                chat_id=env.TELEGRAM_LOGGING_CHAT_ID, text=text
            )


async def log_to_telegram_bot(
    log: Any | str, msg_length_limit: int = 4096
) -> None:
    """
    sink for loguru
    """

    log_length = len(log)
    if log_length > msg_length_limit:
        messages = (
            log[i : i + msg_length_limit]
            for i in range(log_length, msg_length_limit)
        )
        for message in messages:
            await send_message_to_admins_chat(message)
    else:
        await send_message_to_admins_chat(log)


def configure_logging() -> None:
    logger.remove(0)

    logger.add(sink=sys.stderr)

    logger.add(sink='logs.log', rotation='500 MB')

    logger.add(sink=log_to_telegram_bot, format=env.TELEGRAM_LOGGER_FORMAT)
