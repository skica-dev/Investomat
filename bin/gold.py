import re

import bs4
import requests


def gold_price(keyword):
    """
    fetches actual market's gold selling prives from zlotagotowka.pl, searches and return requested one/
    """
    strona = requests.get('https://www.zlotagotowka.pl')
    strona.raise_for_status()
    html = bs4.BeautifulSoup(strona.text, 'html.parser')
    prices = html.select('tr')
    for i in range((len(prices))):
        position = prices[i].getText()
        if re.search(keyword, position):
            return float(position[position[1:].find("\n") + 1:])
