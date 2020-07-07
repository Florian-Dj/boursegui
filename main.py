# -*- coding: utf-8 -*-

import time
import database
import requests
from bs4 import BeautifulSoup

data_info = dict()


def main():
    print("""
    1 - Run
    2 - Ajouter Société
    3 - Supprimer Société
    4 - Liste Société
    0 - Quitter""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        exit()
    elif choose == "1":
        parse()
    elif choose == "2":
        add_society()
    elif choose == "3":
        print("3")
    elif choose == "4":
        list_society()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        main()


def add_society():
    code = input("Code de la société a rajouter : ")
    url = "https://www.boursorama.com/cours/" + code
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
    database.insert_into("company", ("name", "code"), (name, code))
    time.sleep(5)
    main()


def list_society():
    results = database.select()
    for result in results:
        print("Name : {}; Code : {}".format(result[1], result[2]))
    time.sleep(2)
    main()


def parse():
    results = database.select()
    while True:
        for result in results:
            url = "https://www.boursorama.com/cours/" + result[2]
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
            volume = soup.find_all('span', class_="c-instrument c-instrument--totalvolume")[0].text.replace(" ", "")
            value = soup.find_all('span', class_="c-instrument c-instrument--last")[0].text
            var = soup.find_all('span', class_="c-instrument c-instrument--variation")[0].text
            print(name, volume, value, var)
        time.sleep(60)


if __name__ == '__main__':
    main()
