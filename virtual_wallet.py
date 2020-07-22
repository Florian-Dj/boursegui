# -*- coding: utf-8 -*-

import wallet
import database
import parse
import time


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
        wallet.virtual()
    if 0 < action <= len(results):
        volume = 0
        parse.parse(1)
        action = results[action - 1]
        sql = "SELECT * FROM company WHERE company_id={}".format(action[0])
        request = database.select(sql)[0]
        try:
            print("\n{} : {}€".format(action[1], request[1]))
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
            print("----- {n} ({vo}) -----\nValeur: {va}€; Total: {t}€"
                  .format(n=action[1], vo=volume, va=request[1], t=total))
    else:
        print("Merci de rentrer une valeur valable")
        time.sleep(2)
        buy_wallet()
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
    for result in results:
        print(result)
        total = result[3] * result[2]
        print("{} ({}) - {}€  {}€".format(result[5], result[2], result[3], total))
    time.sleep(2)
    wallet.real()


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
