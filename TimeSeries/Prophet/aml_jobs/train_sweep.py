import pandas as pd
import itertools
import numpy as np
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
import logging
logging.getLogger('fbprophet').setLevel(logging.WARNING) 
from tqdm import tqdm

# ! outdated - get from AML

# get data
symbol = 'BTC-USD'
today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'
df_coin = yf.download(symbol, start_date, today)

# transform
df_coin.reset_index(inplace=True)
df_coin.columns 
df = df_coin[["Date", "Open"]]
new_names = {
    "Date": "ds", 
    "Open": "y",
}
df.rename(columns=new_names, inplace=True)

# set the training size - full set
df_train_sweep = df.copy()
print('full train set size = {}'.format(df_train_sweep.shape[0]))

# making the training set smaller to avoid overfit
first_cutoff_day = '2021-07-01'
for start_day in tqdm(['2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01', '2020-01-01', '2021-01-01']):
    df_train_sweep = df[df['ds'] >= start_day]
    init_train_size = df[(df['ds'] >= start_day)&(df['ds'] < first_cutoff_day)].shape[0]
    print('start day {}: train set size = {}'.format(start_day,init_train_size))


# param_grid = {  
#     'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
#     'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
#     'holidays_prior_scale': [0.01, 10],
#     'seasonality_mode': ['additive', 'multiplicative'],
#     'changepoint_range': [0.8, 0.85, 0.9, 0.95, 0.99]
# }

#test
param_grid = {  
    'changepoint_prior_scale': [0.001],
    'seasonality_prior_scale': [0.01],
    'holidays_prior_scale': [0.01],
    'seasonality_mode': ['multiplicative'],
    'changepoint_range': [0.8]
}

# Generate all combinations of parameters
all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
rmses = []  # Store the RMSEs for each params here
mapes = []  # Store the MAPEs for each params here
mdapes = []  # Store the MDAPEs for each params here
tuning_results_all = pd.DataFrame()

# Sweep---------------------------------------
# 1. loop over training set sizes
#for start_day in tqdm(['2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01', '2020-01-01', '2021-01-01'], leave=True, desc='1st loop'):
for start_day in tqdm(['2016-01-01'], leave=True, desc='1st loop'): # test
    df_train_sweep = df[df['ds'] >= start_day]
    init_train_size = df[(df['ds'] >= start_day)&(df['ds'] < first_cutoff_day)].shape[0]

    # 2. Use cross validation to evaluate all parameters
    #for params in all_params:
    for params in tqdm(all_params, leave=True, desc='2nd loop'):
        m_sweep = Prophet(**params).fit(df)  # Fit model with given params
        df_cv = cross_validation(m_sweep, initial='2000 days', period='5 days', horizon = '10 days', parallel='threads')
        df_p = performance_metrics(df_cv, rolling_window=1)
        rmses.append(df_p['rmse'].values[0])
        mapes.append(df_p['mape'].values[0])
        mdapes.append(df_p['mdape'].values[0])

    # Find the best parameters
    tuning_results = pd.DataFrame(all_params)
    tuning_results['rmse'] = rmses
    tuning_results['mape'] = mapes
    tuning_results['mdape'] = mdapes
    tuning_results['init_train_size'] = init_train_size
    tuning_results_all = tuning_results_all.append(tuning_results,ignore_index=True)
    
    #print(tuning_results)
    best_params = all_params[np.argmin(mapes)]
    #print('For start day {} best (MAPE) parameters are: {}'.format(start_day,best_params))

    # reset the lists for next training size iteration
    rmses = []
    mapes = []
    mdapes = []

# Save
tuning_results_all.to_csv('fbprophet_sweep.csv', index=False, mode='a', header=True) # ? first time add header