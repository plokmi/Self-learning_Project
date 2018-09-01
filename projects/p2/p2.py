import json
import requests
import time
from datetime import datetime
# for window 10, speech system
import win32com.client as wincl

convert = 'USD'

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

print()
print('ALERT TRACKING...')
print()

already_hit_symbols = []

while True:
    with open('alerts.txt') as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()
            ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

            request = requests.get(ticker_url)
            results = request.json()

            currency = results['data'][0]
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']

            quotes = currency['quotes'][convert]
            price = quotes['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                speak = wincl.Dispatch("SAPI.SpVoice")
                speak.Speak(name + 'hit ' + amount + convert)
                last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')
                print(name + ' hit ' + amount + ' on ' + last_updated_string)
                already_hit_symbols.append(symbol)

    print('...')
    print()
    print('Do you still want to continue tracking?')
    print()
    ask = input('\t\t (y/n) \t\t ')
    ask = ask.lower()

    if ask == 'y':
        print()
        print('Please insert your preferred update period.')
        print()
        interval = input('How many seconds?  t = ')
        print()
        print('...')
        print('Please wait for ' + interval + ' seconds.')
        time.sleep(int(interval))

    else:
        print()
        print('Thank you for using this track service.')
        print()
        print('This application would shut down in 5 seconds')
        time.sleep(5)
        exit()
