import sqlite3 as sq
fakult_id = 3 #если изменяем факультет, то надо изменить
preparation = 3 # магистр то же самое
print("Введите форму обучение 1 - очная, 2 - очно-заочная, 3 - заочная:\n")
id_form_study = int(input())
print("Введите курс:")
curse = int(input())

with sq.connect('rudn.db') as con:
    cur = con.cursor()
    for i in range(100):
        print(f'Введите {i+1} название группы:')
        name_group = input()
        if name_group == '1':
            break
        cur.execute(f'''
        INSERT INTO groups(fakult_id,id_preparation,Name,id_form_study,id_curse)
        VALUES({fakult_id},{preparation},"{name_group}",{id_form_study},{curse})
        ''')
