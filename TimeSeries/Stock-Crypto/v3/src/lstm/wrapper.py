import yaml
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
from pathlib import Path
import os
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go

from src.lstm.data_processor import DataLoader
from src.lstm.model import Model

# load lstm config
def load_lstm_config(verbose=False):
    """
    Imports LSTM settings from 'lstm-config.yaml in the root project folder'
    """
    path = Path(os.getcwd()) # project root path
    config_path = path.absolute()
    config_path = config_path / 'lstm-config.yaml'

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    if verbose:
        print('LSTM config lodaded')
    return config

def get_data(lstm_configs, use_same_train_validation=True, use_same_validation_test=True, verbose='All'):
    '''
        Gets Train, Val, Test data (normalized)
        Only BTC for now
        Parameters:
            - verbose: 'All' / 'Light' / 'Off'
            - use_same_train_validation: same data file will be split for train / val
            - use_same_validation_test: use the same validation and test set (test = validation)
    '''

    # set data path
    # path = Path(os.getcwd()).parents[1] # 2 folders up
    path = Path(os.getcwd())
    data_path = path.absolute()
    data_file_train = data_path / 'data' / lstm_configs['data']['filename']

    # train data
    data = DataLoader(
        data_file_train,
        lstm_configs['data']['coins'][0], # TODO fix - now only BTC
        lstm_configs['data']['train_test_split'],
        lstm_configs['data']['columns']
    )

    if verbose == 'All':
        print('[Train data] Using file: {}'.format(data_file_train))

    # same coin as train
    if (use_same_validation_test and use_same_train_validation):
        # 1 - same train-val-test data
        data_val = data
        data_test = data
        if verbose == 'All':
            print('[Validation data] Using file: {}'.format(data_file_train))
            print('[Test data] Using file: {}'.format(data_file_train))
    else:
        # <Generalization> Different Tain and test data / coins
        # configs['data']['train_test_split']['type'] = 'ratio'   # TODO FIX, not nice
        # configs['data']['train_test_split']['ratio'] = 0.6
        lstm_configs['data']['train_test_split']['type'] = 'date'
        lstm_configs['data']['train_test_split']['date'] = '2020-07-20'

        # different data file
        data_file_test = data_path / 'data' / 'xxx.csv' # TODO FIX, not nice

        data_eth = DataLoader(
            data_file_test,
            lstm_configs['data']['coins'][0],  # TODO FIX
            lstm_configs['data']['train_test_split'],
            lstm_configs['data']['columns']
        )

        if use_same_train_validation:
            # 2 - same train-val ; different test data
            data_val = data
            data_test = data_eth
            if verbose == 'All':
                print('[Validation data] Using file: {}'.format(data_file_train))
                print('[Test data] Using file: {}'.format(data_file_test))
        else:
            # 3 - same val-test data but different from train
            data_val = data_eth
            data_test = data_eth
            if verbose == 'All':
                print('[Validation data] Using file: {}'.format(data_file_test))
                print('[Test data] Using file: {}'.format(data_file_test))
    '''
    Get data
    - Training set: A set of examples used for learning, that is to fit the parameters of the classifier.
    - Validation set: A set of examples used to tune the parameters of a classifier, for example to choose the number of hidden units in a neural network.
    - Test set: A set of examples used only to assess the performance of a fully-specified classifier.
    '''
    # get TRAIN data
    x, y = data.get_train_data(
        seq_len=lstm_configs['data']['sequence_length'],
        tbl_len=lstm_configs['forecast']['tbl_length'],
        tbl_percentage=lstm_configs['forecast']['tbl_percentage'],
        normalise=lstm_configs['data']['normalise'],
        normalise_exc=lstm_configs['data']['normalise_exceptions']
    )       
    # get VALIDATION data
    x_val, y_val = data_val.get_test_data(
        seq_len=lstm_configs['data']['sequence_length'],
        tbl_len=lstm_configs['forecast']['tbl_length'],
        tbl_percentage=lstm_configs['forecast']['tbl_percentage'],
        normalise=lstm_configs['data']['normalise'],
        normalise_exc=lstm_configs['data']['normalise_exceptions']
    )
    # get TEST data
    x_test, y_test = data_test.get_test_data(
        seq_len=lstm_configs['data']['sequence_length'],
        tbl_len=lstm_configs['forecast']['tbl_length'],
        tbl_percentage=lstm_configs['forecast']['tbl_percentage'],
        normalise=lstm_configs['data']['normalise'],
        normalise_exc=lstm_configs['data']['normalise_exceptions']
    )

    # Shuffles provided train and test data (windows)
    if lstm_configs['data']['shuffle']:
        if lstm_configs['data']["train_test_split"]["type"] != "ratio":
            # not supported yet
            raise ValueError("Only RATIO train_test_split type supported!!")
        if not use_same_train_validation:
            print('[Data] WARNING - Only Train/Val data are shuffled !! ')

        xdata_stacked = np.vstack((x, x_val))
        ydata_stacked = np.vstack((y, y_val))
        x, x_val, y, y_val = train_test_split(xdata_stacked, ydata_stacked, test_size=1-lstm_configs['data']["train_test_split"]["ratio"], random_state=42)

    # Print data summary
    if verbose == 'All':
        if lstm_configs['data']['shuffle']:
            print('[Data] Train & Val data shuffled !!')
        print('[Train data] X data size: {}'.format(x.shape))
        print('[Train data] Y data size: {}'.format(y.shape))
        print('[Train data] X Window size: {}'.format(x[0,:,:].shape))
        print('[Train data] X Window count: {}'.format(x.shape[0]))
        print('[Train data] Y label balance -1 / 0 / 1: {} / {} / {}'.format(y[:,0].sum(),y[:,1].sum(),y[:,2].sum()))
        print('[Validation data] X data size: {}'.format(x_val.shape))
        print('[Validation data] Y data size: {}'.format(y_val.shape))
        print('[Validation data] Window size: {}'.format(x_val[0,:].shape))
        print('[Validation data] Window count: {}'.format(x_val.shape[0]))
        print('[Validation data] Y label bias: -1: {} / 0: {} / +1: {}'.format(y_val[:,0].sum(),y_val[:,1].sum(),y_val[:,2].sum()))
        print('[Test data] X data size: {}'.format(x_test.shape))
        print('[Test data] Y data size: {}'.format(y_test.shape))
        print('[Test data] Window size: {}'.format(x_test[0,:].shape))
        print('[Test data] Window count: {}'.format(x_test.shape[0]))
        print('[Test data] Y label bias: -1: {} / 0: {} / +1: {}'.format(y_test[:,0].sum(),y_test[:,1].sum(),y_test[:,2].sum()))
    elif verbose == 'Summary':
        if lstm_configs['data']['shuffle']:
            print('[Data] Train & Val data shuffled !!')
        print('[Data] Train data loaded, size: {} '.format(x.shape))
        print('[Data] Validation data loaded, size: {} '.format(x_val.shape)) 
        print('[Data] Test data loaded, size: {} '.format(x_test.shape))
    
    return np.array(x), np.array(y), np.array(x_val), np.array(y_val), np.array(x_test), np.array(y_test)

