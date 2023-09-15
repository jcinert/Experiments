import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from pathlib import Path
import os
import requests

def yf_download_data(config, verbose=False):
    """
    Imports price data from YFiannce
    for tickers in 'config'
    and stores in 'price_data.csv'. # TODO pass from config
    Full load always.
    """
    today = datetime.today().strftime('%Y-%m-%d')

    # set CSV file path
    # - expects following structure: (project folder)-->(data,doc,src)-->(src: Data_processing/data_downloader.py)
    path = Path(os.getcwd())
    csv_path = path.absolute()
    csv_path = csv_path / config['folder'] / config['raw_price_data']

    # create headers
    column_names = ['Coin', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    raw_df = pd.DataFrame([],columns=column_names)
    raw_df.to_csv(csv_path, index=False, mode='w', header=True)

    for coin in config['coins_to_import']:
        if verbose:
            print("Importing: {}".format(coin['name']))
        # get data
        raw_df = yf.download(coin['name'], coin['date_from'], progress=verbose)

        # adjust data for saving
        raw_df['Coin'] = coin['name']
        raw_df.reset_index(inplace=True)
        raw_df = raw_df.reindex(columns=column_names)

        # save data
        raw_df.to_csv(csv_path, index=False, mode='a', header=False)

    if verbose:
        print('SUCCESS - Import from yfinance completed')
    return 0

def fgi_download_data(config, verbose=False):
    """
    downloads Bitcoin Fear & Greed Index
    source: https://alternative.me/crypto/fear-and-greed-index/
    Full load always.
    TODO: this is only for BTC
    """
    # api-endpoint
    URL = "https://api.alternative.me/fng/?limit=3000"

    # sending get request and saving the response as response object
    r = requests.get(url = URL)

    # convert to df
    df_index = pd.json_normalize(r.json()['data'])
    df_index['Date'] = df_index['timestamp'].apply(covert_date)
    df_index['FGIndex'] = df_index['value'].apply(scale_index)
    
    # adjust columns
    df_index.drop(['value', 'timestamp', 'time_until_update'], axis=1, inplace=True)
    new_names = {
        "value_classification": "FGI_Class", 
    }
    df_index.rename(columns=new_names, inplace=True)

    # set CSV file path
    # - expects following structure: (project folder)-->(data,doc,src)-->(src: Data_processing/data_downloader.py)
    path = Path(os.getcwd())
    csv_path = path.absolute()
    csv_path = csv_path / config['folder'] / config['raw_fgi_data']
    df_index.to_csv(csv_path, index=False, mode='w', header=True)

    # save
    if verbose:
        print('SUCCESS - Import from fgi completed')
    return 0

# ----- helping functions -----
def covert_date(x):
    return datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d')

def scale_index(x):
    return (float(x) / 100)