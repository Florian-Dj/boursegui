# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def parse_cac40():
    companies = []
    i = 1
    while i <= 2:
        url = "https://www.boursorama.com/bourse/actions/cotations/page-{}?quotation_az_filter%5Bmarket%5D=1rPCAC".format(i)
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        values = soup.find_all(class_="o-pack__item u-ellipsis u-color-cerulean")
        for value in values:
            companies.append(value.text)
        i += 1
    print(companies)


if __name__ == '__main__':
    parse_cac40()
