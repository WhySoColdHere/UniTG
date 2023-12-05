import sqlite3
from databases.general_methods import cur_exe, cur_exe_return

connector_online_db = sqlite3.connect(r"databases/client_schedule_database_dir/ClientSchedule.db")


# connector_online_db = sqlite3.connect(r"ClientSchedule.db")
# cur_exe("""DROP TABLE IF EXISTS Schedules""", connector_online_db)

def connect_client_schedule_database():
    if connector_online_db:
        print("Client schedule is connected")
        cur_exe("""
            CREATE TABLE IF NOT EXISTS Schedules (
            telegram_id TEXT NOT NULL,
            cl_institute TEXT NOT NULL,
            cl_preparation_level TEXT NOT NULL,
            cl_course TEXT NOT NULL,
            cl_education_form TEXT NOT NULL,
            cl_group TEXT NOT NULL
            )
            """, connector_online_db)
    else:
        raise ConnectionError("Client schedule database is not connected")


def insert_into_client_db(telegram_id_value, schedule: list):
    cur_exe(f"""INSERT INTO Schedules (telegram_id, cl_institute, cl_preparation_level, cl_course, cl_education_form, cl_group)
     VALUES ('{telegram_id_value}', '{schedule[0]}', '{schedule[1]}', '{schedule[2]}', '{schedule[3]}', '{schedule[4]}')""",
            connector_online_db)


def get_client_schedule(telegram_id_value):
    client_schedule = [i for i in
                       cur_exe_return(f"""SELECT * FROM Schedules WHERE telegram_id == '{telegram_id_value}'""",
                                      connector_online_db)]
    return client_schedule if len(client_schedule) > 0 else "You're schedule does not exist"
