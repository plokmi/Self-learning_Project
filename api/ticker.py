import json
import requests

while True:

    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/?structure=array'

    limit = 100
    start = 1
    sort = 'rank'
    convert = 'MYR'

    print('Hello, user')
    print()
    print('Please be noticed that the default limit is ' + str(limit) + ' and the start number is ' + str(start) + ' .')
    print()
    print('The sorting would be done by ' + sort + ', and the default currency is ' + convert + ' .')
    print()

    choice = input('Do you want to enter any custom parameters? (y/n): ')

    if choice == 'y':
        print()
        limit = input('What is the custom limit?: ')
        print()
        start = input('What is the custom start number?: ')
        print()
        sort = input('What do you want to sort by?: ')
        print()
        convert = input('What is your preferred currency?: ')
        print()

    ticker_url += '&limit=' + str(limit) + '&sort=' + sort + '&start=' + str(start) + '&convert=' + convert

    request = requests.get(ticker_url)
    results = request.json()

    data = results['data']

    print()
    for currency in data:
        rank = currency['rank']
        name = currency['name']
        symbol = currency['symbol']

        circulating_supply = int(currency['circulating_supply'])
        total_supply = int(currency['total_supply'])

        quotes = currency['quotes'][convert]
        market_cap = quotes['market_cap']
        hour_change = quotes['percent_change_1h']
        day_change = quotes['percent_change_24h']
        week_change = quotes['percent_change_7d']
        price = quotes['price']
        volume = quotes['volume_24h']

        price_string = '{:.2f}'.format(price)
        volume_string = '{:.2f}'.format(volume)
        market_cap_string = '{:.2f}'.format(market_cap)
        circulating_supply_string = '{:.0f}'.format(circulating_supply)
        total_supply_string = '{:.0f}'.format(total_supply)

        coin_in_circulation = (circulating_supply/total_supply*100)
        coin_in_circulation_string = '{:.2f}'.format(coin_in_circulation)

        print(str(rank) + ': ' + name + ' (' + symbol + ')')
        print('Market cap: \t\t$' + market_cap_string)
        print('Price: \t\t\t$' + price_string)
        print('24h Volume: \t\t$' + volume_string)
        print('Hour change: \t\t' + str(hour_change) + '%')
        print('Day change: \t\t' + str(hour_change) + '%')
        print('Week change: \t\t' + str(week_change) + '%')
        print('Total supply: \t\t' + total_supply_string)
        print('Circulating supply: \t' + circulating_supply_string)
        print('Percentage of coins in circulation: ' + coin_in_circulation_string + '%')
        print()

    choice = input('Again? (y/n): ')

    if choice == 'n':
        break
