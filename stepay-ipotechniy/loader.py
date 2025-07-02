from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

__all__ = ['bot', 'dp']
