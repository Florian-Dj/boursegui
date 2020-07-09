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
        print("Dividende d'une société")
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def parse_dividend(year):
    sql = "SELECT * FROM company"
    results = database.select(sql)
    if len(results) > 0:
        for result in results:
            url = "https://www.boursorama.com/cours/" + result[2]
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
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
            print("{n} -  Valeur: {v}; Date: {dd}".format(n=result[1], v=value_div, dd=dividend_date))
            sql = "INSERT INTO interest ('company_id', 'value', 'years', date_div) VALUES ({}, {}, {}, '{}')"\
                .format(result[0], value_div[:-3], year, dividend_date)
            database.insert_data(sql)
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def check(year):
    # print(datetime.date.today())
    sql = """SELECT name, value, date_div
                FROM company
                INNER JOIN interest
                ON company.id = interest.company_id
                WHERE years = {y}"""\
        .format(y=year)
    results = database.select(sql)
    if len(results) > 0:
        for result in results:
            print("{} - Valeur: {}; Date: {}".format(result[0], result[1], result[2]))
        time.sleep(2)
        home()
    else:
        parse_dividend(year)
