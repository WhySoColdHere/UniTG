from create_bot import dp
from aiogram.utils import executor
from handlers import user_handlers


async def on_startup(_):
    print("Здесь должна подключаться БД")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
