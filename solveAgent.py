"""
TO DO:
Test Run it against Sudoku DB to ensure it works in all cicumstances
"""


def dfs(problem):
    return SolveSudoku(problem)
    fringe = []
    return graphSearch(problem, fringe)


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
