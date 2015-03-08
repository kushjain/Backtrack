#!/usr/bin/python2
import inspect
import sys
import os
from random import random,sample,choice, shuffle
import solveAgent
import util


###########################################
"""
ESSENTIAL TO DO
Complete Prune() function           [DO THIS FIRST]
Test the prune(), getSuccessor functions
Test isGoalState() for final incorrect state (see isGoalState for more details)     [Note: Implement prune() before]

OPTIONAL TO DO
Test getStartState : Detect incorrect initial configurations [Note: Implement prune() before]
Can program check for infeasible boards?
Improve Getvalue() to pick least conflicted choice?
Arc Consistency

DONE AND TESTED
init, getStartState, visualize, isGoalState
"""
###########################################

class sudoku:
    """This class contains member functions which describe the empty sudoko board"""

    def __init__(self, N = 9, predefinedValues=()):
        """Initializes sudoku board. Values describe the predefined values in board: It is set containing tuples (position, value)"""
        
        # board size must be n^2 for some n
        if int(N**0.5)**2 != N:
            raise Exception('sudoku: Illegal board size')

        self.size = N
        self.board = [['.' for x in range(self.size)] for y in range(self.size)]

        #Initialize the board positions
        self.fixedPos = set()
        for pos, val in predefinedValues:
            self.fixedPos.add(pos)
            self.board[pos[0]][pos[1]] = val

        #Initialize the rest of board and assign domains to rest of positions
        self.valDomain = {}
        for x in range(self.size):
            for y in range(self.size):
                pos = (x, y)
                if pos not in self.fixedPos:
                    self.valDomain[pos] = [i for i in range(1, self.size+1)]
                else:
                    self.valDomain[pos] = [self.board[x][y]]
        
        self.region = lambda pos: (int(pos[0]/self.size**0.5), int(pos[1]/self.size**0.5))

    def prune(self, state, position):
        
        """Given a position, it takes the value and apply the Unary contraints with respect to fixed configuration of board"""

        queue = [position]
        closed = set()
        
        while queue:
            #print 'queue:', queue
            x, y = queue.pop()
            closed.add((x,y))

            neighbours = []

            neighbours.extend([(x,i) for i in range(self.size) if i != y])            #Same row    
            neighbours.extend([(i,y) for i in range(self.size) if i != x])            #Same columns

            region = self.region((x,y))
            start = region[0]*int(self.size**0.5), region[1]*int(self.size**0.5)
            stop = start[0] + int(self.size**0.5), start[1] + int(self.size**0.5)
            neighbours.extend([(i,j) for i in range(start[0],stop[0]) for j in range(start[1],stop[1]) if (i,j) != (x,y)])

            val = self.board[x][y]
            #raiseNotDefined()
            
            #print 'neighbours', neighbours
            for node in neighbours:
                try:
                    state[node].remove(val)
                except ValueError:
                    pass
                #print 'processed', node, state[node]
                if len(state[node]) == 1 and node not in closed:
                    queue.append(node)
                elif len(state[node]) == 0:
                    return None                                 #Conflict detected
            
        return state

    def getStartState(self):
        """Initializes the board, and returns starting configuration"""
	#In this, instead of board, we propagate value domains. 

        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                if position in self.fixedPos:
                    self.valDomain = self.prune(self.valDomain, position)
                    
                    if self.valDomain == None:
                        print "Conflict Detected in Initial Configuration"
                        sys.exit()

        #print self.valDomain
        for i,j in self.valDomain.items():
            print i,j
        return self.valDomain

    def isGoalState(self, state):
        #Returns whether given state is goal or not
        #Note it does not check constraints. It assumes that if you have reached final state, you would have done it without violating constraints.
        #It only checks whether the given state is leaf node
    
        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                if len(state[position]) !=1:
                    return False
        return True

    def getVar(self, state):
        """Returns Most Heavily constrained variable"""
        #In this case, it means variable with least choices
        
        maxConflicts = self.size + 1
        bestPosition = (-1, -1)
        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                
                #These are already fixed
                if len(state[position]) == 1:
                    continue

                #Figuring out variable with least choices  
                if len(state[position]) < maxConflicts:
                    maxConflicts = len(state[position])
                    bestPosition = position
        
        return bestPosition

		
    def getValue(self, state, var):
        """ Returns least constrained value for given variabe."""
        #This means we plug in all values for variable, and then sum up the values to check.
        #In this test module, however we simply pick the first value in Domain

        return state[var][0]

    def getSuccessor(self, state):
        """Returns a successor for given state"""

        var = self.getVar(state)
        x, y = var

        while state[var]:
            val = self.getValue(state, var)
            state[var] = [val]
            state = self.prune(state, var)

            if state == None:
                state[var].remove(val)

            else:
                return state

        #If no value found
        return None
        
    def unix_visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""
        #works only on *nix system

        # no comment needed ;)
        n = int(self.size**0.5)
        pattern = (util.bcolors.OKGREEN, util.bcolors.OKBLUE)
        print '_' * self.size * 4
        for i in range(self.size):
            print util.bcolors.WARNING + '|' + util.bcolors.ENDC,
            for j in range(self.size):
                if (i,j) in self.fixedPos:
                    print util.bcolors.UNDERLINE + util.bcolors.BOLD + str(state[(i,j)][0]) + util.bcolors.ENDC,
                else:
                    if len(state[(i,j)]) == 1:
                        out = str(state[(i,j)][0])
                    else:
                        out = '.'
                    switch = (reduce(lambda rst, d: rst * n + d, self.region((i,j))))
                    print pattern[switch%2] + out + util.bcolors.ENDC,
                print util.bcolors.WARNING + '|' + util.bcolors.ENDC,
            print ''
        print ''


    def visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""
        
        if os.name == 'posix':
            self.unix_visualize(state)
            return

        print '_' * self.size * 4

        for i in range(self.size):
            print '|', 
            for j in range(self.size):
                position = (i, j)
                if len(state[position]) == 1:
                    print state[position][0], ' |',
                else:
                    print '.', ' |',
            print '' 
        print ''
        
        
