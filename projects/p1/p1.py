import json
import requests
import time
from datetime import datetime
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style

init(convert=True)

convert = 'USD'
sign = '$'

print()
print('Welcome to Alex\'s portfolio!')
print()

print('The default value is shown in USD, do you want to change the notation?')
print()
ask = input('\t\t (y/n) \t\t ')
ask = ask.lower()

if  ask == 'y':
    print()
    convert = input('Please type in your desired notation = ')
    convert = convert.upper()
    print()

    if convert == 'MYR':
        sign = 'RM '

    else:
        print('Sorry, the currency is not supported at the moment!')
        print()
        print('This would be shown in the notation of USD')
        convert = 'USD'
        print()

elif ask == 'n':
    print()
    print('Okay, Please wait for the portfolio to load.')
    print()

else:
    print('Please select \'y\' or \'n\' only!')
    print()
    print('Please rerun the program! Use \'Ctrl + C\' to exit!')
    print()
    print('Alternatively, this program will close in 5 seconds')
    time.sleep(5)
    exit()

listing_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert

url_end = '?structure=array&convert=' + convert

request = requests.get(listing_url)
results = request.json()
data = results['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Coin', 'Amount', convert + ' Value', 'Price', '1h', '24h', '7d'])

with open('portfolio.txt') as inp:
    for line in inp:
        ticker, amount = line.split()
        ticker = ticker.upper()

        ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

        request = requests.get(ticker_url)
        results = request.json()

        currency = results['data'][0]
        rank = currency['rank']
        name = currency['name']
        last_updated = currency['last_updated']
        symbol = currency['symbol']

        quotes = currency['quotes'][convert]
        hour_change = quotes['percent_change_1h']
        day_change = quotes['percent_change_24h']
        week_change = quotes['percent_change_7d']
        price = quotes['price']

        value = float(price) * float(amount)

        if hour_change > 0:
            hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
        else:
            hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if day_change > 0:
            day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
        else:
            day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if week_change > 0:
            week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
        else:
            week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        portfolio_value += value

        value_string = '{:,}'.format(round(value,2))

        table.add_row([name + ' (' + symbol + ')',
                        amount,
                        sign + value_string,
                        sign + str(round(price,2)),
                        str(hour_change),
                        str(day_change),
                        str(week_change)])

print(table)
print()

portfolio_value_string = '{:,}'.format(round(portfolio_value,2))
last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

print('Total Portfolio Value: ' + Back.GREEN + sign + portfolio_value_string + Style.RESET_ALL)
print()
print('API Results Last Updated on ' + last_updated_string)
print()
