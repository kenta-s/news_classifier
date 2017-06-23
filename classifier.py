# You must install mecab before running this script.

# $ brew install mecab
# $ brew install mecab-ipadic
# $ pip install mecab-python3

# And gensim
# $ pip install gensim

import numpy as np
from chainer import Variable, optimizers, serializers
from news_chain import NewsChain

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

def extract_words(text):
    node = mecab.parseToNode(text)
    words = []
    while node:
        meta = node.feature.split(",")
        if meta[0] == "名詞":
            words.append(node.surface)
        node = node.next
    return words

def get_news_list():
    f = open('sample_news/news.json', 'r')
    news_list = json.load(f)
    news_list = [
        news_list['YahooNews'],
        news_list['news_line_me'],
        news_list['TwitterNewsJP'],
        news_list['nhk_news']]
    f.close()

    return news_list

def get_dictionary(news_list):
    dictionary_name = 'words.txt'
    words = []
    for each_news in news_list:
        for key in each_news:
            news = each_news[key]
            text = news['content']
            words.append(extract_words(text))

    dictionary = corpora.Dictionary(words)
    dictionary.save_as_text(dictionary_name)

    return dictionary

def convert_text_into_dense(dictionary, text):
    words = extract_words(text)
    vec = dictionary.doc2bow(words)
    dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
    return dense

def convert_text_into_variable(dictionary, text):
    dense = convert_text_into_dense(dictionary, text)
    return Variable(np.array([dense]))

def prepare_train_variables(dictionary, news_list):
    x_list = []
    y_list = []
    for each_news in news_list:
        for key in each_news:
            news = each_news[key]
            text = news['content']
            dense = convert_text_into_dense(dictionary, text)
            x_list.append(dense)
            y_list.append(int(news['label']))

    X = np.array(x_list).astype(np.float32)
    Y = np.array(y_list).astype(np.int32)
    N = len(X)
    Y2 = np.zeros(3 * N).reshape(N, 3).astype(np.float32)
    for i in range(N):
        Y2[i, Y[i]] = 1.0

    return X, Y, N, Y2

def train(model, optimizer, xtrain, ytrain):
    n = len(xtrain)
    bs = 25
    for j in range(5000):
        sffindx = np.random.permutation(n)
        for i in range(0, n, bs):
            idx = sffindx[i:(i+bs) if (i+bs) < n else n]
            x = Variable(xtrain[idx])
            y = Variable(ytrain[idx])
            model.zerograds()
            loss = model(x, y)
            loss.backward()
            optimizer.update()

def exec_test(model, x):
    y = model.fwd(x)
    ans = y.data
    nrow, ncol = ans.shape
    ok = 0

    for i in range(nrow):
        cls = np.argmax(ans[i,:])
        if cls == yans[i]:
          ok += 1

    print(ok, "/", nrow, " = ", (ok * 1.0)/nrow)

def classify_text(model, dictionary, text):
    x = convert_text_into_variable(dictionary, text)
    idx = str(np.argmax(model.fwd(x).data))

    f = open('categories.json', 'r')
    categories = json.load(f)
    f.close()

    return categories[idx]

news_list = get_news_list()
dictionary = get_dictionary(news_list)

input_length = len(dictionary)
model = NewsChain(input_length)
optimizer = optimizers.Adam()
optimizer.setup(model)

X, Y, N, Y2 = prepare_train_variables(dictionary, news_list)

index = np.arange(N)
xtrain = X[index[index % 2 != 0]]
ytrain = Y2[index[index % 2 != 0]]
xtest = X[index[index % 2 == 0]]
yans = Y[index[index % 2 == 0]]

train(model, optimizer, xtrain, ytrain)

x = Variable(xtest)
exec_test(model, x)

serializers.save_npz('news_classifier.npz', model)

# # saving model:
# serializers.save_npz('hoge_01.npz', model)

# # loading model:
# serializers.load_npz('hoge_01.npz', model)
