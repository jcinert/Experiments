"""
    fuctions to process label price data
"""
import numpy as np
import pandas as pd
from sklearn import metrics

def tbl_form_label(df, column_names=['Date','Open'], threshold_type='ratio', threshold=0.05, T=5):
    # input:
    #     df: dataframe (expected columns: Date, Open, High, Low, Close, Adj Close, Volume)
    #     column_names: list, fist date column name, second price column name in df
    #     threshold_type: 'ratio' or 'specific'
    #     threshold: value
    #     T: length of triple barries
    # output:
    #     label: array, (df.shape[0], )
    #     The output result is 0, -1, 1, -2, where -2 means that the length is not enough
    
    df.sort_values(column_names[0], inplace=True, ascending=True)
    
    price_array = np.array(df[column_names[1]].values)
    label_array = np.zeros(len(price_array))-2
    for i in range(len(price_array)):
        if len(price_array)-i-1 < T:
            continue
        else:
            now_close_price = price_array[i]
            
            if threshold_type == 'ratio':
                temp_threshold = now_close_price*threshold
            else:
                temp_threshold = threshold
            
            flag = 0
            for j in range(T):
                if price_array[i+j+1]-now_close_price > temp_threshold:
                    label_array[i] = 1
                    flag = 1
                    break
                elif price_array[i+j+1]-now_close_price < -temp_threshold:
                    label_array[i] = -1
                    flag = 1
                    break
            if flag == 0:
                label_array[i] = 0
                
    return label_array

def tbl_form_label_all_coins(df_in, config, lstm_config, column_names=['Date','Open'], verbose=False):
    # input:
    #     df: dataframe (expected columns by Prophet: ['Date','Coin','Open']) with all coins
    #     config: crypto config - list of coins to process
    #     column_names: list, fist date column name, second price column name in df
    #     threshold_type: 'ratio' or 'specific'
    #     threshold: value
    #     T: length of triple barries
    # output:
    #     df_labels: dataframe with added column 'Label'
    #       The output result is 0, -1, 1, -2, where -2 means that the length is not enough

    df_labes_all_coins = pd.DataFrame()
    df = df_in.copy()

    # get forecast for each coin
    for coin in config['coins_to_process']: # TODO - L - better to handle dynamically with .unique()
        if coin['create_tbl'] != 'yes':
            if verbose:
                print('SKIP labeling: {}'.format(coin['name']))
            continue
        if verbose:
            print('Running labeling: {}'.format(coin['name']))
        df_coin = df[df['Coin'] == coin['name']]
        # create labels for one coin
        coin_label = tbl_form_label(
            df_coin, 
            column_names=column_names, 
            threshold_type='ratio', 
            threshold=lstm_config['forecast']['tbl_percentage']/100.0, # convert % to ratio (e.g. 5% --> 0.05)
            T=lstm_config['forecast']['tbl_length'])
        # add column to existing data
        df_coin['Label'] = coin_label
        if verbose:
            print('    1: days where price rises:    {}'.format(df_coin[df_coin['Label'] == 1]['Label'].count()))
            print('    0: days where price stays:    {}'.format(df_coin[df_coin['Label'] == 0]['Label'].count()))
            print('  - 1: days where price declines: {}'.format(df_coin[df_coin['Label'] == -1]['Label'].count()))
            print('  - 2: last {} days:              {}'.format(lstm_config['forecast']['tbl_length'],df_coin[df_coin['Label'] == -2]['Label'].count()))
        
        # append to output
        df_labes_all_coins = df_labes_all_coins.append(df_coin,ignore_index=True)
        df_labes_all_coins.reset_index(inplace=True, drop=True)
        #df_labes_all_coins.drop('index',axis=1,inplace=True)

    return df_labes_all_coins

def tbl_form_label_all_coins_today():
    return 0
