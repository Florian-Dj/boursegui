# -*- coding: utf-8 -*-

import time
import my_list
import dividend
import database
import parse


def main():
    print("Boursorama Scrape")
    print("By Mucral    V0.2\n\n")
    print("""
    1 - Run
    2 - Ma liste
    3 - Dividende
    4 - Portefeuille
    0 - Quitter""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        exit()
    elif choose == "1":
        parse.home()
    elif choose == "2":
        my_list.home()
    elif choose == "3":
        dividend.home()
    elif choose == "4":
        print("En cours de dév ...")
        time.sleep(2)
        main()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        main()


if __name__ == '__main__':
    database.create_data()
    main()
