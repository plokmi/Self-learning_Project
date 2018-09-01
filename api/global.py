import json
import requests
from datetime import datetime

currency = 'MYR'

global_url = 'https://api.coinmarketcap.com/v2/global/?convert=' + currency

request = requests.get(global_url)
results = request.json()

# print(json.dumps(results, sort_keys=True, indent=4))

active_currencies = results['data']['active_cryptocurrencies']
active_markets = results['data']['active_markets']
bitcoin_dominance = results['data']['bitcoin_percentage_of_market_cap']
last_updated = results['data']['last_updated']
global_cap = int(results['data']['quotes'][currency]['total_market_cap'])
global_vol = int(results['data']['quotes'][currency]['total_volume_24h'])

active_currencies_string = '{:,}'.format(active_currencies)
active_markets_string = '{:,}'.format(active_markets)
global_cap_string = '{:,}'.format(global_cap)
global_vol_string = '{:,}'.format(global_vol)

last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

print()
print('There are currently ' + active_currencies_string + ' active cryptocurrencies and ' + active_markets_string + ' active markets.')
print('The global cap of all cryptocurrencies is ' + currency + ' ' + global_cap_string + ' and the 24h global volume is ' + currency + ' ' + global_vol_string + '.')
print('Bitcoin\'s total percentage of the global cap is ' + str(bitcoin_dominance) + '%.')
print()
print('This information was last updated on ' + last_updated_string + '.')
