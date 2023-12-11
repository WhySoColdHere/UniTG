"""В этом файле мы считыем занятия с lessons.txt и заполняем дб"""
import sqlite3 as sq
from time import sleep
def db_complect():
    time_count = 1
    error_list = []
    with open("lesson.txt","r",encoding="utf-8") as file:
        with sq.connect("rudn.db") as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM days_of_the_week""")
            all_days = cur.fetchall()
            while True:
                line = file.readline()
                if not line:
                    break
                line = str_trans(line)
                print(line)
                cur.execute(f"""
                    SELECT id_row FROM time_lessons WHERE Name =="{line[0]}"
                    """)
                result = cur.fetchall()
                id_time = result[0][0]
                name_lesson = line[1]
                id_type = type_trasformation(line[2])
                teacher = line[3]
                office = line[4]
                id_day_week = day_trasformation(line[5],all_days)
                id_week = id_week_transformation(line[6])
                name_group = line[7]
                cur.execute(f"""
                SELECT id_row FROM groups WHERE Name =="{line[7]}"
                """)
                id_group_result = cur.fetchall()
                if len(id_group_result) == 0:
                    time_count = time_count + 1
                    error_list.append(time_count)
                    continue
                cur.execute(f"""
                INSERT INTO lessons(Name_lesson,id_time_numbers,Office,id_day_week,id_week,id_type,teacher,group_name,id_group)
                VALUES('{name_lesson}',{id_time},'{office}',{id_day_week},{id_week},{id_type},'{teacher}',"{name_group}",{id_group_result[0][0]})""")
                print(f"{time_count}/28367")

                time_count += 1
    for i in error_list:
        print(i)

#крч ошибка в 1855 строке, надо поставить принт списка
#id_group_result = cur.fetchall()[0][0]
#IndexError: list index out of range
#['13:30 - 14:50', 'Цитология, гистология и эмбриология', 'Лабораторная работа', 'Понедельник', 'нижняя', 'СВТсд-04-21', 83]
#['12:00 - 13:20', 'Цитология', 'гистология и эмбриология', 'Лабораторная работа', 'Понедельник', 'нижняя', 'СВТсд-04-21', '83']
#['13:30 - 14:50', 'Цитология', 'гистология и эмбриология', 'Лабораторная работа', 'Понедельник', 'верхняя', 'СВТсд-04-21', '83']
def type_trasformation(str_type):
    if str_type == "Лекция":
        return 1
    elif str_type == "Практические и другие":
        return 2
    elif str_type == "Лабораторная работа":
        return 3
    elif str_type == "Семинар":
        return 4

def day_trasformation(str_day,db_list_day):
    for i in range(0,len(db_list_day)):
        if db_list_day[i][1] == str_day:
            return db_list_day[i][0]
def id_week_transformation(str_week):
    if str_week == "верхняя":
        return 2
    elif str_week == "нижняя":
        return 1

def str_trans(s):
    a = []
    s = s.replace('[',"")
    s = s.replace(']',"")
    s = s.replace("'",'')
    s = s.split(",")
    s = [i.strip() for i in s]
    print(s)
    if len(s) == 10:
        s[1] = s[1] + s[2]
        s.remove(s[2])
    if len(s) == 8:
        s[1] = s[1] + s[2]
        s.remove(s[2])
    if len(s) == 11:
        s[1] = s[1] + s[2] + s[3]
        s.remove(s[3])
        s.remove(s[2])
    if s[1] == "Histology":
        s[1] = s[1] + s[2] + s[3]
        s.remove(s[3])
        s.remove(s[2])
    if len(s) < 9:
        count = 0
        for i in range(0,9):
            if i == 3 or i == 4:
                a.append("NULL")
                continue
            a.append(s[count])
            count = count + 1
    else:
        a = s
    a[0] = a[0].replace(" ",'')
    # if len(a) == 10:
    #     a[1] = a[1] + a[2]
    #     a.remove(a[2])
    return a
#['16:30 - 17:50', 'Акушерство', 'гинекология и андрология', 'Лабораторная работа', 'Понедельник', 'верхняя', 'СВТсв-01-20', '92']
#['16:30-17:50', 'Акушерство', 'гинекология и андрология', 'NULL', 'NULL', 'Лабораторная работа', 'Понедельник', 'верхняя', 'СВТсв-01-20']
#['10:30 - 11:50', 'Organization of Special Care for Patients', 'Лабораторная работа', 'Среда', 'нижняя', 'МЛДсд-56-22', '755'] 7
#['19:30 - 20:50', 'Histology', 'Embryology', 'Cytology - Oral Histology', 'Лекция', 'Среда', 'верхняя', 'МСЯсд-51-22', '776'] 9

def main():
    db_complect()


if __name__ == "__main__":
    main()