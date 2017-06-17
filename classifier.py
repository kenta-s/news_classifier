# You must install mecab before running this script.

# $ brew install mecab
# $ brew install mecab-ipadic
# $ pip install mecab-python3

# And gensim
# $ pip install gensim

import numpy as np
from chainer import Variable, optimizers
from news_chain import NewsChain
model = NewsChain()
optimizer = optimizers.SGD() # TODO: change this to Adam
optimizer.setup(model)

import MeCab
from gensim import corpora, matutils
mecab = MeCab.Tagger("-Ochasen")
mecab.parse('') # まずいタイミングでtextがGCされるらしくてmecabがエラー吐く問題を対処するハック。これは酷い。

import json
# usage of json is below... (I'm a beginner in Python :P)
#
# foo = open('categories.json', 'r')
# bar = json.load(foo)

# for debug
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
# embed()

# import pandas as pd
# usage of pandas is below
# foo = pd.read_csv('sample_news/yahoonews.csv')
# foo['content'] # this should be a column name

# df = pd.read_csv('sample_news/yahoonews.csv')
# news_list = df.values
f = open('sample_news/yahoo_news.json', 'r')
news_list = json.load(f)
f.close()
for key in news_list:
    news = news_list[key]
    y = np.zeros(3).astype(np.float32)
    index = int(news['label'])
    y[index] = 1.0
    y = Variable(y).reshape(1, 3)

    text = news['content']
    node = mecab.parseToNode(text)
    words = []
    while node:
        meta = node.feature.split(",")
        if meta[0] == "名詞":
            words.append(node.surface)
        node = node.next

    dictionary = corpora.Dictionary([words])
    vec = dictionary.doc2bow(words)
    dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
    cut_dense = dense[0:10]

    x = Variable(np.array(cut_dense).astype(np.float32).reshape(1, 10))
    # sports: 2
    # y = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # refactor this shit
    # y = y[0:8]
    # y = Variable(np.array(y).astype(np.float32).reshape(1, 8))
    model.zerograds()
    loss = model(x, y)
    loss.backward()
    optimizer.update()

    # print(y)

text = "【ナダル快挙 感動表現できない】「赤土の王者」ナダルが全仏10度目のV。「今は感動ばかりで言葉が見つかりません」と優勝杯を力強く抱きかかえ、会心の笑顔。"
node = mecab.parseToNode(text)

words = []
while node:
    meta = node.feature.split(",")
    if meta[0] == "名詞":
        words.append(node.surface)
    node = node.next

# embed()

# # save
# dictionary.save_as_text('hoge.txt')

# # load
# dictionary = corpora.Dictionay.load_from_text('hoge.txt')

dictionary = corpora.Dictionary([words])
vec = dictionary.doc2bow(words)
dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
cut_dense = dense[0:10]

xt = Variable(np.array(cut_dense).astype(np.float32).reshape(1, 10))
yt = model.fwd(xt)
ans = yt.data

print(ans)
# embed()
# nrow, ncol = ans.shape

# for i in range(100):
#     x = Variable(np.array(cut_dense).astype(np.float32).reshape(1, 10))
#     # sports: 2
#     y = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # refactor this shit
#     y = y[0:8]
#     y = Variable(np.array(y).astype(np.float32).reshape(1, 8))
#     model.zerograds()
#     loss = model(x, y)
#     loss.backward()
#     optimizer.update()

# from IPython import embed
# from IPython.terminal.embed import InteractiveShellEmbed
#
# embed()
