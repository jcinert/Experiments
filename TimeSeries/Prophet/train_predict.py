"""
    fuctions to train and predict with Prophet
"""
# load libraries
import yaml
from pathlib import Path
import os
from fbprophet import Prophet
# from fbprophet.plot import plot_plotly, plot_components_plotly
import warnings
warnings.filterwarnings('ignore')
# pd.options.display.float_format = '${:,.2f}'.format

def fbp_train_predict(df, coin, column_names=['ds','y'], forecast_lenght = 5, mode='forecast_only'):
    # input:
    #     df: dataframe (expected columns by Prophet: ds, y)
    #     column_names: list, fist date column name (ds), second price column name in df (y)
    #     forecast_period: int, number of forecasted samples
    #     mode: str,
    #       'forecast_only' - returns only pred values
    #   WIP 'append' - appends pred values to df
    #       'full' - returns full prediction details including history
    # output:
    #     label: array 
    #     The output result is 0, -1, 1, -2, where -2 means that the length is not enough
    
    # settings
    if mode == 'full':
        include_history = True
    else:
        include_history = False

    # format data
    #df_formatted = df.copy()
    df_formatted = df[[column_names[0], column_names[1]]]
    new_names = {
        column_names[0]: "ds", 
        column_names[1]: "y",
    }
    df_formatted.rename(columns=new_names, inplace=True)

    # load train parameters depending on coin
    path = Path(os.getcwd()) # project root path
    config_path = path.absolute()
    config_path = config_path / 'train_config.yaml'

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    parameters = [c for c in config['fbp_parameters'] if c['coin'] == coin]
    parameters = parameters[0]

    # TRAIN
    m = Prophet(
        growth=parameters['growth'],
        changepoint_prior_scale=parameters['changepoint_prior_scale'],
        seasonality_prior_scale=parameters['seasonality_prior_scale'],
        holidays_prior_scale=parameters['holidays_prior_scale'],
        seasonality_mode=parameters['seasonality_mode'],
        changepoint_range=parameters['changepoint_range'],
    )
    m.fit(df_formatted)

    # PREDICT
    future = m.make_future_dataframe(periods=forecast_lenght, include_history=include_history)
    #future['cap'] = xxxx
    forecast = m.predict(future)

    if mode == 'append':
        #df_formatted['a'] = 100
        return forecast #TODO append data
    elif mode == 'forecast_only':
        return forecast[['ds','yhat']]
    else:
        return forecast