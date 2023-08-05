#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File : CategoryTransformer.py
@Author : Braylon1002
@Version : 1.0
@Contact : S.Braylon1002@gmail.com
Desc : None
"""
from .base import CategoryColumn
from collections import Counter
import numpy as np

class CategoryTransformer(CategoryColumn):
    def __init__(self, min_cnt=5, word2idx=None, idx2word=None):
        self.min_cnt = 5
        self.word2idx = word2idx if word2idx else dict()
        self.idx2word = idx2word if idx2word else dict()

    def fit(self, x):
        if not self.word2idx:
            counter = Counter(np.asarray(x).ravel())
            terms = sorted(list(filter(lambda x: counter[x] >= self.min_cnt, counter)))
            self.word2idx = dict(
                zip(terms, range(1, len(terms) + 1))
            )
            self.word2idx['__PAD__'] = 0
            if '__UNKNOWN__' not in self.word2idx:
                self.word2idx['__UNKNOWN__'] = len(self.word2idx)

        if not self.idx2word:
            self.idx2word = {
                idx: word_term for word_term, idx in self.word2idx.items()
            }

        return self

    def transform(self, x):
        transform_x = list()
        for term in np.asarray(x).ravel():
            try:
                transform_x.append(self.word2idx[term])
            except:
                transform_x.append(self.word2idx['__UNKNOWN__'])

        return np.asarray(transform_x, dtype=np.int64)

    def dimension(self):
        return len(self.word2idx)
