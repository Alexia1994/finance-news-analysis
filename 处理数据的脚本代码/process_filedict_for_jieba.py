# encoding: utf-8
import os
import re
# 这一部分的主要工作是：将新词发现的短语整合成userdict，jieba load下来后再进行分词，就不会把这些短语切开
# 返回已经成功爬下来的目录
def load_ticker():
    return set(code[:6] for code in os.listdir('./cache/news01/'))

def loadNewWords():
    new_words = []
    ticker_download = load_ticker()
    # 对于每一个文件
    for dir in ticker_download:
        filename = './cache/news01/' + str(dir)+ '/NewTermlist.txt'
        print(filename)
        with open(filename, 'r', encoding = 'utf-8') as f:
                for idx, line in enumerate(f):
                    if idx == 0:
                        continue
                    new_word = list(line.strip().split('\t'))
                    print(new_word[0])
                    new_words.append(new_word[0])

    fout = open('./input/userdict.txt', 'w', encoding = 'utf-8')
    fout.write('\n'.join(new_words))
    fout.close()
    return

def  main(): 
    loadNewWords()
     
if  __name__ == "__main__": 
    main() 