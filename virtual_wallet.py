# -*- coding: utf-8 -*-

import wallet
import database
import parse
import time
import datetime


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
    company = input("Quelle action avez-vous acheté ?")
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
    sql = """INSERT INTO virtual_wallet (company_id, volume, value, deal) VALUES ({}, {}, {}, '{}')"""\
        .format(company[0], volume, value, "buy")
    result = database.insert(sql)
    if result == "good":
        total = volume * value
        print("\nAchat {n} ({vo})\n{va}€/u  Total: {t}€"
              .format(n=company[1], vo=volume, va=value, t=total))
    time.sleep(2)
    wallet.virtual()


def sell_wallet():
    sql = """SELECT my_list.name, virtual_wallet.volume, virtual_wallet.value, company.value, virtual_id FROM virtual_wallet
            LEFT JOIN my_list ON my_list.id = virtual_wallet.company_id
            LEFT JOIN company ON company.company_id = virtual_wallet.company_id"""
    results = database.select(sql)
    i = 1
    for result in results:
        gain = round(result[1] * (result[3] - result[2]), 2)
        print("{i} - {n} ({v}) : Gain: {g}€"
              .format(i=i, n=result[0], p=result[2], v=result[1], g=gain))
        i += 1
    print("0 - Retour\n")
    action = input("Quelle action voulez-vous vendre ?")
    action = int(action)
    if action == 0:
        wallet.virtual()
    if 0 < action <= len(results):
        action = results[action - 1]
        print(action)
        sql = "DELETE FROM virtual_wallet WHERE virtual_id={i}"\
            .format(i=action[4])
        request = database.delete(sql)
        if request == "delete":
            total = action[1] * action[2]
            gain = action[1] * action[3] - total
            print("----- {n} ({vo}) -----\nVente: {va}€   Gain: {g}"
                  .format(n=action[0], vo=action[2], va=total, g=gain))
    time.sleep(2)
    wallet.virtual()


def list_wallet():
    sql = """SELECT * FROM virtual_wallet
            LEFT JOIN my_list ON my_list.id = virtual_wallet.company_id"""
    results = database.select(sql)
    print()
    if results:
        for result in results:
            total = result[3] * result[2]
            print("{} ({}) - {}€  {}€".format(result[6], result[2], result[3], total))
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.virtual()


def analysis_wallet():
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
                  "Achat: {}€  {}€\n"
                  "Revente: {}€  {}€\n"
                  "Gain: {}€  {}€  {}%\n"
                  .format(result[0], result[1], result[2], investment, result[3], resale, diff, gain, percentage))
            total_win += gain
        print("Gain Total: {}€".format(total_win))
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.virtual()
