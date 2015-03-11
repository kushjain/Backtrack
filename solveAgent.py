"""
these guys solve problems
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

def dfs(problem):
    return SolveSudoku(problem)

def SolveSudoku(problem):

    fringe = [[problem.getStartState(), -1]]
    counter = 1

    while fringe:

        state, oldVar = fringe[-1]                    #Last State and Last Value to be Plugged
        #problem.visualize(state)
        
        minlength, var = problem.getVar(state)

        #there exists a variable for which there are no legal values left
        if minlength == 0:
            fringe.pop()                                #Those values are useless, and hence should be removed.
            oldState, tVar = fringe.pop()               #The oldState has lead to conflict, and should be modified
            val = oldState[oldVar][0]
            oldState[oldVar].remove(val)
            fringe.append([oldState, tVar])

        #Get legal Value
        newState = problem.getSuccessor(state, var)     

        #No correct value exists for given variable.
        if newState == None:
            fringe.pop()                                #This lead to conflict, and should be removed.
            oldState, tVar = fringe.pop()
            val = oldState[oldVar][0]                      #The current value of oldVar should not be used again. 
            oldState[oldVar].remove(val)
            fringe.append([oldState, tVar])

        #Win, return Goal
        elif problem.isGoalState(newState):
            print "Solution found in", counter, "moves"
            problem.visualize(newState)
            return newState

        #keep On Plugging Values
        else:
            fringe.append([newState, var])

        counter += 1
