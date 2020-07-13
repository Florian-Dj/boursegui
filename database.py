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


def create_table_my_list(co):
    c = co.cursor()
    create = """CREATE TABLE IF NOT EXISTS my_list (
            id      INTEGER        PRIMARY KEY    AUTOINCREMENT,
            name    VARCHAR(255)   NOT     NULL    UNIQUE,
            code    VARCHAR(255)   NOT     NULL    UNIQUE
        )"""
    c.execute(create)


def create_table_interest(co):
    c = co.cursor()
    create = """CREATE TABLE IF NOT EXISTS interest (
            interest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id  INTEGER,
            value       FLOAT           NOT NULL,
            interest    VARCHAR(255)    NOT NULL,
            years       INTEGER         NOT NULL,
            date_div    DATE            DEFAULT     CURRENT_DATE,
            date_update DATE            DEFAULT     CURRENT_DATE,
            
            CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES my_list(id) ON DELETE CASCADE
        )"""
    c.execute(create)


def create_table_company(co):
    c = co.cursor()
    create = """CREATE TABLE IF NOT EXISTS company (
            company_id  INTEGER     UNIQUE,
            value       FLOAT       NOT NULL,
            var         VAR(255)    NOT NULL,
            volume      INTEGER     NOT NULL,
            vol_var     VAR(255)    NOT NULL,
            date_update DATETIME    DEFAULT CURRENT_TIMESTAMP,
            
            CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES my_list(id) ON DELETE CASCADE
        )"""
    c.execute(create)


def insert(sql):
    conn = connection()
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        return "good"
    except conn.IntegrityError:
        return "update"
    except Error as e:
        print(e)
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


def select(sql):
    try:
        conn = connection()
        c = conn.cursor()
        c.execute(sql)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)


if __name__ == '__main__':
    create_data()
    conn = connection()
    if conn is not None:
        create_table_my_list(conn)
        create_table_interest(conn)
        create_table_company(conn)
    conn.close()
