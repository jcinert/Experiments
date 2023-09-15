"""
    fuctions to process raw data
"""
import numpy as np

def form_label(df, column_names=['Date','Open'], threshold_type='ratio', threshold=0.05, T=5):
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