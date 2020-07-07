# -*- coding: utf-8 -*-

import parse
import time


def main():
    print("""
    1 - Liste
    2 - Dividende
    3 - CAC40
    0 - Quitter""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        exit()
    elif choose == "1":
        parse.home()
    elif choose == "2":
        print("Dividende")
    elif choose == "3":
        print("Cac40")
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        main()


if __name__ == '__main__':
    main()
