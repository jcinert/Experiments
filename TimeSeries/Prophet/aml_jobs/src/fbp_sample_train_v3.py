# imports
import os
import mlflow
import numpy as np
from random import random

# load libraries
import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from fbprophet import Prophet
import warnings
warnings.filterwarnings('ignore')

# define functions
def main():
    # init
    symbol = 'BTC-USD'
    today = datetime.today().strftime('%Y-%m-%d')
    start_date = '2016-01-01'

    # get data
    df_raw = yf.download(symbol, start_date, today)
    
    # transform
    df_raw.reset_index(inplace=True)
    df = df_raw[["Date", "Open"]]
    new_names = {
        "Date": "ds", 
        "Open": "y",
    }
    df.rename(columns=new_names, inplace=True)

    # model
    m = Prophet(
        seasonality_mode="multiplicative" 
    )
    m.fit(df)

    # forecast
    future = m.make_future_dataframe(periods = 10, include_history=False)
    forecast = m.predict(future)

    # save results
    print(forecast.head(20))
    forecast.to_csv('fbp_forecast.csv', index=False, mode='a', header=True)

    # test
    mlflow.log_param("hello_param", "world")
    mlflow.log_metric("hello_metric", np.random.random_sample())
    os.system(f"echo 'hi Prophet!' > forecast.txt")
    mlflow.log_artifact("forecast.txt")
    mlflow.log_artifact("fbp_forecast.csv")


# run functions
if __name__ == "__main__":
    # run main function
    main()