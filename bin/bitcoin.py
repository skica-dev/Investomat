"""
Bitcoin investments interactions:
- fetching address balance
- fetching exchange balances
- fetching bitcoin price at exchanges
- buying bitcoin throught exchange's api
Supported exchanges:
- BitBay.net
"""
import base64
import hmac
import json
import time

import requests


def get_address_balance(address):
    try:
        return float(requests.get(
            'https://blockchain.info/q/addressbalance/' + address).json()) / 10 ** 8
    except ValueError:
        return 0


def crypto_price(mode='average', crypto='BTC'):
    """
    fetching actual crypto prices at BitBay.net
    types available: average, bid, ask
    """
    return float(requests.get('https://bitbay.net/API/Public/' + crypto
                              + 'PLN/ticker.json').json()[mode])


class BitBayNet(object):
    """class for BitBay.net"""

    def __init__(self, api_public, api_secret):
        self.api_public = str(api_public).encode('utf-8')
        self.api_secret = str(api_secret).encode('utf-8')

    def buy_crypto(self, amount, rate, crypto='BTC'):
        """
        buying cryptocurrencies on BitBay.net throught their API
        """
        request = {'method': 'trade', 'moment': str(int(time.time())),
                   'type': 'buy', 'currency': crypto, 'amount': str(amount),
                   'payment_currency': 'PLN', 'rate': str(rate)}
        sign = hmac.new(bytes(self.api_secret),
                        bytes("&".join([i + '=' + request[i] for i in request]).encode('utf-8')), hashlib.sha512)
        return requests.post(
            'https://bitbay.net/API/Trading/tradingApi.php', request,
            headers={'API-Key': self.api_public,
                     'API-Hash': sign.hexdigest()}).json()

    def get_balances(self):
        request = {'method': 'info', 'moment': str(int(time.time()))}
        sign = hmac.new(bytes(self.api_secret),
                        bytes(('&'.join([i + '=' + request[i] for i in request])).encode('utf-8')), hashlib.sha512)
        balances = requests.post(
            'https://bitbay.net/API/Trading/tradingApi.php',
            request, headers={'API-Key': self.api_public,
                              'API-Hash': sign.hexdigest()}).json()['balances']
        formatted_balances = {}
        account_value = 0
        for i in balances:
            formatted_balances[i] = float(balances[i]['available']) + float(balances[i]['locked'])
            if i == 'PLN':
                formatted_balances[i] = round(formatted_balances[i], 2)
                account_value += formatted_balances[i]
            elif i != 'USD' and i != 'EUR' and formatted_balances[i] != 0:
                formatted_balances[i] = round(formatted_balances[i], 8)
                account_value += formatted_balances[i] * crypto_price('ask', i)
        formatted_balances['account_value'] = round(account_value, 2)
        return formatted_balances


class Bitfinex(object):
    """class for bitfinex.com"""

    def __init__(self, api_public, api_private):
        self.api_public = api_public.encode('utf-8')
        self.api_private = api_private.encode('utf-8')

    def get_balances(self):  # see your balances.
        payload = {
            'request': '/v1/balances',
            'nonce': str(time.time())
        }
        data = base64.b64encode(bytes(json.dumps(payload).encode('utf-8')))
        signed_payload = {
            'X-BFX-APIKEY': self.api_public,
            'X-BFX-SIGNATURE': hmac.new(self.api_private, data, hashlib.sha384).hexdigest(),
            'X-BFX-PAYLOAD': data
        }
        r = requests.post('https://api.bitfinex.com/v1/balances', headers=signed_payload, verify=True)
        rep = r.json()
        balances = {}
        for i in range(len(rep)):
            balances[rep[i]['currency'].upper()] = 0
        for i in range(len(rep)):
            balances[rep[i]['currency'].upper()] += float(rep[i]['amount'])
        return balances
