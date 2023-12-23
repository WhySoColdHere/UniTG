import sqlite3
from databases.general_methods import cur_exe, cur_exe_return

connector_rudn_db = sqlite3.connect(r"databases/schedule_database_dir/rudn.db")


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
#    tables = ["Preparation", "Faculties", "Course", "form_study", "groups"]
#     data_id_dict = dict()
#
#     for key, current_table in zip(data, tables):
#         data_id_dict[key] = \
#             list(cur_exe_return(f"""
#             SELECT id_row FROM '{current_table}' WHERE Name = '{key}'""", connector_rudn_db))[0][0]
#
#     print(data)
#     print(data_id_dict)


# Большой-большой костыль.
def get_institutes_names(name):
    node_id = int(list(
        cur_exe_return(f"""
                SELECT id_row FROM Preparation WHERE Name = '{name}'""", connector_rudn_db))[0][0])

    names_id = list(set(
        cur_exe_return(f"""
                SELECT fakult_id FROM groups WHERE id_preparation == {node_id}""",
                       connector_rudn_db)))
    names_id = [i[0] for i in names_id]

    names = []
    for i in names_id:
        names.append(list(set(
            cur_exe_return(f"""
                        SELECT Name FROM Faculties WHERE id_row == {i}""",
                           connector_rudn_db))))
    names = [i[0][0] for i in names]

    return {"names": names, "preparation_node_id": node_id}


##################

def get_courses_names(name, nodes: dict):
    node_id = int(list(
        cur_exe_return(f"""
                SELECT id_row FROM Faculties WHERE Name = '{name}'""", connector_rudn_db))[0][0])

    names_id = list(set(
        cur_exe_return(f"""
                SELECT id_curse FROM groups WHERE fakult_id == {node_id} AND id_preparation == {nodes["preparation_node_id"]}""",
                       connector_rudn_db)))
    names_id = [i[0] for i in names_id]

    names = []
    for i in names_id:
        names.append(list(set(
            cur_exe_return(f"""
                        SELECT Name FROM Course WHERE id_row == {i}""",
                           connector_rudn_db))))
    names = sorted([i[0][0] for i in names])

    return {"names": names, "institute_node_id": node_id}


##################
def get_education_forms_names(name, nodes: dict):
    node_id = int(list(
        cur_exe_return(f"""
                SELECT id_row FROM Course WHERE Name = '{name}'""", connector_rudn_db))[0][0])

    names_id = list(set(
        cur_exe_return(f"""
                SELECT id_form_study FROM groups 
                WHERE id_curse == {node_id} AND fakult_id == {nodes["institute_node_id"]} AND id_preparation == {nodes["preparation_node_id"]}""",
                       connector_rudn_db)))
    names_id = [i[0] for i in names_id]

    names = []
    for i in names_id:
        names.append(list(set(
            cur_exe_return(f"""
                        SELECT Name FROM form_study WHERE id_row == {i}""",
                           connector_rudn_db))))
    names = [i[0][0] for i in names]

    return {"names": names, "course_node_id": node_id}


##################
def get_groups_names(name, nodes: dict):
    node_id = int(list(
        cur_exe_return(f"""
                SELECT id_row FROM form_study WHERE Name = '{name}'""", connector_rudn_db))[0][0])

    names = list(set(
        cur_exe_return(f"""
                SELECT Name FROM groups
                WHERE id_form_study == {node_id} AND id_curse == {nodes["course_node_id"]}
                 AND fakult_id == {nodes["institute_node_id"]} AND id_preparation == {nodes["preparation_node_id"]}""",
                       connector_rudn_db)))
    names = [i[0] for i in names]

    return {"names": names, "education_form_node_id": node_id}


# def get_appropriate_keyboard(name: str, table_index: int):
#     node_id = int(list(
#         cur_exe_return(f"""
#             SELECT id_row FROM '{TABLES[table_index]}' WHERE Name = '{name}'""", connector_rudn_db))[0][0])
#
#     print(node_id)
# return list(
#         *cur_exe_return(f"""
#         SELECT Name FROM '{TABLES[table_index + 1]}' WHERE id_row = {node_id}""", connector_rudn_db))
# return list(
#         *cur_exe_return(f"""
#         SELECT Name FROM '{TABLES[-1]}' WHERE id_row = {node_id}""", connector_rudn_db))

# id_form_study == {node_id} --> 1220
# id_form_study == {node_id} AND id_curse == {nodes["course_node_id"]} --> 398
# id_form_study == {node_id} AND id_curse == {nodes["course_node_id"]} AND fakult_id == {nodes["institute_node_id"]} --> 40
# id_form_study == {node_id} AND id_curse == {nodes["course_node_id"]} AND fakult_id == {nodes["institute_node_id"]}
#             AND id_preparation == {nodes["preparation_node_id"]} --> 22
