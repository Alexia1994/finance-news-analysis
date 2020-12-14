#新闻的描述性统计
import pandas as pd
import numpy as np 
df = pd.read_table('C:\\Users\\赵一宁\\Desktop\\total.txt', encoding = 'utf-8', header = None, sep=',')
df.columns =['ticker','name','heading','date','time','address']
df.drop(columns = 'address', axis = 1, inplace = True)
df.date = pd.to_datetime(df.date)
news = df.loc[(df.date >= '2016-10-01') & (df.date <= '2020-09-30')]
news.groupby('ticker')['heading'].count() #总新闻数量
news.groupby('ticker')['date'].nunique() #计算有新闻的天数
news.groupby('ticker')['date'].apply(lambda x: x.value_counts()).reset_index(name='date').groupby('ticker')['date'].max()#计算每日最大新闻数
news.groupby('ticker')['date'].min() #计算新闻最早出现日期
import warnings
warnings.filterwarnings('ignore') 
week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期天',
  }
    day = date.weekday()
    return week_day_dict[day]
print(get_week_day(datetime.datetime.now()))
news['week'] = news['date'].apply(lambda x: x.weekday()).map(week_day_dict)#计算新闻出现在周几

import matplotlib 
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置加载的字体名，解决中文不显示的问题
plt.rcParams['axes.unicode_minus'] = False 
sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})
fig = sns.countplot(x=news.week, order=['星期一', '星期二', '星期三','星期四','星期五','星期六','星期天']).get_figure()#周内新闻统计图
fig.savefig("C:\\Users\\赵一宁\\Desktop\\test.png", dpi=1080)