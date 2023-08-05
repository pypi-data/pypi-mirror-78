#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import re
import pandas as pd

def sortclussource(clus,brain):
    cl = brain.wordclus

    #scores = brain.scores
    words = brain.words
    corpus = pd.Series(brain.ppcorpus)
    
    # remover upper e rank
    f = np.vectorize(lambda x: re.split(' -\ ',x)[0].lower())
    w=f(words)
    
    #selecionar cluster
    w = w[cl==clus]
    
    #contar palavras no corpus
    word_counter = np.vectorize(lambda x: corpus.str.count('(\s|^)'+x+'($|\s)'), signature='()->(n)')
    W = pd.DataFrame(word_counter(w).T > 0).astype(int)
    
    #norma
    N = pd.Series(np.linalg.norm(W, axis=1))
    idx=np.argsort(N, kind ='heapsort', axis = 0)[::-1]
    #print(N[idx])
    
    return idx

def sortwordsource(word,brain,neighbors=10):
    word = word.lower()
    scores = brain.wordmat
    words = brain.words
    corpus = pd.Series(brain.ppcorpus)
    
    # remover upper e rank
    f = np.vectorize(lambda x: re.split(' -\ ',x)[0].lower())
    w=f(words)
    
    # definir idx da palavra
    try:
        word_idx = np.argwhere(w==word)[0][0]
    except:
        return
    
    #indexar palavras mais proximas
    dist=[np.linalg.norm(scores[word_idx]-scores[i]) for i in range(0,len(w))]
    idx=np.argsort(dist, kind ='heapsort', axis = 0)
    
    #definir maximo de palavras para usar no processo
    
    if neighbors < 0:
        totalWords=len(idx)
    else:
        totalWords=neighbors
    
    #ordenar palavras
    top10 = w[idx[0:totalWords]]
    top10 = np.insert(top10, 0, word)
    totalWords += 1
    
    #contar palavras no corpus
    word_counter = np.vectorize(lambda x: corpus.str.count('(\s|^)'+x+'($|\s)'), signature='()->(n)')
    c = word_counter(top10).T
    
    #definir pesos
    weight=np.array([10**ii for ii in range(0,totalWords)][::-1])
    weight = weight/weight[0]
    
    #definir scores
    c = c/np.max(c,axis=0)
    c = c*weight
    c = np.sum(c,axis=1)
    
    #ordenar scores
    idx2=np.argsort(c, kind ='heapsort', axis = 0)[::-1]
    
    #retornar idx
    r=corpus[idx2]

    return list(idx2)