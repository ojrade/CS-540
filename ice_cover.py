# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:20:51 2020

@author: ojasr
"""
import csv
import statistics
import math
import random

def get_dataset():
    filepath = "p8dataset.csv"
    data = []
    r = 1
    
    with open(filepath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if(r!=1):
                data.append([int(row[0]),int(row[1])])
            r+=1
    return data
def print_stats(data):
    num = len(data)
    iDays = []
    for d in data:
        iDays.append(d[1])
    mean = statistics.mean(iDays)
    std = statistics.stdev(iDays)
    print("{:.2f}".format(num))
    print("{:.2f}".format(mean))
    print("{:.2f}".format(std))
    
def regression(beta0,beta1):
    data = get_dataset()
    MSETot = 0
    for r in data:
        MSETot += math.pow((beta0 + (beta1*r[0]) - r[1]),2)
    return MSETot/len(data)
    
def gradient_descent(beta0,beta1):
    data = get_dataset()
    tot = 0
    for r in data:
        tot += (beta0 + (beta1*r[0]) - r[1])
    tot = tot * 2
    v1 = tot/len(data)
    
    tot = 0
    for r in data:
        tot += (beta0 + (beta1*r[0]) - r[1])*r[0]
    tot = tot * 2
    v2 = tot/len(data)
    
    return(v1,v2)
    
def iterate_gradient(T,eta):
    b0 = 0
    b1 = 0
    ctr = 1
    while ctr<=T:
        grad = gradient_descent(b0,b1)
        b0t = b0 - eta*grad[0]
        b1t = b1 - eta*grad[1]
        b0 = b0t
        b1 = b1t
        print(ctr,"{:.2f} {:.2f} {:.2f}".format(b0t,b1t,regression(b0t,b1t)))
        ctr+=1
        
def compute_betas():
    data = get_dataset()
    x = []
    y = []
    for row in data:
        x.append(row[0])
        y.append(row[1])
    xPrime = statistics.mean(x)
    yPrime = statistics.mean(y)
    
    b1t = 0
    b1b = 0
    for row in data:
        b1t += (row[0] - xPrime) * (row[1] - yPrime)
        b1b += (row[0] - xPrime) ** 2
    b1 = b1t/b1b
    b0 = yPrime - b1 * xPrime
    
    return (b0,b1,regression(b0,b1))

def predict(year):
    (b0,b1,reg) = compute_betas()
    return b0+b1*year

def ngd(beta0,beta1):
    data = get_dataset()
    x = []
    for row in data:
        x.append(row[0])
    xBar = statistics.mean(x)
    xStd = statistics.stdev(x)
    for row in data:
        row[0] = (row[0]-xBar)/xStd
    
    tot = 0
    for r in data:
        tot += (beta0 + (beta1*r[0]) - r[1])
    tot = tot * 2
    v1 = tot/len(data)
    
    tot = 0
    for r in data:
        tot += (beta0 + (beta1*r[0]) - r[1])*r[0]
    tot = tot * 2
    v2 = tot/len(data)
    
    return(v1,v2)
    
def nreg(beta0,beta1,data):
    MSETot = 0
    for r in data:
        MSETot += math.pow((beta0 + (beta1*r[0]) - r[1]),2)
    return MSETot/len(data)

def iterate_normalized(T,eta):
    data = get_dataset()
    x = []
    for row in data:
        x.append(row[0])
    xBar = statistics.mean(x)
    xStd = statistics.stdev(x)
    for row in data:
        row[0] = (row[0]-xBar)/xStd
        
    b0 = 0
    b1 = 0
    ctr = 1
    while ctr<=T:
        grad = ngd(b0,b1)
        b0t = b0 - eta*grad[0]
        b1t = b1 - eta*grad[1]
        b0 = b0t
        b1 = b1t
        print(ctr,"{:.2f} {:.2f} {:.2f}".format(b0t,b1t,nreg(b0t,b1t,data)))
        ctr+=1


def socgd(beta0,beta1):
    data = get_dataset()
    x = []
    for row in data:
        x.append(row[0])
    xBar = statistics.mean(x)
    xStd = statistics.stdev(x)
    for row in data:
        row[0] = (row[0]-xBar)/xStd
    
    row = random.choice(data)
    v1 = 2*(beta0 + (beta1*row[0]) - row[1])
    v2 = 2*(beta0 + (beta1*row[0]) - row[1])*row[0]
    return(v1,v2)

def sgd(T,eta):
    data = get_dataset()
    x = []
    for row in data:
        x.append(row[0])
    xBar = statistics.mean(x)
    xStd = statistics.stdev(x)
    for row in data:
        row[0] = (row[0]-xBar)/xStd
        
    b0 = 0
    b1 = 0
    ctr = 1
    while ctr<=T:
        grad = socgd(b0,b1)
        b0t = b0 - eta*grad[0]
        b1t = b1 - eta*grad[1]
        b0 = b0t
        b1 = b1t
        print(ctr,"{:.2f} {:.2f} {:.2f}".format(b0t,b1t,nreg(b0t,b1t,data)))
        ctr+=1
    