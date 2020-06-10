# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:00:46 2020

@author: ojasr
"""
import os
import math
from collections import Counter
def create_vocabulary(training_directory,cutoff):
    lines = [];
    for dirName in os.listdir(training_directory):
        for name in os.listdir(training_directory+dirName):
            filename = training_directory+dirName+ "/" + name
            with open(filename,'r', encoding='latin1') as f:
                for line in f:
                    line = line.replace("\n","")
                    lines.append(line)
    count = Counter(lines)
    temp = []
    for el in count:
        if count[el] < cutoff:
            temp.append(el)
    
    vocab = []
    for el in lines:
        if el not in temp:
            vocab.append(el)
    
    vocab = list(dict.fromkeys(vocab))
    vocab = sorted(vocab)
    return vocab
def create_bow(vocab,filepath):
    lines = []
    with open(filepath,'r',encoding='latin1') as f:
        for l in f:
            l = l.replace("\n","")
            lines.append(l)
            
    d = {}
    for tok in lines:
        if tok in vocab:
            if tok not in d.keys():
                    d[tok] = 1
            else:
                d[tok] = d[tok]+1
        else:    
            if None not in d:
                d[None] = 1
            else:
                d[None] = d[None]+1
                
    return d

def load_training_data(vocab,directory):
    tData = []
    newBow = {}
    runCtr = 0;
    for dirName, subdirList, fileList in os.walk(directory):
        if(runCtr == 0):
            runCtr+=1
        else:
            for name in fileList:
                filename = dirName+ "/" + name
                newBow = create_bow(vocab,filename)
                tData.append({'label': (dirName[-4:]), 'bow': newBow})
    return tData

def numWords(bow):
    ctr = 0;
    for key in bow:
        ctr+= bow[key]
    return ctr

def prior(training_data,label_list):
    cnt20 = 0
    cnt16 = 0
    for d in training_data:
        if d['label']=='2020':
            cnt20+=1
            
        if d['label']=='2016':
            cnt16+=1
    prob20 = math.log(cnt20) - math.log(len(training_data))
    prob16 = math.log(cnt16) - math.log(len(training_data))
    logProb = {'2020':prob20,'2016':prob16}
    return logProb

def p_word_given_label(vocab,training_data,label):
    ntd = []
    wordLabel = {}
    totWords = 0;
    for data in training_data:
        if(data['label'] == label):
            ntd.append(data['bow'])
            totWords+=numWords(data['bow'])
    for w in vocab:
        countW = 0
        for td in ntd:
            if w in td:
                countW+=td[w]
            wordLabel[w] = math.log(countW+1) - math.log(len(vocab)+1+totWords)
    countNone = 0
    for td in ntd:
        if None in td:
            countNone+=td[None]
        wordLabel[None] = math.log(countNone+1) - math.log(len(vocab)+1+totWords)
            
    
    return wordLabel

def train(training_directory,cutoff):
    tr = {}
    vocab = create_vocabulary(training_directory,cutoff)
    training_data = load_training_data(vocab,training_directory)
    tr['vocabulary'] = vocab
    tr['log prior'] = prior(training_data,[2016,2020])
    tr['log p(w|y=2016)'] = p_word_given_label(tr['vocabulary'],training_data,'2016')
    tr['log p(w|y=2020)'] = p_word_given_label(tr['vocabulary'],training_data,'2020')
    return tr

def classify(model,filepath):
    fBag = create_bow(model['vocabulary'],filepath)
    total16 = 0
    total20 = 0
    for word in fBag:
        total16 += fBag[word]*model['log p(w|y=2016)'][word]
    total16 += model['log prior']['2016']
    for word in fBag:
        total20 += fBag[word]*model['log p(w|y=2020)'][word]
    total20 += model['log prior']['2020']
    
    if(total16>total20):
        yPred = '2016'
    else:
        yPred = '2020'
        
    return {'log p(y=2020|x)':total20,'log p(y=2016|x)':total16,'predicted y':yPred}
    