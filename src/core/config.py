from aiogram import Bot
from core.env import env


logger_bot = Bot(env.TELEGRAM_LOGGING_BOT_TOKEN)
