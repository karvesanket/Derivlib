# Ingest data from various APIs - to contain stock price and options data (yfinance, Etrade for now)
# (c) Sanket Karve, 2024
# 2024

# Think of whether to include start and end date for the stock data (Not at present given it's only for vol calcs, but added functionality could do with specific dates)


import yfinance as yf
import pandas as pd
import datetime
import time
import sys

class GetData():

    def __init__(self, symbol: str, period="1mo", interval="1d", prepost=False, actions=True, auto_adjust=True, type="stock", api="yahoo") -> None:
        

        '''
        symbol: Ticker / Symbol of the equity security for which stock or option data is required
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: data interval (intraday data cannot extend last 60 days) Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        prepost: Pre and post market data. Default is false owing to lower liquidity
        actions: stock splits or similar actions. Default set to True
        auto_adjust: Adjusted OHLC for dividends etc. Default is True
        type: stock or option data. Default set to stock data
        api: default set to yahoo. support for etrade and other sources in dev

        '''

        self.symbol = symbol.upper()
        self.period = period
        self.interval = interval
        self.prepost = prepost
        self.actions = actions
        self.auto_adjust = auto_adjust
        self.type = type.lower()
        self.api = api.lower()
        

        # For Options data tackle about the output when building out the volcalc module
        if self.type == "option":
            self.period == None

        

        


        
        