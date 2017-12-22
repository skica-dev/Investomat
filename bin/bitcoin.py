"""
Bitcoin investments interactions:
- fetching address balance
- fetching exchange balances
- fetching bitcoin price at exchanges
- buying bitcoin throught exchange's api
Supported exchanges:
- BitBay.net
"""
import hashlib
import hmac
import time

import requests


def get_address_balance(address):
    try:
        return float(requests.get(
            'https://blockchain.info/q/addressbalance/' + address).json()) / 10 ** 8
    except ValueError:
        return 0


def btc_price(mode='average', crypto='BTC'):
    """
    fetching actual crypto prices
    types available: average, bid, ask
    """
    return float(requests.get('https://bitbay.net/API/Public/' + crypto
                              + 'PLN/ticker.json').json()[mode])


class BitBayNet(object):
    """class for BitBay.net exchange"""

    def __init__(self, api_public, api_secret):
        self.api_public = str(api_public)
        self.api_secret = str(api_secret)

    def buy_crypto(self, amount, rate, crypto='BTC'):
        """
        buying cryptocurrencies on BitBay.net throught their API
        """
        request = {'method': 'trade', 'moment': str(int(time.time())),
                   'type': 'buy', 'currency': crypto, 'amount': str(amount),
                   'payment_currency': 'PLN', 'rate': str(rate)}
        sign = hmac.new(bytes(self.api_secret.encode('utf-8')),
                        bytes("&".join([i + '=' + request[i] for i in request]).encode('utf-8')), hashlib.sha512)
        return requests.post(
            "https://bitbay.net/API/Trading/tradingApi.php", request,
            headers={'API-Key': self.api_public,
                     'API-Hash': sign.hexdigest()}).json()

    def get_balances(self):
        request = {'method': 'info', 'moment': str(int(time.time()))}
        sign = hmac.new(bytes(self.api_secret.encode('utf-8')),
                        bytes(('&'.join([i + '=' + request[i] for i in request])).encode('utf-8')), hashlib.sha512)
        return requests.post(
            'https://bitbay.net/API/Trading/tradingApi.php',
            request, headers={'API-Key': self.api_public,
                              'API-Hash': sign.hexdigest()}).json()['balances']
