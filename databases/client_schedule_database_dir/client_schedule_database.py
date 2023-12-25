import sqlite3
from databases.general_methods import cur_exe, cur_exe_return

connector_client_schedule_db = sqlite3.connect(r"databases/client_schedule_database_dir/ClientSchedule.db")

MAX_SCHEDULES_COUNT = 3
DAYS_OF_WEEK = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]


# connector_online_db = sqlite3.connect(r"ClientSchedule.db")
# cur_exe("""DROP TABLE IF EXISTS Schedules""", connector_online_db)

def connect_client_schedule_database():
    if connector_client_schedule_db:
        print("Client schedule is connected")
        cur_exe("""
            CREATE TABLE IF NOT EXISTS Schedules (
            telegram_id TEXT NOT NULL,
            cl_schedule_name TEXT NOT NULL,
            cl_institute TEXT NOT NULL,
            cl_preparation_level TEXT NOT NULL,
            cl_course TEXT NOT NULL,
            cl_education_form TEXT NOT NULL,
            cl_group TEXT NOT NULL
            )
            """, connector_client_schedule_db)
    else:
        raise ConnectionError("Client schedule database is not connected")


def insert_into_client_db(telegram_id_value, schedule_name, schedule: list):
    if len([i for i in cur_exe_return(f"""SELECT telegram_id FROM Schedules 
    WHERE telegram_id == '{telegram_id_value}'""", connector_client_schedule_db)]) >= MAX_SCHEDULES_COUNT:
        return f"У вас уже создано максимальное количество расписаний ({MAX_SCHEDULES_COUNT})."

    if len([i for i in cur_exe_return(f"""SELECT telegram_id FROM Schedules 
        WHERE telegram_id == '{telegram_id_value}' AND cl_schedule_name == '{schedule_name}'""",
                                      connector_client_schedule_db)]) > 0:
        return "У вас уже существует расписание с таким названием."

    if schedule_name[0] == '/':
        return "Название расписания не может начинаться с символа '/'."

    cur_exe(f"""INSERT INTO Schedules (telegram_id, cl_schedule_name, cl_institute, cl_preparation_level, cl_course, cl_education_form, cl_group)
     VALUES ('{telegram_id_value}', '{schedule_name}', '{schedule[0]}', '{schedule[1]}', '{schedule[2]}', '{schedule[3]}', '{schedule[4]}')""",
            connector_client_schedule_db)
    return "Расписание успешно создано."


def get_client_schedule_names(telegram_id_value):
    # Именно благодаря get_client_schedule_names(...) нам выводятся название расписаний пользователя, ее трогать нельзя!
    client_schedule = [i for i in
                       cur_exe_return(f"""SELECT * FROM Schedules WHERE telegram_id == '{telegram_id_value}'""",
                                      connector_client_schedule_db)]
    schedule_names = [i[1] for i in client_schedule]

    if len(client_schedule) > 0:
        client_schedule_dict = dict()
        for key, value in zip(schedule_names, client_schedule):
            client_schedule_dict[key] = value
        return client_schedule_dict
    return None


def get_client_schedule_week_days(schedule):
    # Эта функция будет выводить непосредственно расписание группы на чет. и нечет. недели.
    keys = ["telegram_id", "schedule_name", "preparation_id", "institute_id", "course_id",
            "education_form_id", "group_name"]
    main_schedule = dict()

    for key, value in zip(keys, schedule):
        main_schedule[key] = value

    return {"schedule": main_schedule}


def delete_client_schedule(telegram_id_value, schedule_name):
    cur_exe(f"""DELETE FROM Schedules
    WHERE telegram_id == '{telegram_id_value}' AND cl_schedule_name == '{schedule_name}'""",
            connector_client_schedule_db)
