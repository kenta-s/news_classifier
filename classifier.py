# You must install mecab before running this script.

# $ brew install mecab
# $ brew install mecab-ipadic
# $ pip install mecab-python3

# And gensim
# $ pip install gensim

import numpy as np
from chainer import Variable, optimizers
from news_chain import NewsChain

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

news = pd.read_csv('sample_news/yahoonews.csv')

# from IPython import embed
# from IPython.terminal.embed import InteractiveShellEmbed
#
# embed()

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

model = NewsChain()
optimizer = optimizers.SGD() # TODO: change this to Adam
optimizer.setup(model)

cut_dense = dense[0:10]

for i in range(100):
    x = Variable(np.array(cut_dense).astype(np.float32).reshape(1, 10))
    # sports: 2
    y = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # refactor this shit
    y = y[0:8]
    y = Variable(np.array(y).astype(np.float32).reshape(1, 8))
    model.zerograds()
    loss = model(x, y)
    loss.backward()
    optimizer.update()

print(loss)
# from IPython import embed
# from IPython.terminal.embed import InteractiveShellEmbed
#
# embed()
