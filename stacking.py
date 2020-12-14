#Stacking过程
from sklearn.model_selection import KFold
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin, clone
import numpy as np
import xgboost as xgb
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor as MLP
from sklearn.svm import LinearSVR
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

import process_train_data

class StackingAveragedModels(BaseEstimator, RegressorMixin, TransformerMixin):
    
    def __init__(self, base_models, meta_model, n_folds = 5):
        self.base_models = base_models
        self.meta_model = meta_model
        self.n_folds = n_folds
    #将原来的模型clone出来，并且进行实现fit功能

    def fit(self, X, y):
        self.base_models_ = [list() for x in self.base_models]
        self.meta_model_ = clone(self.meta_model)
        kfold = KFold(n_splits = self.n_folds, shuffle = True, random_state = 156)
        #对于每个模型，使用交叉验证的方法来训练初级学习器，并且得到次级训练集
        out_of_fold_predictions = np.zeros((X.shape[0], len(self.base_models)))
        for i, model in enumerate(self.base_models):
            for train_index, holdout_index in kfold.split(X, y):
                instance = clone(model)
                instance.fit(X[train_index], y[train_index])
                y_pred = instance.predict(X[holdout_index])
                out_of_fold_predictions[holdout_index, i] = y_pred
                self.base_models_[i].append(instance)
        #使用次级训练集来训练次级学习器
        self.meta_model_.fit(out_of_fold_predictions,y)
        return self

    def predict(self, X):
        meta_features = np.column_stack([
        np.column_stack([model.predict(X) for model in base_models]).mean(axis = 1)
        for base_models in self.base_models_ ])
        return self.meta_model_.predict(meta_features)

def run(wordNum = 100):
    train_data = process_train_data.get_data("./input/pre_train.csv")
    train_X = train_data.drop(['date', 'true_volatility', 'label', 'ticker'], axis = 1)
    train_Y = train_data['true_volatility']
    trainX_vec = np.vstack([train_X.iloc[i].values[0] for i in range(len(train_X))])
    trainY_vec = np.array([train_Y.iloc[i] for i in range(len(train_Y))])
    svm = LinearSVR()
    mlp = MLP(activation = 'logistic')
    xgboost = xgb.XGBRegressor()
    gbdt = GradientBoostingRegressor()
    meta_model = xgb.XGBRegressor()
    meta_model = LinearSVR()
    clf = StackingAveragedModels([svm, mlp, xgboost, gbdt], meta_model)
    clf.fit(trainX_vec, trainY_vec)
    joblib.dump(clf, './models/stacking.m')

def predict():
    cls = joblib.load("./models/stacking.m")
    test_data = process_train_data.get_data("./input/pre_test.csv")
    test_X = test_data.drop(['date', 'true_volatility', 'label', 'ticker'], axis = 1)
    test_Y = test_data['true_volatility']
    testX_vec = np.vstack([test_X.iloc[i].values[0] for i in range(len(test_X))])
    testY_vec = np.array([test_Y.iloc[i] for i in range(len(test_Y))])
    result = cls.predict(testX_vec)
    return result

if __name__ == "__main__":
    #run()
    result = predict()
    f = open("./stacking.txt", "w+")
    for v in result:
        f.write(str(v) + "\n")
    f.close()