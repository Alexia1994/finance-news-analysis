import pandas as pd
# 这一部分的主要工作是:
# 因为同一只股票在同一天的新闻可能有多条，会造成数据冗余；
# 我们将将同一只股票在同一天的所有新闻合并成一条数据
def concat_func(x):
    return pd.Series({
        'headline_after_tokenize':' '.join(x['headline_after_tokenize'].unique()),
        'label': x['label'].unique()[0],
        'close': x['close'].unique()[0],
        'rate': x['rate'].unique()[0],
        'volatility': x['volatility'].unique()[0]
    }
    )
    
if  __name__ == "__main__": 
    filename = './input/combined.csv'
    df = pd.read_csv(filename, header = 0, encoding = "utf-8", dtype = {'ticker': str})
    df['ticker'] = df['ticker'].str.zfill(6)
    df.set_index(['ticker', 'date'], inplace = True)
    df.drop(['Unnamed: 0'], axis = 1)
    df = df.groupby(['ticker', 'date']).apply(concat_func)
    print(df)
    df.to_csv('./input/concat.csv', encoding = "utf_8")