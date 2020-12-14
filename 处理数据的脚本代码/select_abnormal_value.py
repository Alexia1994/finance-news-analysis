# 根据真实波动率识别出波动率异常值
import pandas as pd
import numpy as np
df = pd.read_csv("C:\\Users\\赵一宁\\Desktop\\ticker_date_close_rate_volatility1.csv", encoding = 'gbk')
df = df.loc[(df.date >= '2016-10-01') & (df.date <= '2020-09-30')]
df['mean'] = df.groupby('ticker',as_index = False)['volatility'].transform('mean')
df['sigma'] = df.groupby('ticker',as_index = False)['volatility'].transform('std')
df['quantile'] = df.apply(lambda x: x['mean'] + 3 * x['sigma'], axis=1) #计算分位数
df['abnormal'] = df.apply(lambda x: '1' if x['quantile'] < x['volatility'] else '0', axis =1) #3σ原则
df['standardized'] = df.apply(lambda x: (x['volatility'] - x['mean']) / x['sigma'], axis=1) #波动率标准化
df.to_csv("C:\\Users\\赵一宁\\Desktop\\ticker_date_close_rate_volatility_abnormal222.csv")