def get_viz_data(lstm_configs, verbose='All'):
    '''
        Gets Test data not notmalized
        Only BTC for now
        Parameters:
            - verbose: 'All' / 'Light' / 'Off'
    '''

    # set data path
    # path = Path(os.getcwd()).parents[1] # 2 folders up
    path = Path(os.getcwd())
    data_path = path.absolute()
    data_file_viz = data_path / 'data' / lstm_configs['data']['filename']
    #data_file_viz = data_path / 'data' / 'processed_market_data_v4.csv'

    # train data
    data_test = DataLoader(
        data_file_viz,
        lstm_configs['data']['coins'][0], # TODO fix - now only BTC
        lstm_configs['data']['train_test_split'],
        lstm_configs['data']['columns']
    )

    if verbose == 'All':
        print('[Test data] Using file: {}'.format(data_file_viz))

    x_test_viz, y_test_viz = data_test.get_test_data(
    seq_len=lstm_configs['data']['sequence_length'],
    tbl_len=lstm_configs['forecast']['tbl_length'],
    tbl_percentage=lstm_configs['forecast']['tbl_percentage'],
    normalise_exc=lstm_configs['data']['normalise_exceptions'],
    normalise=False
)

    if verbose == 'All':
        print('[Test data] X data size: {}'.format(x_test_viz.shape))
        print('[Test data] Y data size: {}'.format(y_test_viz.shape))
        print('[Test data] Window size: {}'.format(x_test_viz[0,:].shape))
        print('[Test data] Window count: {}'.format(x_test_viz.shape[0]))
        print('[Test data] Y label bias: -1: {} / 0: {} / +1: {}'.format(y_test_viz[:,0].sum(),y_test_viz[:,1].sum(),y_test_viz[:,2].sum()))
    elif verbose == 'Summary': 
            print('[Data] Test data loaded, size: {} '.format(x_test_viz.shape))
    
    return x_test_viz, y_test_viz

