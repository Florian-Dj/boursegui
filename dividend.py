# -*- coding: utf-8 -*-

import time
import requests
import datetime
from bs4 import BeautifulSoup
import main
import database


def home():
    print("""
    1 - Dividende 2020
    2 - Dividende 2021
    3 - Dividende 2022
    4 - Dividende Société
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    elif choose == "1":
        check(2020)
    elif choose == "2":
        check(2021)
    elif choose == "3":
        check(2022)
    elif choose == "4":
        check_company()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def parse_dividend(year, result, *param):
    url = "https://www.boursorama.com/cours/" + result[2]
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
    dividend_date = soup.find_all('li', class_="c-list-info__item c-list-info__item--fixed-width")[1].text.replace(" ", "").split("\n")[3].split(".")
    dividend_date = "20{}-{}-{}".format(dividend_date[2], dividend_date[1], dividend_date[0])
    if year == 2020:
        value_div = soup.find('li', class_="c-list-info__item c-list-info__item--fixed-width").text.replace(" ", "").split("\n")[3]
        if value_div == "-":
            value_div = soup.find('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height c-table__cell--align-top / u-text-left u-text-right u-ellipsis").text.replace(" ", "").replace("\n", "")
    else:
        if year == 2021:
            nb = 1
        elif year == 2022:
            nb = 2
        value_div = soup.find_all('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height c-table__cell--align-top / u-text-left u-text-right u-ellipsis")[nb].text.replace(" ", "").replace("\n", "")
    print("{n} -  Valeur: {v}; Date: {dd}".format(n=name, v=value_div, dd=dividend_date))
    if param:
        sql = """UPDATE interest SET value = {}, date_div = '{}', date_update = '{}' WHERE interest_id = {}"""\
            .format(value_div[:-3], dividend_date, param[0], result[1])
    else:
        sql = """INSERT INTO interest ('company_id', 'value', 'years', date_div)
                    VALUES ({}, {}, {}, '{}')""".format(result[0], value_div[:-3], year, dividend_date)
    database.insert_data(sql)


def check(year):
    print("\n-------- Dividend {} --------".format(year))
    sql = """SELECT * FROM company"""
    results = database.select(sql)
    for result in results:
        sql = """SELECT name, interest_id, code, value, date_div, date_update
                    FROM interest
                    INNER JOIN my_list
                    ON my_list.id = interest.company_id
                    WHERE years = {y} AND name = '{n}'""".format(y=year, n=result[1])
        req = database.select(sql)
        if req:
            req = req[0]
            date = datetime.datetime.today()
            date_div = datetime.datetime.strptime(req[4], "%Y-%m-%d")
            if date_div + datetime.timedelta(days=7) < date:
                parse_dividend(year, req, date.strftime("%Y-%m-%d"))
            else:
                print("{} - Valeur: {}; Date: {}".format(req[0], req[3], req[4]))
        else:
            parse_dividend(year, result)
    time.sleep(2)
    home()


def check_company():
    sql = """SELECT * FROM company"""
    results = database.select(sql)
    if len(results) > 0:
        i = 1
        for result in results:
            print("{} - Nom: {}; Code: {}".format(i, result[1], result[2]))
            i += 1
        choose = input("\nQuelle société voulez-vous voir les dividendes ? ")
        choose = int(choose)
        if 0 < choose <= len(results):
            print("\n----- Dividend {} -----".format(results[choose-1][1]))
            sql = """SELECT name, value, date_div, years
                        FROM interest
                        INNER JOIN my_list
                        ON my_list.id = interest.company_id
                        WHERE name = '{n}'""".format(n=results[choose-1][1])
            req = database.select(sql)
            print("Date: {}\t Action: {}".format(req[0][2], "?"))
            if req:
                for dividend in req:
                    print("{} - Valeur: {}; Intêret:{}".format(dividend[3], dividend[1], "?"))
                time.sleep(2)
                home()
            else:
                parse_dividend(2020, results[choose-1])
                parse_dividend(2021, results[choose-1])
                parse_dividend(2022, results[choose-1])
                time.sleep(2)
                home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()

