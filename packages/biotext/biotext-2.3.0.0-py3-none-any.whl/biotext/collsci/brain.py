#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import numpy as np
import pandas as pd
from biotext.bag import tfidfVect, wcVect, size, pptext, zeros, repmat
from sweep import fas2sweep
from biotext.huflus import Huflus
from biotext.fastatools import list2fasta
from biotext.aminocode import encodetext
from scipy.cluster import hierarchy
from numpy import linalg as LA

def versor(vets):
    # Transforma vets (linhas) em seus versores
    n,m = size(vets)
    Zr = zeros(n,m)
    inorm = np.sqrt(np.sum(vets**2,1))
    
    mret = vets/repmat(inorm,m).T
    mret[inorm==0,:] = Zr[inorm==0,:]
    return mret, inorm
    
def normmaxmin(w):
    xmax = np.max(w)
    xmin = np.min(w)
    n,m = size(w)
    xmax=repmat(xmax,n,1)
    xmin = repmat(xmin,n,1)
    den = (xmax - xmin)
    den[den==0] = 1
    xmin[den==0] = xmax[den==0]
    mret = (w - xmin)/den
    return mret
    
def mat2tree(mat):
    Z = hierarchy.linkage(mat, 'ward')
    tree = hierarchy.to_tree(Z,False)
    return tree

def tree2newick(tree_or_node, leafs, parent_dist, newick=""):
    if tree_or_node.is_leaf():
        return (leafs[tree_or_node.id]+':'+str(round(parent_dist - tree_or_node.dist,2))+newick)
    else:
        if len(newick) > 0:
            newick = '):'+str(round(parent_dist - tree_or_node.dist,2))+newick
        else:
            newick = ');'
        newick = tree2newick(tree_or_node.get_left(), leafs, tree_or_node.dist, newick)
        newick = '('+tree2newick(tree_or_node.get_right(), leafs, tree_or_node.dist, ','+newick)
        return newick

LEN = np.vectorize(lambda x: len(x))    

def wordmat2tree(self,mw=200):
    scores = self.wordmat
    words = self.words
        
    # maximo de palavras
    if mw == 0 or mw > len(words):
        mw = len(words)
        
    words = words[0:mw]
    scores = scores[0:mw,:]
    tree = mat2tree(scores)
    newick = tree2newick(tree, words, tree.dist)

    return newick

def wordmat2tree(brain,mw=200):
    scores = brain.wordmat
    words = brain.words
        
    # maximo de palavras
    if mw == 0 or mw > len(words):
        mw = len(words)
        
    words = words[0:mw]
    scores = scores[0:mw,:]
    tree = mat2tree(scores)
    newick = tree2newick(tree, words, tree.dist)

    return newick

class Brain():    
    def __init__(self,corpus):
        self.corpus = pd.Series(np.array(corpus))
        
    def init(self,verbose=True):
        if verbose:
            print('0%')
        self.corpus2fasta()
        if verbose:
            print('20%')
        self.fasta2sweep()
        if verbose:
            print('40%')
        self.sweep2clus()
        if verbose:
            print('60%')
        self.corpus2ppcorpus()
        if verbose:
            print('80%')
        self.word2vect()
        if verbose:
            print('100%')
        
    def corpus2fasta(self):
        # Codificar
        AC = np.vectorize(lambda x: encodetext(x))
        self.fasta = list2fasta(AC(self.corpus))
        return self.fasta
        
    def corpus2ppcorpus(self):
        # Pré-processar
        PP =  np.vectorize(lambda x: pptext(x))
        ppText = pd.Series(zeros(1,len(self.corpus)).astype(int).astype(str)[0])
        ppText_s = PP(self.corpus[LEN(self.corpus)>0])
        
        ppText[LEN(self.corpus)>0] = ppText_s
        self.ppcorpus = ppText
        return pd.Series(self.ppcorpus)
        
    def fasta2sweep(self):
        # Vetorizar
        f=[]
        bt=[]
        for i in self.fasta:
            if len(str(i.seq)) >= 5:
                f.append(i)
                bt.append(True)
            else:
                bt.append(False)
        
        self.mat=zeros(len(self.fasta),600)
        mat = fas2sweep(f)
        self.mat[bt] = mat
        return self.mat
    
    def sweep2clus(self):        
        clus = zeros(len(self.corpus),1)-1
        # clusterizar
        clus_s = np.array([Huflus(self.mat[LEN(self.corpus)>=5]).clus()]).T
        clus[LEN(self.corpus)>=5] = clus_s
        clus=np.array(clus.T.astype(int).tolist()[0])
        self.he = False
        if np.unique(clus)[0] == -1:
            clus = clus + 1
            self.he = True
        self.corpusclus = clus
        self.clusnum = self.clusnumber = len(np.unique(clus))
        return self.corpusclus
    
    def word2vect(self,vect_method='tfidf'):
        ppText = self.ppcorpus[LEN(self.corpus)>0]
        clus = self.corpusclus[LEN(self.corpus)>0]
        agText = []
        for i in np.unique(clus):
            agText.append(re.sub('\s+$','',' '.join(ppText[clus==i])))
        
        if vect_method == 'tfidf':
            vector,words = tfidfVect(agText)
        elif vect_method == 'wc':
            vector,words = wcVect(agText)
        
        # ordenar
        scores = vector.T
        scores = scores.toarray()
        ns = normmaxmin(np.array([LA.norm(np.array(scores), axis=1)])).T
        idx = sorted(range(len(ns)), key=lambda k: ns[k])[::-1]
        words = np.array(words)
        words = words[idx]
        scores = scores[idx,:]
        words[0:10]=[x.upper() for x in words[0:10]]
        words = np.core.defchararray.add(np.core.defchararray.add(words, np.repeat(' - ', len(words))), np.array(range(1,len(words)+1)).astype(str))
        
        wordclus = Huflus(scores).clus()
        words = np.core.defchararray.add(np.core.defchararray.add(words, np.repeat(' - ', len(words))), wordclus.astype(str))

        self.wordclus = wordclus
        self.wordmat = scores
        self.words = words
        
    def wordmat2tree(self,mw=200):
        scores = self.wordmat
        words = self.words
        
        # maximo de palavras
        if mw == 0 or mw > len(words):
            mw = len(words)
        
        words = words[0:mw]
        scores = scores[0:mw,:]
        tree = mat2tree(scores)
        newick = tree2newick(tree, words, tree.dist)
        return newick