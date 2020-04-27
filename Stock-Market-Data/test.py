from google.cloud import storage
import pandas as pd

storage_client = storage.Client()
bucket = storage_client.get_bucket('ai-final-project')
blob = bucket.blob('historical_data_18_months.csv')
blob.download_to_filename("historic_data.csv")


def get_dataframe_at_date(date):
    df = pd.read_csv('his_data.csv')
    return df.loc[df['date'] == date]


def get_dataframe_between_dates(from_date, to_date):
    df = pd.read_csv('his_data.csv')
    return df[(df['date'] >= from_date) & (df['date'] <= to_date)]


# Symbols in the NYSE
def get_stock_dataframe(symbol):
    df = pd.read_csv('his_data.csv')
    return df.loc[df['symbol'] == symbol]
