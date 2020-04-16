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
# TODO: Register a TD Ameritrade API Key and store on google cloud service.
def daily_equity_quotes(event, context):
    # Get the api key from cloud storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('ai-final-project')
    blob = bucket.blob('TD-AMERITRADE-KEY-HERE')
    api_key = blob.download_as_string()
    # Check if the market was open today.  Convert to eastern time zone.
    today = datetime.today().astimezone(pytz.timezone("America/New_York"))
    today_fmt = today.strftime('%Y-%m-%d')

    # Call the td ameritrade hours endpoint for equities to see if it is open
    market_url = 'https://api.tdameritrade.com/v1/marketdata/EQUITY/hours'

    params = {
        'apikey': api_key,
        'date': today_fmt
    }

    request = requests.get(
        url=market_url,
        params=params
        ).json()

    print(request)
    try:
        # potentially problematic line with not using current date.
        if request['equity']['EQ']['isOpen'] is True:
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
                resp = request.get(url)
                site = resp.content
                soup = BeautifulSoup(site, 'html.parser')
                table = soup.find('table', {'class': 'quotes'})
                for row in table.findAll('tr')[1:]:
                    symbols.append(row.findAll('td')[0].text.rstrip())

            # Remove the extra letters.
            symbols_clean = []

            for each in symbols:
                each = each.replace('.', '-')
                symbols_clean.append((each.split('-'[0])))

            # The TD Ameritrade api has a limit to the number of symbols you
            # can get data for
    except KeyError:
        # Not a weekday
        pass

daily_equity_quotes(None, None)
