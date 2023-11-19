"""
selenium
requests
beautifulsoup4
lxml
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from time import sleep
# from scrappers import get_institutes
from selenium.webdriver.support.ui import Select
def pars():
    url = "https://www.rudn.ru/education/schedule"
    options = webdriver.FirefoxOptions()

    # options.add_argument("--headless")
    s = Service(executable_path="C:\\Users\\tonis\\PycharmProjects\\db_test\\driver\\geckodriver.exe")
    driver = webdriver.Firefox(service=s,options=options)

    # options.headless = True

    try:
        groups = {}
        driver.get(url=url)
        sleep(1)
        select_fakult = Select(driver.find_element(By.NAME,"facultet")) # находим кнопку и делаем из нее обьект select
        with open('group_pars.txt',"a",encoding="utf-8") as file:
            for index_fakult in range(1,17): # факультеты не парсим, мы их помним
                select_fakult.select_by_index(index_fakult) # нажимаем на факултьететы
                sleep(2)
                page_html = driver.page_source # получаем html код, чтобы нажимать на кнопки в соответсвие с их index
                soup = BeautifulSoup(page_html,'lxml') #ПАРСИМ
                list_level = soup.find("select",{'name':'level'}).find_all("option")[1:]
                count_level = len(soup.find("select",{'name':'level'}).find_all("option")[1:]) # забираем кол level, чтобы идти по index
                select_level = Select(driver.find_element(By.NAME,"level"))#нАХОДИМ КНОПКУ LEVEL
                print(f"Факультет - {index_fakult}:".strip())
                for index_level in range(1,count_level+1): # идем по index элементов
                    select_level.select_by_index(index_level)
                    sleep(1)
                    page_html = driver.page_source#берем html с каждого нажатия,ч тобы получить реальное количество курсов
                    soup = BeautifulSoup(page_html,"lxml")
                    count_kurs = len(soup.find("select",{'name':'kurs'}).find_all('option')[1:])
                    select_kurs = Select(driver.find_element(By.NAME,"kurs"))
                    print(f"\n{list_level[index_level-1].text}, количество курсов: {count_kurs}".strip())
                    for index_curse in range(1,count_kurs+1):
                        sleep(1)
                        select_kurs.select_by_index(index_curse)
                        page_html = driver.page_source
                        soup = BeautifulSoup(page_html,'lxml')
                        count_form = len(soup.find("select",{"name":"form"}).find_all('option')[1:])
                        select_form = Select(driver.find_element(By.NAME,"form"))
                        sleep(1)
                        for index_form in range(1,count_form+1):
                            sleep(2)
                            select_form.select_by_index(index_form)
                            print(1)
                            sleep(1)
                            page_html = driver.page_source
                            soup = BeautifulSoup(page_html,'lxml')
                            count_groups = soup.find("select",{"name":"group"}).find_all("option")[1:]
                            sleep(1)
                            for groups in count_groups:
                                file.write(f"{groups.text} {index_fakult} {index_level} {index_curse} {index_form}\n")

                                print(f"Группа:{groups.text}, index_fakult:{index_fakult}, index_level:{index_level}, index_curse:{index_curse}, index_form:{index_form}")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
def main():
    pars()


if __name__ == "__main__":
    main()