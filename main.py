# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

data_society = dict()
data_info = dict()


def cli():
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
        cli()


def add_society():
    society = input("Code de la société a rajouter : ")
    url = "https://www.boursorama.com/cours/" + society
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
    print(society, name)


def list_society():
    with open('data_society.json', "r") as file:
        company = json.load(file)
        i = 1
        for code, companies in company["society"].items():
            print("{i} - {c} ==> {com}".format(i=i, c=code, com=companies))
            i += 1


def parse():
    url = "https://www.boursorama.com/cours/1rPNACON/"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
    volume = soup.find_all('span', class_="c-instrument c-instrument--totalvolume")[0].text
    value = soup.find_all('span', class_="c-instrument c-instrument--last")[0].text
    var = soup.find_all('span', class_="c-instrument c-instrument--variation")[0].text
    date = datetime.now().isoformat(timespec='minutes')
    data_info["1rPFDJ"] = {'name': name, 'valeur': value, "variation": var, 'volume': volume, 'date': date}
    print(data_info)
    with open("data.json", "w") as file:
        json.dump(data_info, file, indent=4)


if __name__ == '__main__':
    # parse()
    cli()
