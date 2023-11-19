from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from scrappers import get_institutes

url = "https://www.rudn.ru/education/schedule"

options = FireFoxOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Firefox(service="C:\\Users\\tonis\\PycharmProjects\\db_test\\driver\\geckodriver.exe",options=options)
driver.get(url=url)
sleep(2)

institutes = get_institutes(driver.find_element(By.NAME, "facultet").text)  # Список институтов

print(institutes)
