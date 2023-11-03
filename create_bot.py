from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from token_file import token

storage = MemoryStorage()

bot = Bot(token=token)
ADMINS_CHAT_ID = -4000883833

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
