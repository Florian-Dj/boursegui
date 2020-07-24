# -*- coding: utf-8 -*-

import main
import real_wallet
import virtual_wallet
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
    1 - Transaction
    2 - Liste
    3 - Analyse
    4 - Historique
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        home()
    elif choose == "1":
        submenu_real()
    elif choose == "2":
        real_wallet.list_wallet()
    elif choose == "3":
        real_wallet.analysis_wallet()
    elif choose == "4":
        real_wallet.history_wallet()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        real()


def submenu_real():
    print("""\nPortefeuille Réel
    1 - Achat
    2 - Vente
    3 - Supprimer
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        real()
    elif choose == "1":
        real_wallet.buy_wallet()
    elif choose == "2":
        real_wallet.sell_wallet()
    elif choose == "3":
        real_wallet.delete_wallet()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        submenu_real()


# Virtual Wallet
def virtual():
    print("""\nPortefeuille Virtuel
    1 - Transaction
    2 - Liste
    3 - Analyse
    4 - Historique
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        home()
    elif choose == "1":
        submenu_virtual()
    elif choose == "2":
        virtual_wallet.list_wallet()
    elif choose == "3":
        virtual_wallet.analysis_wallet()
    elif choose == "4":
        real_wallet.history_wallet()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        virtual()


def submenu_virtual():
    print("""\nPortefeuille Virtuel
    1 - Achat
    2 - Vente
    3 - Supprimer
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        virtual()
    elif choose == "1":
        virtual_wallet.buy_wallet()
    elif choose == "2":
        virtual_wallet.sell_wallet()
    elif choose == "3":
        virtual_wallet.delete_wallet()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        submenu_virtual()
