# -*- coding: utf-8 -*-

import os
import sqlite3
from sqlite3 import Error

data_name = "data.db"


def create_data():
    if not os.path.exists(data_name):
        open(data_name, "w")


def connection():
    conn = None
    try:
        conn = sqlite3.connect(data_name)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(co):
    c = co.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(255) NOT NULL UNIQUE,
            code varchar(255) NOT NULL UNIQUE
        )""")


def insert_into(table, column, value):
    try:
        conn = connection()
        c = conn.cursor()
        sql = "INSERT INTO {t} {c} VALUES {v}".format(t=table, c=column, v=value)
        c.execute(sql)
        conn.commit()
        print("Add {v} in table {t}".format(v=value, t=table))
    except Error as e:
        print(e)


def select():
    try:
        conn = connection()
        c = conn.cursor()
        c.execute("SELECT * FROM company")
        result = c.fetchall()
        return result
    except Error as e:
        print(e)


if __name__ == '__main__':
    create_data()
    conn = connection()
    if conn is not None:
        create_table(conn)
