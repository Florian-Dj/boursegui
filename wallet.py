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
    1 - Ajouter Action
    2 - Supprimer Action
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
    value = None
    volume = None
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    print()
    i = 1
    for result in results:
        print("{} - Name: {}".format(i, result[1]))
        i += 1
    print("0 - Retour\n")
    company = input("Quelle société voulez-vous rajouter ?")
    company = int(company)
    if company == 0:
        home()
    if 0 < company <= len(results):
        company = results[company - 1]
    try:
        volume = int(input("Combien avez-vous de titres ?"))
    except ValueError:
        print("Merci de rentrer une valeur correcte")
        time.sleep(2)
        add_wallet(param)
    try:
        value = float(input("Quel prix unitaire ?"))
    except ValueError:
        print("Merci de rentrer une valeur correcte")
        time.sleep(2)
        add_wallet(param)
    print(company[0], volume, value)
    sql = """INSERT INTO real_wallet (company_id, volume, value) VALUES ({}, {}, {})""".format(company[0], volume, value)
    result = database.insert(sql)
    if result == "good":
        total = volume * value
        print("Ajout Action\nNom: {n}; Volume: {vo}; Value: {va}€; Total: {t}€"
              .format(n=company[1], vo=volume, va=value, t=total))
    time.sleep(2)
    check_return(param)


def delete_wallet(param):
    print("Delete")
    time.sleep(2)
    check_return(param)


def list_wallet(param):
    sql = """SELECT my_list.name, volume, value FROM real_wallet
            LEFT JOIN my_list ON my_list.id = real_wallet.company_id"""
    results = database.select(sql)
    for result in results:
        total = result[1] * result[2]
        print("Nom: {}; Volume: {}; Value: {}€; Investissement: {}€".format(result[0], result[1], result[2], total))
    time.sleep(2)
    check_return(param)


def check_return(param):
    if param == "real":
        real()
    elif param == "virtual":
        virtual()
