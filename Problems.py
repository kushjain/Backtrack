#!/usr/bin/python2
import inspect
import sys
import os
from random import random,sample,choice, shuffle
import solveAgent
import util


###########################################
"""
TO DO
getSuccessor: should iterate over all the domain values?
Test getStartState : Detect incorrect initial configurations [Note: Implement prune() before]
Can program check for infeasible boards?
Improve Getvalue() to pick least conflicted choice?
Arc Consistency

DONE AND TESTED
init, getStartState, visualize, isGoalState, prune
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
        self.valDomain = {}

        # save the fixed positions and assign their domain values
        self.fixedPos = set()
        for pos, val in predefinedValues:
            self.fixedPos.add(pos)
            self.valDomain[pos] = [val]

        # assign domains to rest of the positions
        for x in range(self.size):
            for y in range(self.size):
                pos = (x, y)
                if pos not in self.fixedPos:
                    self.valDomain[pos] = [i for i in range(1, self.size+1)]
        
        self.region = lambda pos: (int(pos[0]/self.size**0.5), int(pos[1]/self.size**0.5))

    def getStartState(self):
        """Initializes the board, and returns starting configuration. The 'state' is the set of domains of all the positions in the board"""

        for position in self.fixedPos:
            # apply unary constraints wrt to the 'fixedPos'
            self.valDomain = self.prune(self.valDomain, position, ignoreFixed=False)

            if self.valDomain == None:
                print "Conflict Detected in Initial Configuration"
                sys.exit()

        return self.valDomain

    def prune(self, state, position, ignoreFixed=True):
        """Given a position, it takes the value and apply the Unary contraints with respect to fixed configuration of board"""

        queue = [position]          # nodes which can be used for applying unary constraints
        closed = set(position)      # for preventing dups

        while queue:
            # get the next node
            x, y = queue.pop()
            val = self.getValue(state, (x,y))

            # get its neighbours
            neighbours = []

            neighbours.extend([(x,i) for i in range(self.size) if i != y])            #Same row    
            neighbours.extend([(i,y) for i in range(self.size) if i != x])            #Same columns

            region = self.region((x,y))
            start = region[0]*int(self.size**0.5), region[1]*int(self.size**0.5)
            stop = start[0] + int(self.size**0.5), start[1] + int(self.size**0.5)
            neighbours.extend([(i,j) for i in range(start[0],stop[0]) for j in range(start[1],stop[1]) if (i,j) != (x,y)])  # same region

            # apply constraint over the neighbours
            for node in neighbours:
                try:
                    # delete 'value' from each neighbour
                    state[node].remove(val)
                except ValueError:  # if 'val' is not present in 'state[node]'
                    pass

                # we can process the node iff there is single value in its domain i.e. no confusion regarding its value
                if len(state[node]) == 1 and node not in closed and (not ignoreFixed or node not in self.fixedPos):     # ignoreFixed: ignore the 'fixedPos' as they cannot reduce the domain further
                    queue.append(node)
                    closed.add(node)
                elif len(state[node]) == 0:
                    return None                                 #Conflict detected
            
        return state

    def isGoalState(self, state):
        """Returns whether given state is goal or not"""
        #Note it does not check constraints. It assumes that if you have reached final state, you would have done it without violating constraints.
        #It only checks whether the given state is leaf node
        # This assumption is based on 'prune' which ensures that constraints are not violated
    
        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                if len(state[position]) != 1:
                    return False
        return True

    def getVar(self, state):
        """Returns the 'Most Heavily' constrained variable"""
        #In this case, it means variable with least choices
        
        try:
            _, bestPosition = min([(len(state[(x,y)]), (x,y)) for x in range(self.size) for y in range(self.size) if len(state[(x,y)]) != 1])
        except ValueError:  # if we are in goal state i.e. all the values have been assigned
            return (-1,-1)

        return bestPosition
		
    def getValue(self, state, var):
        """ Returns least constrained value for given variabe."""
        #This means we plug in all values for variable, and then sum up the values to check.
        #In this test module, however we simply pick the first value in Domain

        return state[var][0]

    def getSuccessor(self, state):
        """Returns a successor for given state"""
        # TODO: should iterate over all the values or just get the value as arg

        var = self.getVar(state)
        if var == (-1,-1):
            return None

        while state[var]:
            val = self.getValue(state, var)

            newState = state.copy()
            newState[var] = [val]
            newState = self.prune(newState, var)

            if newState == None:        # new state is conflicted
                try:
                    state[var].remove(val)
                except ValueError:
                    break
            else:
                return newState
        
        return None      #If no value found
        
    def unix_visualize(self, state):
        """Visualize the current state using ASCII-art of the board with fancy colors. For *nix systems only"""
        #works only on *nix system
        # no comment needed ;)

        undecided = []
        n = int(self.size**0.5)
        pattern = (util.bcolors.OKGREEN, util.bcolors.OKBLUE)

        print ''
        print '   ' + util.bcolors.HEADER + ''.join(['  '+str(i)+' ' for i in range(self.size)]) + util.bcolors.ENDC
        for i in range(self.size):
            print ' ' + util.bcolors.HEADER + str(i) + ' ' + util.bcolors.ENDC + util.bcolors.WARNING + '|' + util.bcolors.ENDC,
            for j in range(self.size):
                if (i,j) in self.fixedPos:
                    print util.bcolors.UNDERLINE + util.bcolors.BOLD + str(state[(i,j)][0]) + util.bcolors.ENDC,
                else:
                    if len(state[(i,j)]) == 1:
                        out = str(state[(i,j)][0])
                    else:
                        out = '.'
                        undecided.append((i,j))
                    switch = (reduce(lambda rst, d: rst * n + d, self.region((i,j))))
                    print pattern[switch%2] + out + util.bcolors.ENDC,
                print util.bcolors.WARNING + '|' + util.bcolors.ENDC,
            print ''
        print ''

        for i in undecided:
            print util.bcolors.HEADER + str(i) + util.bcolors.ENDC + ' -> ' + util.bcolors.BOLD + str(state[i]) + util.bcolors.ENDC


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

incompleteBoard = [((0, 0), 4), ((1, 1), 3), ((2, 2), 2), ((3, 3), 1), ((1, 2), 1), ((2, 1), 4)]
completeBoard = [((0, 0), 4), ((1, 1), 3), ((2, 2), 2), ((3, 3), 1), ((1, 2), 1), ((2, 1), 4), ((0, 1), 1), ((0, 2), 3), ((0, 3), 2), ((1, 0), 2), ((1, 3), 4), ((2, 0), 1), ((2, 3), 3), ((3, 0), 3), ((3, 1), 2), ((3, 2), 4)]

# run with '-h' for 'usage'
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, default=9, help="size of problem")
parser.add_argument("-i", default='test', help="file containing the initial input configuration for sudoku")
args = parser.parse_args()

predefValues = util.readConfigFile(args.i, args.n)

print len(predefValues), 'sudoku(s)'

prob = [sudoku(N=args.n, predefinedValues=val) for val in predefValues]

for p in prob:
    start_state = p.getStartState()
    p.visualize(start_state)
    print p.isGoalState(start_state)
    state = p.getSuccessor(start_state)
    if state != None:
        print p.visualize(state)
    raw_input()

    #solveAgent.dfs(p)
