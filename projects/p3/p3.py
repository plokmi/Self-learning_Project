import json
import requests
import time
from datetime import datetime
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style

init(convert=True)

convert = 'USD'
sign = '$'

global_url = 'https://api.coinmarketcap.com/v2/global/?convert' + convert

request = requests.get(global_url)
results = request.json()
data = results['data']

global_cap = int(data['quotes'][convert]['total_market_cap'])
global_cap_string = '{:,}'.format(global_cap)

while True:

    print()
    print('Welcome to the CoinMarketCap Explorer Menu!')
    print()
    print('The current global market cap is ' + sign + ' ' + global_cap_string)
    print()
    print('Top 100 coins.')
    print()
    print('Sort by?')
    print()
    print('1 - rank')
    print('2 - 24h change')
    print('3 - 24h volume')
    print('0 - Exit')
    print()
    print('What is your choice? (1-3): ')
    print()
    choice = input('Your choice is   ')

    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/?structure=array&sort='

    if choice == '1':
        ticker_url += 'rank'
    elif choice == '2':
        ticker_url += 'percent_change_24h'
    elif choice == '3':
        ticker_url += 'volume_24h'
    elif choice == '0':
        print()
        print('Thanks for using our service.')
        print()
        print('This application would shut down in 5 seconds.')
        time.sleep(5)
        break
    else:
        print()
        print('Please rerun with correct input!')
        print()
        print('This application would shut down in 5 seconds.')
        time.sleep(5)
        break

    request = requests.get(ticker_url)
    results = request.json()
    data = results['data']

    table = PrettyTable(['Rank', 'Coin', 'Price', 'Market Cap', 'Volume', '1h', '24h', '7d'])
    print()

    for currency in data:
        rank = currency['rank']
        name = currency['name']
        symbol = currency['symbol']
        quotes = currency['quotes'][convert]
        market_cap = quotes['market_cap']
        hour_change = quotes['percent_change_1h']
        day_change = quotes['percent_change_24h']
        week_change = quotes['percent_change_7d']
        price = quotes['price']
        volume = quotes['volume_24h']

        market_cap_string = '{:,}'.format(market_cap)
        volume_string = '{:,}'.format(volume)
        
        if hour_change is not None:
            if hour_change > 0:
                hour_change = Back.GREEN + str(hour_change) + '$' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '$' + Style.RESET_ALL
        if day_change is not None:
            if day_change > 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL
        if week_change is not None:
            if week_change > 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        if volume is not None:
            volume_string = '{:,}'.format(volume)

        if market_cap is not None:
            market_cap_string = '{:,}'.format(market_cap)

        table.add_row([rank,
                        name + ' (' + symbol + ')',
                        sign + str(price,),
                        sign + market_cap_string,
                        sign + volume_string,
                        str(hour_change),
                        str(day_change),
                        str(week_change)])

    print()
    print(table)
    print()

    choice = input('Again? (y/n): ')

    if choice == 'n':
        break
