"""
TO DO:
Check against your solution and find out which works better.
Check on basis of time, and not on iterations!!
"""

def backtracking_search(problem):
    result = backtracking_recur(problem, problem.getStartState())
    if result == False:
        print 'Failed!!'
    else:
        print 'Solved!!'

def backtracking_recur(problem, state):
    if problem.isGoalState(state):
        #problem.visualize(state)
        return True

    # get the next uninitialized var
    var = problem.getVar(state)

    if var == (-1,-1):  # this is not supposed to happen; but may be happen due to cosmic activities; better not take any chances
        print 'PANIC!!!!!!!!!!!!'
        #problem.visualize()
        exit()

    # iterate over all possible values of 'var'
    for val in list(problem.getDomain(state, var)):
        newState = problem.trySetValue(state, var, val)
        # check if solution is possible for 'var' == 'val'
        if newState != None:
            # recurse!!
            result = backtracking_recur(problem, newState)
            if result == True:      # we're good
                return True
            # 'val' is not the right choice for 'var'
            problem.removeValue(state, var, val)

    # no solution!!
    return False

######################################################################

def SolveSudoku(problem):

    fringe = []
    fringe.append((problem.getStartState(), (-1,-1)))
    counter = 1
    
    while fringe:
        state, oldVar = fringe[-1]                    #Last State and Last Value to be Plugged

        #Win, return Goal.
        #Necessary in start, to check whether initial state is goal state.
        if problem.isGoalState(state):
            #print "Solution found in", counter, "moves"
            #problem.visualize(newState)
            return state, counter
        
        #Get legal Value
        newState, var = problem.getSuccessor(state)

        #No correct value exists for given variable. It will happen if our forward check reveals that no value fits.
        if newState == None:
            #We should modify the last state to correct this conflict.
            fringe.pop()                             # drop the current state
            oldState, _ = fringe[-1]                 # This led to conflict, and should be modified.
            val = problem.getValue(oldState, oldVar)       # The current value of oldVar should not be used again
            problem.removeValue(oldState, oldVar, val)
        else:
            #Keep On Plugging Values
            fringe.append((newState, var))

        counter += 1

    #No solution found.
    return None, counter                                    
