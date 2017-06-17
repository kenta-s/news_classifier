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

def extract_words(text):
    node = mecab.parseToNode(text)
    words = []
    while node:
        meta = node.feature.split(",")
        if meta[0] == "名詞":
            words.append(node.surface)
        node = node.next
    return words

f = open('sample_news/yahoo_news.json', 'r')
news_list = json.load(f)
f.close()
dictionary_name = 'words.txt'
dictionary = corpora.Dictionary.load_from_text(dictionary_name)
for key in news_list:
    news = news_list[key]
    text = news['content']
    words = extract_words(text)
    new_dictionary = corpora.Dictionary([words])
    dictionary.merge_with(new_dictionary)
    dictionary.save_as_text(dictionary_name)

for i in range(100):
    for key in news_list:
        news = news_list[key]
        text = news['content']
        words = extract_words(text)

        y = np.zeros(3).astype(np.float32)
        index = int(news['label'])
        y[index] = 1.0
        y = Variable(y).reshape(1, 3)
        vec = dictionary.doc2bow(words)
        dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
        # cut_dense = dense[0:10]

        # x = Variable(np.array(cut_dense).astype(np.float32).reshape(1, 1853))
        x = Variable(np.array(dense).astype(np.float32).reshape(1, 1853))
        # sports: 2
        # y = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # refactor this shit
        # y = y[0:8]
        # y = Variable(np.array(y).astype(np.float32).reshape(1, 8))
        model.zerograds()
        loss = model(x, y)
        loss.backward()
        optimizer.update()

text = "【森下悠里が結婚 昨年から交際】タレントの森下悠里がインスタグラムで、昨年末から交際していた男性と6月8日に結婚したことを報告。10年来の友人だという。"
words = extract_words(text)

# embed()

# # save
# dictionary.save_as_text('hoge.txt')

# # load
# dictionary = corpora.Dictionay.load_from_text('hoge.txt')

vec = dictionary.doc2bow(words)
dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
# cut_dense = dense[0:10]

# xt = Variable(np.array(cut_dense).astype(np.float32).reshape(1, 1853))
xt = Variable(np.array(dense).astype(np.float32).reshape(1, 1853))
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
