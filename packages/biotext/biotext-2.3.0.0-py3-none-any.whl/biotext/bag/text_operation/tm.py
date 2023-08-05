from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import re
import unidecode
import pandas as pd
import numpy as np
import os

def createVectorizer():
    vectorizer = TfidfVectorizer(encoding='utf-8',lowercase=True)
    return vectorizer
cvect = cv = createVectorizer

def vectorize(vectorizer,docs):
    vectorizer.fit_transform(docs)
    vector = vectorizer.transform(docs)
    words = vectorizer.get_feature_names()
    return vector,words
vect = vectorize

def wcVect(corpus):
    vectorizer = CountVectorizer(encoding='utf-8',lowercase=True)
    vectorizer.fit_transform(corpus)
    vector = vectorizer.transform(corpus)
    words = vectorizer.get_feature_names()
    return vector,words

def tfidfVect(corpus):
    vectorizer = TfidfVectorizer(encoding='utf-8',lowercase=True)
    vectorizer.fit_transform(corpus)
    vector = vectorizer.transform(corpus)
    words = vectorizer.get_feature_names()
    return vector,words

LEN = np.vectorize(lambda x: len(x))
REMOVE_ONLY_NUMBER = np.vectorize(lambda x: re.sub('^\d+$','',x))
REMOVE_ALL_WITH_NUMBER = np.vectorize(lambda x: re.sub('.*\d.*','',x))
def pptext(text):
    #normalizeSpaces
    text = re.sub('\s+',' ',text)
    #removePunctuation
    text = text.lower()
    #removePunctuation
    text = re.sub('','',text)
    #removeAccents
    text = unidecode.unidecode(text)
    #removeNonAlphanum
    text = re.sub('[^\w\d\s]','',text)
    #removeStopWords
    libLocal = re.sub('[\\\/][^\\\/]+$','',os.path.realpath(__file__))
    stop_words = list(pd.read_csv(libLocal+'/stopwords.txt',header=None)[0])
    word_tokens = re.split('\s+',text)
    word_tokens = REMOVE_ALL_WITH_NUMBER(word_tokens)
    word_tokens = word_tokens[LEN(word_tokens)>2] # remover palavras com 2 ou menos caracters
    word_tokens = word_tokens[LEN(word_tokens)<20] # remover palavras com 20 ou mais caracteres
    text = [w for w in word_tokens if not w in stop_words]
    text = ' '.join(text)
    text = re.sub('\s$','',text)
    
    return text
    
def tokenize(text):
    text = re.sub('\s+$','',text)
    text = re.split('\s+',text)
    return text