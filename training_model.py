#支持向量机，神经网络，XGBoost，GBDT训练
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVR
import joblib
from sklearn.neural_network import MLPRegressor as MLP
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor

import process_train_data
import numpy as np

def svm_fit(train_X, train_Y):
    clf = LinearSVR()
    clf.fit(train_X, train_Y)
    joblib.dump(clf, './models/svr.m')

def mlp_fit(train_X, train_Y):
    clf = MLP(activation = 'logistic')
    clf.fit(train_X, train_Y)
    joblib.dump(clf, './models/mlp.m')

def xgboost_fit(train_X, train_Y):
    clf = xgb.XGBRegressor()
    clf.fit(train_X, train_Y)
    joblib.dump(clf, './models/xgb.m')

def gbdt_fit(trian_X, train_Y):
    clf  =  GradientBoostingRegressor()
    clf.fit(trian_X, train_Y)
    joblib.dump(clf, './models/gbdt.m')

def predict():
    cls = joblib.load("./models/xgb.m")
    test_data = process_train_data.get_data("./input/pre_test.csv")
    test_X = test_data.drop(['date', 'true_volatility', 'label', 'ticker'], axis = 1)
    test_Y = test_data['true_volatility']
    testX_vec = np.vstack([test_X.iloc[i].values[0] for i in range(len(test_X))])
    testY_vec = np.array([test_Y.iloc[i] for i in range(len(test_Y))])
    result = cls.predict(testX_vec)
    f = open("./xgb.txt", "w+")
    for v in result:
        f.write(str(v) + "\n")
    f.close()

def main():
    train_data = process_train_data.get_data("./input/pre_train.csv")
    train_X = train_data.drop(['date', 'true_volatility', 'label', 'ticker'], axis = 1)
    train_Y = train_data['true_volatility']
    trainX_vec = np.vstack([train_X.iloc[i].values[0] for i in range(len(train_X))])
    trainY_vec = np.array([train_Y.iloc[i] for i in range(len(train_Y))])
    svm_fit(trainX_vec, trainY_vec)
    mlp_fit(trainX_vec, trainY_vec)
    xgboost_fit(trainX_vec, trainY_vec)
    gbdt_fit(trainX_vec, trainY_vec)

if __name__ == "__main__":
    #main()
    predict()