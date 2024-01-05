import sqlite3
from databases.general_methods import cur_exe_return

connector_rudn_db = sqlite3.connect(r"databases/schedule_database_dir/rudn.db")


def connect_schedule_database():
    if connector_rudn_db:
        print("Schedule database is connected")
    else:
        raise ConnectionError("Schedule database is not connected")


# Большой-большой костыль.
def get_institutes_names(name):
    try:
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
    except IndexError:
        return "Произошла ошибка. Скорее всего, были введены некорректные данные."


##################

def get_courses_names(name, nodes: dict):
    try:
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
    except IndexError:
        return "Произошла ошибка. Скорее всего, были введены некорректные данные."


##################
def get_education_forms_names(name, nodes: dict):
    try:
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
    except IndexError:
        return "Произошла ошибка. Скорее всего, были введены некорректные данные."


##################
def get_groups_names(name, nodes: dict):
    try:
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
    except IndexError:
        return "Произошла ошибка. Скорее всего, были введены некорректные данные."


def get_week_objects(week_cur_day, week_id, day, group_name):
    week_objects_list = list()
    for i in range(0, len(week_cur_day)):
        week_object = dict()
        week_object['name'] = week_cur_day[i][0]
        my_time = list(cur_exe_return(f"""SELECT Name, account_number FROM time_lessons
                                                            WHERE id_row == {week_cur_day[i][1]}""",
                                      connector_rudn_db))[0]
        week_object['time'] = my_time[0]
        week_object['lesson_number'] = my_time[1]
        week_object['office'] = week_cur_day[i][2]
        week_object['week_type'] = list(cur_exe_return(f"""SELECT numbers FROM week_numbers 
                                                                WHERE row_id == {week_id}""", connector_rudn_db))[0][0]
        week_object['lesson_type'] = list(cur_exe_return(f"""SELECT Name FROM type_lessons
                                                                  WHERE id_row == {week_cur_day[i][5]}""",
                                                         connector_rudn_db))[0][0]
        week_object['teacher'] = week_cur_day[i][6]
        week_object['day'] = day
        week_object['group_name'] = group_name

        for key, value in zip(week_object.keys(), week_object.values()):
            week_object[key] = 'Сам(a) думай' if value == "NULL" else value

        week_objects_list.append(week_object)
    return week_objects_list


def get_client_schedule_from_rudn(schedule, day_of_week):
    day_of_week_raw_dict = {"Пн": "Понедельник", "Вт": "Вторник", "Ср": "Среда", "Чт": "Четверг", "Пт": "Пятница",
                            "Сб": "Суббота"}

    day_of_week_id = int(list(
        cur_exe_return(f"""SELECT id_row FROM days_of_the_week WHERE Name == '{day_of_week_raw_dict[day_of_week]}'""",
                       connector_rudn_db))[0][0])

    upper_week_id = 2
    lower_week_id = 1

    lessons_all_weeks_cur_day = list(cur_exe_return(f"""SELECT * FROM lessons
                                WHERE group_name == '{schedule['group_name']}'
                                AND id_day_week == {day_of_week_id}""",
                                                    connector_rudn_db))

    lessons_upper_week_cur_day = [i[1:] for i in lessons_all_weeks_cur_day if i[5] == upper_week_id]
    lessons_lower_week_cur_day = [i[1:] for i in lessons_all_weeks_cur_day if i[5] == lower_week_id]

    upper_week_objects = get_week_objects(lessons_upper_week_cur_day, upper_week_id, day_of_week_raw_dict[day_of_week],
                                          schedule['group_name'])
    lower_week_objects = get_week_objects(lessons_lower_week_cur_day, lower_week_id, day_of_week_raw_dict[day_of_week],
                                          schedule['group_name'])

    schedule_dict = {'upper_week': upper_week_objects, 'lower_week': lower_week_objects}

    return schedule_dict
