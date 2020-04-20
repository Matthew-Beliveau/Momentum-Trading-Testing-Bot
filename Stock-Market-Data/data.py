import alpaca_trade_api as tradeapi
from google.cloud import storage
from google.cloud import bigquery
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import string
import requests
import pandas as pd
import numpy as np
import pyarrow
import pytz


# TODO: Implement date variable so add functionality for stock market
# simulation.
def daily_equity_quotes(event, context):
    # Get the api key from cloud storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('ai-final-project')
    blob = bucket.blob('alpaca-key.txt')
    blob2 = bucket.blob('alpaca-key-ID.txt')
    api_key = blob.download_as_string()[:-1].decode('utf-8')
    api_id = blob2.download_as_string()[:-1].decode('utf-8')
    api = tradeapi.REST(
        key_id=api_id,
        secret_key=api_key,
        api_version='v2',
        base_url='https://paper-api.alpaca.markets')

    # Check if the market was open today.  Convert to eastern time zone.
    today = datetime.today().astimezone(pytz.timezone("America/New_York"))
    today_fmt = today.strftime('%Y-%m-%d')

    clock = api.get_clock()

    try:
        # potentially problematic line with not using current date.
        # if clock.is_open is True:
        if True:
            # Get a current list of all the stocks symbols for the NYSE.
            # Create a list of every letter in the alphabet.
            # Each page has a letter for all those symbols.
            # i.e. http://eodatta.com/stocklist/NYSE/A.html'
            alpha = list(string.ascii_uppercase)

            symbols = []
            # Loop through the letters in the alphabet to get the stocks on
            # each page from the table and store them in a list
            for each in alpha:
                url = 'http://eoddata.com/stocklist/NYSE/{}.htm'.format(each)
                resp = requests.get(url)
                site = resp.content
                soup = BeautifulSoup(site, 'html.parser')
                table = soup.find('table', {'class': 'quotes'})
                for row in table.findAll('tr')[1:]:
                    symbols.append(row.findAll('td')[0].text.rstrip())

            # Remove the extra letters.
            symbols_clean = []

            for each in symbols:
                each = each.replace('.', '-')
                symbols_clean.append((each.split('-')[0]))

            # The Alpaca api has a limit to the number of requests that can be
            # made for a single call, so we have to call only 200 at a time.
            def chunks(l, n):
                """
                Takes in a list and how long you want
                each chunk to be
                """
                n = max(1, n)
                return (l[i:i+n] for i in range(0, len(l), n))


            symbols_chunked = list(chunks(list(set(symbols_clean)), 200))

            # Function for the api request to get the data from Alpaca
            def quotes_request(stocks):
                """
                Makes an API call for a list of stock symbols and
                returns a dataframe
                """
                barset = api.get_barset(stocks, 'day', 1)
                time.sleep(1)

                return pd.DataFrame.from_dict(
                    barset,
                    orient='index'
                    ).reset_index(drop=True)

            # Loop through the chunked list of symbols
            # and call the api. Append all the resulting dataframs into one
            df = pd.concat([quotes_request(each) for each in symbols_chunked])

    except KeyError:
        # Not a weekday
        pass


daily_equity_quotes(None, None)
