# You must install mecab before running this script.

# $ brew install mecab
# $ brew install mecab-ipadic
# $ pip install mecab-python3

# And gensim
# $ pip install gensim

import MeCab
import json
# usage of json is below... (I'm a beginner in Python :P)
#
# foo = open('categories.json', 'r')
# bar = json.load(foo)

import pandas as pd
# usage of pandas is below
# foo = pd.read_csv('sample_news/yahoonews.csv')
# foo['content'] # this should be a column name

from gensim import corpora, matutils

mecab = MeCab.Tagger("-Ochasen")

mecab.parse('') # まずいタイミングでtextがGCされるらしくてmecabがエラー吐く問題を対処するハック。これは酷い。

text = "【ナダル快挙 感動表現できない】「赤土の王者」ナダルが全仏10度目のV。「今は感動ばかりで言葉が見つかりません」と優勝杯を力強く抱きかかえ、会心の笑顔。"
node = mecab.parseToNode(text)

words = []
while node:
    meta = node.feature.split(",")
    if meta[0] == "名詞":
        words.append(node.surface)
    node = node.next

# # save
# dictionary.save_as_text('hoge.txt')

# # load
# dictionary = corpora.Dictionay.load_from_text('hoge.txt')
dictionary = corpora.Dictionary([words])
vec = dictionary.doc2bow(words)
dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])

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
            l1 = L.Linear(10, 8), # what if the words are less than 10 words?
            l2 = L.Linear(8, 8)
        )

    def __call__(self, x, y):
        return F.mean_squared_error(self.fwd(x, y))

    def fwd(self, x, y):
        return F.softmax(self.l1(x))

model = NewsChain()
optimizer = optimizers.SGD() # TODO: change this to Adam
optimizer.setup(model)

# from IPython import embed
# from IPython.terminal.embed import InteractiveShellEmbed
#
# embed()

# x = Variable(np.array(dense).astype(np.float32).reshape(1, ?))
