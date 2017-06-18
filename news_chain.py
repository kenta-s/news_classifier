import numpy as np
import matplotlib.pyplot as plt
import chainer
from chainer import cuda, Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
# embed()

class NewsChain(Chain):
    def __init__(self):
        super(NewsChain, self).__init__(
            l1 = L.Linear(1843, 10), # what if the words are less than 10 words?
            l2 = L.Linear(10, 3)
        )

    def __call__(self, x, y):
        return F.mean_squared_error(self.fwd(x), y)

    def fwd(self, x):
        h1 = F.softmax(self.l1(x))
        h2 = self.l2(h1)
        return h2
