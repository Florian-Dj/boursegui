# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import database
import time
import main

list_companies = [("DAX30", "49", "5pDAX", 2), ("BEL20", "32", "FF11-BEL20", 1), ("IBEX35", "34", "FF55-IBEX", 2),
                  ("Nasdaq100", "1", "%24NDX.X", 4), ("FTSE MIB", "39", "7fI945", 2), ("AEX25", "31", "1rAZMA", 1),
                  ("PSI20", "35", "1rLPSI20", 1), ("Footsie 100", "44", "UKX.L", 4), ("SMI25", "41", "1hSMI", 1)]


def parse_cac40():
    i = 1
    while i <= 2:
        url = "https://www.boursorama.com/bourse/actions/palmares/france/page-{}".format(i)
        param = "?france_filter%5Bmarket%5D=1rPCAC&france_filter%5Bvariation%5D=128&france_filter%5Bperiod%5D=1"
        req = requests.get(url + param)
        soup = BeautifulSoup(req.content, 'html.parser')
        values = soup.find_all(class_="o-pack__item u-ellipsis u-color-cerulean")
        for value in values:
            name = value.text
            if "'" in name:
                name = name.replace("'", "")
            code = value.a['href'].split("/")[2]
            print(name, code)
            sql = """INSERT INTO companies ('name', 'code', 'clues') VALUES ('{n}', '{c}', '{i}')"""\
                .format(n=name, c=code, i="CAC40")
            database.insert(sql)
        i += 1
    parse_int()


def parse_int():
    for comp in list_companies:
        i = 1
        while i <= comp[3]:
            url = "https://www.boursorama.com/bourse/actions/cotations/international/page-{}".format(i)
            param = "?international_quotation_az_filter%5Bcountry%5D={}&international_quotation_az_filter%5Bmarket%5D={}".format(comp[1], comp[2])
            req = requests.get(url + param)
            soup = BeautifulSoup(req.content, 'html.parser')
            values = soup.find_all(class_="o-pack__item u-ellipsis u-color-cerulean")
            for value in values:
                name = value.text
                if "'" in name:
                    name = name.replace("'", "")
                code = value.a['href'].split("/")[2]
                sql = """INSERT INTO companies ('name', 'code', 'clues') VALUES ('{n}', '{c}', '{i}')"""\
                    .format(n=name, c=code, i=comp[0])
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
