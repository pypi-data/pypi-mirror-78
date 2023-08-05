#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File : NumberTransformer.py
@Author : Braylon1002
@Version : 1.0
@Contact : S.Braylon1002@gmail.com
Desc : None
"""

import numpy as np
from sklearn.preprocessing import StandardScaler

from .base import NumberColumn


class NumberTransformer(NumberColumn):
    def __init__(self):
        self.scaler = StandardScaler()

    def fit(self, x):
        self.scaler.fit(np.asarray(x, dtype=np.float).reshape(-1, 1))
        return self

    def transform(self, x):
        transformed_x = self.scaler.transform(
            np.asarray(x, dtype=np.float32).reshape(-1, 1)
        )
        return transformed_x.ravel()

