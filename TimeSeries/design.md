# CryptoBot Design
## Bot Versions
| Version | Description |
| --- | --- | 
| 1 | FB Prophet |
| 2 | FB Prophet + LSTM1 + LSTM2 (synthetic) |
| 2 | LSTM1 + LSTM2 (synthetic) + LSTM3 (ema7+fgi) |
| 3 | LSTM1 + LSTM2 (synthetic) + LSTM3 (ema7+fgi) + 2 more |
## Data Desing
| Column num | Column id | Description | Type | Values | Notes |
| --- | --- | --- | --- | --- | --- | 
| 01 | Coin | Coin id | str | ['BTC-USD','ETH-USD','Synth'] | |
| 02 | Date | Date YYYY-MM-DD | str | | | 
| 03 | Open | Day Open price | float | | | 
| 04 | High | Day High price | float | | | 
| 05 | Low | Day Low price | float | | | 
| 06 | Close | Day Close price | float | | | 
| 07 | Adj Close | Day Close Adj price | float | | | 
| 08 | Volume | Day Trade volume | int | | | 
| 09 | FGI_Class | Fear&Greed Index class (0=EF, 5=EG) | int | [0,1,2,3,4,5] | see fear_greed_index.ipynb | 
| 10 | FGIndex | Fear&Greed Index value (0-100) | float | (0-100) | see fear_greed_index.ipynb | 
| 11 | FGI_Class_num | Fear&Greed Index class (0-5) | int | [0,1,2,3,4,5] | see fear_greed_index.ipynb | 
| 12 | FGI_Class_ef | Fear&Greed - One hot encoded: Extreme fear | int | [0,1] | | 
| 13 | FGI_Class_f | Fear&Greed - One hot encoded: Fear | int | [0,1] | | 
| 14 | FGI_Class_n | Fear&Greed - One hot encoded: Neutral | int | [0,1] | | 
| 15 | FGI_Class_g | Fear&Greed - One hot encoded: Greed | int | [0,1] | | 
| 16 | FGI_Class_nan | Fear&Greed - One hot encoded: Not a Number | int | [0,1] | index not available for all dates | 
| 17 | FGI_Class_eg | Fear&Greed - One hot encoded: Extreme greed | int | [0,1] | | 

## FB Prophet