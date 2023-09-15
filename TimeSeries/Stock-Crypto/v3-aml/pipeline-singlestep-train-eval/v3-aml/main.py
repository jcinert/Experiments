# imports
import os
import mlflow
import argparse
import pandas as pd
from pathlib import Path
# init
from datetime import datetime
from src.common_functions import load_config
# data processing
from src.data_processing.data_downloader import yf_download_data, fgi_download_data
from src.data_processing.data_transformer import merge_price_fgi_data, generate_ta_data, generate_synth_data
# LSTM models
from tqdm import tqdm
import plotly.graph_objects as go
import numpy as np
from src.common_functions import save_forecast
from src.common_functions import load_config, get_backfill_range
import src.lstm.wrapper as lstm

## --------- MAIN FUNCTION ----------------------------------------------------
def main(args):
    # enable logging
    # with mlflow.start_run():

    # data_path = Path(args.data_path) IRNORED for now
    data_path = Path(args.output_folder)
    # print(f"[Init] Mounted input path: {data_path}")
    print(f"[Init] Mounted output path: {data_path}")
    print("[Init] Mounted data_path files: ")
    arr = os.listdir(data_path)
    print(arr)

    # init & get config
    config, days_to_process, TEST_MODE = init(data_path)

    # download, process & save data
    print(f"------------------- DATA PROCESSING -------------------------------------")
    process_data(config, data_path, TEST_MODE)

    # train & score LSTM model 1
    print(f"------------------- MODEL LSTM 1 -------------------------------------")
    train_score_lstm1(config, data_path, days_to_process, TEST_MODE)

    # train & score LSTM model 2
    print(f"------------------- MODEL LSTM 2 -------------------------------------")
    train_score_lstm2(config, data_path, days_to_process, TEST_MODE)

    # train & score LSTM model 3
    print(f"------------------- MODEL LSTM 3 -------------------------------------")
    train_score_lstm(2, data_path, days_to_process, TEST_MODE)
    
    # train & score LSTM model 4
    print(f"------------------- MODEL LSTM 4 -------------------------------------")
    train_score_lstm(3, data_path, days_to_process, TEST_MODE)

    # train & score LSTM model 5
    print(f"------------------- MODEL LSTM 5 -------------------------------------")
    train_score_lstm(4, data_path, days_to_process, TEST_MODE)


## --------- INIT ----------------------------------------------------
def init(data_path):
    # test mode will skip saving results
    TEST_MODE = False
    BACKFILL_MODE = True
    print(f'[Init] Test mode = {TEST_MODE}')
    print(f'[Init] Backfill mode = {BACKFILL_MODE}')

    DATE_FORMAT = '%Y-%m-%d'
    today = datetime.today().strftime(DATE_FORMAT)

    # get number of days forecast wasnt done - mostly 1
    days_to_process = []
    if BACKFILL_MODE == False:
        days_to_process.append(today)
    else:
        days_to_process = get_backfill_range(data_path, verbose=True)
    
    # get config
    config = load_config(verbose=True)
        
    return config, days_to_process, TEST_MODE

## --------- DATA PROCESSING ----------------------------------------------------
def process_data(config, data_path, TEST_MODE):
    # download fresh data
    if TEST_MODE == False:
        result = yf_download_data(config, data_path, verbose=True)
        result = fgi_download_data(config, data_path, verbose=True)
    else:
        print('[Data] Download SKIPPED')

    # process and generate data
    if TEST_MODE == False:
        result = merge_price_fgi_data(config, data_path, verbose=True)
        result = generate_synth_data(config, data_path, verbose=True)
        result = generate_ta_data(config, data_path, verbose=True)
    else:
        print('[Data] Processing SKIPPED')  

