"""
Investomat by m4k5
personal automatic investor
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
except:
    print "CONFIGURE.PY"


exchange = bitcoin.BitBay_net(api_public, api_secret)
bal = exchange.getBalance()
for i in bal:
    if bal[i]['available'] != "0" or bal[i]['locked'] != "0":
        print "Available for {!s}: {!s}".format(i, bal[i]['available'])
        print "Locked for {!s}: {!s}\n".format(i, bal[i]['locked'])


def count_wd(d0, d1, wd=4, f=0):
    while d0 != d1:
        d0 += datetime.timedelta(1)
        if d0.weekday() == 0:
            f += 1
    return f
# print imejl.send_email('Kasomat %s' % datetime.date(), 'maks1823@protonmail.com', 'akt')
