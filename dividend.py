# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
import main
import database


def home():
    print("""
    1 - Dividende 2020
    2 - Dividende 2021
    3 - Dividende 2022
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    elif choose == "1":
        list_dividend_2020()
    elif choose == "4":
        analysis_dividend()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def list_dividend_2020():
    results = database.select()
    if len(results) > 0:
        for result in results:
            url = "https://www.boursorama.com/cours/" + result[2]
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            dividend_price = soup.find('li', class_="c-list-info__item c-list-info__item--fixed-width").text.replace(" ", "").split("\n")[3]
            dividend_date = soup.find_all('li', class_="c-list-info__item c-list-info__item--fixed-width")[1].text.replace(" ", "").split("\n")[3]
            value = soup.find_all('span', class_="c-instrument c-instrument--last")[0].text
            if dividend_price == "-":
                dividend_date = "?"
                dividend_price = soup.find('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height c-table__cell--align-top / u-text-left u-text-right u-ellipsis").text.replace(" ", "").replace("\n", "")
            interest = round(float(dividend_price[:-3]) * 100 / float(value), 2)
            print("{n} -  Prix: {dp}; Date: {dd}; Intêret: {i}%".format(n=result[1], dp=dividend_price, dd=dividend_date, i=interest))
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()

