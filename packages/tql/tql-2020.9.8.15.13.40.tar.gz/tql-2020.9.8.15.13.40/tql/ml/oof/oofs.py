#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : LGBMClassifierOOF
# @Time         : 2020/9/5 8:40 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .base_oof import BaseOOF
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier


class LGBMClassifierOOF(BaseOOF):

    def __init__(self, X, y, params=None, **kwargs):
        super().__init__(X, y, **kwargs)
        self.params = params

    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        clf = LGBMClassifier()
        if self.params is not None:
            clf.set_params(**self.params)
            # print(clf.get_params())

        clf.fit(X_train, y_train,
                eval_set=[(X_train, y_train), (X_valid, y_valid)],
                eval_names=('Train', 'Valid'),
                verbose=True,
                early_stopping_rounds=None  # fit_params
                )

        valid_predict = clf.predict_proba(X_valid)[:, 1]
        test_predict = clf.predict_proba(X_test)[:, 1]
        return valid_predict, test_predict
