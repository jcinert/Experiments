import yaml
from pathlib import Path
import os
import pandas as pd
from datetime import datetime
from datetime import timedelta
from sklearn import metrics as metrics 
import numpy as np
import plotly.graph_objects as go

def load_config(verbose=False):
    """
    Imports settings from 'config.yaml in the root project folder'
    """
    path = Path(os.getcwd()) # project root path
    config_path = path.absolute()
    config_path = config_path / 'config.yaml'

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    if verbose:
        print('Import config lodaded')
    return config

def get_backfill_range(verbose=False):
    """
    returns list of dates for which forecast hasnt been done
    """
    path = Path(os.getcwd())
    data_path = path.absolute()
    forecast_path = data_path / 'data' / 'forecast.csv'

    df_backfill = pd.read_csv(forecast_path)
    df_backfill['Timestamp'] = pd.to_datetime(df_backfill['Timestamp'])
    last_forecast = df_backfill['Timestamp'].max()
    if verbose:
        print('Last forecast done for: ' + last_forecast.strftime('%Y-%m-%d'))

    delta = (datetime.today().date() - last_forecast.date()).days
    backfill_days = []
    
    # if forecast was done yesterday delta can be 0
    if delta < 1:
        backfill_days.append(datetime.today().strftime('%Y-%m-%d'))
        if verbose:
            print('Backfill will run {}x for {}.'.format(1,backfill_days[0]))
    else:
        for d in range(delta):
            backfill_day = (datetime.today() - timedelta(d)).strftime('%Y-%m-%d')
            backfill_days.append(backfill_day)
        backfill_days.sort(reverse=False)
        if verbose:
            print('Backfill will run {}x from {} to {}.'.format(delta,backfill_days[0],backfill_days[-1]))
     
    return backfill_days

def save_forecast(df_forecast, model, value_column='Open', verbose=False):
    """
    Formats the forecast data and saves to "data" folder
    Input: 
        df_forecast - pd dataframe
        model - str, expected values: ['fbp','fbp-tb','fbp-tb-2','lstm-tb-3']
        value_column - str, expected values: ['Open']

    Output:
    """
    # TODO - M - add feature of replacing value for the same day?

    # validation
    if model not in ['fbp','fbp-tb','lstm-tb','lstm-tb-2','lstm-tb-3']:
        raise NameError('ERROR: model {} not defined yet!'.format(model))

    forecast_columns=['Forecast_day','Coin','Value','Model','Value_type','Timestamp']
    # combine data
    forecast_to_store = df_forecast
    forecast_to_store['Timestamp'] = datetime.today()
    forecast_to_store['Model'] = model
    forecast_to_store['Value_type'] = value_column
    #rename columns
    new_names = {
                    "Date": "Forecast_day", 
                    value_column: "Value",
                }
    forecast_to_store.rename(columns=new_names, inplace=True)
    # reorder as per CSV format
    forecast_to_store = forecast_to_store.reindex(columns=forecast_columns)

    # set output CSV file path
    # - expects following structure: (project folder)-->(data,doc,src)
    path = Path(os.getcwd())
    csv_path = path.absolute()
    csv_path = csv_path / 'data' / 'forecast.csv'

    # save 
    forecast_to_store.to_csv(csv_path, index=False, mode='a', header=False)

    if verbose:
        print('Forecast data for {} saved to {}'.format(model,csv_path))

