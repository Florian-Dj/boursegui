# -*- coding: utf-8 -*-

import database
import datetime
import requests
from bs4 import BeautifulSoup


def parse(results):
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    if "9:29AM" < time_now < "5:40PM":
        print("Bourse fermée")
        pass
    datetime_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print()
    print("--- {t} ---".format(t=datetime_now))
    print()
    for result in results:
        url = "https://www.boursorama.com/cours/" + result[2]
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
        value = soup.find_all('span', class_="c-instrument c-instrument--last")[0].text
        var = soup.find_all('span', class_="c-instrument c-instrument--variation")[0].text
        volume = soup.find_all('span', class_="c-instrument c-instrument--totalvolume")[0].text.replace(" ", "")
        vol_var = soup.find_all('li', class_="c-list-info__item--small-gutter")[2]
        vol_var = vol_var.text.replace(" ", "").split("\n")[3]
        dividend_date = soup.find_all('li', class_="c-list-info__item c-list-info__item--fixed-width")[1]
        dividend_date = dividend_date.text.replace(" ", "").split("\n")[3].split(".")
        dividend_date = "20{}-{}-{}".format(dividend_date[2], dividend_date[1], dividend_date[0])
        value_div = []
        value_div_20 = soup.find('li', class_="c-list-info__item c-list-info__item--fixed-width")
        value_div_20 = value_div_20.text.replace(" ", "").split("\n")[3]
        if value_div_20 == "-":
            value_div_20 = soup.find('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height"
                                               " c-table__cell--align-top / u-text-left u-text-right u-ellipsis")
            value_div.append(value_div_20.text.replace(" ", "").replace("\n", "").replace("EUR", ""))
        else:
            value_div.append(value_div_20.replace("EUR", ""))
        nb = 1
        while nb <= 5:
            value_div_other = soup.find_all('td', class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height"
                                                " c-table__cell--align-top / u-text-left u-text-right u-ellipsis")[nb]
            value_div.append(value_div_other.text.replace(" ", "").replace("\n", "").replace("EUR", ""))
            nb += 1
        sql = """INSERT INTO company (company_id, value, var, volume, vol_var, date_update)
                VALUES ({}, '{}', '{}', {}, '{}', '{}')"""\
            .format(result[0], value, var, volume, vol_var, datetime_now)
        req = database.insert_data(sql)
        if req == "update":
            sql = """UPDATE company SET value = '{}', var = '{}', volume = {}, vol_var = '{}', date_update = '{}'
                    WHERE company_id = {}""".format(value, var, volume, vol_var, datetime_now, result[0])
            database.insert_data(sql)
        print("\t\t{n}\nAction: {val}€\t{var}\nVolume: {vo}\t{vov}\nDividende: {vd}€\t{vp}\t{dd} "
              .format(n=name, val=value, var=var, vo=volume, vov=vol_var, vd=value_div[0], vp=value_div[3], dd=dividend_date))
        print()
