# -*- coding: utf-8 -*-

import time
import database
import requests
import datetime
import main
from bs4 import BeautifulSoup


def home():
    print("""
    1 - Run
    2 - Ajouter Société
    3 - Supprimer Société
    4 - Liste Société
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    elif choose == "1":
        parse()
    elif choose == "2":
        add_society()
    elif choose == "3":
        delete_society()
    elif choose == "4":
        list_society()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def add_society():
    code = input("Code de la société a rajouter : ")
    url = "https://www.boursorama.com/cours/" + code
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
    database.insert_into("company", ("name", "code"), (name, code))
    time.sleep(5)
    home()


def delete_society():
    results = database.select()
    if len(results) > 0:
        i = 1
        for result in results:
            print("{} - Name: {}; Code: {}".format(i, result[1], result[2]))
            i += 1
        choose = input("Quelle société voulez-vous enlever ? ")
        choose = int(choose)
        if 0 < choose <= len(results):
            database.delete("company", results[choose - 1])
        time.sleep(3)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def list_society():
    results = database.select()
    if len(results) > 0:
        for result in results:
            print("Name: {}; Code: {}".format(result[1], result[2]))
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def parse():
    results = database.select()
    if len(results) > 0:
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        while True:
            for result in results:
                url = "https://www.boursorama.com/cours/" + result[2]
                req = requests.get(url)
                soup = BeautifulSoup(req.content, 'html.parser')
                name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
                volume = soup.find_all('span', class_="c-instrument c-instrument--totalvolume")[0].text.replace(" ", "")
                vol_var = soup.find_all('li', class_="c-list-info__item--small-gutter")[2].text.replace(" ", "").split("\n")[3]
                value = soup.find_all('span', class_="c-instrument c-instrument--last")[0].text
                var = soup.find_all('span', class_="c-instrument c-instrument--variation")[0].text
                print(name, value, var, volume, vol_var)
            if not "9:29AM" > time_now > "5:40PM":
                print("Bourse fermée")
                time.sleep(2)
                home()
            time.sleep(60)
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()