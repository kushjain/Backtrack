"""
TO DO:
Check against your solution and find out which works better.
Check on basis of time, and not on iterations!!
"""

def SolveSudoku(problem):

    fringe = [[problem.getStartState(), -1]]
    counter = 1
    
    while fringe:

        state, oldVar = fringe[-1]                    #Last State and Last Value to be Plugged

        #Win, return Goal.
        #Necessary in start, to check whether initial state is goal state.
        if problem.isGoalState(state):
            #print "Solution found in", counter, "moves"
            #problem.visualize(newState)
            return state, counter
        
        minlength, var = problem.getVar(state)

        #There exists a variable for which there are no legal values left.
        #It will happen when backtracking we keep removing values from variable, and are left with none : i.e. the state leading to it was wrong.
        if minlength == 0:
            fringe.pop()                                #Current state is useless, and thrown away
            oldState, tVar = fringe.pop()               #The Last state has led to conflict and should be modified.
            val = oldState[oldVar][0]                   
            oldState[oldVar].remove(val)                
            fringe.append([oldState, tVar])
            continue

        #Get legal Value
        newState = problem.getSuccessor(state, var)

        #No correct value exists for given variable. It will happen if our forward check reveals that no value fits.
        #We should modify the last state to correct this conflict.
        if newState == None:
            lastState, lastVar = fringe.pop()           
            oldState, tVar = fringe.pop()                  #This led to conflict, and should be modified.
            val = oldState[oldVar][0]                      #The current value of oldVar should not be used again. 
            oldState[oldVar].remove(val)
            fringe.append([oldState, tVar])

        #Keep On Plugging Values
        else:
            fringe.append([newState, var])

        counter += 1

    #No solution found.
    return None, counter                                    
