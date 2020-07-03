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
    c.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL
        )""")
    print("Table Company Create")


if __name__ == '__main__':
    create_data()
    conn = connection()
    if conn is not None:
        create_table(conn)
