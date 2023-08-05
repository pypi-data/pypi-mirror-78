#!/usr/bin/python
# -*- coding: utf-8 -*-
from biotext.bag import size, zeros, repmat, rand
import numpy as np
from scipy.cluster.hierarchy import ward, leaves_list
from scipy.signal import argrelextrema
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt

def euclDist(a,b):
    dist = np.linalg.norm(a-b)
    return dist
ED = np.vectorize(lambda a,b: euclDist(a,b), signature='(n),(n)->()')

def smoothTriangle(y, box_pts,hedge=1):
    box = (np.concatenate((np.arange(box_pts + 1), np.arange(box_pts)[::-1])) / box_pts) ** hedge
    box = box[1:-1]
    y_smooth = np.convolve(y, box, mode='same')/np.sum(box_pts)
    return np.array(y_smooth)
    
def versor(vets):
    # Transforma vets (linhas) em seus versores
    n,m = size(vets);
    
    Zr = zeros(n,m);
    inorm = np.sqrt(np.sum(vets**2,1));

    mret = vets/repmat(inorm,m,1).T;
    mret[inorm==0,:] = Zr[inorm==0,:]
    return mret

def normavect(mat1):
    # Calcula a norma 2 por lina de mat
    mret = np.sqrt(np.sum(mat1**2,1));
    return mret

def kpred(X,loops=100,hfclus_plot=False):    
    Z = ward(pdist(X))
    leaves = list(leaves_list(Z))

    leaves.append(0)
    leaves = np.array(leaves)
    a=np.array([leaves[0:-2]]).T
    b=np.array([leaves[1:-1]]).T
    
    win = np.hstack((a,b))

    win = X[win]

    dist = ED(win[:,0],win[:,1])

    ii=1
    if hfclus_plot:
        f, ax = plt.subplots(figsize=(10, 15),nrows=6)
        ax[0].ticklabel_format(style='sci',scilimits=(0,0),axis='y')
        lMin = argrelextrema(dist, np.less)[0]
        ax[0].plot(dist)
        ax[0].plot(lMin,dist[lMin],'k.')
    for i in range(0,loops):
        dist = smoothTriangle(dist,3,hedge=3)
        if hfclus_plot and ((i+1)%20==0):
            ax[ii].ticklabel_format(style='sci',scilimits=(0,0),axis='y')
            lMin = argrelextrema(dist, np.less)[0]
            ax[ii].plot(dist)
            ax[ii].plot(lMin,dist[lMin],'k.')
            ii+=1
    lMin = argrelextrema(dist, np.less)[0]
    
    k = len(lMin)
    X2=X[a]
    cent=X2[lMin].reshape(k,len(X[0]))

    return k,cent,Z

def kmeansKNN(W,n,cent):
    # kmeans convencional
    cl = KMeans(n_clusters=n,init=cent,n_init=1).fit(W)
    c = np.array(cl.cluster_centers_)
    cl = np.array(cl.labels_)

    # gerar versores
    nvt = 1000 #total de versores; original=50
    versors=versor(rand(nvt,size(W)[1])-0.5)
    
    # gerar variaveis
    VRSi=[]
    vcts=[]
    ivcts=[]
    
    # contronar clusters
    for ii in range(0,max(cl)+1):
        nw, mw = size(W);
        DSTi = repmat(c[ii,:],nw,1) - W;
        dci = DSTi[cl==ii,:];
        versorsi=(np.dot(versors , (versor(dci) / repmat(normavect(dci)**0,mw).T).T).T)
        versorsi[versorsi<0] = 0;
        VRSi.append(sum(versorsi))
        sz = size(dci);
        if sz[0]!=1:
            prt1 = np.max(np.dot(versors,dci.T).T,axis=0)
        else:
            prt1 = np.dot(versors,dci.T).T
        U = repmat(prt1,mw).T * versors + repmat(c[ii,:],nvt)
        vcts=(vcts + [c[ii,:].tolist()] + U.tolist());
        ivcts=(ivcts + list(repmat(ii,nvt+1,1))); #clus idx
    vcts=np.array(vcts)
    ivcts=np.array(ivcts)
    
    neigh = KNeighborsClassifier(n_neighbors=1000)
    neigh.fit(vcts, ivcts.ravel())
    clf = np.array(neigh.predict(W))
    
    return vcts,ivcts,clf,cl
    
class Huflus:
    def __init__(self, X):
        self.X = X
    def clus(self,loops=100,hfclus_plot=False):
        k,self.cent,self.Z = kpred(self.X,loops=loops,hfclus_plot=hfclus_plot)
        self.vcts,self.ivcts,self.clf,self.cl = kmeansKNN(self.X,k,self.cent)
        return self.cl
    
    def plot(self):
        X = self.X
        vcts = self.vcts
        clf = self.clf
        cl = self.cl
        n = max(clf)
        
        cmap = plt.get_cmap('viridis')
        colors = [cmap(i) for i in np.linspace(0, 1, n+1)] 
        
        f, ax = plt.subplots(figsize=(10, 7))
        plt.subplot(1, 2, 1)
        plt.plot(vcts[:,0],vcts[:,1],'x',markersize=3)
        for ii in range(0,n+1):
            plt.plot(X[cl==ii,0],X[cl==ii,1],'.',color=colors[ii])
        
        plt.subplot(1, 2, 2)
        plt.plot(vcts[:,0],vcts[:,1],'x',markersize=3)
        for ii in range(0,n+1):
            plt.plot(X[clf==ii,0],X[clf==ii,1],'.',color=colors[ii])
        
        return f
        
def cluster(mat, loops=100):
    cluster_idx = Huflus(mat).clus()
    return cluster_idx
clus = cluster