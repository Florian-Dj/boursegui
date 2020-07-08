# -*- coding: utf-8 -*-

import main
import time


def home():
    print("""
    1 - Liste Dividende
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    elif choose == "1":
        list_dividend()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def list_dividend():
    print("Ok")
