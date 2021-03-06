import sys, os
import json
import numpy as np
from chainer import Variable, optimizers, serializers
from news_chain import NewsChain

import MeCab
from gensim import corpora, matutils

from IPython import embed
mecab = MeCab.Tagger("-Ochasen")
mecab.parse('') # まずいタイミングでtextがGCされるらしくてmecabがエラー吐く問題を対処するハック。これは酷い。

def extract_words(text):
    node = mecab.parseToNode(text)
    words = []
    while node:
        meta = node.feature.split(",")
        if meta[0] == "名詞":
            words.append(node.surface)
        node = node.next
    return words

def convert_text_into_dense(dictionary, text):
    words = extract_words(text)
    vec = dictionary.doc2bow(words)
    dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
    return dense

def convert_text_into_variable(dictionary, text):
    dense = convert_text_into_dense(dictionary, text)
    return Variable(np.array([dense]))

base_path = os.path.dirname(os.path.abspath(__file__))
dic_file = os.path.normpath(os.path.join(base_path, 'trained/words.txt'))
npz_file = os.path.normpath(os.path.join(base_path, 'trained/news_classifier.npz'))
category_file = os.path.normpath(os.path.join(base_path, 'categories.json'))

dictionary = corpora.Dictionary.load_from_text(dic_file)
input_length = len(dictionary)
model = NewsChain(input_length)
serializers.load_npz(npz_file, model)

text = sys.argv[1]
x = convert_text_into_variable(dictionary, text)
loss = model.fwd(x)

f = open(category_file, 'r')
categories = json.load(f)
f.close()
idx = str(np.argmax(loss.data))

print(categories[idx])
