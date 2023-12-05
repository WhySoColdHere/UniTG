import sqlite3
from databases.general_methods import cur_exe, cur_exe_return

connector_rudn_db = sqlite3.connect(r"databases/schedule_database_dir/rudn_database.py")


def connect_schedule_database():
    if connector_rudn_db:
        print("Schedule database is connected")
    else:
        raise ConnectionError("Schedule database is not connected")


def get_schedule(data: list):
    # Честно? Не ебу как это дело реализовывать без заполненной бд
    pass
    # temp = cur_exe_return("""SELECT * FROM Users""")


def select_notes(command):
    my_list = [i for i in cur_exe(command, connector_rudn_db)]
    print(my_list)
