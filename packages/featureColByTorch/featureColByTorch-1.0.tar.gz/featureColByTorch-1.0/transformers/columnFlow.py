#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File : columnFlow.py
@Author : Braylon1002
@Version : 1.0
@Contact : S.Braylon1002@gmail.com
Desc : None
"""
import numpy as np

class ColumnFlow(object):
    """
    class of column flow
    implementing the fit & transform
    """
    def __init__(self, transformers, verbose=False):
        ColumnFlow.__check_transformers(transformers)
        self.transformers = transformers
        self.verbose = verbose

    @staticmethod
    def __check_transformers(transformers):
        if not isinstance(transformers, list):
            raise TypeError(
                "transformer must be list type"
            )
        types = [
            transformer.column_type for transformer in transformers
        ]

        if len(set(types)) != 1:
            raise ValueError(
                "transformers must be the same type"
            )

    def fit(self, x):
        """
        fit all the transformers in the transformers_list
        :param x: target data
        :return:
        """
        transformed_x = np.asarray(x).ravel()
        for transformer in self.transformers:
            transformer.fit(transformed_x)
            transformed_x = transformer.transform(transformed_x)
        return self

    def transform(self, x):
        """
        transform x by all fitted transformers
        :param x: array-like
            column data to be transformed
        :return: array-like
            transformed data
        """
        transformed_x = np.asarray(x).ravel()
        for transformer in self.transformers:
            transformed_x = transformer.transform(transformed_x)
        return transformed_x
