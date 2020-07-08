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
        dividend(2020)
    elif choose == "2":
        dividend(2021)
    elif choose == "3":
        dividend(2022)
    elif choose == "4":
        print("Dividende d'une société")
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def dividend(year):
    sql = "SELECT * FROM company"
    results = database.select(sql)
    if len(results) > 0:
        print("\t\t----- Dividendes {y} -----".format(y=year))
        for result in results:
            url = "https://www.boursorama.com/cours/" + result[2]
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            value_action = soup.find_all('span', class_="c-instrument c-instrument--last")[0].text
            dividend_date = soup.find_all('li', class_="c-list-info__item c-list-info__item--fixed-width")[1].text.replace(" ", "").split("\n")[3]
            if year == 2020:
                value_div = soup.find('li', class_="c-list-info__item c-list-info__item--fixed-width").text.replace(" ", "").split("\n")[3]
                if value_div == "-":
                    dividend_date = "?"
                    value_div = soup.find('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height c-table__cell--align-top / u-text-left u-text-right u-ellipsis").text.replace(" ", "").replace("\n", "")
            else:
                if year == 2021:
                    nb = 1
                elif year == 2022:
                    nb = 2
                value_div = soup.find_all('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height c-table__cell--align-top / u-text-left u-text-right u-ellipsis")[nb].text.replace(" ", "").replace("\n", "")
            interest = round(float(value_div[:-3]) * 100 / float(value_action), 2)
            print("{n} -  Valeur: {v}; Date: {dd}; Intêret: {i}%".format(n=result[1], v=value_div, dd=dividend_date, i=interest))
            sql = "INSERT INTO interest ('company_id', 'value', 'interest', 'years') VALUES ('{}', '{}', '{}', '{}')"\
                .format(result[0], value_div[:-3], interest, year)
            database.insert_data(sql)
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def check():
    print(datetime.datetime.now().strftime("%Y-%m-%d"))
    sql = "SELECT name, value, interest, years FROM company INNER JOIN interest ON company.id = interest.company_id"
    results = database.select(sql)
    if len(results) > 0:
        for result in results:
            print("Nom: {}; Value: {}; Interest: {}; Years: {}".format(result[0], result[1], result[2], result[3]))
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


if __name__ == '__main__':
    check()
