"""
Investomat by m4k5
24/7 personal automatic investor powered with Python
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
import notify
import bitcoin
try:
    with open('data') as data:
        settings = data.read().splitlines()
        api_public = settings[0]
        api_secret = settings[1]
        address = settings[2]
except (IOError, IndexError):
    print 'CONFIGURE.PY'
    exit()


exchange = bitcoin.BitBay_net(api_public, api_secret)
exchange_balances = exchange.getBalance()
exchange_price = exchange.btcPrice()
result = ''
for i in exchange_balances:
    if (exchange_balances[i]['available'] != '0' or exchange_balances[i]['locked'] != '0'):
        if i != 'PLN':
            result += 'Available for {}: {} {}\n'.format(
                i, exchange_balances[i]['available'], i)
            result += 'Locked for {}: {} {}\n\n'.format(
                i, exchange_balances[i]['locked'], i)
        else:
            result += 'Available for {}: {} {}\n'.format(
                i, round(float(exchange_balances[i]['available']), 2), i)
            result += 'Locked for {}: {} {}\n\n'.format(
                i, round(float(exchange_balances[i]['locked']), 2), i)
bitcoin_balance = bitcoin.getAddressBalance(address)
result += 'Address balance is {!s} (~{!s} PLN)\n'.format(
    bitcoin_balance, round(bitcoin_balance * exchange_price, 2))
print result

"""
def count_wd(d0, d1, wd=4, f=0):
    while d0 != d1:
        d0 += datetime.timedelta(1)
        if d0.weekday() == 0:
            f += 1
    return f
"""
