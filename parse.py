# -*- coding: utf-8 -*-

import database
import datetime
import requests
import main
import time
from bs4 import BeautifulSoup


def home():
    print("""
    1 - Run 1 fois
    2 - Run x fois
    3 - Jusqu'à la fermeture
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    if choose == "1":
        parse(1)
    if choose == "2":
        number_run()
    if choose == "3":
        parse(32768)


def number_run():
    choose = input("\nCombien de fois voulez-vous run ? : ")
    if choose.isdigit():
        parse(int(choose))
    else:
        print("Merci de rentrer un nombre correcte !")
        number_run()


def parse(run, draw=True):
    sql = """SELECT * FROM my_list"""
    results = database.select(sql)
    if results:
        i = 1
        while i <= run:
            day = datetime.datetime.today().weekday()
            time_now = datetime.datetime.now()
            morning = time_now.replace(hour=9, minute=00)
            evening = time_now.replace(hour=17, minute=40)
            if morning < time_now < evening and day != 5 and day != 6:
                datetime_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                if draw:
                    print()
                    print("--- {t} ---".format(t=datetime_now))
                    print()
                for result in results:
                    url = "https://www.boursorama.com/cours/" + result[2]
                    req = requests.get(url)
                    soup = BeautifulSoup(req.content, 'html.parser')
                    name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
                    value = soup.find_all('span', class_="c-instrument c-instrument--last")[0].text
                    var = soup.find_all('span', class_="c-instrument c-instrument--variation")[0].text
                    volume = soup.find_all('span', class_="c-instrument c-instrument--totalvolume")[0].text.replace(" ", "")
                    vol_var = soup.find_all('li', class_="c-list-info__item--small-gutter")[2]
                    vol_var = vol_var.text.replace(" ", "").split("\n")[3]
                    dividend_date = soup.find_all('li', class_="c-list-info__item c-list-info__item--fixed-width")[1]
                    dividend_date = dividend_date.text.replace(" ", "").split("\n")[3].split(".")
                    dividend_date = "20{}-{}-{}".format(dividend_date[2], dividend_date[1], dividend_date[0])
                    value_div = []
                    value_div_20 = soup.find('li', class_="c-list-info__item c-list-info__item--fixed-width")
                    value_div_20 = value_div_20.text.replace(" ", "").split("\n")[3]
                    company_id = result[0]
                    if value_div_20 == "-":
                        value_div_20 = soup.find('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height"
                                                           " c-table__cell--align-top / u-text-left u-text-right u-ellipsis")
                        value_div.append(value_div_20.text.replace(" ", "").replace("\n", "").replace("EUR", ""))
                    else:
                        value_div.append(value_div_20.replace("EUR", ""))
                    nb = 1
                    while nb <= 5:
                        value_div_other = soup.find_all('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height"
                                                            " c-table__cell--align-top / u-text-left u-text-right u-ellipsis")[nb]
                        value_div.append(value_div_other.text.replace(" ", "").replace("\n", "").replace("EUR", ""))
                        nb += 1
                    company(company_id, value, var, volume, vol_var, datetime_now)
                    interest(company_id, value_div, dividend_date, datetime_now)
                    if draw:
                        print("\t\t{n}\nAction: {val}€\t{var}\nVolume: {vo}\t{vov}\nDividende: {vd}€\t{vp}"
                              .format(n=name, val=value, var=var, vo=volume, vov=vol_var, vd=value_div[0], vp=value_div[3]))
                        print()
                if run > 1:
                    time.sleep(60)
            else:
                if draw:
                    print("\nBourse fermée\n")
                    time.sleep(2)
                    break
            i += 1
    else:
        print("\nAucune Entreprise dans la liste")
        return "None"
    if draw:
        time.sleep(2)
        main.main()


def company(company_id, value, var, volume, vol_var, datetime_now):
    sql = """INSERT INTO company (company_id, value, var, volume, vol_var, date_update)
            VALUES ({}, '{}', '{}', {}, '{}', '{}')"""\
        .format(company_id, value, var, volume, vol_var, datetime_now)
    req = database.insert(sql)
    if req == "update":
        sql = """UPDATE company SET value = '{}', var = '{}', volume = {}, vol_var = '{}', date_update = '{}'
                WHERE company_id = {}""".format(value, var, volume, vol_var, datetime_now, company_id)
        database.insert(sql)


def interest(company_id, dividend, date_div, datetime_now):
    year = 2020
    i = 0
    while i <= 2:
        sql = """SELECT * FROM interest WHERE company_id = '{}' AND years = {}""".format(company_id, year)
        req = database.select(sql)
        if req:
            sql = """UPDATE interest SET value = '{}', interest = '{}', date_update = '{}'
                    WHERE company_id = {} AND years = {}""".format(dividend[i], dividend[i+3], datetime_now, company_id, year)
            database.insert(sql)
        else:
            sql = """INSERT INTO interest (company_id, value, interest, years, date_div, date_update)
                    VALUES ({}, '{}', '{}', {}, '{}', '{}')"""\
                .format(company_id, dividend[i], dividend[i+3], year, date_div, datetime_now)
            database.insert(sql)
        year += 1
        i += 1