############################################
    #TESTING
###########################################

"""
# run with '-h' for 'usage'
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, default=4, help="size of problem")
parser.add_argument("-i", dest='input', default=[], help="initial input configuration for sudoku; syntax: x1 y1 val1 x2 y2 val2 ..", nargs='+')
args = parser.parse_args()

values = args.input
predefValues = []
for i in range(0,len(values),3):
    predefValues.append(((int(values[i]),int(values[i+1])),int(values[i+2])))

prob = sudoku(N=args.n, predefinedValues=predefValues)
print 'sudoku: n =', args.n
"""

incompleteBoard = [((0, 0), 4), ((1, 1), 3), ((2, 2), 2), ((3, 3), 1), ((1, 2), 1), ((2, 1), 4)]
completeBoard = [((0, 0), 4), ((1, 1), 3), ((2, 2), 2), ((3, 3), 1), ((1, 2), 1), ((2, 1), 4), ((0, 1), 1), ((0, 2), 3), ((0, 3), 2), ((1, 0), 2), ((1, 3), 4), ((2, 0), 1), ((2, 3), 3), ((3, 0), 3), ((3, 1), 2), ((3, 2), 4)]
prob = sudoku(4, incompleteBoard)
state = prob.getStartState()
prob.visualize(state)
print prob.isGoalState(state)
state = prob.getSuccessor(state)
prob.visualize(state)
state = prob.getSuccessor(state)
prob.visualize(state)
state = prob.getSuccessor(state)
prob.visualize(state)
state = prob.getSuccessor(state)
prob.visualize(state)
state = prob.getSuccessor(state)
prob.visualize(state)
state = prob.getSuccessor(state)
prob.visualize(state)
#print solveAgent.dfs(prob)
