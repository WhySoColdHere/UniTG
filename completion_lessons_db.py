"""
selenium
requests
beautifulsoup4
lxml
"""
from test_pars_page import pars_PageLessons
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from time import sleep
# from scrappers import get_institutes
from selenium.webdriver.support.ui import Select
def pars():
    url = "https://www.rudn.ru/education/schedule"
    id_group = 0
    options = webdriver.FirefoxOptions()

    # options.add_argument("--headless")
    # options.set_preference("dom.webdriver.enabled",False)
    # options.headless = True
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    #options.set_preference("dom.webdriver.enabled",False) # отключение автоматического управления

    try:
        groups = {}
        driver.get(url=url)
        sleep(1)
        driver.find_element(By.CLASS_NAME,"use-cookie-block__close").click() # кликаем по куки
        select_fakult = Select(driver.find_element(By.NAME,"facultet")) # находим кнопку и делаем из нее обьект select
        with open('group_pars.txt',"a",encoding="utf-8") as file:
            for index_fakult in range(1,17): # факультеты не парсим, мы их помним
                sleep(1)
                select_fakult.select_by_index(index_fakult) # нажимаем на факултьететы
                sleep(1)
                page_html = driver.page_source # получаем html код, чтобы нажимать на кнопки в соответсвие с их index
                soup = BeautifulSoup(page_html,'lxml') #ПАРСИМ
                list_level = soup.find("select",{'name':'level'}).find_all("option")[1:]
                count_level = len(list_level) # забираем кол level, чтобы идти по index
                select_level = Select(driver.find_element(By.NAME,"level"))# нАХОДИМ КНОПКУ LEVEL
                print(f"Факультет - {index_fakult}:".strip())
                for index_level in range(1,count_level+1): # идем по index элементов
                    sleep(2)
                    select_level.select_by_index(index_level)
                    sleep(1)
                    page_html = driver.page_source# берем html с каждого нажатия,ч тобы получить реальное количество курсов
                    soup = BeautifulSoup(page_html,"lxml")
                    list_curs = soup.find("select",{'name':'kurs'}).find_all('option')[1:]
                    count_kurs = len(list_curs)
                    select_kurs = Select(driver.find_element(By.NAME,"kurs"))
                    print(f"\n{list_level[index_level-1].text}, количество курсов: {count_kurs}".strip())
                    for index_curse in range(1,count_kurs+1):
                        sleep(1)
                        select_kurs.select_by_index(index_curse)
                        sleep(1)
                        page_html = driver.page_source
                        soup = BeautifulSoup(page_html,'lxml')
                        list_form = soup.find("select",{"name":"form"}).find_all('option')[1:]
                        count_form = len(list_form)
                        select_form = Select(driver.find_element(By.NAME,"form"))
                        for index_form in range(1,count_form+1):
                            sleep(1)
                            select_form.select_by_index(index_form)
                            print(1)
                            sleep(1)
                            page_html = driver.page_source
                            soup = BeautifulSoup(page_html,'lxml')
                            list_groups = soup.find("select",{"name":"group"}).find_all("option")[1:]
                            count_groups = len(list_groups)
                            sleep(1)
                            select_group = Select(driver.find_element(By.NAME,"group"))
                            for groups in range(1,count_groups+1):
                                sleep(1)
                                select_group.select_by_index(groups)
                                id_group+=1# чтобы связать id группы с уроками, мы же идем с первой группы и до конца, следовательно и с парами идем также
                                sleep(5)
                                button = driver.find_element(By.XPATH,"//button[@class='btn btn-primary btn__ajax__search animate']")
                                button.click()
                                sleep(3)
                                pars_PageLessons(driver.page_source,id_group)
                                sleep(1)




    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
def main():
    pars()


if __name__ == "__main__":
    main()