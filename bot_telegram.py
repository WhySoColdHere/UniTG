from create_bot import dp
from aiogram.utils import executor
from databases.online_database_dir import online_database
from databases.schedule_database_dir import rudn_database
from databases.client_schedule_database_dir import client_schedule_database
from handlers import user_handlers


async def on_startup(_):
    online_database.connect_online_database()
    rudn_database.connect_schedule_database()
    client_schedule_database.connect_client_schedule_database()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# Онлайн
