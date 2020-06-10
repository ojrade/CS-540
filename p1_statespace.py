# -*- coding: utf-8 -*-
"""
Created on Fri Jan  31 22:01:13 2020

@author: ojasr
"""

def fill(state,max,which):
    ret = state.copy()
    ret[which] = max[which]
    return ret

def empty(state,max,which):
    ret = state.copy()
    ret[which]=0
    return ret

def xfer(state, max, source, dest):
    ret = state.copy()
    while ret[dest]!=ret[source] and ret[source]>0 and ret[dest]<max[dest]:
        ret[dest]+=1
        ret[source]-=1
    return ret

def succ(state,max):
    cop = state.copy()
    succ = []
    temp = ['','','']
    overlap = 0;
    for i in range(2):
        temp[0] = fill(state,max,i)
        temp[1] = empty(state,max,i)
        temp[2] = xfer(state,max,i,(i+1)%2)
        if i==0:
            succ.append(temp[0])
        for x in range(3):
            overlap = 0;
            l = len(succ)
            for s in range(l):
                if temp[x]==succ[s]:
                    overlap+=1
            if overlap==0:
                succ.append(temp[x])
    for o in succ:
        print(o)