from create_bot import bot, dp
from aiogram.utils import executor
from data_base import sqlite_db
from handlers import admin_side, user_side


async def on_startup(_):
    sqlite_db.sql_start()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# Так как заполнение бд будет происходить непосредственно через интерфейс, то всю хрень с admin_side
# Возможность добавлять расписание убираем
# Возможность создания собственных групп убираем.
# Добавление новостей убираем
# Фигня с фотками не нужна.
# Расписание учителей стоит добавить.
# Подумать над системой вопросов.