def get_fbp_accuracy(model, config, exclude_today=True, verbose=False):
    """
    Formats and returns the forecast data and real price
    Calculates MAPE metrics - Mean absolute percentage error
    reads data from CSV files
    expects value in 'Open' columns
    Input: 
        model - str, expected values: ['fbp']
        exclude_today - bool, exclude from evaluation forecast done for the same day when the forecast is executed

    Output:
        df_mape - pd dataframe, contains MAPE for all coins
        df_accuracy - pd dataframe, contains actual and forecasted data for all coins
    """
  # get forecast & price data
    path = Path(os.getcwd())
    data_path = path.absolute()
    forecast_path = data_path / config['folder'] / config['forecast']
    df_forecast_all = pd.read_csv(forecast_path)

    price_path = data_path / config['folder'] / config['processed_marked_data']
    df_price_data = pd.read_csv(price_path)

    # select only fbp forecast values
    df_forecast_fbp = df_forecast_all[df_forecast_all['Model'] == model]

    # drop colums where timestamp = forecast
    if exclude_today:
        df_forecast_fbp = df_forecast_fbp.drop(df_forecast_fbp[
            df_forecast_fbp['Timestamp'] > df_forecast_fbp['Forecast_day'] 
        ].index,axis=0)


    # fix column names / types
    df_price_data['Date'] =pd.to_datetime(df_price_data['Date'])
    df_forecast_fbp['Forecast_day'] =pd.to_datetime(df_forecast_fbp['Forecast_day'])

    #rename columns
    new_names = {
                    "Forecast_day": "Date", 
                }
    df_forecast_fbp.rename(columns=new_names, inplace=True)

    # join forecast data to real prices
    df_accuracy = pd.merge(df_forecast_fbp, df_price_data, how='left', on=['Date','Coin'])
    # removing na values - expected for future values
    df_accuracy.dropna(inplace=True)
    df_accuracy.drop(['Model', 'Value_type', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], axis=1, inplace=True)

    from sklearn import metrics as metrics 

    df_mape = pd.DataFrame([],columns=['Coin','MAPE'])
    # Mean absolute percentage error
    for coin in df_accuracy['Coin'].unique():
        df_accuracy_coin = df_accuracy[df_accuracy['Coin'] == coin]
        mape = metrics.mean_absolute_percentage_error(df_accuracy_coin['Value'], df_accuracy_coin['Open'])
        df_mape = df_mape.append({'Coin':coin, 'MAPE':mape},ignore_index=True)

        if verbose:
            print('fbp accuracy over 5 days forecast: {:,.2f}%'.format(mape*100))

    df_accuracy_data = df_accuracy

    return df_mape, df_accuracy_data

# def get_metrics(df,day,forecast_lenght):
#     # input:
#     #     df: dataframe (expected columns: y, yhat)
#     #     day: first day of the forecast
#     # output:
#     #     df_metrics: dataframe, metrics for this dataframe 
#     #         ['ds','forecast_lenght','ME','MAE','RMSE','MAPE'])
#     #           'ds' = day

#     # Mean Forecast Error (or Forecast Bias)
#     ME = np.mean(df['y'] - df['yhat'])
#     #print('ME: {:,.2f}'.format(ME))

#     # Mean Absolute Error
#     MAE = metrics.mean_absolute_error(df['y'], df['yhat'])
#     #print('MAE: {:,.2f}'.format(MAE))

#     # Mean Squared Error
#     MSE = metrics.mean_squared_error(df['y'], df['yhat'])
#     #print('MSE: {:,.2f}'.format(MSE))

#     # Root Mean Squared Error
#     RMSE = np.sqrt(metrics.mean_squared_error(df['y'], df['yhat']))
#     #print('RMSE: {:,.2f}'.format(RMSE))

#     # Mean absolute percentage error
#     MAPE = metrics.mean_absolute_percentage_error(df['y'], df['yhat'])
#     #print('MAPE: {:,.2f}%'.format(MAPE*100))

#     # Mean absolute percentage error - custom
#     MAPE2 = np.mean(np.abs(df['y'] - df['yhat'])/df['y'])
#     #print('MAPE2: {:,.2f}%'.format(MAPE2*100))

#     return pd.DataFrame([[day, forecast_lenght, ME, MAE, RMSE, MAPE]],columns=['ds','forecast_lenght','ME','MAE','RMSE','MAPE'])

