import hashlib
import hmac
import requests
import time


def baj(amount, crypto):
    data = {'method': 'trade', 'moment': str(int(time.time(
    ))), 'type': 'buy', 'currency': crypto, 'amount': str(amount), 'payment_currency': 'PLN', 'rate': '20430'}
    tosign = "&".join([i + '=' + data[i] for i in data])
    sign = hmac.new(apisecret, tosign, hashlib.sha512)
    resp = requests.post(
        "https://bitbay.net/API/Trading/tradingApi.php",
        data, headers={'API-Key': apikey, 'API-Hash': sign.hexdigest()}).json()
    return resp
    return resp.json()


if __name__ == '__main__':
    a = 0.00009790
    print baj(a, 'BTC')
