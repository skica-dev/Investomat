"""
Investomat by m4k5
24/7 personal automatic investor powered with Python
Currently supports:
- Bitcoin (exchanges listed in bitcoin.py)
"""
import os

import bitcoin
import configure
import notify

try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'investomat.conf')) as data:
        settings = data.read().splitlines()
        api_public = settings[0]
        api_secret = settings[1]
        address = settings[2]
        amount = settings[3]
        user = settings[4]
        password = settings[5]
        server = settings[6]
        port = settings[7]
        receipent = settings[8]
except (IOError, IndexError, TypeError):
    configure.make_config('investomat.conf')
    exit()
exchange = bitcoin.BitBayNet(api_public, api_secret)
exchange_balances = exchange.get_balances()
exchange_price = bitcoin.btc_price()
bitcoin_balance = bitcoin.get_address_balance(address)
result = ''
for i in exchange_balances:
    if (exchange_balances[i]['available'] != '0' or
            exchange_balances[i]['locked'] != '0'):
        if i != 'PLN':
            result += 'Available for {}: {} {} (~{} PLN)\n'.format(
                i, exchange_balances[i]['available'], i,
                round(float(exchange_balances[i]['available']) * exchange_price, 2))
            result += 'Locked for {}: {} {}\n\n'.format(
                i, exchange_balances[i]['locked'], i)
        else:
            result += 'Available for {}: {} {}\n'.format(
                i, round(float(exchange_balances[i]['available']), 2), i)
            result += 'Locked for {}: {} {}\n\n'.format(
                i, round(float(exchange_balances[i]['locked']), 2), i)
result += 'Address balance is {!s} BTC (~{!s} PLN)\n\n'.format(
    bitcoin_balance, round(bitcoin_balance * exchange_price, 2))
buy_data = exchange.buy_crypto(
    round(float(amount) / exchange_price, 8), exchange_price)
result += 'Bought {!s} satoshis @ {} for {!s} PLN'.format(
    int(buy_data['amount'] * 100000000), buy_data['rate'], round(float(buy_data['price'])), 2)
print(result)
notify.send_email('Report Investomat', receipent, result, user, password,
                  server, port)