def plot_prediction_tb5(model='fbp', coin='BTC-USD', day_range=30):
    """
    Displays a plot of:
    - history data (loaded from price_data.csv
    - forecast data (loaded from forecast.csv)
    - tb box
    assumes price is "Open" and prediction for 5 days from today
    Input: 
        model - string, name of model used to generate forecast (stored in forecast dataset)
        coin - string, coin name
        day_range - number, number of days of history to be shown
    Output: 
        displays a plotly chart
    """
    # load data
    path = Path(os.getcwd())
    data_path = path.absolute()
    real_data_path = data_path / 'data' / 'price_data.csv'
    forecast_path = data_path / 'data' / 'forecast.csv'

    # import all price data
    df_price_data = pd.read_csv(real_data_path)
    df_forecast_data = pd.read_csv(forecast_path)


    # prep data
    df_plot = pd.DataFrame([],columns=['x','real','forecast'])
    df_plot['x'] = df_price_data[(
        df_price_data['Date'] >= ((datetime.today() - timedelta(day_range)).strftime('%Y-%m-%d'))) 
        & (df_price_data['Coin'] == coin)]['Date']
    df_plot['real'] = df_price_data[(
        df_price_data['Date'] >= ((datetime.today() - timedelta(day_range)).strftime('%Y-%m-%d'))) 
        & (df_price_data['Coin'] == coin)]['Open']

    # add forecast dates
    for day in range(1,6,1):
        df_plot = df_plot.append({
            'x':((datetime.today() + timedelta(day)).strftime('%Y-%m-%d')),
            'real':np.nan,
            'forecast':np.nan
            },ignore_index=True)

    # add forecast values (today + 5) in last 6 rows
    df_plot['forecast'].iloc[-6:] = df_forecast_data[
        (df_forecast_data['Coin'] == coin) & 
        (df_forecast_data['Model'] == model)]['Value'].tail(6)

    # create TBL box (+/- 5% lines compared to todays value)
    tbl_day_from = ((datetime.today()).strftime('%Y-%m-%d'))
    tbl_day_to = ((datetime.today() + timedelta(5)).strftime('%Y-%m-%d'))
    tbl_val_from =df_plot[df_plot['x']==tbl_day_from]['real']*0.95
    tbl_val_to =df_plot[df_plot['x']==tbl_day_from]['real']*1.05
    
    # plot - add real price 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_plot['x'], y=df_plot['real'], name='real'))
    # Set title
    fig.update_layout(
        title_text= 'Forecast for: ' + coin + ' - model: ' + model
    )
    # plot forecast 
    fig.add_trace(go.Scatter(x=df_plot['x'], y=df_plot['forecast'], name='forecast'))

    fig.add_shape(type="rect",
        x0=tbl_day_from,  
        x1=tbl_day_to,
        y0=tbl_val_from.values[0], 
        y1=tbl_val_to.values[0],
        line=dict(
            color="RoyalBlue",
            width=1,
            dash='dot'
        ),
        fillcolor="LightSkyBlue",
        opacity=0.4,
        name='tbl'
    )
    
    # use dark background: ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]:
    fig.update_layout(template="plotly_dark")

    # TODO - L - add middle line

    # # Add TBL 
    # fig.add_trace(
    #     go.Scatter(
    #         name= 'Down',
    #         mode='markers',
    #         x=df_tbl[df_tbl['label'] == -1]['Date'],
    #         y=df_tbl[df_tbl['label'] == -1]['Open'],
    #         marker=dict(
    #             # symbol = 'triangle-up',
    #             color='rgba(204, 20, 20, 0.5)',
    #             size=3,
    #             line=dict(
    #                 color='Red',
    #                 width=1
    #             )
    #         ),
    #         showlegend=True
    #     )
    # )

    # fig.add_trace(
    #     go.Scatter(
    #         name= 'Up',
    #         mode='markers',
    #         x=df_tbl[df_tbl['label'] == 1]['Date'],
    #         y=df_tbl[df_tbl['label'] == 1]['Open'],
    #         marker=dict(
    #             # symbol = 'triangle-up',
    #             color='rgba(20, 200, 20, 0.5)',
    #             size=3,
    #             line=dict(
    #                 color='Green',
    #                 width=1
    #             )
    #         ),
    #         showlegend=True
    #     )
    # )

    fig.show()


