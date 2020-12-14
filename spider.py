# encoding: utf-8
#新浪财经个股新闻爬虫代码
import os
import re
import sys
import time
import sqlite3
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import numpy as np
import requests
import chardet
import copy
import json

# return date_range of past numdays
def generate_past_n_days(numdays):
    """Generate N days until now,e.g.,[20151231, 20151230]."""
    base = datetime.datetime.today()
    date_range = [base - datetime.timedelta(days = x) for x in range(0, numdays)]
    return [x.strftime("%Y%m%d") for x in date_range]

# 得到 BeautifulSoup(html)
def get_soup_with_repeat(url, repeat_times = 3, verbose = True):
    for i in range(repeat_times):#repeat in case of httpfailure
        try:
            response = requests.get(url)
            html = response.content
            #print(chardet.detect(html))
            html = html.decode(chardet.detect(html)['encoding'],'ignore')
            #print(html[:100])
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            if i == 0:
                print(url)
                print(e)
            if verbose:
                print('retry...')
            time.sleep(np.random.poisson(3))
            continue

class SinaCrawler:
    def __init__(self):
        self.ticker_list_filename = './input/tickerList.csv'
        self.finished_reuters_filename = './input/finished.sina'
        self.failed_reuters_filename = './input/news_failed_tickers.csv'
        self.news_filename = './input/news_reuters.csv'
        self.log_filename = './input/news_sina.log'

    def load_finished_tickers(self):
        #when we restart a task,we may call calc_finished_ticker() in crawler/yahoo_finance.py
        #so that we can load the already finished reuters if any
        #return set(self._load_from_file(self.finished_reuters_filename))
        return set(code[:6] for code in os.listdir('./cache/news/'))

    def load_failed_tickers(self):
        failed_tickers = {} # {ticker:priority}
        for line in self._load_from_file(self.failed_reuters_filename):
            ticker, _, priority = line.split(',')
            failed_tickers[ticker] = priority
        return failed_tickers

    def _load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    yield line.strip()

    def fetch_content(self, task, date_range):
        ticker, name, exchange, market = task
        print("%s - %s - %s - %s" % (ticker, name, market, exchange))
        # exchange：交易所
        # shanghai & shenzhen ,only shanghai & shenzhen has exchange
        suffix = {'SSE':'sh','SZSE':'sz'}

        #e.g.http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh600000&Page=2

        url = "http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=" + suffix[exchange] + ticker + "&Page="
        ticker_failed = open(self.failed_reuters_filename, 'a+')
        today = datetime.datetime.today().strftime("%Y%m%d")
        
        # 如果第一页拿到的长度 >= 1
        if self.has_news(url + "1"):
            #this company has news, then fetch for N consecutive days in the past
            has_content = self.fetch_within_date_range(url, date_range, task, ticker)
            # 如果没有内容，输出没有内容
            if not has_content:
                print('%s has no content with in date range' % ticker)
            # 进入下面的else
        else:
            #this company has no news even if we don't set a date
            #add it into the lowest priority list
            print("%s has no news at all, set as LOWEST priority" % (ticker))
            ticker_failed.write(ticker+ ',' + today + ',' + 'LOWEST\n')

        ticker_failed.close()
    
    # 返回长度
    def has_news(self, url):
        #check the website to see if the ticker has any news
        #return the number of news
        soup = get_soup_with_repeat(url, repeat_times = 4)
        # return headline + time
        if soup:
            return len(soup.find_all("div", {'class': 'datelist'}))
        return 0

    def fetch_within_date_range(self, url, date_range, task, ticker):
        has_content = False
        page = 0
        self.last_content = None
        self.news = []
        while True:
            page += 1
            print('Crawlering page ' + str(page), end = ' ', flush = True)
            soup = get_soup_with_repeat(url + str(page))

            if soup and self.parse_news(soup, task, ticker, date_range):
                has_content = True
            else:
                break
        
        pd.DataFrame(self.news, columns=['ticker', 'name', 'title', 'date', 'time', 'url']).to_csv('./cache/news/'+ticker+'.csv', index = False, header = False)
        
        with open(self.log_filename, 'a+') as f:
            f.write(','.join((ticker, date_range[-1], date_range[0])) + '\n')
        return has_content

    # 将从content拿到的内容转移到self.news这个列表里
    def parse_news(self, soup, task, ticker, date_range):
        content = soup.find_all('div', {'class': 'datelist'})
        # 如果没有内容，返回false
        if not content:
            return False
        if content == self.last_content:
            return False
        else:
            self.last_content = content

        finish = False

        for i in range(len(content)):
            titles = [news.get_text() for news in content[i].find_all('a')]
            dates = re.findall(r'\d\d\d\d\-\d\d\-\d\d', content[i].get_text())
            times = re.findall(r'\d\d:\d\d', content[i].get_text())
            urls = [news.get('href') for news in content[i].find_all('a')]

            for title, dt, tm, url in zip(titles, dates, times, urls):
                if(dt[:4] + dt[5:6] + dt[7:8]) < date_range[-1]:
                    finish = True
                    break
                title = title.replace("," , " ").replace("\n", " ")
                self.news.append((ticker, task[1], title, dt, tm, url))
                
            if finish:
                break

        return True


    def run(self, numdays = 1000):
        """Start crawler back to numdays"""
        finished_tickers = self.load_finished_tickers()
        failed_tickers = self.load_failed_tickers()
        date_range = generate_past_n_days(numdays)
        #look back on the past X days
        #store low-priority task and run later
        delayed_tasks = {'LOWEST': set()}

        # ticker: stock code
        # 迭代所有的银行个股
        with open(self.ticker_list_filename, encoding = 'utf-8') as ticker_list:
            for idx, line in enumerate(ticker_list):
                #iterate all possible tickers
                if idx == 0:
                    continue
                task = tuple(line.strip().split(','))
                ticker, name, exchange, market = task
                if ticker in finished_tickers:
                    continue
                if ticker in failed_tickers:
                    priority = failed_tickers[ticker]
                    delayed_tasks[priority].add(task)
                    continue

                self.fetch_content(task, date_range)

        #run task with lowest priority
        for task in delayed_tasks['LOWEST']:
            self .fetch_content(task, date_range)


def  main(): 
     sina_crawler = SinaCrawler() 
     sina_crawler.run(2500) 
     
if  __name__ == "__main__": 
     main()
