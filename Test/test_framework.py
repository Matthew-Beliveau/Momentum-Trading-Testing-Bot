from google.cloud import storage
import alpaca_trade_api as tradeapi
import pandas as pd
import unittest
import time
from datetime import datetime
from pathlib import Path

"""
  Globals for historical data.
  PREDICTION_MONTH: is a csv for the month between Feburary 2020 and March 2020
  HISTORICAL_DATA_* are csv's for the historical data of the time frame
    specified in the name.
"""
PREDICTION_MONTH = 'prediction_month.csv'
HISTORICAL_DATA_18_MONTHS = 'historical_data_18_months.csv'
HISTORICAL_DATA_24_MONTHS = 'historical_data_24_months.csv'
HISTORICAL_DATA_20_YEARS = 'historical_data_20_years.csv'


class API:

    historical_filename = ''
    api = None

    def setup_API(self, filename):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('ai-final-project')
        if not Path(filename).is_file():
            blob = bucket.blob(filename)
            blob.download_to_filename(filename)
        blob2 = bucket.blob('alpaca-key.txt')
        blob3 = bucket.blob('alpaca-key-ID.txt')
        api_key = blob2.download_as_string()[:-1].decode('utf-8')
        api_id = blob3.download_as_string()[:-1].decode('utf-8')
        return tradeapi.REST(
            key_id=api_id,
            secret_key=api_key,
            api_version='v2',
            base_url='https://paper-api.alpaca.markets')

    def __init__(self, filename):
        self.historical_filename = filename
        self.api = self.setup_API(self.historical_filename)


class DataFrameMethods:

    api = None
    df = None

    def __init__(self, filename):
        self.api = API(filename)
        self.df = pd.read_csv(self.api.historical_filename)

    def get_symbol_list(self):
        return [
            each.symbol for each in self.api.list_assets(status='active')
            if each.exchange == 'NASDAQ' or each.exchange == 'NYSE']

    def get_dataframe_at_date(self, date):
        return self.df.loc[self.df['date'] == date].reset_index(drop=True)

    def get_dataframe_between_dates(self, from_date, to_date):
        return (self.df[(self.df['date'] >= from_date)
                & (self.df['date'] <= to_date)].reset_index(drop=True))

    # Symbols in the NYSE and NASDAQ
    def get_stock_dataframe(self, symbol):
        return self.df.loc[self.df['symbol'] == symbol].reset_index(drop=True)


class UnitTests(unittest.TestCase):

    obj = DataFrameMethods(HISTORICAL_DATA_20_YEARS)

    def test_get_stock_dataframe(self):
        s = 'TESS'
        df = self.obj.get_stock_dataframe(s)
        self.assertEqual(s, df['symbol'][0])

    def test_get_dataframe_at_date(self):
        date = '2019-01-10'
        df = self.obj.get_dataframe_at_date(date)
        s = df['date'][0]
        print(s)
        self.assertEqual(date, s)


if __name__ == '__main__':
    unittest.main()
