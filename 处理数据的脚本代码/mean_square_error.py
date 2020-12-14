#计算均方误差
import pandas as pd
import numpy as np
df = pd.read_csv('C:\\Users\\赵一宁\\Desktop\\pre_test.csv', encoding = 'gbk')
def get_mse(records_real, records_predict):
    """
    均方误差 估计值与真值 偏差
    """
    if len(records_real) == len(records_predict):
        return sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real)
    else:
        return None
get_mse(df.true_volatility, df.fore_volatility)
get_mse(df.true_volatility, df.fore_volatility)
get_mse(df.true_volatility, df.stacking)
get_mse(df.true_volatility, df.svr)
get_mse(df.true_volatility, df.xgb)