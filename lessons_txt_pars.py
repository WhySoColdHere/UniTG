"""В этом файле мы считыем занятия с lessons.txt и заполняем дб"""
import sqlite3 as sq
from time import sleep
def db_complect():
    time_count = 1
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
                id_group_result = cur.fetchall()[0][0]

                cur.execute(f"""
                INSERT INTO lessons(Name_lesson,id_time_numbers,Office,id_day_week,id_week,id_type,teacher,group_name,id_group)
                VALUES("{name_lesson}",{id_time},"{office}",{id_day_week},{id_week},{id_type},"{teacher}","{name_group}",{id_group_result})""")
                print(f"{time_count}/28367")
                time_count += 1
                sleep(1)
#крч ошибка в 1855 строке, надо поставить принт списка
#id_group_result = cur.fetchall()[0][0]
#IndexError: list index out of range
#['16:30-17:50', 'Цитология', 'гистология и эмбриология', 'Лекция', 'Рысцова Екатерина Олеговна', 'АТИ-зал№1', 'Четверг', 'нижняя', 'СВЭбз-01-22', '13']
#['09:00-10:20', 'Цитология', 'гистология и эмбриология', 'Лабораторная работа', 'Рысцова Екатерина Олеговна', 'АТИ-343', 'Понедельник', 'верхняя', 'СВЭбд-01-22', '17']
def type_trasformation(str_type):
    if str_type == "Лекция":
        return 1
    elif str_type == "Практические и другие":
        return 2
    elif str_type == "Лабораторная работа":
        return 3

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
    if len(a) == 10:
        a[1] = a[1] + a[2]
        a.remove(a[2])
    return a
def main():
    db_complect()


if __name__ == "__main__":
    main()