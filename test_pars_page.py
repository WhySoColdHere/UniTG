"""
В функцию main приходит html код страницы, и id группы(которое мы собираем простым счетчиком,
по идее оно должно подходить, но мы все равно будем сверять название,которое мы будем получать
с помощью парсера) с помощью одного html можно собрать все две недели.
функции возращает двумерный массив, в каждом массиве есть строка
"""
from bs4 import BeautifulSoup
with open("3.html",'r',encoding="utf-8") as file:
    s = file.read()
def main(page,id_group):
    soup = BeautifulSoup(page,"lxml")
    page = soup.find("div",{"class":"tabs__block-dir js_tabs_bt tabs__block-gray"})
    name_group = page.find("span",{"style":"white-space: nowrap;"}).text
    id_group = id_group
    # week = page.find("ul",{"class":"nav nav-tabs visible-lg visible-md js_tabs_for_select"}).find_all('li')
    # for i in week:
    #     print(i)
    # print(week)
    all_week = page.find_all("table",{"class":"edss__table vm-swipe"})
    for i in range(0,2):
        all_tr = all_week[0].find_all('tr')
        for j in all_tr:
            print(j.text)


main(s,1)