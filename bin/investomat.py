"""
Investomat by m4k5
24/7 personal automatic investor powered with Python
Currently supports:
- Bitcoin (exchanges listed in bitcoin.py)
- gold (logging gold possesions and checking their values from zlotagotowka.pl
"""
import os

import bitcoin
import configure
import gold
import notify
import records

try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'investomat.conf')) as data:
        settings = data.read().splitlines()
        bitbay_api_public = settings[0]
        bitbay_api_secret = settings[1]
        bitfinex_api_public = settings[2]
        bitfinex_api_secret = settings[3]
        address = settings[4]
        amount = settings[5]
        user = settings[6]
        password = settings[7]
        server = settings[8]
        port = settings[9]
        receipent = settings[10]
        gold_possesions = settings[11:]
except (IOError, IndexError, TypeError):
    configure.make_config('investomat.conf')
    exit()
bitbay = bitcoin.BitBayNet(bitbay_api_public, bitbay_api_secret)
bitfinex = bitcoin.Bitfinex(bitfinex_api_public, bitfinex_api_secret)
bitbay_price = bitcoin.crypto_price()
bitcoin_balance = bitcoin.get_address_balance(address)
buy_data = bitbay.buy_crypto(round(float(amount) / bitbay_price, 8), bitbay_price)
bitbay_user_info = bitbay.get_balances()
bitfinex_user_info = bitfinex.get_balances()
bitcoin_value = round((bitbay_user_info['BTC'] + bitfinex_user_info['BTC'] + bitcoin_balance) * bitbay_price, 2)
records_file = records.RecordsLog('investomat.data')
gold_value = gold.gold_value(gold_possesions)
email = '''PLN:     {!s} PLN
Gold:    {!s} PLN
Bitcoin: {!s} PLN
-------> BitBay:   {!s} PLN
-------> Bitfinex: {!s} PLN
TOTAL:   {!s} PLN'''.format(bitbay_user_info['PLN'], gold_value, bitcoin_value,
                            round(bitbay_user_info['BTC'] * bitbay_price, 2),
                            round(bitfinex_user_info['BTC'] * bitbay_price, 2),
                            round(bitbay_user_info['PLN'] + gold_value + bitcoin_value, 2))
print(email)
notify.send_email('Raport Investomat', receipent, email, user, password, server)
records_file.new_record(bitcoin_value, gold_value, bitbay_user_info['PLN'])
