"""
reusable module to interact with BitBay.net
"""
import hashlib
import hmac
import requests
import time


def buy_crypto(amount, rate, apikey, apisecret, crypto='BTC'):
    """
    buying cryptocurrencies on bitbay throught their API
    """
    data = {'method': 'trade', 'moment': str(int(time.time())),
            'type': 'buy', 'currency': crypto, 'amount': str(amount),
            'payment_currency': 'PLN', 'rate': str(rate)}
    sign = hmac.new(apisecret, "&".join(
        [i + '=' + data[i] for i in data]), hashlib.sha512)
    response = requests.post(
        "https://bitbay.net/API/Trading/tradingApi.php",
        data, headers={'API-Key': apikey, 'API-Hash': sign.hexdigest()}).json()
    return response
