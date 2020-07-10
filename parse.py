# -*- coding: utf-8 -*-

import time
import database
import requests
import datetime
import main
from bs4 import BeautifulSoup


def home():
    print("""
    1 - Ajouter Société
    2 - Supprimer Société
    3 - Liste Société
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    elif choose == "1":
        add_society()
    elif choose == "2":
        delete_society()
    elif choose == "3":
        list_society()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def add_society():
    code = input("Code de la société a rajouter : ")
    url = "https://www.boursorama.com/cours/" + code
    req = requests.get(url)
    if "cours" in req.url:
        soup = BeautifulSoup(req.content, 'html.parser')
        name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
        sql = """INSERT INTO my_list ('name', 'code') VALUES ('{n}', '{c}')""".format(n=name, c=code)
        request = database.insert_data(sql)
        if request == "good":
            print("Ajout Compagnie Nom: {n}; Code: {c}".format(n=name, c=code))
    else:
        print("Code Société Erreur")
    time.sleep(2)
    home()


def delete_society():
    sql = "SELECT * FROM company"
    results = database.select(sql)
    if len(results) > 0:
        i = 1
        for result in results:
            print("{} - Name: {}; Code: {}".format(i, result[1], result[2]))
            i += 1
        choose = input("Quelle société voulez-vous enlever ? ")
        choose = int(choose)
        if 0 < choose <= len(results):
            database.delete("company", results[choose - 1])
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def list_society():
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    if len(results) > 0:
        for result in results:
            print("Nom: {}; Code: {}".format(result[1], result[2]))
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def parse():
    sql = """SELECT * FROM my_list"""
    results = database.select(sql)
    if len(results) > 0:
        while True:
            time_now = datetime.datetime.now().strftime("%H:%M:%S")
            datetime_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
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
                sql = """INSERT INTO company (company_id, value, var, volume, vol_var, date_update)
                        VALUES ({}, '{}', '{}', {}, '{}', '{}')"""\
                    .format(result[0], value, var, volume, vol_var, datetime_now)
                req = database.insert_data(sql)
                if req == "update":
                    sql = """UPDATE company 
                            SET value = '{}',
                                var = '{}',
                                volume = {},
                                vol_var = '{}',
                                date_update = '{}'
                            WHERE company_id = {}""".format(value, var, volume, vol_var, datetime_now, result[0])
                    database.insert_data(sql)
                print("\t\t{n}\nAction : {val}\t{var}\nVolume : {vo}\t{vov}"
                      .format(n=name, val=value, var=var, vo=volume, vov=vol_var))
                print()
            if "9:29AM" < time_now < "5:40PM":
                print("Bourse fermée")
                time.sleep(2)
                home()
            time.sleep(60)
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        main.main()
