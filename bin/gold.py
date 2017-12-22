"""
Gold investments interactions:
- fetching gold price
Supported data sources:
- zlotagotowka.pl
"""
import bs4
import requests


def gold_price(keyword):
    """
    fetches actual market's gold selling prives from zlotagotowka.pl, searches and return requested one
    """
    strona = requests.get('https://www.zlotagotowka.pl')
    strona.raise_for_status()
    html = bs4.BeautifulSoup(strona.text, 'html.parser')
    prices = html.select('tr')
    for i in range((len(prices))):
        position = prices[i].getText()
        if keyword in position:
            return float(position[position[1:].find('\n') + 1:])


def gold_value(gold_list):
    value = 0
    for i in gold_list:
        value += gold_price(i)
    return value
