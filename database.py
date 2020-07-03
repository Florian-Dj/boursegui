# -*- coding: utf-8 -*-

import os
import sqlite3
from sqlite3 import Error


def create_data(file):
    if os.path.exists(file):
        print("Ok")
    else:
        print("Create file - test.sqlite")
        open(file, "w")


if __name__ == '__main__':
    create_data("data.db")