def get_accuracy_tb(model, config, lstm_config, exclude_today=True, verbose=False):
    """
    Formats and returns the forecast data and real price
    reads data from CSV files
    calculatest real TB based on 'Open' real price data
    Input: 
        model - str, expected values: ['fbp-tb', 'lstm-tb', 'lstm-tb-2', 'lstm-tb-3']

    Output:
        df_mape - pd dataframe, contains MAPE for all coins  TBC
        df_accuracy - pd dataframe, contains actual and forecasted data for all coins
            forecasted label column: Value
            True label column: Label
    """
  # get forecast & price data
    path = Path(os.getcwd())
    data_path = path.absolute()
    forecast_path = data_path / config['folder'] / config['forecast']
    df_forecast_all = pd.read_csv(forecast_path)

    price_path = data_path / config['folder'] / config['processed_marked_data']
    df_price_data = pd.read_csv(price_path)

    # select only forecast values
    df_forecast = df_forecast_all[df_forecast_all['Model'] == model]

     # fix column names / types
    df_price_data['Date'] =pd.to_datetime(df_price_data['Date'])
    df_forecast['Forecast_day'] =pd.to_datetime(df_forecast['Forecast_day'])

    #rename columns
    new_names = {
                    "Forecast_day": "Date", 
                }
    df_forecast.rename(columns=new_names, inplace=True)

    # join forecast data to real prices
    df_accuracy = pd.merge(df_forecast, df_price_data, how='left', on=['Date','Coin'])
    # removing na values - expected for future values
    df_accuracy.dropna(inplace=True)
    df_accuracy.drop(['Model', 'Value_type', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], axis=1, inplace=True)


    from sklearn import metrics as metrics
    from src.TripleBarrierLabel.label_price_data import tbl_form_label_all_coins

    # get tb labels for real values
    df_tbl = tbl_form_label_all_coins(df_accuracy, config, lstm_config=lstm_config, column_names=['Date', lstm_config['forecast']['tbl_column']])

    # exclude -2.0 values (future values - no real value yet)
    df_tbl = df_tbl[df_tbl['Label'] != -2.0]

    # get metrics
    # for our multiclass clasification good metics is 
    #  - accuracy (preferably) - (TP+TN)/(TP+TN+FP+FN)
    #  - weighted F1
    # towardsdatascience.com/multi-class-metrics-made-simple-part-ii-the-f1-score-ebe8b2c2ca1

    if len(df_tbl) == 0:
        print('WARNING: Not enough data to form TBL')
        return pd.DataFrame([],columns=['Coin','Accuracy']), df_tbl

    # total accuracy
    accuracy = metrics.accuracy_score(df_tbl['Label'], df_tbl['Value'])

    if verbose:
        # Print the confusion matrix
        print('Confusion matrix: ')
        print(metrics.confusion_matrix(df_tbl['Label'], df_tbl['Value']))
        # Print the precision and recall, among other metrics
        print(metrics.classification_report(df_tbl['Label'], df_tbl['Value'], digits=3))

    df_accuracy = pd.DataFrame([],columns=['Coin','Accuracy'])
    # Accuracy for each coin
    for coin in df_tbl['Coin'].unique():
        df_accuracy_coin = df_tbl[df_tbl['Coin'] == coin]
        accuracy = metrics.accuracy_score(df_accuracy_coin['Label'], df_accuracy_coin['Value'])
        df_accuracy = df_accuracy.append({'Coin':coin, 'Accuracy':accuracy}, ignore_index=True)

        if verbose:
            print('{}: TB classification accuracy over 5 days forecast: {:,.2f}%'.format(coin,accuracy*100))

    return df_accuracy, df_tbl

