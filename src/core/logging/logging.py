import sys

from loguru import logger
from core.env import env
from core.logging import log_to_telegram_bot


def configure_logging() -> None:
    logger.remove(0)

    logger.add(sink=sys.stderr)

    logger.add(sink='logs.log', rotation='500 MB')

    logger.add(sink=log_to_telegram_bot, format=env.TELEGRAM_LOGGER_FORMAT)
