# -*- coding: utf-8 -*-

import time
import main
import database
import parse


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
        check_company()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def dividend(year):
    print("\n--- Dividende {} ---".format(year))
    sql = """SELECT companies.name, interest.value, company.value, (interest.value*100/company.value)
            FROM companies
            LEFT JOIN interest ON companies.id = interest.company_id
            LEFT JOIN company ON companies.id = company.company_id
            WHERE years = {y}
            ORDER BY (SELECT (interest.value*100/company.value) FROM companies) DESC""".format(y=year)
    results = database.select(sql)
    for result in results:
        print("{}: {}€  {}%".format(result[0], result[1], round(result[3], 2)))
    time.sleep(2)
    home()


def check_company():
    sql = """SELECT * FROM companies"""
    results = database.select(sql)
    if len(results) > 0:
        i = 1
        print()
        for result in results:
            print("{} - {}".format(i, result[1]))
            i += 1
        print("0 - Retour")
        choose = input("\nQuelle société voulez-vous voir les dividendes ? ")
        choose = int(choose)
        if choose == 0:
            home()
        elif 0 < choose <= len(results):
            print("\n-------- Dividend {} --------".format(results[choose-1][1]))
            sql = """SELECT name, company.value, interest.date_div, interest.years, interest.value
                        FROM companies
                        LEFT JOIN interest ON companies.id = interest.company_id
                        LEFT JOIN company ON companies.id = company.company_id
                        WHERE name = '{n}'""".format(n=results[choose-1][1])
            req = database.select(sql)
            print("Date: {}\t Action: {}€".format(req[0][2], req[0][1]))
            for dividend in req:
                interest = round(dividend[4] * 100 / dividend[1], 2)
                print("{}: {}€  {}%".format(dividend[3], dividend[4], interest))
            time.sleep(2)
            check_company()
        else:
            print("\nMerci de choisir un choix valide")
            time.sleep(2)
            check_company()
    time.sleep(2)
    home()
