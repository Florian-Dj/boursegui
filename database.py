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
        conn.execute('PRAGMA foreign_keys = 1')
        return conn
    except Error as e:
        print(e)
    return conn


def create_table_company(co):
    c = co.cursor()
    create = """CREATE TABLE IF NOT EXISTS company (
            id INTEGER  PRIMARY KEY    AUTOINCREMENT,
            name        VARCHAR(255)   NOT     NULL    UNIQUE,
            code        VARCHAR(255)   NOT     NULL    UNIQUE
        )"""
    c.execute(create)


def create_table_interest(co):
    c = co.cursor()
    create = """CREATE TABLE IF NOT EXISTS interest (
            company_id  INTEGER,
            value       FLOAT   NOT NULL,
            interest    INTEGER NOT NULL,
            years       INTEGER NOT NULL,
            
            CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
        )"""
    c.execute(create)


def insert_data(sql):
    try:
        conn = connection()
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        return "good"
    except Error as e:
        # print(e)
        print("\nCompagnie déjà dans la liste !\n")


def delete(table, company):
    try:
        conn = connection()
        c = conn.cursor()
        sql = "DELETE FROM {t} WHERE id={i}".format(t=table, i=company[0])
        c.execute(sql)
        conn.commit()
        conn.close()
        print("Société {n} supprimée".format(n=company[1]))
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
        create_table_company(conn)
        create_table_interest(conn)
    conn.close()
