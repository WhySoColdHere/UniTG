import sqlite3
from databases.general_methods import cur_exe, cur_exe_return

connector_rudn_db = sqlite3.connect(r"databases/schedule_database_dir/rudn.db")
TABLES = ["Preparation", "Faculties", "Course", "form_study", "groups"]


# data = ["Бакалавриат", "АТИ", "1", "Очная", "САГбд-01-23"]
# data_id_dict = dict()
# tables = ["Preparation", "Faculties", "Course", "form_study", "groups"]
# for key, current_table in zip(data, tables):
#     data_id_dict[key] = list(
#         cur_exe_return(f"""SELECT id_row FROM '{current_table}' WHERE Name = '{key}'""", connector_rudn_db))
#
# print(data_id_dict)

# print(list(cur_exe_return("""SELECT * FROM Preparation""", connector_rudn_db)))


def connect_schedule_database():
    if connector_rudn_db:
        print("Schedule database is connected")
    else:
        raise ConnectionError("Schedule database is not connected")


# def select_notes(data: list):
#     data_id_dict = dict()
#
#     for key, current_table in zip(data, TABLES):
#         data_id_dict[key] = \
#             list(cur_exe_return(f"""
#             SELECT id_row FROM '{current_table}' WHERE Name = '{key}'""", connector_rudn_db))[0][0]
#
#     print(data)
#     print(data_id_dict)


# def get_appropriate_keyboard(name: str, table_index: int):
#     node_id = int(list(
#             cur_exe_return(f"""
#             SELECT id_row FROM '{TABLES[table_index]}' WHERE Name = '{name}'""", connector_rudn_db))[0][0])

    # return list(
    #         *cur_exe_return(f"""
    #         SELECT Name FROM '{TABLES[table_index + 1]}' WHERE id_row = {node_id}""", connector_rudn_db))
    # return list(
    #         *cur_exe_return(f"""
    #         SELECT Name FROM '{TABLES[-1]}' WHERE id_row = {node_id}""", connector_rudn_db))
