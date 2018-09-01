import requests
import json

convert = 'MYR'

listing_url = 'https://api.coinmarketcap.com/v2/listings/'
url_end = '?structure=array&convert=' + convert

request = requests.get(listing_url)
results = request.json()

data = results['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print(ticker_url_pairs)

while True:

    print()
    choice = input('Enter the ticker symbol of a cryptocurrency: ')
    choice = choice.upper()

    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/'+ str(ticker_url_pairs[choice]) + '/' + url_end

    request = requests.get(ticker_url)
    results = request.json()

    currency = results['data'][0]

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
