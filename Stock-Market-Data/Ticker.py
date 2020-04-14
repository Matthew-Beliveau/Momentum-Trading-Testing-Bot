import yfinance as yf

msft = yf.Ticker("MSFT") # Microsoft stock
"""

returns
<yfinance.Ticker object at 0x1a1715e898>
"""

# get stock info
msft.info
"""
returns:
{
 'quoteType': 'EQUITY',
 'quoteSourceName': 'Nasdaq Real Time Price',
 'currency': 'USD',
 'shortName': 'Microsoft Corporation',
 'exchangeTimezoneName': 'America/New_York',
  ...
 'symbol': 'MSFT'
}
"""

# get historical market data
"""
Available paramaters for the history() method are:

period: data period to download (Either Use period parameter or use start and end) Valid periods are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
interval: data interval (intraday data cannot extend last 60 days) Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
start: If not using period - Download start date string (YYYY-MM-DD) or datetime.
end: If not using period - Download end date string (YYYY-MM-DD) or datetime.
prepost: Include Pre and Post market data in results? (Default is False)
auto_adjust: Adjust all OHLC automatically? (Default is True)
actions: Download stock dividends and stock splits events? (Default is True)
"""
msft.history(period="max")
"""
returns:
              Open    High    Low    Close      Volume  Dividends  Splits
Date
1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
...
2019-04-15  120.94  121.58  120.57  121.05    15792600        0.0     0.0
2019-04-16  121.64  121.65  120.10  120.77    14059700        0.0     0.0
"""

# show actions (dividends, splits)
msft.actions
"""
returns:
            Dividends  Splits
Date
1987-09-21       0.00     2.0
1990-04-16       0.00     2.0
...
2018-11-14       0.46     0.0
2019-02-20       0.46     0.0
"""

# show dividends
msft.dividends
"""
returns:
Date
2003-02-19    0.08
2003-10-15    0.16
...
2018-11-14    0.46
2019-02-20    0.46
"""

# show splits
msft.splits
"""
returns:
Date
1987-09-21    2.0
1990-04-16    2.0
...
1999-03-29    2.0
2003-02-18    2.0
"""

data = yf.download("SPY AAPL", start="2020-01-01", end="2020-02-01")
print(data)
