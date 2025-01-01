# Ingest data from various APIs - to contain stock price and options data (yfinance, Etrade for now)
# (c) Sanket Karve, 2024
# 2024

# Think of whether to include start and end date for the stock data (Not at present given it's only for vol calcs, but added functionality could do with specific dates)


import yfinance as yf
import pandas as pd
import datetime
import time
import sys

class Getdata():

    def __init__(self, symbol: str, period="1mo", interval="1d", prepost=False, actions=True, auto_adjust=True, type="stock", api="yahoo") -> None:
        

        '''
        symbol: Ticker / Symbol of the equity security for which stock or option data is required
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: data interval (intraday data cannot extend last 60 days) Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        prepost: Pre and post market data. Default is false owing to lower liquidity
        actions: stock splits or similar actions. Default set to True
        auto_adjust: Adjusted OHLC for dividends etc. Default is True
        type: stock or option data. Default set to stock data
        api: yahoo and FRED available. support for etrade and other sources in dev

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
        
    def ProcessStockData(self, delzero = False):
        '''
        delzero = Whether to delete columns where all values are zero (Usually dividends and stock splits). Default setting is False
        '''
        if self.api == "yahoo":
            df_stock = pd.DataFrame()
            df_stock = yf.Ticker(self.symbol).history(self.period, self.interval, prepost=self.prepost, auto_adjust=self.auto_adjust, actions=self.actions)
            df_stock.index = pd.to_datetime(df_stock.index, format="%Y%m%d")
            df_stock = df_stock.rename_axis("Date")


            if delzero == True:
                df_stock = df_stock.loc[:, df_stock.any()] #Deleting columns with all zero values
                return df_stock
            else:
                return df_stock
        else: #(Change to elif equals etrade etc. for other API functionality)
            pass #Add second API of Etrade here
    
    def ProcessOptData(self, opex = "Yes"):
        self.opex = opex.lower()
        
        options = pd.DataFrame()
        df_opt = yf.Ticker(self.symbol)
        expiry_dt = df_opt.options

        options = pd.DataFrame()

        for e in expiry_dt:       
            opt = df_opt.option_chain(e)
            opt = pd.DataFrame()._append(opt.calls)._append(opt.puts)
            opt['expirationDate'] = e
            options = options._append(opt, ignore_index=True)

            options['expirationDate'] = pd.to_datetime(options['expirationDate'])  
            options['dte'] = (((options['expirationDate'] ) + datetime.timedelta(days = 1)) - datetime.datetime.today()).dt.days
            #Find method to adjust for hourly dte corrections instead of daily. can use pre-ovn-mkt asts

            # Boolean column if the option is a CALL
            options['Type'] = options['contractSymbol'].str[4:].apply(
                lambda x: "C" in x)
            
            options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
            # Using mid price
            options['mid'] = (options['bid'] + options['ask']) / 2 

            #Dropping unwanted columns
            options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange'])

            if self.opex == "No":
                break
            else:
                return(options)
        return(options)


if __name__ == "__main__":
    print("Module handling data ingestion from various APIs")