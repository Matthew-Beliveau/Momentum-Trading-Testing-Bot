import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import string
import time
from datetime import datetime
from google.cloud import storage
import sys

if(len(sys.argv) < 3):
    print("Invalid amount of arguments. 2 needed: start-date, end-date"\
            " (YY-MM-DD)")
    exit(1)
# Get the historical dates you need.
from_date = sys.argv[1]
to_date = sys.argv[2]

# Get a current list of all the stocks symbols for the NYSE
alpha = list(string.ascii_uppercase)

symbols = []

for each in alpha:
    url = 'http://eoddata.com/stocklist/NYSE/{}.htm'.format(each)
    resp = requests.get(url)
    site = resp.content
    soup = BeautifulSoup(site, 'html.parser')
    table = soup.find('table', {'class': 'quotes'})
    for row in table.findAll('tr')[1:]:
        symbols.append(row.findAll('td')[0].text.rstrip())

# Remove the extra letters on the end
symbols_clean = []
for each in symbols:
    each = each.replace('.', '-')
    symbols_clean.append((each.split('-')[0]))

storage_client = storage.Client()
bucket = storage_client.get_bucket('ai-final-project')
blob = bucket.blob('alpaca-key-ID.txt')
api_id = blob.download_as_string()[:-1].decode('utf-8')

data_list = []

for each in symbols_clean:
    url = fr"https://api.polygon.io/v2/aggs/ticker/{each}/range/1/day"\
            fr"/{from_date}/{to_date}"
    params = {
        'apiKey': api_id
    }

    request = requests.get(
        url=url,
        params=params
    )

    data_list.append(request.json())
    time.sleep(.5)
# Create a list for each data point and loop through the json, adding the data
# to the lists
symbl_l, open_l, high_l, low_l, close_l = [], [], [], [], []
volume_l, date_l = [], []

for data in data_list:
    symbol_name = data['ticker']
    print(symbol_name)
    if symbol_name is None:
        continue
    try:
        for each in data['results']:
            symbl_l.append(symbol_name)
            open_l.append(each['o'])
            high_l.append(each['h'])
            low_l.append(each['l'])
            close_l.append(each['c'])
            volume_l.append(each['v'])
            date_l.append(each['t'])
    except KeyError:
        pass

# Create a datafrom from the lists
df = pd.DataFrame(
     {
        'symbol': symbl_l,
        'open': open_l,
        'high': high_l,
        'low': low_l,
        'close': close_l,
        'volume': volume_l,
        'date': date_l
    }
)

# Format the Dates
df['date'] = pd.to_datetime(df['date'], unit='ms')
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Save to csv
df.to_csv(r'back_data.csv')
