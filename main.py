# -*- coding: utf-8 -*-

import parse
import time


def main():
    print("""
    1 - Run
    2 - Société
    3 - Dividende
    4 - Portefeuille
    0 - Quitter""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        exit()
    elif choose == "1":
        parse.parse()
    elif choose == "2":
        parse.home()
    elif choose == "3":
        print("Dividende")
    elif choose == "4":
        print("Portefeuille")
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        main()


if __name__ == '__main__':
    main()
