# -*- coding: utf-8 -*-

import wallet
import database
import parse
import time


def buy_wallet():
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
        wallet.submenu_real()
    if 0 < company <= len(results):
        company = results[company - 1]
    else:
        print("Merci de rentrer une valeur valable")
        time.sleep(2)
        buy_wallet()
    try:
        volume = int(input("Combien avez-vous de titres ?"))
    except ValueError:
        print("Merci de rentrer une valeur correcte")
        time.sleep(2)
        buy_wallet()
    try:
        value = float(input("Quel prix unitaire ?"))
    except ValueError:
        print("Merci de rentrer une valeur correcte")
        time.sleep(2)
        buy_wallet()
    sql = """INSERT INTO real_wallet (company_id, volume, value, deal) VALUES ({}, {}, {}, '{}')"""\
        .format(company[0], volume, value, "buy")
    result = database.insert(sql)
    if result == "good":
        total = volume * value
        print("\nAjout Action {n} ({vo})\n{va}€/u  Total: {t}€"
              .format(n=company[1], vo=volume, va=value, t=total))
    time.sleep(2)
    wallet.real()


def delete_wallet():
    sql = """SELECT my_list.name, value, volume, my_list.id, real_id FROM real_wallet
            LEFT JOIN my_list ON my_list.id = real_wallet.company_id"""
    results = database.select(sql)
    i = 1
    if results:
        for result in results:
            print("{i} - {n} : {p}€ {v}".format(i=i, n=result[0], p=result[1], v=result[2]))
            i += 1
        print("0 - Retour\n")
        action = input("Quelle action voulez-vous supprimer ?")
        action = int(action)
        if action == 0:
            wallet.real()
        if 0 < action <= len(results):
            action = results[action - 1]
            sql = "DELETE FROM real_wallet WHERE real_id={i}"\
                .format(i=action[4])
            request = database.delete(sql)
            if request == "delete":
                print("----- {n} ({vo}) -----\nValeur: {va}€ supprimé".format(n=action[0], vo=action[2], va=action[1]))
        else:
            print("Merci de rentrer une valeur valable")
            time.sleep(2)
            delete_wallet()
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.submenu_real()


def list_wallet():
    sql = """SELECT * FROM real_wallet
            LEFT JOIN my_list ON my_list.id = real_wallet.company_id"""
    results = database.select(sql)
    print()
    if results:
        for result in results:
            total = result[3] * result[2]
            print("{} ({}) - {}€  {}€".format(result[6], result[2], result[3], total))
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.real()


def analysis_wallet():
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
                  "Achat: {}€  {}€\n"
                  "Revente: {}€  {}€\n"
                  "Gain: {}€  {}€  {}%\n"
                  .format(result[0], result[1], result[2], investment, result[3], resale, diff, gain, percentage))
            investment_total += investment
            resale_total += resale
            win_total += gain
        percentage = round((resale_total / investment_total - 1) * 100, 3)
        print("\n-------- Total --------")
        print("Achat: {}€\n"
              "Revente: {}€\n"
              "Gain: {}€  {}%\n"
              .format(investment_total, resale_total, win_total, percentage))
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.real()


def history_wallet():
    sql = """SELECT my_list.name, real_wallet.value, real_wallet.volume, real_wallet.deal FROM real_wallet
            LEFT JOIN my_list ON my_list.id = real_wallet.company_id"""
    results = database.select(sql)
    buy_list = []
    sell_list = []
    for result in results:
        if result[3] == "buy":
            buy_list.append(result)
        elif result[3] == "sell":
            sell_list.append(result)
    if buy_list:
        print("\n----- Achat Action -----")
        for buy in buy_list:
            print("{} ({}) - {}€/u  {}€".format(buy[0], buy[2], buy[1], buy[1] * buy[2]))
    if sell_list:
        print("\n----- Vente Action -----")
        for sell in sell_list:
            print(sell)
    time.sleep(2)
    wallet.real()
