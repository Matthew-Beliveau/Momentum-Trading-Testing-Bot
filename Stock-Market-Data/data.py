import alpaca_trade_api as tradeapi
from google.cloud import storage
from google.cloud import bigquery
import time
import string
from datetime import datetime, timedelta


def daily_equity_quotes(event, context):
    # Get the api key from cloud storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('ai-final-project')
    blob = bucket.blob('alpaca-key.txt')
    api_key = blob.download_as_string()
    # Check if the market was open today.  Convert to eastern time zone.
    today = datetime.today().astimezone(pytz.timezone("America/New_York"))
    today_fmt = today.strftime('%Y-%m-%d')

    # Call the td ameritrade hours endpoint for equities to see if it is open
    maket_url = 'https://api.tdameritrade.com/v1/marketdata/EQUITY/hours'