def get_coin_summary(df_tbl, df_accuracy, df_mape, df_accuracy_lstm):
    """
    Combines and formats summary
    Input: 
        df_tbl - df, dataframe with TBL for today
        df_accuracy - df, dataframe with fbp tbl accuracy so far 
        df_mape - df, dataframe with fbp mape error so far 
        df_accuracy_lstm - df, dataframe with lstm tbl accuracy so far 
    Output:
        df_summary - pd dataframe, summary to view
    """
    # summary add - coins and rolling error
    df_summary = pd.DataFrame([],columns=['Coin','fbp-mape'])
    df_summary[['Coin','fbp-mape']] = df_mape[['Coin','MAPE']]
    # summary add - label
    df_summary = pd.merge(df_summary, 
        df_tbl[df_tbl['Date'] == datetime.today().strftime('%Y-%m-%d')][['Coin','Label']],
        on='Coin')
    # summary add - label accuracy
    df_summary = pd.merge(df_summary, 
        df_accuracy[['Coin','Accuracy']],
        on='Coin')
    df_summary.drop('Coin', axis=1)
    # format
    new_names = {
        'Label': 'fbp-tb-label',
        'Accuracy': 'fbp-tb-accuracy'
    }
    # summary add - label accuracy LSTM
    df_summary = pd.merge(df_summary, 
        df_accuracy_lstm[['Coin','Accuracy']],
        on='Coin')
    df_summary.drop('Coin', axis=1)
    # format LSTM
    new_names = {
        'Label': 'lstm-tb-label',
        'Accuracy': 'lstm-tb-accuracy'
    }
    df_summary.rename(columns=new_names, inplace=True)
    df_summary = df_summary.reindex(columns=['Coin', 'fbp-tb-label', 'fbp-tb-accuracy', 'fbp-mape', 'lstm-tb-label', 'lstm-tb-accuracy'])

    # summary add - expected accuracy (from training sweep)
    # load parameters depending on coin
    config = load_config(verbose=False)

    df_exp_acc = pd.DataFrame([],columns=['Coin','fbp-expected-mape','lstm-expected-acc'])
    for idx, row in df_summary.iterrows():
        # take the expected accuracy from config (ultimatelly from sweep output)
        parameters = [c for c in config['fbp_parameters'] if c['coin'] == row['Coin']]
        parameters = parameters[0]
        # same for LSTM
        parameters = [c for c in config['lstm_parameters'] if c['coin'] == row['Coin']]
        parameters = parameters[0]
        df_exp_acc = df_exp_acc.append({'Coin':row['Coin'],'lstm-expected-acc':parameters['expected_accuracy']['acc']},ignore_index=True)
    df_summary = pd.merge(df_summary, df_exp_acc, on='Coin')

    # format numbers to %
    #df_summary['fbp-tb-label'] = pd.Series([round(val, 0) for val in df_summary['fbp-tb-label']], index = df_summary.index)
    df_summary['fbp-tb-label'] = pd.Series(["{0:.0f}".format(val) for val in df_summary['fbp-tb-label']], index = df_summary.index)
    df_summary['fbp-tb-accuracy'] = pd.Series(["{0:.0f}%".format(val * 100) for val in df_summary['fbp-tb-accuracy']], index = df_summary.index)
    df_summary['fbp-mape'] = pd.Series(["{0:.1f}%".format(val * 100) for val in df_summary['fbp-mape']], index = df_summary.index)
    df_summary['fbp-expected-mape'] = pd.Series(["{0:.1f}%".format(val * 100) for val in df_summary['fbp-expected-mape']], index = df_summary.index)
    df_summary['lstm-expected-acc'] = pd.Series(["{0:.1f}%".format(val * 100) for val in df_summary['lstm-expected-acc']], index = df_summary.index)
    return df_summary