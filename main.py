# global setting
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas


#輸入要查詢的時間
print("請輸入你想要搜尋的時間, 請依序輸入年(ex: 2017),月(ex: 05),日(ex: 01), 最早可回溯到2013-04-28")
year = input()
month = input()
date = input()
fin = [year, '-', month, '-', date]
fin1 = ''.join(fin)


#crawler
res = requests.get("https://www.coingecko.com/zh-tw/%E5%8C%AF%E7%8E%87%E8%B5%B0%E5%8B%A2%E5%9C%96/%E6%AF%94%E7%89%B9%E5%B9%A3/twd")
soup = BeautifulSoup(res.text, "html.parser")
a = soup.select("#coin_maxd_historical_price_chart")[0].prettify("utf-8").decode("utf-8")
m = re.search('<div data-prices="(.*?)"', a)

#build dataframe
js = json.loads(m.group(1))
df = pandas.DataFrame(js)
df.columns = ["time", "twd"]
df["time"] = pandas.to_datetime(df["time"], unit = "ms")
df.index = df["time"]


#prepare to plot
%pylab inline
#df["twd"].plot(kind = "line", figsize = [15, 5])


# calculate MA, EMA
ma_list = [12, 26]
for ma in ma_list:
    df['EMA_' + str(ma)] = df["twd"].ewm(span = ma).mean()
for ma in ma_list:
    df['MA_' + str(ma)] = df["twd"].rolling(window = ma).mean()
    

# calculate DIF, DEM
df['dif'] = df['EMA_12'] - df['EMA_26']
df["dem"] = df["dif"].ewm(span = 9).mean()


# plot for Moving Average
df2 = df[df["time"] >= fin1]
df2[["twd","MA_12"]].plot(kind = "line", figsize = [20, 5])


# plot  for Moving Average Convergence / Divergence
df2[['twd']].plot(kind = "line", figsize = [20, 5], fontsize = 10)
df2[['dif','dem']].plot(kind = "line", figsize = [20,5], fontsize = 10)
