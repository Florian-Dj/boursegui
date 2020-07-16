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
    print("Add")
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
