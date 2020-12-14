import os
import numpy as np
import pandas as pd
# 这一部分的主要工作是：
# 将新闻进行one-hot编码，并和garch模型的输出进行concat；
# 经过这一部分处理后的数据 作为后边机器学习模型的输入（数据已经向量化）
def get_feature_words():
    filename = './input/feature_selected.txt'
    feature_selected = []
    #拿到feature_selected
    with open(filename, 'r', encoding = 'utf-8') as f:
        for line in f:
            feature_selected.append(line.strip())
    return feature_selected

def onehotEncoding(instance1, class1):
    temp1 = np.zeros(len(class1))
    temp1[class1.index(instance1)] = 1
    return temp1
    
def calVec(x):
    feature_selected = get_feature_words()
    Vec = np.zeros(len(feature_selected))
    if pd.isna(x):
        return Vec
    news_per = list(x.split(' '))
    Vec = np.zeros(len(feature_selected))
    for news in news_per:
        Vec_ = onehotEncoding(news, feature_selected)
        Vec += Vec_
    return Vec

def concat_all_feature(x):
    return np.append(x['headline_after_tokenize'], x['fore_volatility'])


def get_data(concat_file):
    pre_train = pd.read_csv(concat_file, header = 0, encoding = "utf-8", dtype = {'ticker': str})
    pre_train['ticker'] = pre_train['ticker'].str.zfill(6)
    
    pre_train['headline_after_tokenize'] = pre_train['headline_after_tokenize'].apply(calVec)
    pre_train['feature_vec'] = pre_train.apply(concat_all_feature, axis = 1)
    pre_train.drop(['headline_after_tokenize', 'fore_volatility'], axis = 1, inplace = True)
    #pre_train.to_csv('./input/train.csv', encoding = "utf_8")
    return pre_train

