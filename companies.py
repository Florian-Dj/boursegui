# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import database
import time
import main


def parse_cac40():
    i = 1
    while i <= 2:
        url = "https://www.boursorama.com/bourse/actions/cotations/page-{}".format(i)
        param = "?quotation_az_filter%5Bmarket%5D=1rPCAC"
        req = requests.get(url + param)
        soup = BeautifulSoup(req.content, 'html.parser')
        values = soup.find_all(class_="o-pack__item u-ellipsis u-color-cerulean")
        for value in values:
            name = value.text
            if "'" in name:
                name = name.split("'")[1]
            code = value.a['href'].split("/")[2]
            sql = """INSERT INTO companies ('name', 'code', 'clues') VALUES ('{n}', '{c}', '{i}')"""\
                .format(n=name, c=code, i="CAC40")
            database.insert(sql)
        i += 1


def clues():
    print("\n1 - Ma Liste")
    print("2 - Tout")
    sql = """SELECT clues FROM companies GROUP BY clues"""
    results = database.select(sql)
    i = 3
    for result in results:
        if result[0]:
            print("{} - {}".format(i, result[0]))
            i += 1
    print("0 - Retour")
    choose = input("\nAction que vous voulez effectuer : ")
    try:
        choose = int(choose)
        if 0 <= choose <= len(results)+1:
            info = results[choose-2][0]
            return choose, info
        else:
            print("\nMerci de rentrer un nombre correcte !")
            time.sleep(2)
            main.main()
    except ValueError:
        print("\nMerci de rentrer un nombre correcte !")
        time.sleep(2)
        main.main()


if __name__ == '__main__':
    parse_cac40()
