import sqlite3
from databases.general_methods import cur_exe

connector_rudn_db = sqlite3.connect(r"databases/schedule_database_dir/rudn_database.py")


def connect_schedule_database():
    if connector_rudn_db:
        print("Schedule database is connected")
    else:
        raise ConnectionError("Schedule database is not connected")


def get_schedule(values: list):
    keys = ["Preparation", "Faculties", "Course", "form_study", "groups"]

    db_dict = dict()
    for key, value in zip(keys, values):
        db_dict[key] = value

    print(db_dict)
    # cur_exe("""SELECT * FROM """, connect)


def select_notes(command):
    my_list = [i for i in cur_exe(command, connector_rudn_db)]
    print(my_list)
