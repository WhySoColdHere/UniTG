"""В этом файле мы считыем группы с lessons.txt и заполняем дб"""
import sqlite3 as sq
from time import sleep
def db_complect():
    with open("lesson.txt","r",encoding="utf-8") as file:
        for i in range(0,10):
            print(file.readline().strip())

def main():
    db_complect()


if __name__ == "__main__":
    main()