# encoding: utf-8
#2. 新闻预处理
import os
import operator
import argparse
import pandas as pd
import json
import numpy as np
import platform
import jieba
import re
import dataset
import datetime

def tokenize_news(headline,  stopWords):
    tokens = jieba.lcut(headline)#+nltk.word_tokenize(body)
    print(1)
    tokens = list(map(digit_filter, tokens))
    tokens=[t for t in tokens if t not in stopWords and t != ""]
    return(tokens)

def digit_filter(word):
    check = re.match(r'\d*\.?\d*', word).group() 
    if check == "":
        return word
    else:
        return ""

# 去除重叠部分
def isSimilar(x, y):
    x_ = set(x.split(' '))
    y_ = set(y.split(' '))
    return x_.issubset(y_) or y_.issubset(x_)

# 定一下开始时间
def run(date_begin = '20160101'):
    news = dataset.loadNews('./input/news/')
    stopWords = dataset.loadStopWords('./input/HIT_stop_words.txt')
    tokenized_news = {}
    print(news[0])
    file_userdict = "./input/userdict.txt"
    jieba.load_userdict(file_userdict)
    for task in news:
        if(len(task) != 6):
            print(task)
        tkr, name, headline, dt, tm, url = task
        dt = dt[:4] + dt[5:7] + dt[8:10]
        if dt < date_begin:
            continue
        if ('晚间公告速递' in headline) or ('股海导航' in headline) or ('公告（系列）' in headline):
            continue
        # 用停用词去分词
        # tokenized_news这个词典中，每一个tkr对应的是 分好词的news
        tokens = tokenize_news(headline, stopWords)
        if not tkr in tokenized_news.keys():
            tokenized_news[tkr]=[]
        tokenized_news[tkr].append((' '.join(tokens), datetime.datetime.strptime(dt, "%Y%m%d")))

    fout = open('./input/news_tokenized.csv', 'w', encoding = 'utf-8')

    for tkr in tokenized_news.keys():
        news = tokenized_news[tkr]
        # 按照时间排序
        news.sort(key = lambda x:x[1])
        l = 0
        r = 1

        # 先写入对应的第一个news
        print(news[0][0])
        fout.write(','.join((tkr, news[0][0], news[0][1].strftime("%Y%m%d"), '\n')))
        while r < len(news):
            dt = news[r][1]
            #判断最近7天的新闻的相似程度，如果有重复的就不要写
            while (l < r) and (dt > news[l][1] + datetime.timedelta(days = 7)):
                l += 1
            flag = True
            for i in range(l, r):
                if isSimilar(news[i][0], news[r][0]):
                    flag = False
                    break
            if flag:
                print(news[r][0])
                fout.write(','.join((tkr,news[r][0], news[r][1].strftime("%Y%m%d"), '\n')))
            r += 1

    fout.close()

if __name__ == "__main__":
    run()
