# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """
        in_open = False
        # TODO: set in_open to True if the state is in the queue already
        # TODO: handle that case correctly
        ctr = 0;
        i = 0
        for d in self.queue:
            if d['state'] == state_dict['state']:
                in_open = True
                i = ctr
            ctr+=1
        
        temp = 0
        if in_open:
            if state_dict['g'] < self.queue[i]['g']:
                temp = state_dict['g']
            else:
                temp = self.queue[i]['g']
            self.queue[i]['g'] = temp
            self.queue[i]['f'] = self.queue[i]['g'] + self.queue[i]['h']
            self.queue[i]['parent']  = state_dict['parent']
        
        if not in_open:
            self.queue.append(state_dict)

    
        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state


def hCount(sArray):
    ctr = 0
    v = 1
    for i in sArray :
        if i != v and i != 0:
            ctr+=1
        v+=1
    return ctr  


def succ(state):
    i = state.index(0)
    # switch above
    state1=state.copy()
    state1[i] = state1[(i-3)%9]
    state1[(i-3)%9] = 0;
    #switch below
    state2=state.copy()
    state2[i] = state2[(i+3)%9]
    state2[(i+3)%9] = 0;
    
    if i<3:
        #switch left
        state3=state.copy()
        state3[i] = state3[(i-1)%3]
        state3[(i-1)%3] = 0;
        
        #switch right
        state4=state.copy()
        state4[i] = state4[(i+1)%3]
        state4[(i+1)%3] = 0;
    elif i>3 and i<6:
        #switch left
        state3=state.copy()
        state3[i] = state3[(i-1)%3+3]
        state3[(i-1)%3+3] = 0;
        
        #switch right
        state4=state.copy()
        state4[i] = state4[(i+1)%3+3]
        state4[(i+1)%3+3] = 0;
    else:
        #switch left
        state3=state.copy()
        state3[i] = state3[(i-1)%3+6]
        state3[(i-1)%3+6] = 0;
        
        #switch right
        state4=state.copy()
        state4[i] = state4[(i+1)%3+6]
        state4[(i+1)%3+6] = 0;
        
    s = [state1,state2,state3,state4]
    return sorted(s)
    
def print_succ(state):
    s = succ(state)
    for a in s:
        print(a," h = ",hCount(a),sep="")
        
def printPath(state,parent):
    result = []
    result.insert(0,state)
    result.insert(0,parent['state'])
    while parent['parent'] != None:
        parent = parent['parent']
        result.insert(0,parent['state']);
    moves=0
    for r in result:
        print(r,"  h=",hCount(r),"  moves: ",moves,sep="")
        moves+=1
    
def solve(state):
    op = PriorityQueue();
    closed = []
    goal = [1,2,3,4,5,6,7,8,0]
    g = 0
    h = hCount(state)
    f = g+h
    op.enqueue({'state': state,'h':h,'g':0,'parent': None,'f':f})
    while(op.is_empty() == False):
        q = op.pop()
        closed.append(q)
        succs = succ(q['state'])
        for s in succs:
            cL = False
            h = hCount(s)
            g = q['g']+1
            f = g+h
            index = 0
            ctr = 0
            for c in closed:
                if (c['state'] == s):#checking if in closed
                    cL = True
                    index = ctr
                ctr+=1
            if (s == goal):
                closed.append(q)
                printPath(s,q)
                print("Max queue length: ",op.max_len,sep="")
                return;
            elif (cL == False):
                op.enqueue(
                        {'state':s,'h':h,'g':g,'parent': q,'f':f})
            elif(cL == True):
                if(g < closed[index]['g']):
                    op.enqueue(
                        {'state':s,'h':h,'g':g,'parent': q,'f':f})