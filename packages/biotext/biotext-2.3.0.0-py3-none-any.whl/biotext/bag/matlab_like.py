#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import math

def upper(txt):
    x = txt.upper()
    return x

def lower (txt):
    x = txt.lower()
    return x

def length(n):
    r = len (n)
    return r
    
def ones(lin,col):
    M = np.ones((lin,col))
    return M

def zeros(lin,col):
    M = np.zeros((lin,col))
    return M

def floor(n):
    r = math.floor(n)
    return r

def ceil(n):
    r = math.ceil(n)
    return r

def rand (lin,col):
    m = np.random.rand(lin,col)
    return m

# retorna o singular value decomposition
def svd (M):
    Q, s, Vt = np.linalg.svd(M, full_matrices=False)
    #V = Vt.T
    S = np.diag(s)
    return Q,S

# retorna a diagonal principal
def diag (M):
    R = np.diag(M)
    return R
    
# Floating-point relative accuracy
def eps (M):
    return np.finfo(M).eps
    
# return dimensions of a matrix
def size (M):
    return M.shape

def double(text):
    R=[]
    for i in text:
        i = map(bin,bytearray(i, 'utf8'))
        r = []
        for i2 in i:
            r.append(int(i2,2))
        R.append(r)
    return np.array(R)
     
def repmat(M,m,n=1):
    return np.tile(M,(m,n))

def prod(A):
    R=[]
    for i in A:
        R.append(np.prod(i))
    return np.array(R)

def find(a, func=lambda x:x>0):
    return [i for (i, val) in enumerate(a) if func(val)]
