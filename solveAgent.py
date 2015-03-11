
"""
Test the Problem Board before!
I have written a general algorithm. which should be correct, but without problem defintion, cannot test it.
"""

def graphSearch(problem, fringe):
    #Generic Graph Search Algorithm Main Function
    closed = set()                          #Needed? 
    fringe.append([(problem.getStartState(), -1)])     #Structure is : [(item), (item), ...], priority where each item is (state, direction, total Cumulative Cost)
    
    while True:
        if not len(fringe):
            return []
            
        node = fringe.pop()
        print "Node", len(node)
        
        lastState, lastVar = node[-1]
        problem.visualize(lastState)
        
        if problem.isGoalState(lastState):
            return lastState

        minLength, var = problem.getVar(lastState)
        print var, minLength

        if minLength == 0:
            #Call last state
            newNode = node[:-1]
            val = lastState[lastVar]
            lastState[lastVar].remove(val)
            state = problem.getSuccessor(lastState, lastVar)           
        else:
            state = problem.getSuccessor(lastState, var)

        #If conflict, pop the state
        if state == None:
            newNode = node[:-1]
        #Else, push the new state
        else:
            newNode = node + [(state, var)]
            
        fringe.append(newNode)
        
        #raw_input()

def dfs(problem):
    fringe = []
    return graphSearch(problem, fringe)
