# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:22:06 2020

@author: ojasr
"""

#time_series_covid19_confirmed_global.csv
import csv
from scipy.cluster.hierarchy import linkage
import math

def load_data(filepath):
    data = []
    r = 0
    with open(filepath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if(r != 0):
                data.append({'Providence':row[0],'Name':row[1], 'Cases':row[4:len(row)]})
            else:
                r+=1
    return data

def calculate_x_y(time_series):
    cases = time_series['Cases']
    curI = len(cases) - 1
    n = int(cases[curI])
    nDiv = n/10
    n10I = -1
    n100I = -1
    updated = False
    if(n == 0):
        return (-1,-1)
    while(curI >= 0):
        cur = int(cases[curI])
        if(cur <= nDiv):
            if(not updated):
                n10I = curI
                nDiv = n/100
                updated = True
            else:
                n100I = curI
                nDiv = -1
        curI -= 1
    if(n10I == -1):
        x = -1
    else:
        x = len(cases) - 1
        x = x - n10I
    if(n100I == -1):
        y = -1
    else:
        y = n10I - n100I
    return (x,y)

def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
    return dist

def hac(dataset):
    minDist = distance(dataset[0][0],dataset[0][1],dataset[1][0],dataset[1][1])
    mi = 0
    mj = 1
    cluster = []
    for x in range (0,len(dataset)):
        if(dataset[x][0] != -1 and dataset[x][1] != -1):
            cluster.append([[dataset[x]],1])
    retInd = 0
    bst = []
    clLen = len(cluster)
    while(retInd < clLen - 1):
        for d in range(0,len(cluster)-1):
            for d2 in range(d+1,len(cluster)): 
                for c in range (0,len(cluster[d][0])):
                    for c2 in range (0,len(cluster[d2][0])):
                        if(cluster[d][1] != -1 and cluster[d2][1] != -1):
                            dist = distance(cluster[d][0][c][0],cluster[d][0][c][1],cluster[d2][0][c2][0],cluster[d2][0][c2][1])
                            if(dist < minDist):
                                minDist = dist
                                mi = d
                                mj = d2
        c1 = cluster[mi]
        c2 = cluster[mj]
        iClust = c1[1]
        jClust = c2[1]
        numClust = iClust + jClust
        
        for e in c2[0]:
            c1[0].append(e)
        aftM = [c1[0],numClust]
        
        cluster.append(aftM)
        bst.append([mi,mj,minDist,numClust])
        cluster[mi] = [[-1],-1]
        cluster[mj] = [[-1],-1]
        mi = 0
        mj = 1
        minDist = 10000000
        retInd += 1
    return bst

if __name__=="__main__":
    data = load_data('time_series_covid19_confirmed_global.csv')
    dxy = []
    for d in data:
        dxy.append(calculate_x_y(d))
    print(hac(dxy))
    cluster = []
    for x in range (0,len(dxy)):
        if(dxy[x][0] != -1 and dxy[x][1] != -1):
            cluster.append(dxy[x])
    print(linkage(cluster))
