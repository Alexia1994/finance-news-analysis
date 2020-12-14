# encoding: utf-8
import os
import pandas as pd
# 这一部分的主要工作是：提供数据接口给外部使用
# 返回已经成功爬下来的目录
def load_ticker():
    return set(code for code in os.listdir('./cache/news/'))

def loadNews(input_path):
    news = []
    ticker_download = load_ticker()
    # 对于每一个文件
    for dir in ticker_download:
        filename = input_path + str(dir)
        with open(filename, 'r', encoding = 'utf-8') as f:
                for line in f:
                    task = tuple(line.strip().split(','))
                    news.append(task)
    
    return news

def loadStopWords(stopwords_filename):
    stopWords = []
    with open(stopwords_filename, 'r', encoding = 'utf-8') as stop_words:
        for line in stop_words:
            stopWords.append(line.strip())
    return stopWords
    
def loadNewsTokenizedAndLabel(input_path):
    filename = input_path + 'concat.csv'
    news_tokenized = pd.read_csv(filename, header = 0, encoding = "utf-8")
    return news_tokenized
