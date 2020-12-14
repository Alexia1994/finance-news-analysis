#encoding: utf-8
#3.异常波动下新闻特征选择
#特征权重计算
import pandas as pd
import dataset
import numpy as np

def  wet(rcd):
    a = rcd.normal_contain
    b = rcd.abnormal_contain
    c = rcd.normal_discontain
    d = rcd.abnormal_discontain
    contain = a + b
    discontain = c + d
    N = a + b + c + d
    p_c = (a+c) / N
    p_c_t = (a+1) / (contain + 2)
    ret = np.fabs(p_c * np.log(p_c_t*(1-p_c) / p_c / (1-p_c_t)))
    p_c = (b+d) / N
    p_c_t = (b+1) / (contain+2)
    ret += np.fabs(p_c * np.log(p_c_t*(1-p_c)/p_c/(1-p_c_t)))
    return  ret*contain / N

def IG(rcd):
    def entropy(p):
        if p==1 or p==0:
            return 0
        return-(p*np.log2(p) + (1-p) * np.log2(1-p))

    a = rcd.normal_contain
    b = rcd.abnormal_contain
    c = rcd.normal_discontain
    d = rcd.abnormal_discontain
    contain = a+b
    discontain = c+d
    N = a+b+c+d
    p_c = (a+c)/N
    p_c_t = a/contain
    p_c_t_ = c/discontain
    return entropy(p_c) - contain/N * entropy(p_c_t) - discontain/N * entropy(p_c_t_)

def ECE(rcd):
    a = rcd.normal_contain
    b = rcd.abnormal_contain
    c = rcd.normal_discontain
    d = rcd.abnormal_discontain
    contain = a+b
    discontain = c+d
    N = a+b+c+d
    p_t = (contain+1) / (N+2)
    p_c = (a+c+1) / (N+2)
    p_c_ = (b+d+1) / (N+2)
    p_c_t = (a+1)/ (contain+2)
    p_c_t_ = (b+1)/(contain+2)
    return p_t * p_c_t * np.log2(p_c_t/p_c) + p_t * p_c_t_ * np.log2(p_c_t_/p_c_)

def chisquare(rcd):
    a = rcd.normal_contain
    b = rcd.abnormal_contain
    c = rcd.normal_discontain
    d = rcd.abnormal_discontain
    N = a+b+c+d
    return N/(a+b) * (a*d-b*c)/(a+c) * (a*d-b*c)/(b+d)/(c+d)

# 整出了一个dataframe
# 计算某列中有多少不同的值
def calcDF(news_in_normal, news_in_abnormal):
    word_in_normal = pd.DataFrame(' '.join(news_in_normal.headline_after_tokenize).split(' '), columns = ['normal_cnt'])['normal_cnt'].value_counts()
    word_in_abnormal = pd.DataFrame(' '.join(news_in_abnormal.headline_after_tokenize).split(' '), columns = ['abnormal_cnt'])['abnormal_cnt'].value_counts()
    df = pd.concat([word_in_normal, word_in_abnormal], axis = 1)
    print(df)
    return df

# 计算混淆矩阵
def calcConfMatrix(news_in_normal, news_in_abnormal):
    words_in_normal = set(' '.join(news_in_normal.headline_after_tokenize).split(' '))
    words_in_abnormal = set(' '.join(news_in_abnormal.headline_after_tokenize).split(' '))
    # 统计所有的单词
    words = words_in_normal|words_in_abnormal
    normal_contain = {x:0 for x in words}
    abnormal_contain = {x:0 for x in words}
    
    for rcd in news_in_normal.headline_after_tokenize:
        for word in set(rcd.split(' ')):
            normal_contain[word] += 1
    for rcd in news_in_abnormal.headline_after_tokenize:
        for word in set(rcd.split(' ')):
            abnormal_contain[word] += 1

    df = []
    df.append(pd.DataFrame.from_dict(normal_contain, orient='index',
    columns = ['normal_contain']))

    df.append(pd.DataFrame.from_dict(abnormal_contain, orient='index',
    columns = ['abnormal_contain']))
    df=pd.concat(df, axis = 1)
    df['normal_discontain'] = len(news_in_normal) - df['normal_contain']
    df['abnormal_discontain'] = len(news_in_abnormal) - df['abnormal_contain']
    return df

def run():
    news_tokenized = dataset.loadNewsTokenizedAndLabel('./input/')
    news_in_normal = news_tokenized[news_tokenized['label'] == 0]
    news_in_abnormal = news_tokenized[news_tokenized['label'] == 1]
    #计算不同类别中的字频
    df = calcDF(news_in_normal, news_in_abnormal)
    df.to_csv('./input/character_frequency.csv', encoding="utf_8")
    #计算混淆矩阵
    df = calcConfMatrix(news_in_normal, news_in_abnormal)
    #各权重计算方法
    df['WET'] = df.apply(wet, axis = 1)#文本证据权重
    df['IG'] = df.apply(IG, axis = 1)#信息增益
    df['ECE'] = df.apply(ECE, axis = 1)#期望交叉熵
    df['chisquare'] = df.apply(chisquare, axis = 1)#卡方统计量
    df.to_csv('./input/feature_weight.csv', encoding = "utf_8")

if __name__ == "__main__":
    run()