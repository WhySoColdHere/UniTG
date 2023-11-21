import sqlite3 as sq
from time import sleep
def completion_db():
    # with sq.connect('rudn.db') as con:
    #     cur = con.cursor()
    count = 0
    with open("group_pars.txt",'r',encoding="utf-8") as file:
        with sq.connect('rudn.db') as con:
            cur = con.cursor()
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.split(' ')
                name_group = line[0]
                id_fakult = int(line[1])
                level = int(level_transformation(line[2]))
                kurs = int(line[3])
                form_study = int(form_transformation(line[5]))
                sleep(1)
                count = count + 1
                cur.execute(f"""
                INSERT INTO groups(fakult_id,id_preparation,Name,id_form_study,id_curse)
                VALUES({id_fakult},{level},'{name_group}',{form_study},{kurs})
                """)
                print(f"{name_group} {id_fakult} {level} {kurs} {form_study} - {count}")

                print(line)
def level_transformation(str_level):
    if str_level == 'Бакалавриат':
        return 1
    elif(str_level == 'Магистратура'):
        return 2
    elif (str_level == 'Специалитет'):
        return 3
def form_transformation(str_form):
    if str_form == "Очная":
        return 1
    elif(str_form == "Очно-заочная"):
        return 2
    elif (str_form == "Заочная"):
        return 3
def main():
    completion_db()

if __name__ == "__main__":
    main()