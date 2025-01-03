# (c) Sanket Karve, 2024
# 2024

import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay

def dayfinder(df):
    '''
    Custom function to find end of the week and month, Mark via 1 in new column to help with resampling without taking the means etc
    '''
    

# Add check to see if dataframe is daily weekly etc. frequency of the data. Asssume daily for now
def stockret(df, rettype="daily"):
    '''
    df = DataFrame to be passed with stock data. Price column named as Close
    rettype = Return Frequency. daily, weekly and monthly available. For weekly or monthly stock intervals daily function will get the required interval returns
    '''
    rettype = rettype.lower()

    if rettype == "daily":
        df['DailyPctChg'] = np.log(df['Close'] / df['Close'].shift(1))
        return df
    
    elif rettype == "weekly":
        df['last_business_day'] = df.index.to_series().apply(lambda x: x - BDay(0))
        df["last business day"] = df.last_business_day.max()
        # df['WkPctChg'] = np.log(df['Close'] / df['Close'].shift(1))
        return df

    elif rettype == "montly":
        df.resample("M").ffill()  
        df["MnthPctChg"] = np.log(df["Close"] / df["Close"].shift(1))
        return df
    

# Add thrust indicators tonight


if __name__ == "__main__":
    print("Module containing general and helper functions")