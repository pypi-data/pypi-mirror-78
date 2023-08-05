#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File : SequenceTransformer.py
@Author : Braylon1002
@Version : 1.0
@Contact : S.Braylon1002@gmail.com
Desc : None
"""

from .base import SequenceColumn
from collections import Counter
import numpy as np

class SequenceTransformer(SequenceColumn):
    def __init__(self, sep=' ', min_cnt=5, max_len=None,
                 word2idx=None, idx2word=None):
        self.sep = sep
        self.min_cnt = min_cnt
        self.max_len = max_len
        self.word2idx = word2idx
        self.idx2word = idx2word

    def fit(self, x):
        if not self.word2idx:
            counter = Counter()
            max_len = 0
            for sequence in np.array(x).ravel():
                words = sequence.split(self.sep)
                counter.update(words)
                max_len = max(max_len, len(words))
            if not self.max_len:
                self.max_len = max_len

            words = sorted(list(filter(lambda x: counter[x] >= self.min_cnt, counter)))
            self.word2idx = dict(
                zip(words, range(1, len(words) + 1))
            )
            self.word2idx['__PAD__'] = 0
            if '__UNKNOWN__' not in self.word2idx:
                self.word2idx['__UNKNOWN__'] = len(self.word2idx)

        if not self.idx2word:
            self.idx2word = {
                idx: word for word, idx in self.word2idx.items()
            }

        if not self.max_len:
            max_len = 0
            for sequence in np.array(x).ravel():
                words = sequence.split(self.sep)
                max_len = max(max_len, len(words))
            self.max_len = max_len

        return self

    def transform(self, x):
        transformed_x = list()
        for sequence in np.asarray(x).ravel():
            words = list()
            for word in sequence.split(self.sep):
                try:
                    words.append(self.word2idx[word])
                except:
                    words.append(self.word2idx['__UNKNOWN__'])

            transformed_x.append(np.asarray(words[0: self.max_len], dtype=np.int64))
        return np.asarray(transformed_x, dtype=np.object)

    def dimension(self):
        return len(self.word2idx)

    def max_length(self):
        return self.max_len