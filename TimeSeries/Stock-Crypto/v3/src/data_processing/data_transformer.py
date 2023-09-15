import pandas as pd
from datetime import datetime
from datetime import timedelta
from pathlib import Path
import os
from keras.utils import to_categorical
import talib
import numpy as np

BB_LENGHT = 20
START = 400
CONNECTION_POINT = 1020

def merge_price_fgi_data(config, verbose=False):
    """
    joins f&g data to price data
    """
    # set CSV file path
    # - expects following structure: (project folder)-->(data,doc,src)-->(src: data_processing/data_downloader.py)
    path = Path(os.getcwd())
    fgi_path = path.absolute()
    fgi_path = fgi_path / config['folder'] / config['raw_fgi_data']
    df_fgi_raw = pd.read_csv(fgi_path)

    # read raw price data
    price_path = path.absolute()
    price_path = price_path / config['folder'] / config['raw_price_data']
    df_price_raw = pd.read_csv(price_path)

    # merge fgi and price data
    df_price = df_price_raw[df_price_raw['Date'] > '2018-01-31']
    df_export = pd.merge(df_price, df_fgi_raw, how='left', on=['Date'])

    # add one hot encoding
    total_labels = df_export['FGI_Class'].unique()

    ### map each label to an integer
    mapping = {
        'Extreme Fear': 0,
        'Fear': 1,
        'Neutral': 2,
        'Greed': 3,
        'Extreme Greed': 4,
        np.NaN: 5}

    # integer representation
    fgi_class = df_export['FGI_Class']
    for x in range(len(fgi_class)):
        fgi_class[x] = mapping[fgi_class[x]]

    one_hot_encode = to_categorical(fgi_class)

    df_export['FGI_Class_ef'] = one_hot_encode[:,0]
    df_export['FGI_Class_f'] = one_hot_encode[:,1]
    df_export['FGI_Class_n'] = one_hot_encode[:,2]
    df_export['FGI_Class_g'] = one_hot_encode[:,3]
    df_export['FGI_Class_eg'] = one_hot_encode[:,4]
    df_export['FGI_Class_nan'] = one_hot_encode[:,5]
    df_export.head()

    # save
    data_path = path.absolute()
    data_path_export = data_path / config['folder'] / config['processed_marked_data']
    df_export.to_csv(data_path_export, index=False, mode='w', header=True)

    if verbose:
        print('new data shape: {}'.format(df_export.shape))
        print('SUCCESS - fgi added to price data')
    return 0

