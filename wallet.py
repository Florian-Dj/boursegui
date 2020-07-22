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
        virtual()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


# Real Wallet
def real():
    print("""\nPortefeuille Réel
    1 - Ajouter Action
    2 - Supprimer Action
    3 - Liste Action
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
        print("{} - {}".format(i, result[1]))
        i += 1
    print("0 - Retour\n")
    company = input("Quelle action voulez-vous rajouter ?")
    company = int(company)
    if company == 0:
        real()
    if 0 < company <= len(results):
        company = results[company - 1]
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
    sql = """INSERT INTO real_wallet (company_id, volume, value) VALUES ({}, {}, {})"""\
        .format(company[0], volume, value)
    result = database.insert(sql)
    if result == "good":
        total = volume * value
        print("Ajout Action\n{n}; Volume: {vo}; Valeur: {va}€; Total: {t}€"
              .format(n=company[1], vo=volume, va=value, t=total))
    time.sleep(2)
    real()


def delete_wallet():
    sql = """SELECT my_list.name, value, volume, my_list.id, real_id FROM real_wallet
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
        print(action)
        sql = "DELETE FROM real_wallet WHERE real_id={i}"\
            .format(i=action[4])
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
    if results:
        parse.parse(1)
        investment_total = 0
        resale_total = 0
        win_total = 0
        for result in results:
            investment = result[1] * result[2]
            resale = round(result[1] * result[3], 2)
            diff = round(result[3] - result[2], 2)
            gain = round((result[3] - result[2]) * result[1], 2)
            percentage = round((resale / investment - 1) * 100, 2)
            print("-------- {} ({}) --------\n"
                  "Investissement: {}€  {}€\n"
                  "Revente: {}€  {}€\n"
                  "Gain: {}€  {}€  {}%\n"
                  .format(result[0], result[1], result[2], investment, result[3], resale, diff, gain, percentage))
            investment_total += investment
            resale_total += resale
            win_total += gain
        percentage = round((resale_total / investment_total - 1) * 100, 3)
        print("\n-------- Total --------")
        print("Investissement: {}€\nRevente: {}€\nGain: {}€  {}%\n"
              .format(investment_total, resale_total, win_total, percentage))
    else:
        print("Pas d'actions")
    time.sleep(2)
    real()


# Virtual Wallet
def virtual():
    print("""\nPortefeuille Virtuel
    1 - Acheter Action
    2 - Vendre Action
    3 - Liste Action
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        home()
    elif choose == "1":
        buy_wallet()
    elif choose == "2":
        sell_wallet()
    elif choose == "3":
        list_virtual_wallet()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def buy_wallet():
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    i = 1
    for result in results:
        print("{i} - {n}".format(i=i, n=result[1]))
        i += 1
    print("0 - Retour\n")
    action = input("Quelle action voulez-vous acheter ?")
    action = int(action)
    if action == 0:
        virtual()
    if 0 < action <= len(results):
        volume = 0
        parse.parse(1)
        action = results[action - 1]
        sql = "SELECT * FROM company WHERE company_id={}".format(action[0])
        request = database.select(sql)[0]
        try:
            print("\n--- {}  {}€ ---".format(action[1], request[1]))
            volume = int(input("Combien voulez-vous de titres ?"))
        except ValueError:
            print("Merci de rentrer une valeur correcte")
            time.sleep(2)
            buy_wallet()
        sql = """INSERT INTO virtual_wallet (company_id, volume, value) VALUES ({}, {}, {})""" \
            .format(request[0], volume, request[1])
        result = database.insert(sql)
        if result == "good":
            total = volume * request[1]
            print("Achat Action : {n}; Volume: {vo}; Valeur: {va}€; Total: {t}€"
                  .format(n=action[1], vo=volume, va=request[1], t=total))
    else:
        print("Merci de rentrer une valeur valable")
        time.sleep(2)
        buy_wallet()
    time.sleep(2)
    virtual()


def sell_wallet():
    sql = """SELECT * FROM virtual_wallet
            LEFT JOIN my_list ON my_list.id = virtual_wallet.company_id"""
    results = database.select(sql)
    i = 1
    for result in results:
        print("{i} - {n} : {p}€ {v}".format(i=i, n=result[4], p=result[2], v=result[1]))
        i += 1
    print("0 - Retour\n")
    action = input("Quelle action voulez-vous vendre ?")
    action = int(action)
    if action == 0:
        virtual()
    if 0 < action <= len(results):
        print("Delete")
    time.sleep(2)
    virtual()


def list_virtual_wallet():
    sql = """SELECT my_list.name, virtual_wallet.volume, virtual_wallet.value, company.value FROM virtual_wallet
            LEFT JOIN my_list ON my_list.id = virtual_wallet.company_id
            LEFT JOIN company ON my_list.id = company.company_id"""
    results = database.select(sql)
    parse.parse(1)
    total_win = 0
    if results:
        for result in results:
            investment = result[1] * result[2]
            resale = round(result[1] * result[3], 2)
            diff = round(result[3] - result[2], 2)
            gain = round((result[3] - result[2]) * result[1], 2)
            percentage = round((resale / investment - 1) * 100, 2)
            print("-------- {} ({}) --------\n"
                  "Investissement: {}€  {}€\n"
                  "Revente: {}€  {}€\n"
                  "Gain: {}€  {}€  {}%\n"
                  .format(result[0], result[1], result[2], investment, result[3], resale, diff, gain, percentage))
            total_win += gain
        print("Gain Total: {}€".format(total_win))
    else:
        print("Pas d'actions")
    time.sleep(2)
    virtual()