def get_todays_data(lstm_configs, days_shift, verbose='Summary'):
    '''
        Gets Train, Val, Test data (normalized)
        Only BTC for now
        Parameters:
            - days_shift: number of days to shift window in the past (0 = today, 1 = yesterday, ...)
            - verbose: 'All' / 'Summary' / 'Off'
    '''

    # set data path
    # path = Path(os.getcwd()).parents[1] # 2 folders up
    path = Path(os.getcwd())
    data_path = path.absolute()
    # data_file_train = data_path / 'data' / 'processed_market_data_v4.csv'
    data_file_train = data_path / 'data' / lstm_configs['data']['filename']

    # train data
    data = DataLoader(
        data_file_train,
        lstm_configs['data']['coins'][0], # TODO fix - now only BTC
        lstm_configs['data']['train_test_split'],
        lstm_configs['data']['columns']
    )

    if verbose == 'All':
        print('[Todays data] Using file: {}'.format(data_file_train))

    # get todays data
    x = data.get_todays_data(
        seq_len=lstm_configs['data']['sequence_length'],
        normalise=lstm_configs['data']['normalise'],
        normalise_exc=lstm_configs['data']['normalise_exceptions'],
        days_shift=days_shift
    )
    if verbose == 'All' or verbose == 'Summary':
        print('[Todays data] X data size: {}'.format(x.shape))
    
    return x

# Train
def train_model(lstm_configs, x, y, x_val, y_val, verbose='All'):
    '''
        Trains LSTM model
        returns model
    '''
    model = Model()
    model.build_model(lstm_configs)

    val_data = (x_val, y_val)

    if verbose == 'All':
        verbose_n = 1
    elif verbose == 'Summary':
        verbose_n = 0

    # in-memory training
    history = model.train(
        x,
        y,
        configs_train = lstm_configs['training'],
        validation_data = val_data,
        verbose = verbose_n
    )
    if verbose == 'All' or verbose == 'Summary':
        print('Max validation accuracy: {:3.1f}% @ epoch: {:}'.format(max(history.history['val_accuracy'])*100, history.history['val_accuracy'].index(max(history.history['val_accuracy']))))
        print('Min validation loss: {:3.1f} @ epoch: {:}'.format(min(history.history['val_loss']), history.history['val_loss'].index(min(history.history['val_loss']))))
    elif verbose == 'All':
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=history.history['accuracy'], name='Train'))
        fig.add_trace(go.Scatter(y=history.history['val_accuracy'], name='Validation'))
        fig.update_layout(title_text= 'Accuracy')
        fig.update_layout(template="plotly_dark")
        fig.show()
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=history.history['loss'], name='Train'))
        fig.add_trace(go.Scatter(y=history.history['val_loss'], name='Validation'))
        fig.update_layout(title_text= 'Loss')
        fig.update_layout(template="plotly_dark")
        fig.show()
    return model

