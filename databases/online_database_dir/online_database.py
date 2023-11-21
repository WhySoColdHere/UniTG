import sqlite3

connect = sqlite3.connect(r"databases\online_database_dir\OnlineUniTG.db")


def connect_database():
    with connect as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT NOT NULL,
        last_usage TEXT NOT NULL
        )
        """)


def insert_into(telegram_id_value, last_usage_value):
    with connect as con:
        cur = con.cursor()
        cur.execute(
            f"""INSERT INTO Users (telegram_id, last_usage) VALUES ('{telegram_id_value}', '{last_usage_value}')""")
