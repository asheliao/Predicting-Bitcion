# 以傳統均線法和MACD預測比特幣之最佳買點
predicting-bitcion-best-buying-point-with python pandas, MA, MACD

### import packages
requests, BeautifulSoup for web clawler
re, json for preprocess cleaning
pandas for buliding dataframe
matlibplot, pandas for plot

### Calculate MA, EMA
```
ma_list = [12, 26]
for ma in ma_list:
    df['EMA_' + str(ma)] = df["twd"].ewm(span = ma).mean()
for ma in ma_list:
    df['MA_' + str(ma)] = df["twd"].rolling(window = ma).mean()
```
* MA for Moving Average 12d / 26d
* EMA for Exponential Moving Averages 12d / 26d

### Calculate DIF, DEM
```
df['dif'] = df['EMA_12'] - df['EMA_26']
df["dem"] = df["dif"].ewm(span = 9).mean()
```
* DIF for difference between EMA_12 and EMA_26
* DEM for signal line, using DIF and calculate for its exponential moving average 9d