def test_model(lstm_configs, model, x_test, y_test, x_test_viz, y_test_viz, verbose='All'):  
    '''
        Test model and print/plot metrics
        Parameters:
            x_test, y_test - normalized test data 
            x_test_viz, y_test_viz - not normalized data
    '''  

    if verbose == 'All':
        verbose_n = 1
    elif verbose == 'Summary':
        verbose_n = 0

    # Test model
    predictions = model.predict_sequence_full_tbl(x_test,verbose=verbose_n)
    predictions_argmax = np.argmax(predictions[:], axis=1)
    y_argmax  = np.argmax(y_test, axis=1)
    accu = accuracy_score(y_argmax, predictions_argmax)

    confusion_matrix(y_argmax, predictions_argmax)

    if verbose == 'All' or verbose == 'Summary':
        print('[Test] Test accuracy: {:.4}%'.format(accu*100))
        print('pred > 0.7: {}%'.format(predictions[predictions > 0.7].shape[0]/(predictions.shape[0]*3)*100))
        print('pred > 0.5: {}%'.format(predictions[predictions > 0.5].shape[0]/(predictions.shape[0]*3)*100))
        print('pred < 0.5: {}%'.format(predictions[predictions < 0.5].shape[0]/(predictions.shape[0]*3)*100))
    elif verbose == 'All':
        print('pred size: {}x{}'.format(predictions.shape[0],predictions.shape[1]))
        print('pred data sample: {}'.format(predictions[0]))
        target_names = ['-1', '0', '1']
        class_rep = classification_report(y_argmax, predictions_argmax  , target_names=target_names, digits=4, output_dict = False)
        print(class_rep)
   
    # Create VIZ and return figure
    # align price data and PREDICTED labesl - labels needs to be shifed sequence_lenght right
    #  (just for display purpose, but we are loosing first sequence_lenght labels)
    viz_data_labels = np.vstack([
        np.array(range(lstm_configs['data']['sequence_length'],x_test_viz.shape[0])),  # x
        x_test_viz[lstm_configs['data']['sequence_length']:,0,0],                      # y
        predictions_argmax[:-lstm_configs['data']['sequence_length']]                  # TBL predicted (shortened to align with TBL)
    ])                
    viz_data_labels = viz_data_labels.T

    # REAL DATA
    # align price data and REAL labesl - labels needs to be shifed sequence_lenght right
    #  (just for display purpose, but we are loosing first sequence_lenght labels)
    viz_data_real = np.vstack([
        np.array(range(lstm_configs['data']['sequence_length'],x_test_viz.shape[0])),  # x
        x_test_viz[lstm_configs['data']['sequence_length']:,0,0],                      # y
        y_test_viz[:-lstm_configs['data']['sequence_length'],0],
        y_test_viz[:-lstm_configs['data']['sequence_length'],1],
        y_test_viz[:-lstm_configs['data']['sequence_length'],2]        # TBL real (shortened to align with price)
    ])                
    viz_data_real = viz_data_real.T
    
    pd_acc_pred = pd.DataFrame(viz_data_labels,columns=['x','open','label'])
    pd_acc_real = pd.DataFrame(viz_data_real,columns=['x','open','labeld','labels','labelu'])
    df_viz_acc = pd.merge(pd_acc_pred, pd_acc_real, how='left', on=['x'])

    df_viz_acc['acc'] = 0.0
    df_viz_acc.loc[(df_viz_acc['label'] == 0.0) & (df_viz_acc['labeld'] == 1.0), 'acc'] = 1.0  # 1.0 when the prediction down was right
    df_viz_acc.loc[(df_viz_acc['label'] == 1.0) & (df_viz_acc['labels'] == 1.0), 'acc'] = 1.0  # 1.0 when the prediction stay was right
    df_viz_acc.loc[(df_viz_acc['label'] == 2.0) & (df_viz_acc['labelu'] == 1.0), 'acc'] = 1.0  # 1.0 when the prediction up was right

    # validate that we got the labels right (should match the above acc)
    if verbose == 'All':
        print('Viz data Accuracy: {:.4f}'.format(df_viz_acc['acc'].sum() / df_viz_acc['acc'].count()))

    # viz
    viz_acc = np.array(df_viz_acc)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=x_test_viz[:,0,0], name='Open'))

    # down & right
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 7] == 1.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 7] == 1.0), 1],   # y
        0.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        1.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # down & wrong
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 7] == 0.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 7] == 0.0), 1],   # y
        0.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        0.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)                                                
    # stay & right
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 7] == 1.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 7] == 1.0), 1],   # y
        1.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        1.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # stay & wrong
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 7] == 0.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 7] == 0.0), 1],   # y
        1.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        0.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # up & right
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 7] == 1.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 7] == 1.0), 1],   # y
        2.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        1.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # up & wrong
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 7] == 0.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 7] == 0.0), 1],   # y
        2.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        0.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  

    fig.update_layout(title_text= 'TBL predicition accuracy')
    fig.update_layout(template="plotly_dark")
    return fig