## --------- TRAIN-SCORE LSTM MODEL 1 ----------------------------------------------------
def train_score_lstm1(config, data_path, days_to_process, TEST_MODE = True):
    """Trains and scores LSTM model 1

    Data:
    Loads data bases on lstm-config.yaml file
    Outputs forecast to forecast.csv

    Keyword arguments:
    config -- str(yaml), config.yaml
    data_path -- str(or Path), folder path where input & output data is
    TEST_MODE -- bool, True runs training, but does not save the forecast 
    BACKFILL_MODE - bool, process all missing predictions between today and last forecast in forecast.csv
    
    Model 1 - LSTM trained on most of the historic data, including wild peaks of 2020-2021, including synthetic. 
    see __generate_synthetic_data.ipynb__ v4
    """

    ## init
    # get LSTM config
    DATE_FORMAT = '%Y-%m-%d'
    today = datetime.today().strftime(DATE_FORMAT)
    lstm_configs = lstm.load_lstm_config(verbose=True)
    lstm_config_1 = lstm_configs['models'][0] # LSTM model 1

    if not os.path.exists(lstm_config_1['training']['model_save_dir']): os.makedirs(lstm_config_1['training']['model_save_dir'])

    # get data
    x, y, x_val, y_val, x_test, y_test = lstm.get_data(
        lstm_config_1, 
        data_path,
        use_same_train_validation=True, 
        use_same_validation_test=True, 
        verbose='Summary'
        )

    # get data - not normalized for viz
    lstm_config_1['data']['normalise'] = False
    x2, y2, x_val2, y_val2, x_test_viz, y_test_viz = lstm.get_data(
        lstm_config_1, 
        data_path,
        use_same_train_validation=True, 
        use_same_validation_test=True, 
        verbose='Summary'
        )

    # train model
    m = lstm.train_model(lstm_config_1, x, y, x_val, y_val, verbose='Summary')

    fig_acc = lstm.test_model(lstm_config_1, m, x_test, y_test, x_test_viz, y_test_viz, verbose='Summary')
    fig_acc.show()

    # score model
    for day in tqdm(days_to_process):
        days_shift = (datetime.strptime(today, DATE_FORMAT) - datetime.strptime(day, DATE_FORMAT)).days

        # Forecast
        todays_window = lstm.get_todays_data(lstm_config_1,data_path,days_shift,verbose='Summary')
        todays_window_temp = []
        todays_window_temp.append(todays_window)
        todays_pred = m.predict_sequence_full_tbl(todays_window_temp)

        # target_names = ['-1', '0', '1']
        predictions_argmax = np.argmax(todays_pred[:], axis=1)
        if predictions_argmax[0] == 0:
            pred_direction = '-1.0'
        elif predictions_argmax[0] == 1:
            pred_direction = '0.0'
        else:
            pred_direction = '1.0'

        # Create DataFrame
        df_pred_lstm = pd.DataFrame(
            {'Date': [day],
            'Coin': ['BTC-USD'],
            'Label': [pred_direction]})
            
        # save forecast
        if TEST_MODE:
            print('Test mode - saving skipped')
        else:
            # save tbl forecast
            save_forecast(
                data_path,
                df_pred_lstm,
                model='lstm-tb', 
                value_column='Label', 
                verbose=False)
            
    print('Todays prediction confidence: {}'.format(todays_pred))
    print('Todays prediction direction: {}'.format(pred_direction))

