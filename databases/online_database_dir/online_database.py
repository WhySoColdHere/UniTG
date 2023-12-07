import sqlite3
from databases.general_methods import cur_exe, cur_exe_return
from datetime import datetime

connector_online_db = sqlite3.connect(r"databases/online_database_dir/OnlineUniTG.db")
DAYS_TO_STORE = 365


# connector_online_db = sqlite3.connect(r"OnlineUniTG.db")
# cur_exe("""DROP TABLE IF EXISTS Users""", connector_online_db)

def connect_online_database():
    if connector_online_db:
        print("Online database is connected")
        cur_exe("""
            CREATE TABLE IF NOT EXISTS Users (
            telegram_id TEXT NOT NULL,
            last_usage INTEGER NOT NULL
            )
            """, connector_online_db)
    else:
        raise ConnectionError("Online database is not connected")


def get_julian_day():
    return int(list(*cur_exe_return(f"""SELECT julianday('{datetime.now().date()}')""", connector_online_db))[0])


def insert_into_online_db(telegram_id_value):
    # Удаляем все записи, хранящиеся более чем DAYS_TO_STORE дней. Начинается отчет с текущего дня.
    cur_exe(f"""DELETE FROM Users WHERE {get_julian_day() + 1} - last_usage > {DAYS_TO_STORE}""", connector_online_db)

    # Если записи, идентичной добавляемой в бд нет, то вставляем запись, все норм.
    info = [i for i in cur_exe_return(f"""
        SELECT * FROM Users WHERE telegram_id='{telegram_id_value}' AND last_usage={get_julian_day()}""",
                                      connector_online_db)]
    if len(info) == 0:
        cur_exe(f"""INSERT INTO Users (telegram_id, last_usage) VALUES ('{telegram_id_value}', {get_julian_day()})""",
                connector_online_db)
    del info


def get_online(period):
    my_set = {i for i in cur_exe_return(f"""
    SELECT telegram_id, last_usage FROM Users WHERE last_usage >= {get_julian_day() - int(period) + 1}
    """, connector_online_db)}
    return my_set
