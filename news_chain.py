import numpy as np
import matplotlib.pyplot as plt
import chainer
from chainer import cuda, Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

class NewsChain(Chain):
    def __init__(self):
        super(NewsChain, self).__init__(
            l1 = L.Linear(10, 3), # what if the words are less than 10 words?
            l2 = L.Linear(3, 3)
        )

    def __call__(self, x, y):
        return F.mean_squared_error(self.fwd(x), y)

    def fwd(self, x):
        return F.softmax(self.l1(x))
