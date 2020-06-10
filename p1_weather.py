# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 17:07:04 2020

@author: Ojas Rade
"""
import math

def euclidean_distance(data_point1,data_point2):
    x1 = float(data_point1.get('TMAX')) - float(data_point2.get('TMAX'))
    x2 = float(data_point1.get('PRCP')) - float(data_point2.get('PRCP'))
    x3 = float(data_point1.get('TMIN')) - float(data_point2.get('TMIN'))
    d = math.sqrt(math.pow(x1,2) + math.pow(x2,2) + math.pow(x3,2))
    return d

def read_dataset(filename):
    lines = []
    with open(filename,'r') as f:
        for line in f:
            lines.append(line)
    spline = [] #line split into pieces to be processed
    dPoints = {} #a singular data point
    retList = [] #list of datapoints that were read
    for l in lines:
        spline = l.split(' ')
        dPoints = {
                'DATE':spline[0],
                'TMAX':spline[2],
                'PRCP':spline[1],
                'TMIN':spline[3],
                'RAIN':spline[4]
        }
        retList.append(dPoints)
    return retList

def majority_vote(nearest_neighbors):
    falses = 0
    trues = 0
    for dp in nearest_neighbors:
        if(dp.get('RAIN') == 'TRUE\n' or dp.get('RAIN') == 'TRUE'):
            trues+=1
        else:
            falses+=1
    if(falses > trues):
        return 'FALSE'
    else:
        return 'TRUE'
    
    
def k_nearest_neighbors(filename,test_point,k):
    def sortSecond(val):#used to sort by second element
        return val[1]
    dataset = read_dataset(filename)
    distances = []#a list of arrays which have distances & a datapoint it match
    temp = [0,0]#temporary holder for arry to be added to distances
    index = 0;#incrementing index
    for dp in dataset:
        temp[0] = index;
        temp[1] = euclidean_distance(dataset[index],test_point)
        distances.append(temp[:])
        index+=1
    distances.sort(key = sortSecond)#sorting the list by the distances
    kNeighbors = []#holds nearest neighbors
    
    #take first k elements of order list distances and 
    #find corresponding datapoint and add to kneighbors
    for i in range(k):
        point = distances[i];
        kNeighbors.append(dataset[point[0]])
    return majority_vote(kNeighbors)