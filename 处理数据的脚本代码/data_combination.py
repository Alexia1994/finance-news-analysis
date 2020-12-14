#最后数据结合 将新闻文本与异常指标结合

import pandas as pd
import datetime
df = pd.read_csv('C:\\Users\\93599\\Desktop\\news_tokenized.csv', encoding = 'gbk' ,header =None)

df.columns = ['ticker','headline_after_tokenize','date']
df2 = pd.read_csv('C:\\Users\\93599\\Desktop\\ticker_date_close_rate_volatility_abnormal(1).csv', encoding = 'gbk')
df3 = pd.merge(df,df2,on = ['ticker','date'])
#df3.drop(columns=[''])

def fun(x):
    x.ticker = str(x.ticker)

df3.apply(fun ,axis=1 )
