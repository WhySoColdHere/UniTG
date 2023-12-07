s = """
18:00 - 19:20
Неорганическая и аналитическая химия
Лекция
Маркова Екатерина Борисовна
ОРД-558
Понедельник
верхняя
"""

string_list = []
string = ''
for i in s:
    string+=i
    if i == "\n":
        string_list.append(string)
        string = ''
string_list = [string_list[i].strip() for i in range(1,len(string_list))]
print(string_list)
