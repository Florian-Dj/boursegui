# -*- coding: utf-8 -*-

import wallet
import database
import parse
import time


def buy_wallet():
    value = None
    volume = None
    sql = "SELECT * FROM companies"
    results = database.select(sql)
    print()
    if results:
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
        sql = """INSERT INTO real_wallet (company_id, volume, value, deal) VALUES ({}, {}, {}, '{}')"""\
            .format(company[0], volume, value, "buy")
        result = database.insert(sql)
        if result == "good":
            total = volume * value
            print("\nAchat {n} ({vo})\n{va}€/u  Total: {t}€"
                  .format(n=company[1], vo=volume, va=value, t=total))
        time.sleep(2)
        wallet.real()
    else:
        print("Pas d'actions")
        time.sleep(2)
        wallet.submenu_real()


def sell_wallet():
    volume = 0
    value = 0
    sql = """SELECT companies.name, real_wallet.value, real_wallet.volume, companies.id FROM real_wallet
            LEFT JOIN companies ON companies.id = real_wallet.company_id
            WHERE deal = 'buy'"""
    results = database.select(sql)
    i = 1
    print()
    if results:
        for result in results:
            print("{} - {} ({})  {}€/u".format(i, result[0], result[2], result[1]))
            i += 1
        print("0 - Retour")
        company = input("\nQuelle action avez-vous vendu ?")
        company = int(company)
        if company == 0:
            wallet.submenu_real()
        if 0 < company <= len(results):
            company = results[company - 1]
        else:
            print("Merci de rentrer une valeur valable")
            time.sleep(2)
            sell_wallet()
        try:
            volume = int(input("Combien avez-vous vendu de titres ?"))
            if volume > company[2]:
                print("Vous n'avez pas assez de volume ({})".format(company[2]))
                time.sleep(2)
                sell_wallet()
        except ValueError:
            print("Merci de rentrer une valeur correcte")
            time.sleep(2)
            sell_wallet()
        try:
            value = float(input("Quel prix unitaire ?"))
        except ValueError:
            print("Merci de rentrer une valeur correcte")
            time.sleep(2)
            sell_wallet()
        sql = """INSERT INTO real_wallet (company_id, volume, value, deal) VALUES ({}, {}, {}, '{}')"""\
            .format(company[3], volume, value, "sell")
        result = database.insert(sql)
        if result == "good":
            total = volume * value
            print("\nVente {n} ({vo})\n{va}€/u  Total: {t}€"
                  .format(n=company[0], vo=volume, va=value, t=total))
        time.sleep(2)
        wallet.submenu_real()
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.submenu_real()


def delete_wallet():
    sql = """SELECT companies.name, value, volume, companies.id, real_id FROM real_wallet
            LEFT JOIN companies ON companies.id = real_wallet.company_id"""
    results = database.select(sql)
    print()
    i = 1
    if results:
        for result in results:
            print("{i} - {n} : {p}€ {v}".format(i=i, n=result[0], p=result[1], v=result[2]))
            i += 1
        print("0 - Retour\n")
        action = input("Quelle action voulez-vous supprimer ?")
        action = int(action)
        if action == 0:
            wallet.submenu_real()
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
    sql = """SELECT companies.name, round(SUM(volume*value)/SUM(volume),2), real_wallet.volume, SUM(volume) FROM real_wallet
            LEFT JOIN companies ON companies.id = real_wallet.company_id
            GROUP BY real_wallet.company_id"""
    results = database.select(sql)
    print()
    if results:
        for result in results:
            if result[3] > 0:
                print("{} ({}) - {}€/u".format(result[0], result[3], result[1]))
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.real()


def analysis_wallet():
    sql = """SELECT companies.id, companies.name, companies.code,
                    round(SUM(real_wallet.volume*real_wallet.value)/SUM(real_wallet.volume),2),
                    company.value, SUM(real_wallet.volume)
            FROM real_wallet
            LEFT JOIN companies ON companies.id = real_wallet.company_id
            LEFT JOIN company ON companies.id = company.company_id
            GROUP BY real_wallet.company_id"""
    results = database.select(sql)
    print()
    if results:
        parse.parse(1, results, draw=False)
        investment_total = 0
        resale_total = 0
        win_total = 0
        for result in results:
            if result[5] > 0:
                investment = round(result[5] * result[3], 2)
                resale = round(result[5] * result[4], 2)
                diff = round(result[4] - result[3], 2)
                gain = round((result[4] - result[3]) * result[5], 2)
                percentage = round((resale / investment - 1) * 100, 2)
                print("-------- {n} ({v}) --------\n"
                      "Achat: {bu}€/u  {bt}€\n"
                      "Revente: {su}€/u  {st}€\n"
                      "Gain: {gu}€  {gt}€  {p}%\n"
                      .format(n=result[1], v=result[5], bu=result[3], bt=investment, su=result[4], st=resale, gu=diff, gt=gain, p=percentage))
                investment_total += investment
                resale_total += resale
                win_total += gain
        percentage = round((resale_total / investment_total - 1) * 100, 3)
        print("\n-------- Total --------")
        print("Achat: {}€\n"
              "Revente: {}€\n"
              "Gain: {}€  {}%\n"
              .format(investment_total, round(resale_total, 2), win_total, percentage))
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.real()


def history_wallet():
    sql = """SELECT companies.name, real_wallet.value, real_wallet.volume, real_wallet.deal
            FROM real_wallet
            LEFT JOIN companies ON companies.id = real_wallet.company_id"""
    results = database.select(sql)
    buy_list = []
    sell_list = []
    print()
    if results:
        for result in results:
            if result[3] == "buy":
                buy_list.append(result)
            elif result[3] == "sell":
                sell_list.append(result)
        buy_total = 0
        sell_total = 0
        if buy_list:
            print("\n----- Achat Action -----")
            for buy in buy_list:
                total = buy[1] * buy[2]
                print("{} ({}) - {}€/u  {}€".format(buy[0], buy[2], buy[1], total))
                buy_total += total
        if sell_list:
            print("\n----- Vente Action -----")
            for sell in sell_list:
                total = sell[1] * -sell[2]
                print("{} ({}) - {}€/u  {}€".format(sell[0], -sell[2], sell[1], sell_total))
                sell_total += total
        print("\n----- Récap -----")
        print("Achat: {}€\nVente: {}€\nGain: {}€".format(buy_total, sell_total, sell_total-buy_total))
        time.sleep(2)
        wallet.real()
    else:
        print("Pas d'actions")
    time.sleep(2)
    wallet.real()
