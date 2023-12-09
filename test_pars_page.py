"""
В функцию main приходит html код страницы, и id группы(которое мы собираем простым счетчиком,
по идее оно должно подходить, но мы все равно будем сверять название,которое мы будем получать
с помощью парсера) с помощью одного html можно собрать все две недели.
функции возращает двумерный массив, в каждом массиве есть строка
"""
from bs4 import BeautifulSoup
def pars_Page_2(page,id_group):
    lessons = []
    time = ['09:00 - 10:20', "10:30 - 11:50", '12:00 - 13:20', '13:30 - 14:50', '15:00 - 16:20', '16:30 - 17:50',
            '18:00 - 19:20', '19:30 - 20:50',"11:59 - 13:19","08:59 - 10:19","10:29 - 11:49","13:29 - 14:49","14:59 - 16:19","16:29 - 17:49","17:59 - 19:19","19:29 - 20:49"]
    day_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    soup = BeautifulSoup(page, "lxml")
    name_group = soup.find("div",{"class":"item__h mb40"}).text.strip()
    #парсим названия недель например верхняя и нижняя
    name_week_number = soup.find("ul",{"class":"nav nav-tabs visible-lg visible-md js_tabs_for_select"}).find_all("li") #блок ul в котором все li
    #парсим две недели в список
    list_week = soup.find_all("div",{'class':"plate-item_content clearfix"})
    for index in range(0,len(list_week)):
        flag_day = ''
        week = list_week[index]
        index_week = name_week_number[index].find_all('span')[1].text.split()[1].strip()
        all_tr = week.find_all("tr")
        for index_tr in range(0,len(all_tr)):
            if all_tr[index_tr].text.strip() in day_week:
                flag_day = all_tr[index_tr].text.strip()
                continue
            responce = strip_del(f'{all_tr[index_tr].text}{flag_day}\n{index_week}\n{name_group}\n')

            lessons.append(responce)

            # в итоге у нас получается список lessons со всеми tr, в том числе и без времени, нужно убрать элементы-
            # без времени и у одного первого элемента до этих элементов убрать кабинет и учителя
            # мы не принтуем элемент у которого нет времени в начале а у элемента после него должны убрать
            # имя учителя и кабинет
    lessons = english_del(lessons,time)
    for i in lessons:
        i.append(id_group)
    return lessons
    # крч вроде все сделал, осталось понять,что делать с id группы, возможно похуй на него
    # теперь надо сделать запись в файл и запустить парсер
    #впринципе можно удалить первую функцию
def strip_del(s):
    string_list = []
    string = ''
    for i in s:
        string += i
        if i == "\n":
            string_list.append(string)
            string = ''
    string_list = [string_list[i].strip() for i in range(1,len(string_list))]
    return string_list

def english_del(a,slovar_time):
    for i in range(0,len(a)):
        if a[i][0] not in slovar_time:
            a[i-1].append("angl.")
    for i in reversed(range(len(a))):
        if a[i][0] not in slovar_time:
            a.remove(a[i])
    for i in range(0,len(a)):
        if a[i][-1] == "angl.":
            a[i].pop(8),a[i].pop(4),a[i].pop(3)
    return a
# with open("Расписание занятий РУДН5.htm",'r',encoding="utf-8") as file:
#     s = file.read()
# a = pars_Page_2(s,1)
# for i in a:
#     print(i)