def viz_generate_accuracy_chart(viz_acc):
    '''
        viz_acc: np array, columns = [Date(or index), Open, True Label, Pred Label]
            label should be (1.0 = up / 0.0 = stay / -1.0 = down)
    '''
    # TODO - reuse this above

    df_viz_acc = viz_acc[['Date','Open','Value','Label']]
    # adjust label to be positive [0,1,2]
    df_viz_acc['Value'] = df_viz_acc['Value'] + 1 # forecasted label
    df_viz_acc['Label'] = df_viz_acc['Label'] + 1 # true label

    viz_acc = np.array(df_viz_acc)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=viz_acc[:,0],y=viz_acc[:,1], name='Open'))

    # down & right
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 3] == 0.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 3] == 0.0), 1],   # y
        0.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        1.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # down & wrong
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 3] != 0.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 0.0) & (viz_acc[:, 3] != 0.0), 1],   # y
        0.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        0.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)                                                
    # stay & right
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 3] == 1.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 3] == 1.0), 1],   # y
        1.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        1.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # stay & wrong
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 3] != 1.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 1.0) & (viz_acc[:, 3] != 1.0), 1],   # y
        1.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        0.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # up & right
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 3] == 2.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 3] == 2.0), 1],   # y
        2.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        1.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  
    # up & wrong
    viz_add_tbl_points_acc(
        fig,
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 3] != 2.0), 0],   # x
        viz_acc[(viz_acc[:, 2] == 2.0) & (viz_acc[:, 3] != 2.0), 1],   # y
        2.0,                                        # point type (2.0 = up / 1.0 = stay / 0.0 = down)
        0.0)                                        # pred accuracy (1.0 = accurate , 0.0 = wrong)  

    fig.update_layout(title_text= 'TBL predicition accuracy')
    fig.update_layout(template="plotly_dark")

    return fig

# viz test
def viz_add_tbl_points_acc(fig,x,y,tbl,acc):
    if acc == 1.0: # prediction was accurate
        color='rgba(20, 200, 20, 0.5)'
        line='Green'
        name='True'
    else:
        color='rgba(204, 20, 20, 0.5)'
        line='Red'
        name='False'

    if tbl == 0.0:
        symbol = 'triangle-down'
        name=name+' Down'
    elif tbl == 1.0: 
        symbol = 'x'
        name=name+' Stay'
    else:
        symbol = 'triangle-up'
        name=name+' Up'
    
    fig.add_trace(
            go.Scatter(
                name = name,
                mode='markers',
                y=y,
                x=x,
                marker=dict(
                    symbol = symbol,
                    color=color,
                    size=6,
                    line=dict(
                        color=line,
                        width=1
                    )
                ),
                showlegend=True
            )
        )

# # viz real data prediction accuracy
# def viz_real_data_prediction_acc(df_accuracy_data):
    
#     return fig