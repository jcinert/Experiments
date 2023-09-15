import math
import numpy as np
import pandas as pd
from src.lstm.tbl import form_label_window
from tensorflow.keras.utils import to_categorical
import warnings

class DataLoader():
    """A class for loading and transforming data for the lstm model"""

    def __init__(self, filename, coin, split, cols):
        '''
        Reads the input data
        Ajusted for crypto: 
            - expects columns 'Coin' in the data
        Inputs:
            filename: string, full path to CSV file
            split: structure, 
                split["type"]: string, "date" / "ratio". Will split train/test based on date or proportionally
                split["date_column"]: string, date column name in the input data
                split["date"]: string, to be provided with split based on date, e.g. "2020-12-31"
                split["ratio"]: float, to be provided with split based on ratio, e.g. 0.7
        '''
        dataframe = pd.read_csv(filename)
        dataframe = dataframe[dataframe['Coin'] == coin]

        if split["type"] == "date":
            date_column = split["date_column"]
            self.data_train = dataframe[dataframe[date_column] < split["date"]].get(cols).values[:]
            self.data_test  = dataframe[dataframe[date_column] >= split["date"]].get(cols).values[:]
        else:
            i_split = int(len(dataframe) * split["ratio"])
            self.data_train = dataframe.get(cols).values[:i_split]
            self.data_test  = dataframe.get(cols).values[i_split:]

        self.len_train  = len(self.data_train)
        self.len_test   = len(self.data_test)
        self.len_train_windows = None

    def get_test_data(self, seq_len, tbl_len, tbl_percentage, normalise, normalise_exc):
        '''
        Create x, y train data windows
        Warning: batch method, not generative, make sure you have enough memory to
        load data, otherwise use generate_training_window() method.
        '''
        # validation that TBL window is < sequence
        if tbl_len >= seq_len:
            raise ValueError("TBL window length (tbl_length) must be smaller than (sequence_length)")

        data_x = []
        data_y = []
        for i in range(self.len_test - (seq_len+tbl_len)):
            x, y = self._next_window(i, self.data_test, seq_len, tbl_len, tbl_percentage, normalise, normalise_exc)
            data_x.append(x)
            data_y.append(y)

        return np.array(data_x), np.array(data_y)

    def get_train_data(self, seq_len, tbl_len, tbl_percentage, normalise, normalise_exc):
        '''
        Create x, y train data windows
        Warning: batch method, not generative, make sure you have enough memory to
        load data, otherwise use generate_training_window() method.
        '''

        # validation that TBL window is < sequence
        if tbl_len >= seq_len:
            raise ValueError("TBL window length (tbl_length) must be smaller than (sequence_length)")

        data_x = []
        data_y = []
        for i in range(self.len_train - (seq_len+tbl_len)):
            x, y = self._next_window(i, self.data_train, seq_len, tbl_len, tbl_percentage, normalise, normalise_exc)
            data_x.append(x)
            data_y.append(y)

        return np.array(data_x), np.array(data_y)

    def generate_train_batch(self, seq_len, tbl_len, tbl_percentage, batch_size, normalise, normalise_exc):
        '''Yield a generator of training data from filename on given list of cols split for train/test'''

        # validation that TBL window is < sequence
        if tbl_len >= seq_len:
            raise ValueError("TBL window length (tbl_length) must be smaller than (sequence_length)")

        i = 0
        while i < (self.len_train - seq_len):
            x_batch = []
            y_batch = []
            for b in range(batch_size):
                if i >= (self.len_train - (seq_len+tbl_len)):
                    # stop-condition for a smaller final batch if data doesn't divide evenly
                    yield np.array(x_batch), np.array(y_batch)
                    i = 0
                x, y = self._next_window(i, self.data_train, seq_len, tbl_len, tbl_percentage, normalise, normalise_exc)
                x_batch.append(x)
                y_batch.append(y)
                i += 1
            yield np.array(x_batch), np.array(y_batch)

    def _next_window(self, i, data, seq_len, tbl_len, tbl_percentage, normalise, normalise_exc):
        '''
        Generates the next data window from the given index location i
        Udated: creates y = TBL based on price (x[0,:]) and one-hot encode it
        '''
        # window = self.data_train[i:i+seq_len] TODO delete
        window = data[i:i+seq_len]
        # create labels - based on price only
        # labels are provided for the next next window. We want to estimate the label based on current window
        # e.g. window = [0:29], label for [30:34]
        label = []
        if len(data) > i + seq_len + tbl_len:
            next_window = data[i+seq_len:i+seq_len+tbl_len]
            labels = form_label_window(next_window[:,0], threshold_type='ratio', threshold=tbl_percentage/100.0, T=tbl_len) # TODO fix hardcoded value
            label.append(labels[0])
            label = np.array(label).astype(float)
        else:   
            # this should not occur as we dont draw data windows when we dont have enough
            label = np.array([-2]).astype(float)
            #raise ValueError("N must be non-negative")
            warnings.warn("WARNING - not enough data (X) to generate TBL (Y). Label might be incorrect.")

        window = self.normalise_windows(window, normalise_exc, single_window=True)[0] if normalise else window
    
        # X:
        x = window[:]
        # Y: one hot encoded TBL; down(-1) = [1,0,0], stay(0) = [0,1,0], up(1) = [0,0,1]
        y = to_categorical(label.flatten()+1,3).flatten() # +1: to convert -1 >> 0
        
        return x, y

    def normalise_windows(self, window_data, normalise_exc=[], single_window=False):
        '''Normalise window with a base value of zero'''
        normalised_data = []
        window_data = [window_data] if single_window else window_data
        for window in window_data:
            normalised_window = []
            for col_i in range(window.shape[1]):
                if col_i in normalise_exc:
                    normalised_col = window[:, col_i]
                    normalised_window.append(normalised_col)
                    # print(normalised_col)
                else:
                    normalised_col = [((float(p) / float(window[0, col_i])) - 1) for p in window[:, col_i]]
                    normalised_window.append(normalised_col)
                    # print(normalised_col)
            normalised_window = np.array(normalised_window).T # reshape and transpose array back into original multidimensional format
            normalised_data.append(normalised_window)
        return np.array(normalised_data)

    def get_todays_data(self, seq_len, normalise, normalise_exc, days_shift = 0):
        '''
        Create x (not y) predicion data window ending with today
            - days_shift: number of days to shift window in the past (0 = today, 1 = yesterday, ...)
        '''
        data_x = []
        latest_window_start = self.len_test - seq_len - days_shift
        data_x = self.data_test[latest_window_start:latest_window_start+seq_len]
        data_x = self.normalise_windows(data_x, normalise_exc, single_window=True)[0] if normalise else data_x

        return np.array(data_x)


