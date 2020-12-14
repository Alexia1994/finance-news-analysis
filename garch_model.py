#使用带时移窗口的GARCH模型计算波动率
import pandas as pd
import numpy as np
import arch

def garch(close, window = 30):
    def fit_transform(returns):
        #初始化Garch模型
        am = arch.arch_model(returns)
        #训练模型
        res = am.fit(update_freq = 5)
        #预测波动率
        forecasts = res.forecast(horizon=1)
        ret = np.sqrt(list(forecasts.variance['h.1'].tail(1))[-1])
        return ret
    r = np.log(close).diff()[1:]
    variances = []
    for i in range(1, len(r)-window):
        variances.append(fit_transform(r[i: i+window]))
    return variances

import warnings
warnings.filterwarnings("ignore")
trade_data = pd.read_csv('C:\\Users\\赵一宁\\Desktop\\close.csv')
res = []
for tkr,data in trade_data.groupby('ticker'):
    data.sort_values('date', inplace = True)
    variances = garch(data['close'])
    date = list(data['date'])
    date = date[-len(variances):]
    tkr='%06d' % tkr
    for variance, day in zip(variances, date):
        res.append((tkr,day,variance))
df = pd.DataFrame(res, columns=['ticker', 'date', 'variance'])
df.to_csv('C:\\Users\\赵一宁\\Desktop\\garch_forecast.csv',index = False)