def generate_ta_data(config, verbose=False):
    """
    creates TA values and signals
    - typically run after fgi
    """

    # read price data
    # - expects following structure: (project folder)-->(data,doc,src)-->(src: data_processing/data_downloader.py)
    path = Path(os.getcwd())
    price_path = path.absolute()
    price_path = price_path / config['folder'] / config['processed_marked_data']
    df_price_raw = pd.read_csv(price_path)

    '''
    V1 - calculate TA values
    '''
    df_out = df_price_raw.copy()
    for coin in config['coins_to_process']:
        Coin = coin['name']
        # SMA
        df_out.loc[df_out['Coin'] == Coin, 'sma3'] = talib.SMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=3)
        df_out.loc[df_out['Coin'] == Coin, 'sma5'] = talib.SMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=5)
        df_out.loc[df_out['Coin'] == Coin, 'sma7'] = talib.SMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=7)
        df_out.loc[df_out['Coin'] == Coin, 'sma10'] = talib.SMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=10)
        df_out.loc[df_out['Coin'] == Coin, 'sma20'] = talib.SMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=20)
        df_out.loc[df_out['Coin'] == Coin, 'sma50'] = talib.SMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=50)
        df_out.loc[df_out['Coin'] == Coin, 'sma200'] = talib.SMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=200)
        # EMA
        df_out.loc[df_out['Coin'] == Coin, 'ema3'] = talib.EMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=3)
        df_out.loc[df_out['Coin'] == Coin, 'ema5'] = talib.EMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=5)
        df_out.loc[df_out['Coin'] == Coin, 'ema7'] = talib.EMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=7)
        df_out.loc[df_out['Coin'] == Coin, 'ema30'] = talib.EMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=30)
        df_out.loc[df_out['Coin'] == Coin, 'ema50'] = talib.EMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=50)
        df_out.loc[df_out['Coin'] == Coin, 'ema144'] = talib.EMA(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=144)
        # BB
        bb_upperband, bb_middleband, bb_lowerband = talib.BBANDS(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=BB_LENGHT, nbdevup=2, nbdevdn=2, matype=0)
        df_out.loc[df_out['Coin'] == Coin, 'bb_upperband'] = bb_upperband
        df_out.loc[df_out['Coin'] == Coin, 'bb_middleband'] = bb_middleband
        df_out.loc[df_out['Coin'] == Coin, 'bb_lowerband'] = bb_lowerband
        # MACD
        macd, macdsignal, macdhist = talib.MACD(df_out.loc[df_out['Coin'] == Coin, 'Open'], fastperiod=12, slowperiod=26, signalperiod=9)
        df_out.loc[df_out['Coin'] == Coin, 'macd'] = macd
        df_out.loc[df_out['Coin'] == Coin, 'macdsignal'] = macdsignal
        df_out.loc[df_out['Coin'] == Coin, 'macdhist'] = macdhist
        # RSI
        df_out.loc[df_out['Coin'] == Coin, 'rsi'] = talib.RSI(df_out.loc[df_out['Coin'] == Coin, 'Open'], timeperiod=14)
        # V7 - Volume ema7
        df_out.loc[df_out['Coin'] == Coin, 'vol_ema7'] = talib.EMA(df_out.loc[df_out['Coin'] == Coin, 'Volume'], timeperiod=7)

    # trim the NaN values
    df_out.dropna(inplace=True)

    '''
    V2 - MA signals
    - if price > MA value = 1
    - if price < MA value = 0
    '''
    df_out['above_sma5'] = 0
    df_out.loc[df_out['sma5'] < df_out['Open'], 'above_sma5'] = 1
    df_out['above_sma10'] = 0
    df_out.loc[df_out['sma10'] < df_out['Open'], 'above_sma10'] = 1
    df_out['above_sma20'] = 0
    df_out.loc[df_out['sma20'] < df_out['Open'], 'above_sma20'] = 1
    df_out['above_sma50'] = 0
    df_out.loc[df_out['sma50'] < df_out['Open'], 'above_sma50'] = 1
    df_out['above_sma200'] = 0
    df_out.loc[df_out['sma200'] < df_out['Open'], 'above_sma200'] = 1
    # EMA
    df_out['above_ema30'] = 0
    df_out.loc[df_out['ema30'] < df_out['Open'], 'above_ema30'] = 1
    df_out['above_ema50'] = 0
    df_out.loc[df_out['ema50'] < df_out['Open'], 'above_ema50'] = 1
    df_out['above_ema144'] = 0
    df_out.loc[df_out['ema144'] < df_out['Open'], 'above_ema144'] = 1

    '''
    V3 - BB signals
    - https://www.investopedia.com/terms/b/bollingerbands.asp
    - if price > upper line = 100 = sell
    - if price < lower line = 001 = buy
    - if else 010 = sell
    - bucket the hist (one-hot)
    '''
    df_out['bb_signal_above_h'] = 0
    df_out['bb_signal_between'] = 0
    df_out['bb_signal_below_l'] = 0
    df_out.loc[df_out['Open'] > df_out['bb_upperband'], 'bb_signal_above_h'] = 1
    df_out.loc[df_out['Open'] < df_out['bb_lowerband'], 'bb_signal_below_l'] = 1
    df_out.loc[(df_out['Open'] <= df_out['bb_upperband']) & (df_out['Open'] >= df_out['bb_lowerband']), 'bb_signal_between'] = 1

    '''
    V4 - MACD signals
    - https://www.investopedia.com/terms/m/macd.asp
    - if MACD > signal line = 1 = buy
    - if MACD < signal line = 0 = sell
    - bucket the hist (one-hot)
    '''
    df_out['macd_signal'] = 0
    df_out.loc[df_out['macdsignal'] < df_out['macd'], 'macd_signal'] = 1

    ''' 
    V5 - RSI signals
    # - https://www.investopedia.com/terms/r/rsi.asp
    # - An asset is usually considered overbought when the RSI is above 70 and oversold when it is below 30.
    # - The RSI line crossing below the overbought line or above oversold line is often seen by traders as a signal to buy or sell.
    '''
    df_out['rsi_signal_b20'] = 0
    df_out['rsi_signal_b30'] = 0
    df_out['rsi_signal_b40'] = 0
    df_out['rsi_signal_b50'] = 0
    df_out['rsi_signal_b60'] = 0
    df_out['rsi_signal_b70'] = 0
    df_out['rsi_signal_b80'] = 0
    df_out['rsi_signal_a80'] = 0
    df_out.loc[df_out['rsi'] <= 20, 'rsi_signal_b20'] = 1
    df_out.loc[(df_out['rsi'] <= 30) & (df_out['rsi'] >= 20), 'rsi_signal_b30'] = 1
    df_out.loc[(df_out['rsi'] <= 40) & (df_out['rsi'] >= 30), 'rsi_signal_b40'] = 1
    df_out.loc[(df_out['rsi'] <= 50) & (df_out['rsi'] >= 40), 'rsi_signal_b50'] = 1
    df_out.loc[(df_out['rsi'] <= 60) & (df_out['rsi'] >= 50), 'rsi_signal_b60'] = 1
    df_out.loc[(df_out['rsi'] <= 70) & (df_out['rsi'] >= 60), 'rsi_signal_b70'] = 1
    df_out.loc[(df_out['rsi'] <= 80) & (df_out['rsi'] >= 70), 'rsi_signal_b80'] = 1
    df_out.loc[(df_out['rsi'] >= 80), 'rsi_signal_a80'] = 1

    # save
    data_path = path.absolute()
    data_path_export = data_path / config['folder'] / config['processed_marked_data']
    df_out.to_csv(data_path_export, index=False, mode='w', header=True)

    if verbose:
        print('new data shape: {}'.format(df_out.shape))
        print('SUCCESS - TA added to price data')
    return 0

