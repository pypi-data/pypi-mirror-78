#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : base
# @Time         : 2020/9/5 7:12 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import time
import numpy as np
import pandas as pd
from abc import abstractmethod
from sklearn.model_selection import StratifiedKFold

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : base
# @Time         : 2020/9/5 7:12 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import time
import numpy as np
import pandas as pd
from abc import abstractmethod
from sklearn.model_selection import StratifiedKFold


class BaseOOF(object):

    def __init__(self, X, y, X_test=None, cv=5, feval=None, split_random_state=7):
        self.X = X
        self.y = y
        self.X_test = X_test if X_test is not None else self.X[:100]
        self.feval = feval

        self.oof_train = np.zeros(len(X))
        self.oof_test = np.zeros([len(self.X_test), cv])

        # n_fold, (train_index, valid_index)
        self.n_fold2index = list(
            enumerate(StratifiedKFold(cv, shuffle=True, random_state=split_random_state).split(X, y)))

    @abstractmethod
    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        """
        valid_predict, test_predict
        """
        raise NotImplementedError

    def run(self, oof_file=None):

        for n_fold, (train_index, valid_index) in self.n_fold2index:
            print(f"\033[94mFold {n_fold + 1} started at {time.ctime()}\033[0m")
            X_train, y_train = self.X[train_index], self.y[train_index]
            X_valid, y_valid = self.X[valid_index], self.y[valid_index]

            valid_predict, test_predict = self.fit_predict(X_train, y_train, X_valid, y_valid, self.X_test)

            self.oof_train[valid_index] = valid_predict
            self.oof_test[:, n_fold] = test_predict

        self.oof_test_rank = pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)
        self.oof_test = self.oof_test.mean(1)

        if self.feval is not None:
            score = self.feval(self.y, self.oof_train)
            print(f"\n\033[94mCV Sorce: {score} ended at {time.ctime()}\033[0m")

        if oof_file is not None:
            print("Save OOF Prediction")
            self.oof_train_test = np.r_[self.oof_train, self.oof_test]
            pd.DataFrame({'oof': self.oof_train_test}).to_csv(oof_file, index=False)
