# Ingest data from various APIs - to contain stock price and options data (yfinance, Etrade for now)
# (c) Sanket Karve, 2024
# 2024

import yfinance as yf
import pandas as pd
import datetime
import time
import sys

class GetData():
    def __init__(self, symbol, type="stock", api="yahoo") -> None:
        '''
        symbol: Ticker / Symbol of the equity security for which stock or option data is required
        type: stock or option data. Default set to stock data
        api: default set to yahoo. support for etrade and other sources in dev

        '''

        self.type = type.lower()
        self.api = api.lower()
        
        