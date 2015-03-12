"""
TO DO:
Check against your solution and find out which works better.
Check on basis of time, and not on iterations!!
"""

def SolveSudoku(problem):

    fringe = [problem.getStartState()]
    counter = 1
    
    while fringe:

        state = fringe.pop()

        #problem.visualize(state)

        #If Win, return That!
        if problem.isGoalState(state):
            return state, counter

        #All successors of current state
        newStateList = problem.getSuccessors(state)

        #If there are valid successors, add them to stack.
        if newStateList:
            for newState in newStateList:
                fringe.append(newState)

        counter += 1

    return None, counter