# -------------------- TEMP GRAVEYARD --------------------------

    # def denormalise_window(self, window, base_value = 1): 
    #     '''
    #     TODO FIX
    #     De-Normalise window with a base value provided
    #     base_value: float - typically this can be a X_0 value of a normalization window for all values of the window 
    #         or for values forecasted by predict_sequences_multiple
    #     '''
    #     denormalised_window = []
    #     denormalised_window = [((float(p) + 1 ) * float(base_value)) for p in window[:]]
    #     denormalised_window = np.array(denormalised_window).T # reshape ad transpose array back into original multidimensional format
    #     return np.array(denormalised_window)

    # def get_test_data(self, seq_len, tbl_len, normalise, normalise_exc):
    #     '''
    #     Create x, y test data windows
    #     Warning: batch method, not generative, make sure you have enough memory to
    #     load data, otherwise reduce size of the training split.
    #     Udated: creates y = TBL based on x[0,:] and one-hot encode it
    #     '''

    #     # validation that TBL window is < sequence
    #     if tbl_len >= seq_len:
    #         raise ValueError("TBL window length (tbl_length) must be smaller than (sequence_length)")

    #     data_windows = []
    #     for i in range(self.len_test - seq_len): # check (seq_len+tbl_len)?
    #         data_windows.append(self.data_test[i:i+seq_len])

    #     data_windows = np.array(data_windows).astype(float)

    #     # create labels - based on price only
    #     labels = []
    #     i = 0
    #     # for each window we create triple barrier label
    #     # e.g. window = [0:29], label for [30:34] 
    #     for window in data_windows[:, :, 0]:     
    #         if len(data_windows) > i + tbl_len:
    #             next_window = data_windows[i+tbl_len,:,0] # here we assume price is the first column
    #             label = form_label_window(next_window[-tbl_len:], threshold_type='ratio', threshold=0.05, T=tbl_len)
    #             labels.append(label[0])
    #         i = i + 1
    #     labels = np.array(labels).astype(float)
    #     labels = np.expand_dims(labels, axis=1)
        
    #     data_windows = self.normalise_windows(data_windows, normalise_exc, single_window=False) if normalise else data_windows

    #     # X: drop last <tbl_len> values where we dont have label
    #     x = data_windows[:len(labels), :] 
    #     # Y: one hot encoded TBL; down(-1) = [1,0,0], stay(0) = [0,1,0], up(1) = [0,0,1]
    #     y = to_categorical(labels.flatten()+1,3)    # +1: to convert -1 >> 0

    #     return x,y