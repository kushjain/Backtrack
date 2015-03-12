#!/usr/bin/python2
import sys
import os
import solveAgent
import util
import copy

"""
TO DO:
Add support for reading files
Add support for checking if read file is in wrong format. [for example: if 4x4 sudoku is given with args -n 9]
Check whether it can detect infeasible puzzles
"""

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
        
        # useful small functions
        self.region = lambda pos: (int(pos[0]/self.size**0.5), int(pos[1]/self.size**0.5))
        self.getValue = lambda state, var: state[var][0]
        self.getDomain = lambda state, var: state[var]
        self.removeValue = lambda state, var, val: state[var].remove(val)

    def prune(self, state, position, ignoreFixed=True):
        """Given a position, it takes the value and apply the Unary contraints with respect to fixed configuration of board"""

        queue = [position]
        closed = set(position)
        
        while queue:
            x, y = queue.pop()
            val = self.getValue(state, (x,y))               

            neighbours = []

            neighbours.extend([(x,i) for i in range(self.size) if i != y])            #Same row    
            neighbours.extend([(i,y) for i in range(self.size) if i != x])            #Same columns

            region = self.region((x,y))
            start = region[0]*int(self.size**0.5), region[1]*int(self.size**0.5)
            stop = start[0] + int(self.size**0.5), start[1] + int(self.size**0.5)
            neighbours.extend([(i,j) for i in range(start[0],stop[0]) for j in range(start[1],stop[1]) if (i,j) != (x,y)])  # same region

            # check the effect of setting 'val' to 'position' on neighbours 
            for node in neighbours:
                try:
                    # remove 'val' from domain
                    state[node].remove(val)
                except ValueError:
                    pass

                # single value left?
                if len(state[node]) == 1  and node not in closed and (not ignoreFixed or node not in self.fixedPos):
                    queue.append(node)
                    closed.add(node)

                # domain empty?
                elif len(state[node]) == 0:
                    return None                                 #Conflict detected
            
        return state

    def getStartState(self):
        """Initializes the board, and returns starting configuration"""

        for position in self.fixedPos:
            self.valDomain = self.prune(self.valDomain, position, ignoreFixed=False)

            if self.valDomain == None:
                print "Conflict Detected in Initial Configuration"
                sys.exit()

        return self.valDomain


    def isGoalState(self, state):
        """Returns whether given state is goal or not"""
        #Note it does not check constraints. It assumes that if you have reached final state, you would have done it without violating constraints.
        #It only checks whether the given state is leaf node
    
        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                if len(state[position]) != 1:
                    return False
        return True

    def getVar(self, state):
        """Returns Most Heavily constrained variable"""
        #In this case, it means variable with least choices
        
        minLength, bestPosition = min([(len(state[(x,y)]), (x,y)) for x in range(self.size) for y in range(self.size) if len(state[(x,y)]) != 1])
        
        if minLength == 0:
            return None
        else:
            return bestPosition
		
    def setValue(self, state, var, val):
        """Set the value of 'var' to 'val'"""
        state[var] = [val]

    def trySetValue(self, state, var, val):
        """sets 'var' to 'val and checks for constraints. Returns 'None' if constraints fail else the new state"""
        
        newState = copy.deepcopy(state)
        newState[var] = [val]
        newState = self.prune(newState, var)

        return newState

    def getSuccessor(self, state):
        """Returns a successor for given state"""
        
        var = self.getVar(state)
        if var == None:
            return None, None

        while state[var]:
            val = self.getValue(state, var)
            newState = copy.deepcopy(state)
            self.setValue(newState, var, val)
            newState = self.prune(newState, var)

            if newState == None:        # new state is conflicted
                try:
                    state[var].remove(val)
                except ValueError:
                    break
            else:
                return newState, var
    
        return None, None         #If no value found
        
    def unix_visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""
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

        #If there is no state
        if state == None:
            print "No State"
            return
        
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
############################################

# run with '-h' for 'usage'
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, default=9, help="size of problem")
parser.add_argument("-i", default='tests.txt', help="file containing the initial input configuration for sudoku")
args = parser.parse_args()

predefValues = util.readConfigFile(args.i, args.n)

print len(predefValues), 'sudoku(s)'

prob = [sudoku(N=args.n, predefinedValues=val) for val in predefValues]

total_counter = 0
index = 1
win = 0

for p in prob:
    #solveAgent.backtracking_search(p)
    state, ctr = solveAgent.SolveSudoku(p)

    if state != None:
        #print "Solution found for", index, "in", ctr
        #p.visualize(state)
        total_counter += ctr
        win += 1

    index += 1
    
index -= 1
print "In total", win, "solutions found out of", index, "problems"
print "Win Rate", win*100.0/index
try:                                            #In case of No Win.
    print "Mean Total Iterations before Solution found", float(total_counter)/win
except:
    print "No wins :("