def generate_synth_data(config, verbose=False):
    """
    creates synhetic train data (from BTC)
    - to be run after fgi, before TA
    - Normalize + Concat BTC Open+Low+Close+High+(1% noise), volume+(1% noise), f&g, ma, macd, bb, rsi, ma-signals, bb_signals, macd-signal, rsi_signals (1070:) 
    """

    # read price data
    # - expects following structure: (project folder)-->(data,doc,src)-->(src: data_processing/data_downloader.py)
    path = Path(os.getcwd())
    price_path = path.absolute()
    price_path = price_path / config['folder'] / config['processed_marked_data']
    df_price_data = pd.read_csv(price_path)

    # normalize 
    columns = ['Open','Close','High','Low','Volume']
    df_btc = df_price_data[df_price_data['Coin'] == 'BTC-USD']
    df_btc_s = pd.DataFrame(normalize(df_btc[['Open','Close','High','Low','Volume']]), columns=columns)

    df_eth = df_price_data[df_price_data['Coin'] == 'ETH-USD']
    df_eth_s = pd.DataFrame(normalize(df_eth[['Open','Close','High','Low','Volume']]), columns=columns)

    # concatenate O+L+C+H
    # 1/4 copy the whole data
    df_temp_v4 = df_price_data.copy()
    df_btc_out = df_temp_v4.loc[df_temp_v4['Coin'] == 'BTC-USD',:]
    df_btc_out.reset_index(inplace=True)
    # df_btc_s.reset_index(inplace=True)
    df_btc_out.loc[:,'Open'] = df_btc_s.loc[:,'Open']
    df_btc_out.loc[:,'Volume'] = df_btc_s.loc[:,'Volume']
    df_btc_out.loc[:,'High'] = df_btc_s.loc[:,'High']
    df_btc_out.loc[:,'Low'] = df_btc_s.loc[:,'Low']
    df_btc_out.loc[:,'Close'] = df_btc_s.loc[:,'Close']
    # 2/4 append Low to Open
    df_btc_low = df_btc_out.copy()
    df_btc_low['Open'] = df_btc_s['Low']
    # 3/4 append Close to Open
    df_btc_close = df_btc_out.copy()
    df_btc_close['Open'] = df_btc_s['Close']
    # 4/4 append High to Open
    df_btc_high = df_btc_out.copy()
    df_btc_high['Open'] = df_btc_s['High']
    # concat High/low/open close
    df_signal_v4 = pd.concat([df_btc_out.iloc[START:],df_btc_low.iloc[CONNECTION_POINT:,:],df_btc_close.iloc[CONNECTION_POINT:,:],df_btc_high.iloc[CONNECTION_POINT:,:]], ignore_index=True)

    # add noise
    df_signal_v4['Coin'] = 'Synth'
    df_signal_v4.drop(['index'], axis=1, inplace=True)
    df_signal_v4.reset_index(inplace=True)
    df_signal_v4.drop(['index'], axis=1, inplace=True)
    # 1/3 copy the whole data
    df_noise_v4 = df_signal_v4.copy()
    df_noise_v4 = df_noise_v4.iloc[(CONNECTION_POINT-START):]
    df_out_v4 = df_signal_v4.copy()
    # 2/3 add noise (gausian)
    mu = 0
    sigma_open =  df_noise_v4['Open'].mean()*0.015  # 1.5%
    sigma_vol =  df_noise_v4['Volume'].mean()*0.05  # 5%

    noise_open = np.random.normal(mu, sigma_open, [df_noise_v4.shape[0]])
    noise_vol = np.random.normal(mu, sigma_vol, [df_noise_v4.shape[0]])

    df_noise_v4['Open'] = df_noise_v4['Open'] + noise_open
    df_noise_v4['Volume'] = df_noise_v4['Volume'] + noise_vol
    # 3/3 concatenate
    df_out_v4 = pd.concat([df_out_v4,df_noise_v4], ignore_index=True)
    df_out_v4.reset_index(inplace=True)
    df_out_v4.drop(['index'], axis=1, inplace=True)

    # add TA values for new signal
    # SMA
    df_out_v4.loc[:, 'sma3'] = talib.SMA(df_out_v4.loc[:, 'Open'], timeperiod=3)
    df_out_v4.loc[:, 'sma5'] = talib.SMA(df_out_v4.loc[:, 'Open'], timeperiod=5)
    df_out_v4.loc[:, 'sma7'] = talib.SMA(df_out_v4.loc[:, 'Open'], timeperiod=7)
    df_out_v4.loc[:, 'sma10'] = talib.SMA(df_out_v4.loc[:, 'Open'], timeperiod=10)
    df_out_v4.loc[:, 'sma20'] = talib.SMA(df_out_v4.loc[:, 'Open'], timeperiod=20)
    df_out_v4.loc[:, 'sma50'] = talib.SMA(df_out_v4.loc[:, 'Open'], timeperiod=50)
    df_out_v4.loc[:, 'sma200'] = talib.SMA(df_out_v4.loc[:, 'Open'], timeperiod=200)
    # EMA
    df_out_v4.loc[:, 'ema3'] = talib.EMA(df_out_v4.loc[:, 'Open'], timeperiod=3)
    df_out_v4.loc[:, 'ema5'] = talib.EMA(df_out_v4.loc[:, 'Open'], timeperiod=5)
    df_out_v4.loc[:, 'ema7'] = talib.EMA(df_out_v4.loc[:, 'Open'], timeperiod=7)
    df_out_v4.loc[:, 'ema30'] = talib.EMA(df_out_v4.loc[:, 'Open'], timeperiod=30)
    df_out_v4.loc[:, 'ema50'] = talib.EMA(df_out_v4.loc[:, 'Open'], timeperiod=50)
    df_out_v4.loc[:, 'ema144'] = talib.EMA(df_out_v4.loc[:, 'Open'], timeperiod=144)
    # BB
    bb_upperband, bb_middleband, bb_lowerband = talib.BBANDS(df_out_v4.loc[:, 'Open'], timeperiod=BB_LENGHT, nbdevup=2, nbdevdn=2, matype=0)
    df_out_v4.loc[:, 'bb_upperband'] = bb_upperband
    df_out_v4.loc[:, 'bb_middleband'] = bb_middleband
    df_out_v4.loc[:, 'bb_lowerband'] = bb_lowerband
    # MACD
    macd, macdsignal, macdhist = talib.MACD(df_out_v4.loc[:, 'Open'], fastperiod=12, slowperiod=26, signalperiod=9)
    df_out_v4.loc[:, 'macd'] = macd
    df_out_v4.loc[:, 'macdsignal'] = macdsignal
    df_out_v4.loc[:, 'macdhist'] = macdhist
    # RSI
    df_out_v4.loc[:, 'rsi'] = talib.RSI(df_out_v4.loc[:, 'Open'], timeperiod=14)
    # V7 - Volume ema7
    df_out_v4.loc[:, 'vol_ema7'] = talib.EMA(df_out_v4.loc[:, 'Volume'], timeperiod=7)

    # add TA signal values
    # SMA
    df_out_v4['above_sma5'] = 0
    df_out_v4.loc[df_out_v4['sma5'] < df_out_v4['Open'], 'above_sma5'] = 1
    df_out_v4['above_sma10'] = 0
    df_out_v4.loc[df_out_v4['sma10'] < df_out_v4['Open'], 'above_sma10'] = 1
    df_out_v4['above_sma20'] = 0
    df_out_v4.loc[df_out_v4['sma20'] < df_out_v4['Open'], 'above_sma20'] = 1
    df_out_v4['above_sma50'] = 0
    df_out_v4.loc[df_out_v4['sma50'] < df_out_v4['Open'], 'above_sma50'] = 1
    df_out_v4['above_sma200'] = 0
    df_out_v4.loc[df_out_v4['sma200'] < df_out_v4['Open'], 'above_sma200'] = 1
    # EMA
    df_out_v4['above_ema30'] = 0
    df_out_v4.loc[df_out_v4['ema30'] < df_out_v4['Open'], 'above_ema30'] = 1
    df_out_v4['above_ema50'] = 0
    df_out_v4.loc[df_out_v4['ema50'] < df_out_v4['Open'], 'above_ema50'] = 1
    df_out_v4['above_ema144'] = 0
    df_out_v4.loc[df_out_v4['ema144'] < df_out_v4['Open'], 'above_ema144'] = 1
    # BB
    df_out_v4['bb_signal_above_h'] = 0
    df_out_v4['bb_signal_between'] = 0
    df_out_v4['bb_signal_below_l'] = 0
    df_out_v4.loc[df_out_v4['Open'] > df_out_v4['bb_upperband'], 'bb_signal_above_h'] = 1
    df_out_v4.loc[df_out_v4['Open'] < df_out_v4['bb_lowerband'], 'bb_signal_below_l'] = 1
    df_out_v4.loc[(df_out_v4['Open'] <= df_out_v4['bb_upperband']) & (df_out_v4['Open'] >= df_out_v4['bb_lowerband']), 'bb_signal_between'] = 1
    # MACD
    df_out_v4['macd_signal'] = 0
    df_out_v4.loc[df_out_v4['macdsignal'] < df_out_v4['macd'], 'macd_signal'] = 1
    # RSI
    df_out_v4['rsi_signal_b20'] = 0
    df_out_v4['rsi_signal_b30'] = 0
    df_out_v4['rsi_signal_b40'] = 0
    df_out_v4['rsi_signal_b50'] = 0
    df_out_v4['rsi_signal_b60'] = 0
    df_out_v4['rsi_signal_b70'] = 0
    df_out_v4['rsi_signal_b80'] = 0
    df_out_v4['rsi_signal_a80'] = 0
    df_out_v4.loc[df_out_v4['rsi'] <= 20, 'rsi_signal_b20'] = 1
    df_out_v4.loc[(df_out_v4['rsi'] <= 30) & (df_out_v4['rsi'] >= 20), 'rsi_signal_b30'] = 1
    df_out_v4.loc[(df_out_v4['rsi'] <= 40) & (df_out_v4['rsi'] >= 30), 'rsi_signal_b40'] = 1
    df_out_v4.loc[(df_out_v4['rsi'] <= 50) & (df_out_v4['rsi'] >= 40), 'rsi_signal_b50'] = 1
    df_out_v4.loc[(df_out_v4['rsi'] <= 60) & (df_out_v4['rsi'] >= 50), 'rsi_signal_b60'] = 1
    df_out_v4.loc[(df_out_v4['rsi'] <= 70) & (df_out_v4['rsi'] >= 60), 'rsi_signal_b70'] = 1
    df_out_v4.loc[(df_out_v4['rsi'] <= 80) & (df_out_v4['rsi'] >= 70), 'rsi_signal_b80'] = 1
    df_out_v4.loc[(df_out_v4['rsi'] >= 80), 'rsi_signal_a80'] = 1

    # remove NaN (~200 values from start)
    df_out_v4.dropna(inplace=True)

    # save
    data_path = path.absolute()
    data_path_export = data_path / config['folder'] / config['synt_data']
    df_out_v4.to_csv(data_path_export, index=False, mode='w', header=True)

    if verbose:
        print('new data shape: {}'.format(df_out_v4.shape))
        print('SUCCESS - Synthetic data generated')
    return 0

# ----- helping functions -----
def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        result[feature_name] = (df[feature_name]) / (max_value)
    return result