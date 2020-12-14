import pandas as pd
import os
# 这一部分的主要工作是：
# 首先，将经过特征选择后的单词load下来，作为特征表
# 其次，对于每一只股票在每一天的新闻数据（此时已进行了jieba分词），只保留特征表里的词
# 也就是说，以特征表里的词作为影响波动率的考量，对于其他的词不做考虑
def select_feature_words(x):
    feature = []
    news_per = list(x.split(' '))
    for new in news_per:
        if new in feature_selected:
            feature.append(new)
    feature = list(set(feature))
    return ' '.join(feature)

if  __name__ == "__main__": 
    filename = './input/feature_selected.txt'
    feature_selected = []
    #拿到feature_selected
    with open(filename, 'r', encoding = 'utf-8') as f:
        for line in f:
            feature_selected.append(line.strip())
    concat_file = "./input/concat.csv"
    news_concat = pd.read_csv(concat_file, header = 0, encoding = "utf-8", dtype = {'ticker': str})
    news_concat['ticker'] = news_concat['ticker'].str.zfill(6)
    print(news_concat)
    news_concat['headline_after_tokenize'] = news_concat['headline_after_tokenize'].apply(select_feature_words)
    news_concat.set_index(['ticker', 'date'], inplace = True)
    news_concat.to_csv('./input/tmp.csv', encoding = "utf_8")