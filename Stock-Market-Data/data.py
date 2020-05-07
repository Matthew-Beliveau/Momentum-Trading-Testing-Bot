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
from pandas import json_normalize


# TODO: implement date function to work on past date's data as if it were today
def daily_equity_quotes(event, context):
    # Get the api key from cloud storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('ai-final-project')
    blob = bucket.blob('alpaca-key.txt')
    blob2 = bucket.blob('alpaca-key-ID.txt')
    api_key = blob.download_as_string()[:-1].decode('utf-8')
    api_id = blob2.download_as_string()[:-1].decode('utf-8')
    api = tradeapi.REST(
        key_id="api_id",
        secret_key="api_key",
        api_version='v2',
        base_url='https://api.alpaca.markets')

    # Check if the market was open today.  Convert to eastern time zone.
    today = datetime.today().astimezone(pytz.timezone("America/New_York"))
    today_fmt = today.strftime('%Y-%m-%d')

    clock = api.get_clock()

    try:
        if clock.is_open is True:
            # Call API endpoint to get snapshot of all symbols.
            url = "https://api.polygon.io/v2/snapshot/locale/us/markets/stocks\
                    /tickers/"
            params = {
                'apiKey': api_id,
            }

            request = requests.get(
                url=url,
                params=params
            ).json()

            request.pop('status')
            df = pd.json_normalize(request['tickers'], sep="_")

            # Add the date and fmt the dates for BQ
            df['date'] = pd.to_datetime(today_fmt)
            df['date'] = df['date'].dt.date
            df = df.loc[df['lastQuote_p'] > 0]
            # Add to bigquery
            client = bigquery.Client()

            dataset_id = 'equity_data'
            table_id = 'daily_quote_data'

            dataset_ref = client.dataset(dataset_id)
            table_ref = dataset_ref.table(table_id)

            job_config = bigquery.LoadJobConfig()
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.autodetect = True
            job_config.ignore_unknown_values = True
            job = client.load_table_from_dataframe(
                df,
                table_ref,
                location='US',
                job_config=job_config
            )

            job.result()

            return 'Success'

        else:
            # Not Open
            pass
    except KeyError:
        # Not a weekday
        pass
