import pymysql.cursors
import pandas as pd
import warnings
import os

import env
import universal

warnings.filterwarnings("ignore")
os.system('cls||clear')
name = input('Имя бд: ')
name_table = input('Имя таблицы: ')

def check_db() -> None:
    conn = pymysql.connect(host='localhost',
                             user=env.USER,
                             password=env.PASSWORD,
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `%s`" % name)

    conn = pymysql.connect(host='localhost',
                             user=env.USER,
                             password=env.PASSWORD,
                             database=name,
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    print("База данных подключена")

    try:
        cursor.execute("SELECT * FROM %s" % name_table)
    except pymysql.err.MySQLError:
        with open('create_structure.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.execute(sql_script % name_table)
            conn.commit()
            print("Скрипт SQL успешно выполнен")
    return

def save_result(operation, result):
    conn = pymysql.connect(host='localhost',
                             user=env.USER,
                             password=env.PASSWORD,
                             database=name,
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    stri =  "INSERT INTO " + name_table + f" (operat, result) VALUES (%s, %s)", (operation, str(result))
    print(stri)
    cursor.execute("INSERT INTO " + name_table + f" (operat, result) VALUES (%s, %s)", (operation, str(result)))
    conn.commit()
    return
def save_db_to_xlsx():
    conn = pymysql.connect(host='localhost',
                            user=env.USER,
                            password=env.PASSWORD,
                            database=name,
                            cursorclass=pymysql.cursors.DictCursor)
    new_df = pd.read_sql("SELECT * FROM " + name_table, conn)
    new_df.to_csv("out.txt")
    return

def print_db():
    conn = pymysql.connect(host='localhost',
                            user=env.USER,
                            password=env.PASSWORD,
                            database=name,
                            cursorclass=pymysql.cursors.DictCursor)
    new_df = pd.read_sql_query(f"SELECT *  FROM {name_table}" , conn)
    print(new_df)
    return

def print_exel():
    name = input('Путь до файла и название: ')
    new_df = pd.read_csv(name)
    print(new_df)
    return

def gen_list():
    my_list = []
    for i in range(120):
        my_list.append(i)
    print(my_list)
    save_result('list', my_list)
    return

def len_list():
    my_list = []
    for i in range(120):
        my_list.append(i)
    length = len(my_list)
    print('Длина списка: ', length)
    save_result('len(list)', len(my_list))
    return
def sum_list():
    my_list = []
    for i in range(120):
        my_list.append(i)
    total_sum = sum(my_list)
    print('Сумма элементов списка: ', total_sum)
    save_result('sum(list)', total_sum)
    return

def avg_list():
    my_list = []
    for i in range(120):
        my_list.append(i)
    length = len(my_list)
    total_sum = sum(my_list)
    avg = total_sum / length
    print('Среднне значенаие элемента списка: ', avg)
    save_result('avg(list)', avg)
    return

def main():
    run = True
    commands = """==========================================================================
1. Создать таблицу и БД в MySQL.
2. Сгенерировать один список длиной 120 значений, результат сохранить в MySQL.
3. Вывести длину списка, результат сохранить в MySQL.
4. Вывести сумму элементов списка, результат сохранить в MySQL.
5. Вывести среднее значение элементов списка, результат сохранить в MySQL.  
6. Все результаты вывести на экран из MySQL.
7. Сохранить все данные из MySQL в Excel.
8. Вывести все данные на экран из Excel.
9. Завершить"""
    while run:
        run = universal.uni(commands,
                      check_db, gen_list,
                      len_list, sum_list, avg_list,
                      print_db, save_db_to_xlsx, print_exel)
    return

if __name__ == '__main__':
    main()

