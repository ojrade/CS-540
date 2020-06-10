# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:00:18 2020

@author: ojasr
"""
import random

def pick_envelope(switch,verbose):
    env1 = []
    env2 = []
    envs = [env1,env2]
    correct = 0
    r = random.randint(1,4);
    if r==1:
        env1.append('r')
        env1.append('b')
        env2.append('b')
        env2.append('b')
    if r==2:
        env1.append('b')
        env1.append('r')
        env2.append('b')
        env2.append('b')
    if r==3:
        env1.append('b')
        env1.append('b')
        env2.append('r')
        env2.append('b')
        correct = 1
    if r==4:
        env1.append('b')
        env1.append('b')
        env2.append('b')
        env2.append('r')
        correct = 1
    if(verbose):
        print("Envelope 0: ",env1[0],env1[1])
        print("Envelope 1: ",env2[0],env2[1])
    envPick = random.randint(0,1)
    ballPick = random.randint(0,1)
    if(verbose):
        print("I picked envelope ",envPick)
        print("and drew a ",envs[envPick][ballPick])
    if(envs[envPick][ballPick] == 'r'):
        return True
    if(switch):
        envPick = (envPick+1)%2
        if(verbose):
            print("Switch to envelope ",envPick)
    if(envPick == correct):
        return True
    else:
        return False
    
def run_simulation(n):
    trueSwitch = 0
    falseSwitch = 0
    for i in range(n):
        if(pick_envelope(True,False)):
            trueSwitch+=1
        if(pick_envelope(False,False)):
            falseSwitch+=1
    print("After ",n," simulations:")
    print("  Switch successful: ",(trueSwitch/n)*100,"%")
    print("  No-switch successful: ",(falseSwitch/n)*100,"%")
    