## --------- TRAIN-SCORE LSTM MODEL 2 ----------------------------------------------------
def train_score_lstm2(config, data_path, days_to_process, TEST_MODE = True):
    """Trains and scores LSTM model 2

    Data:
    Loads data bases on lstm-config.yaml file
    Outputs forecast to forecast.csv

    Keyword arguments:
    config -- str(yaml), config.yaml
    data_path -- str(or Path), folder path where input & output data is
    TEST_MODE -- bool, True runs training, but does not save the forecast 
    BACKFILL_MODE - bool, process all missing predictions between today and last forecast in forecast.csv
    
    Model 2 - LSTM trained on only recent data enhanced with synthetic data - see generate_synthetic_data v5.5
    """

    # --------- GENERATE data for LSTM2 ---------
    #TODO - move to wrapper (if model results are good)
    # settings - only used for V5
    SOURCE_FILE = 'processed_market_data_v7.csv'
    OUTPUT_FILE = 'synth_market_data_v5_5_train.csv'
    TEST_FILE = 'synth_market_data_v5_5_test.csv'

    # set data path
    if data_path == '':
        path = Path(os.getcwd())
        data_path = path.absolute()
    else:
        data_path = Path(data_path).absolute()

    price_path = data_path / SOURCE_FILE
    df_price_data = pd.read_csv(price_path)

    # limits data to a subset
    # train set: TRAIN_FROM ---- CONNECTION_POINT_1 + CONNECTION_POINT_2 --- TRAIN_TO (repeated 4x)
    # test set: TRAIN_TO ---- end
    TRAIN_FROM = 1400    # 5.3 was 850
    TRAIN_TO = 1659      # 5.3 was 1535 
    TEST_FROM = 1530     # 5.3 was TRAIN_TO

    BB_LENGHT = 20
    CONNECTION_POINT_1 = 1420 # 5.3 was 867
    CONNECTION_POINT_2 = 1421 # 5.3 was 1362

    df_btc_temp = df_price_data.loc[df_price_data['Coin'] == 'BTC-USD',:]
    df_btc_cut = pd.concat([df_btc_temp.iloc[TRAIN_FROM:CONNECTION_POINT_1],df_btc_temp.iloc[CONNECTION_POINT_2:TRAIN_TO]], ignore_index=True)

    # viz
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y = df_btc_cut['Open'], 
        name='Open'))

    fig.update_layout(title_text= 'BTC Open CUT')
    fig.update_layout(template="plotly_dark")
    fig.show()

    def normalize(df):
        result = df.copy()
        for feature_name in df.columns:
            max_value = df[feature_name].max()
            result[feature_name] = (df[feature_name]) / (max_value)
        return result

    import talib

    # normalize 
    columns = ['Open','Close','High','Low','Volume']
    df_btc = df_price_data[df_price_data['Coin'] == 'BTC-USD']
    df_btc_s = pd.DataFrame(normalize(df_btc[['Open','Close','High','Low','Volume']]), columns=columns)

    df_eth = df_price_data[df_price_data['Coin'] == 'ETH-USD']
    df_eth_s = pd.DataFrame(normalize(df_eth[['Open','Close','High','Low','Volume']]), columns=columns)

    # concatenate O+L+C+H
    # 1/4 copy the whole data
    df_temp_v5 = df_price_data.copy()
    df_btc_out = df_temp_v5.loc[df_temp_v5['Coin'] == 'BTC-USD',:]
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
    # V5 - cut part of the series only
    # concat High/low/open close
    df_signal_v5 = pd.concat([df_btc_out.iloc[TRAIN_FROM:CONNECTION_POINT_1],df_btc_out.iloc[CONNECTION_POINT_2:TRAIN_TO],
                            df_btc_low.iloc[TRAIN_FROM:CONNECTION_POINT_1],df_btc_low.iloc[CONNECTION_POINT_2:TRAIN_TO],
                            df_btc_close.iloc[TRAIN_FROM:CONNECTION_POINT_1],df_btc_close.iloc[CONNECTION_POINT_2:TRAIN_TO],
                            df_btc_high.iloc[TRAIN_FROM:CONNECTION_POINT_1],df_btc_high.iloc[CONNECTION_POINT_2:TRAIN_TO],
                            ], ignore_index=True)

    # add noise
    df_signal_v5['Coin'] = 'Synth'
    df_signal_v5.drop(['index'], axis=1, inplace=True)
    df_signal_v5.reset_index(inplace=True)
    df_signal_v5.drop(['index'], axis=1, inplace=True)
    # 1/3 copy the whole data
    df_noise_v5 = df_signal_v5.copy()
    #df_noise_v5 = df_noise_v5.iloc[(CONNECTION_POINT-START):]
    df_out_v5 = df_signal_v5.copy()
    # 2/3 add noise (gausian)
    mu = 0
    sigma_open =  df_noise_v5['Open'].mean()*0.015  # 1.5%
    sigma_vol =  df_noise_v5['Volume'].mean()*0.05  # 5%

    noise_open = np.random.normal(mu, sigma_open, [df_noise_v5.shape[0]])
    noise_vol = np.random.normal(mu, sigma_vol, [df_noise_v5.shape[0]])

    df_noise_v5['Open'] = df_noise_v5['Open'] + noise_open
    df_noise_v5['Volume'] = df_noise_v5['Volume'] + noise_vol
    # 3/3 concatenate
    df_out_v5 = pd.concat([df_out_v5,df_noise_v5], ignore_index=True)
    df_out_v5.reset_index(inplace=True)
    df_out_v5.drop(['index'], axis=1, inplace=True)

    # add TA values for new signal
    # SMA
    df_out_v5.loc[:, 'sma5'] = talib.SMA(df_out_v5.loc[:, 'Open'], timeperiod=5)
    df_out_v5.loc[:, 'sma10'] = talib.SMA(df_out_v5.loc[:, 'Open'], timeperiod=10)
    df_out_v5.loc[:, 'sma20'] = talib.SMA(df_out_v5.loc[:, 'Open'], timeperiod=20)
    df_out_v5.loc[:, 'sma50'] = talib.SMA(df_out_v5.loc[:, 'Open'], timeperiod=50)
    df_out_v5.loc[:, 'sma200'] = talib.SMA(df_out_v5.loc[:, 'Open'], timeperiod=200)
    # EMA
    df_out_v5.loc[:, 'ema30'] = talib.EMA(df_out_v5.loc[:, 'Open'], timeperiod=30)
    df_out_v5.loc[:, 'ema50'] = talib.EMA(df_out_v5.loc[:, 'Open'], timeperiod=50)
    df_out_v5.loc[:, 'ema144'] = talib.EMA(df_out_v5.loc[:, 'Open'], timeperiod=144)
    # BB
    bb_upperband, bb_middleband, bb_lowerband = talib.BBANDS(df_out_v5.loc[:, 'Open'], timeperiod=BB_LENGHT, nbdevup=2, nbdevdn=2, matype=0)
    df_out_v5.loc[:, 'bb_upperband'] = bb_upperband
    df_out_v5.loc[:, 'bb_middleband'] = bb_middleband
    df_out_v5.loc[:, 'bb_lowerband'] = bb_lowerband
    # MACD
    macd, macdsignal, macdhist = talib.MACD(df_out_v5.loc[:, 'Open'], fastperiod=12, slowperiod=26, signalperiod=9)
    df_out_v5.loc[:, 'macd'] = macd
    df_out_v5.loc[:, 'macdsignal'] = macdsignal
    df_out_v5.loc[:, 'macdhist'] = macdhist
    # RSI
    df_out_v5.loc[:, 'rsi'] = talib.RSI(df_out_v5.loc[:, 'Open'], timeperiod=14)

    # add TA signal values
    # SMA
    df_out_v5['above_sma5'] = 0
    df_out_v5.loc[df_out_v5['sma5'] < df_out_v5['Open'], 'above_sma5'] = 1
    df_out_v5['above_sma10'] = 0
    df_out_v5.loc[df_out_v5['sma10'] < df_out_v5['Open'], 'above_sma10'] = 1
    df_out_v5['above_sma20'] = 0
    df_out_v5.loc[df_out_v5['sma20'] < df_out_v5['Open'], 'above_sma20'] = 1
    df_out_v5['above_sma50'] = 0
    df_out_v5.loc[df_out_v5['sma50'] < df_out_v5['Open'], 'above_sma50'] = 1
    df_out_v5['above_sma200'] = 0
    df_out_v5.loc[df_out_v5['sma200'] < df_out_v5['Open'], 'above_sma200'] = 1
    # EMA
    df_out_v5['above_ema30'] = 0
    df_out_v5.loc[df_out_v5['ema30'] < df_out_v5['Open'], 'above_ema30'] = 1
    df_out_v5['above_ema50'] = 0
    df_out_v5.loc[df_out_v5['ema50'] < df_out_v5['Open'], 'above_ema50'] = 1
    df_out_v5['above_ema144'] = 0
    df_out_v5.loc[df_out_v5['ema144'] < df_out_v5['Open'], 'above_ema144'] = 1
    # BB
    df_out_v5['bb_signal_above_h'] = 0
    df_out_v5['bb_signal_between'] = 0
    df_out_v5['bb_signal_below_l'] = 0
    df_out_v5.loc[df_out_v5['Open'] > df_out_v5['bb_upperband'], 'bb_signal_above_h'] = 1
    df_out_v5.loc[df_out_v5['Open'] < df_out_v5['bb_lowerband'], 'bb_signal_below_l'] = 1
    df_out_v5.loc[(df_out_v5['Open'] <= df_out_v5['bb_upperband']) & (df_out_v5['Open'] >= df_out_v5['bb_lowerband']), 'bb_signal_between'] = 1
    # MACD
    df_out_v5['macd_signal'] = 0
    df_out_v5.loc[df_out_v5['macdsignal'] < df_out_v5['macd'], 'macd_signal'] = 1
    # RSI
    df_out_v5['rsi_signal_b20'] = 0
    df_out_v5['rsi_signal_b30'] = 0
    df_out_v5['rsi_signal_b40'] = 0
    df_out_v5['rsi_signal_b50'] = 0
    df_out_v5['rsi_signal_b60'] = 0
    df_out_v5['rsi_signal_b70'] = 0
    df_out_v5['rsi_signal_b80'] = 0
    df_out_v5['rsi_signal_a80'] = 0
    df_out_v5.loc[df_out_v5['rsi'] <= 20, 'rsi_signal_b20'] = 1
    df_out_v5.loc[(df_out_v5['rsi'] <= 30) & (df_out_v5['rsi'] >= 20), 'rsi_signal_b30'] = 1
    df_out_v5.loc[(df_out_v5['rsi'] <= 40) & (df_out_v5['rsi'] >= 30), 'rsi_signal_b40'] = 1
    df_out_v5.loc[(df_out_v5['rsi'] <= 50) & (df_out_v5['rsi'] >= 40), 'rsi_signal_b50'] = 1
    df_out_v5.loc[(df_out_v5['rsi'] <= 60) & (df_out_v5['rsi'] >= 50), 'rsi_signal_b60'] = 1
    df_out_v5.loc[(df_out_v5['rsi'] <= 70) & (df_out_v5['rsi'] >= 60), 'rsi_signal_b70'] = 1
    df_out_v5.loc[(df_out_v5['rsi'] <= 80) & (df_out_v5['rsi'] >= 70), 'rsi_signal_b80'] = 1
    df_out_v5.loc[(df_out_v5['rsi'] >= 80), 'rsi_signal_a80'] = 1

    # remove NaN (~200 values from start)
    df_out_v5.dropna(inplace=True)

    # viz
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y = df_out_v5['Open'], 
        name='Open'))

    fig.update_layout(title_text= 'BTC Open OUT')
    fig.update_layout(template="plotly_dark")
    fig.show()

    # save - train
    print('new data shape: {}'.format(df_out_v5.shape))
    print('SUCCESS - Synthetic data generated')

    data_path_export = data_path / OUTPUT_FILE

    df_out_v5.to_csv(data_path_export, index=False, mode='w', header=True)

    df_test_v5 = df_btc_out.iloc[TEST_FROM:]
    df_test_v5['Coin'] = 'Synth'
    df_test_v5.drop(['index'], axis=1, inplace=True)
    df_test_v5.reset_index(inplace=True)
    df_test_v5.drop(['index'], axis=1, inplace=True)

    # save - test
    print('new data shape: {}'.format(df_test_v5.shape))
    print('SUCCESS - Synthetic data generated (test)')

    data_path_export = data_path / TEST_FILE
    df_test_v5.to_csv(data_path_export, index=False, mode='w', header=True)

    ## --------- INIT ---------
    DATE_FORMAT = '%Y-%m-%d'
    today = datetime.today().strftime(DATE_FORMAT)
    # get LSTM config
    lstm_configs = lstm.load_lstm_config(verbose=False)
    lstm_config_2 = lstm_configs['models'][1]

    ## --------- GET DATA ---------
    x, y, x_val, y_val, x_test, y_test = lstm.get_data(
        lstm_config_2, 
        data_path,
        use_same_train_validation=True, 
        use_same_validation_test=True, 
        verbose='Summary')

    # reload not normalized for viz
    lstm_config_2['data']['normalise'] = False
    x2, y2, x_val2, y_val2, x_test_viz, y_test_viz = lstm.get_data(
        lstm_config_2, 
        data_path,
        use_same_train_validation=True, 
        use_same_validation_test=True, 
        verbose='Summary')

    ## --------- TRAIN ---------
    m = lstm.train_model(lstm_config_2, x, y, x_val, y_val, verbose='Summary')

    ## --------- TEST ---------
    fig_acc = lstm.test_model(lstm_config_2, m, x_test, y_test, x_test_viz, y_test_viz, verbose='Summary')
    fig_acc.show()

    ## --------- SCORE ---------
    for day in tqdm(days_to_process):
        days_shift = (datetime.strptime(today, DATE_FORMAT) - datetime.strptime(day, DATE_FORMAT)).days

        # Forecast
        todays_window = lstm.get_todays_data(lstm_config_2,data_path,days_shift,verbose='Summary')
        todays_window_temp = []
        todays_window_temp.append(todays_window)
        todays_pred = m.predict_sequence_full_tbl(todays_window_temp)

        # target_names = ['-1', '0', '1']
        predictions_argmax = np.argmax(todays_pred[:], axis=1)
        if predictions_argmax[0] == 0:
            pred_direction = '-1.0'
        elif predictions_argmax[0] == 1:
            pred_direction = '0.0'
        else:
            pred_direction = '1.0'

        # Create DataFrame
        df_pred_lstm = pd.DataFrame(
            {'Date': [day],
            'Coin': ['BTC-USD'],
            'Label': [pred_direction]})
            
        # save forecast
        if TEST_MODE:
            print('Test mode - saving skipped')
        else:
            # save tbl forecast
            save_forecast(
                data_path,
                df_pred_lstm,
                model='lstm-tb-2', 
                value_column='Label', 
                verbose=False)
            
    print('Todays prediction confidence: {}'.format(todays_pred))
    print('Todays prediction direction: {}'.format(pred_direction))

