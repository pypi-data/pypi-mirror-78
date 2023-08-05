#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File : base.py
@Author : Braylon1002
@Version : 1.0
@Contact : S.Braylon1002@gmail.com
Desc : None
"""

from abc import ABC, abstractmethod
from enum import Enum

class Column(ABC):
    """
    base class for column transformers
    """
    @abstractmethod
    def fit(self, x):
        """
        fit func for a column
        :param x: array-like
        the col of data
        :return: self
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, x):
        """
        transform func for a column processed by fit finc in advance
        :param x: array-like
        target col
        :return:
        """

        raise NotImplementedError

class ColumnType(Enum):
    NUMBER = 1
    CATEGORY = 2
    SEQUENCE = 3

class NumberColumn(Column):
    column_type = ColumnType.NUMBER

class CategoryColumn(Column):
    column_type = ColumnType.CATEGORY

class SequenceColumn(Column):
    column_type = ColumnType.SEQUENCE

    @abstractmethod
    def dimension(self):
        raise NotImplementedError

    @abstractmethod
    def max_length(self):
        raise NotImplementedError