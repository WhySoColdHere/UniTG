from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from token_file import token

storage = MemoryStorage()

bot = Bot(token=token)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
print("create_bot.py executed successfully")