## --------- TRAIN-SCORE LSTM MODEL [id] ----------------------------------------------------
def train_score_lstm(id, data_path, days_to_process, TEST_MODE = True):
    """Trains and scores LSTM model [id]

    Data:
    Loads data bases on lstm-config.yaml file
    Outputs forecast to forecast.csv

    Keyword arguments:
    id -- int, [0,1,...] model id from lstm-config.yaml file
    data_path -- str(or Path), folder path where input & output data is
    TEST_MODE -- bool, True runs training, but does not save the forecast 
    BACKFILL_MODE - bool, process all missing predictions between today and last forecast in forecast.csv
    
    Model [id] - model info in lstm-config.yaml file
    """
    ## --------- INIT ---------
    DATE_FORMAT = '%Y-%m-%d'
    today = datetime.today().strftime(DATE_FORMAT)

    ## --------- GET CONFIG ---------
    # get LSTM config
    lstm_configs = lstm.load_lstm_config(verbose=False)
    lstm_config_x = lstm_configs['models'][id]

    ## --------- GET DATA ---------
    x, y, x_val, y_val, x_test, y_test = lstm.get_data(lstm_config_x, data_path, use_same_train_validation=True, use_same_validation_test=True, verbose='Summary')

    ## --------- TRAIN ---------
    m = lstm.train_model(lstm_config_x, x, y, x_val, y_val, verbose='Summary')

    ## --------- TEST ---------
    # TODO - didnt work for shuffled data
    # fig_acc = lstm.test_model(lstm_config_3, m, x_test, y_test, x_test_viz, y_test_viz, verbose='Summary')
    # fig_acc.show()

    ## --------- SCORE ---------
    for day in tqdm(days_to_process):
        days_shift = (datetime.strptime(today, DATE_FORMAT) - datetime.strptime(day, DATE_FORMAT)).days

        # Forecast
        todays_window = lstm.get_todays_data(lstm_config_x,data_path,days_shift,verbose='Summary')
        todays_window_temp = []
        todays_window_temp.append(todays_window)
        todays_pred = m.predict_sequence_full_tbl(todays_window_temp)

        # target_names = ['-1', '0', '1']
        predictions_argmax = np.argmax(todays_pred[:], axis=1)
        if predictions_argmax[0] == 0:
            pred_direction = '-1.0'
        elif predictions_argmax[0] == 1:
            pred_direction = '0.0'
        else:
            pred_direction = '1.0'

        # Create DataFrame
        df_pred_lstm = pd.DataFrame(
            {'Date': [day],
            'Coin': ['BTC-USD'],
            'Label': [pred_direction]})
            
        # save forecast
        if TEST_MODE:
            print('Test mode - saving skipped')
        else:
            # save tbl forecast
            save_forecast(
                data_path,
                df_pred_lstm,
                model=lstm_config_x['name'], 
                value_column='Label', 
                verbose=False)
            
    print('Todays prediction confidence: {}'.format(todays_pred))
    print('Todays prediction direction: {}'.format(pred_direction))

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--data_path", type=str, help="Path to data - Read only") # ignore
    parser.add_argument("--output_folder", type=str, help="Path to all data - R/W")

    # parse args
    args = parser.parse_args()

    # return args
    return args

# run script
if __name__ == "__main__":
    # parse args
    args = parse_args()

    # run main function
    main(args)
