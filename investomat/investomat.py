"""
Kasomat by m4k5
"""
try:
    import hashlib
    import hmac
    import requests
    import time
    import datetime
except ImportError:
    print 'Missing dependencies, please check requirments.'
    exit()
import imejl

# please set up everything using sth.py
with open('data') as data:
    settings = data.readlines()
api_key = settings[0]
api_secret = settings[1]
address = settings[2]


def btc_price():
    return float(requests.get(
        'https://bitbay.net/API/Public/BTCPLN/ticker.json').json()['average'])


def get_add_bal(addr):
    return float(requests.get(
        'https://blockchain.info/q/addressbalance/' + addr).json()) / 10 ** 8


def info_bb(c=True):
    data = {'method': 'info', 'moment': str(int(time.time()))}
    tosign = '&'.join([i + '=' + data[i] for i in data])
    sign = hmac.new(api_secret, tosign, hashlib.sha512)
    resp = requests.post(
        'https://bitbay.net/API/Trading/tradingApi.php',
        data, headers={'API-Key': api_key, 'API-Hash': sign.hexdigest()}).json()
    if c:
        return resp['balances']
    else:
        return resp


def count_wd(d0, d1, wd=4, f=0):
    while d0 != d1:
        d0 += datetime.timedelta(1)
        if d0.weekday() == 0:
            f += 1
    return f


'''
bb_akt = float(info_bb()['PLN']['available']) + \
    float(info_bb()['PLN']['locked'])
btc_bb = float(info_bb()['BTC']['available']) + \
    float(info_bb()['BTC']['locked'])
btc = get_add_bal(address)
actual = int((bb_akt + btc * btc_price()))
print 'Aktualna wartość oszczędności:       ' + '\033[1m' + '\033[92m' + str(actual) + ' PLN' + '\033[0m'
przew = actual + kw_pia * count_wd(datetime.date.today(), data_doc)
print 'Przewidywana wartość oszczędności:   ' + '\033[1m' + str(int(przew * (1.0 - float(info_bb(False)['fee']) / 100))) + ' PLN' + '\033[0m'
'''
print imejl.send_email('Kasomat %s' % datetime.date(), 'maks1823@protonmail.com', 'akt')
