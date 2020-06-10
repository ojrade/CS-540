# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 18:41:56 2020

@author: ojasr
"""

import matplotlib.pyplot as mp
from scipy.io import loadmat
from scipy.linalg import eigh
import numpy as np

def load_and_center_dataset(filename):
    dataset = loadmat(filename)
    x = dataset['fea']
    x = np.array(x,dtype='float64')
    cent = x - np.mean(x,axis=0,)
    return cent

def get_covariance(dataset):
    corv = np.dot(np.transpose(dataset),dataset)
    f = 1/(len(dataset)-1)
    corv = f*corv
    return corv
    
def get_eig(S,m):
    eigVal,eigVec = eigh(S,eigvals=(1024-(m),1023))
    eigVal = np.flip(eigVal,0)
    adjEigVal = []
    for x in range(0,eigVal.size):
        tempArr = [0.]*eigVal.size
        """
        Changed this line from
        tempArr[x] = eigVal[0]
        """
        tempArr[x] = eigVal[x]
        adjEigVal.append(tempArr)
    adjEigVec=[]
    for vec in eigVec:
        adjEigVec.append(np.flip(vec,0))
    return adjEigVal,adjEigVec

def project_image(image,U):
    #goes from [0,1024)
    xi = 0
    for vec in np.transpose(U):
        aij = np.dot(np.transpose(vec),image)
        xi += aij*vec
    return xi

def display_image(orig,proj):
    #32x32
    orig = np.reshape(orig,[32,32])
    orig = np.transpose(orig)
    proj = np.reshape(proj,[32,32])
    proj = np.transpose(proj)
    #subplots
    fig, (original,project) = mp.subplots(1,2)
    #title imshow colorbar
    original.set_title('Original')
    origShow = original.imshow(orig,aspect='equal')
    fig.colorbar(origShow, ax=original)
    
    project.set_title('Projection')
    projShow = project.imshow(proj,aspect='equal')
    fig.colorbar(projShow, ax=project)
    #render
    mp.show()
    