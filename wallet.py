# -*- coding: utf-8 -*-

import database
import main
import time


def home():
    print("""
    1 - Réel
    2 - Virtuel
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    elif choose == "1":
        real()
    elif choose == "2":
        virtual()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def real():
    print("""\nPortefeuille Réel
    1 - Ajouter Société
    2 - Supprimer Société
    3 - Liste Portefeuille
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        home()
    elif choose == "1":
        add_wallet("real")
    elif choose == "2":
        delete_wallet("real")
    elif choose == "3":
        list_wallet("real")
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def virtual():
    print("""\nPortefeuille Vituel
    1 - Ajouter Société
    2 - Supprimer Société
    3 - Liste Portefeuille
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        home()
    elif choose == "1":
        add_wallet("virtual")
    elif choose == "2":
        delete_wallet("virtual")
    elif choose == "3":
        list_wallet("virtual")
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def add_wallet(param):
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    i = 1
    for result in results:
        print("{} - Name: {}".format(i, result[1]))
        i += 1
    print("0 - Retour")
    company = input("Quelle société voulez-vous rajouter ?")
    company = int(company)
    if company == 0:
        home()
    if 0 < company <= len(results):
        company = results[company - 1]
    volume = input("Combien avez-vous de titres ?")
    if volume.isdigit():
        volume = volume
    else:
        print("Merci de rentrer une valeur correcte")
    print(company)
    time.sleep(2)
    check_return(param)


def delete_wallet(param):
    print("Delete")
    time.sleep(2)
    check_return(param)


def list_wallet(param):
    print("List")
    time.sleep(2)
    check_return(param)


def check_return(param):
    if param == "real":
        real()
    elif param == "virtual":
        virtual()
