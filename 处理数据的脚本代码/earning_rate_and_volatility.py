import csv
import math
import numpy as np
f = open('1.csv','a')#打开一个新的文件，写入数据
#f.write('ticker,date,close,value,std\n')#写入表头
def read_csv(file_name):#将csv文件转换为list，一行是一个list
    f = open(file_name, 'r')
    content = f.read()
    final_list = list()
    rows = content.split('\n')
    for row in rows:
        final_list.append(row.split(','))
    return final_list
df = read_csv('ticker_date_close.csv')[1:]#截去表头
dit = {}#存储股票信息，股票代码为key
for i in df:
    if(i[0]):
        dit[i[0]] = [[],[],[0],[]].copy()#values值为[[],[],[0]]，是一个list，第一个list存储时间信息，第二个list存储对应估价，第三个list存储收益，第四个list存储标准差
for i in df:
    if(len(i)>1):
        dit[i[0]][0].append(i[1])
        dit[i[0]][1].append(float(i[2]))#加入相关信息
for i in dit.keys():
    for index in range(1,len(dit[i][0])):
        value = math.log(dit[i][1][index]/dit[i][1][index-1])#计算收益
        dit[i][2].append(value)#加入收益率
    l = dit[i]
    for j in range(len(l[2]) - 5):#计算标准差
        d = np.array(l[2][j:j+5])
        std = np.std(d)
        l[3].append(std)
    for j in range(len(l[2])-5,len(l[2])):#最后五天补0
        l[3].append(0)
for i in df:
    if(len(i)>=2):
        code = i[0]
        data = i[1]
        l = dit[code]#找到股票相关信息
        index = l[0].index(data)
        value = l[2][index]#找到股票某一天的相关信息
        a = ''
        for j in i:
            a = a + j + ','
        a = a + str(value) + ','#将每一行的数据综合起来
        a = a + str(l[3][index])#标准差
        #f.write(a+'\n')#写入文件