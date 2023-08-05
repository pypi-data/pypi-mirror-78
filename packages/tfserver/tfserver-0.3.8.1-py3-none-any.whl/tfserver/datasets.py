import numpy as np
from rs4 import pathtool
from hashlib import md5
import os
import math
import rs4
import random
import pickle
from .label import Label
from .normalizer import Normalizer
import tensorflow as tf

class Datasets:
    def __init__ (self, steps, trainset, validset, testset = None, labels = None, normalizer = None):
        self.trainset = trainset
        self.validset = validset
        self.testset = testset
        if testset is None:
            self.testset = validset
        self.steps = steps
        self.labels = labels
        self.normalizer = normalizer
        self.raw_testset = [None, None]

    def _to_numpy (self, data):
        if isinstance (data, dict):
            return { k: np.array (v) for k, v in data.items ()}
        else:
            return np.array (data)

    def _collect (self, data, index):
        if isinstance (data, dict):
            if self.raw_testset [index] is None:
                self.raw_testset [index] = { k: [] for k in data.keys () }
            for k, v in data.items ():
                self.raw_testset [index][k].extend (v)
        else:
            if self.raw_testset [index] is None:
                self.raw_testset [index] = []
            self.raw_testset [index].extend (data)

    def collect_testset (self):
        for xs, ys in self.testset.as_numpy_iterator ():
            self._collect (xs, 0)
            self._collect (ys, 1)
        self.raw_testset = (self._to_numpy (self.raw_testset [0]), self._to_numpy (self.raw_testset [1]))
        return self.raw_testset

    def testset_as_numpy (self):
        return self.raw_testset

    def save (self, assets_dir, save_testset = True): # typically checkpoint/assets
        pathtool.mkdir (assets_dir)
        if self.labels:
            obj = [ (lb._origin, lb.name) for lb in self.labels ]
            with open (os.path.join (assets_dir, 'labels'), 'wb') as f:
                f.write (pickle.dumps (obj))
        self.normalizer and self.normalizer.save (assets_dir)
        if save_testset:
            with open (os.path.join (assets_dir, 'testset'), 'wb') as f:
                f.write (pickle.dumps (self.collect_testset ()))

    @classmethod
    def load (cls, assets_dir):
        lables, testset, raw_testset = None, None, None
        if os.path.isfile (os.path.join (assets_dir, 'labels')):
            with open (os.path.join (assets_dir, 'labels'), 'rb') as f:
                labels = [Label (classes, name) for classes, name in pickle.loads (f.read ())]

        if os.path.isfile (os.path.join (assets_dir, 'testset')):
            with open (os.path.join (assets_dir, 'testset'), 'rb') as f:
                testset = pickle.loads (f.read ())
                raw_testset = testset
                testset = tf.data.Dataset.from_tensor_slices (testset).batch (8)

        dss = Datasets (0, None, None, testset, labels, Normalizer.load (assets_dir))
        dss.raw_testset = raw_testset
        return dss

def load (assets_dir):
    return Datasets.load (assets_dir)
