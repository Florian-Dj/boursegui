# -*- coding: utf-8 -*-

import database
import main
import parse
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
        vitual()
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
        add_wallet()
    elif choose == "2":
        delete_wallet()
    elif choose == "3":
        list_wallet()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def add_wallet():
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
    company = input("Quelle action voulez-vous rajouter ?")
    company = int(company)
    if company == 0:
        real()
    if 0 < company <= len(results):
        company = results[company - 1]
        print(company)
    else:
        print("Merci de rentrer une valeur valable")
        time.sleep(2)
        add_wallet()
    try:
        volume = int(input("Combien avez-vous de titres ?"))
    except ValueError:
        print("Merci de rentrer une valeur correcte")
        time.sleep(2)
        add_wallet()
    try:
        value = float(input("Quel prix unitaire ?"))
    except ValueError:
        print("Merci de rentrer une valeur correcte")
        time.sleep(2)
        add_wallet()
    print(company[0], volume, value)
    sql = """INSERT INTO real_wallet (company_id, volume, value) VALUES ({}, {}, {})"""\
        .format(company[0], volume, value)
    result = database.insert(sql)
    if result == "good":
        total = volume * value
        print("Ajout Action\nNom: {n}; Volume: {vo}; Valeur: {va}€; Total: {t}€"
              .format(n=company[1], vo=volume, va=value, t=total))
    time.sleep(2)
    real()


def delete_wallet():
    sql = """SELECT my_list.name, value, volume, my_list.id FROM real_wallet
            LEFT JOIN my_list ON my_list.id = real_wallet.company_id"""
    results = database.select(sql)
    i = 1
    for result in results:
        print("{i} - {n} : {p}€ {v}".format(i=i, n=result[0], p=result[1], v=result[2]))
        i += 1
    print("0 - Retour\n")
    action = input("Quelle action voulez-vous supprimer ?")
    action = int(action)
    if action == 0:
        real()
    if 0 < action <= len(results):
        action = results[action - 1]
        sql = "DELETE FROM real_wallet WHERE company_id={i} AND volume={vo} AND value="\
            .format(i=action[3], vo=action[2], va=action[1])
        request = database.delete(sql)
        if request == "delete":
            print("Action {n}; Volume: {vo}; Valeur: {va}€ supprimé".format(n=action[0], vo=action[2], va=action[1]))
    else:
        print("Merci de rentrer une valeur valable")
        time.sleep(2)
        delete_wallet()
    time.sleep(2)
    real()


def list_wallet():
    sql = """SELECT my_list.name, real_wallet.volume, real_wallet.value, company.value FROM real_wallet
            LEFT JOIN my_list ON my_list.id = real_wallet.company_id
            LEFT JOIN company ON my_list.id = company.company_id"""
    results = database.select(sql)
    parse.parse(1)
    total_win = 0
    if results:
        for result in results:
            total = result[1] * result[2]
            gain = round((result[3] - result[2]) * result[1], 2)
            print("Nom: {}; Volume: {}\nAchat: {}€; Investissement: {}€\nValeur: {}€; Gain: {}€\n"
                  .format(result[0], result[1], result[2], total, result[3], gain))
            total_win += gain
        print("Gain Total: {}€".format(total_win))
    else:
        print("Pas d'actions")
    time.sleep(2)
    real()
