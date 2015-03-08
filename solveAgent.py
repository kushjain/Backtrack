
"""
Test the Problem Board before!
I have written a general algorithm. which should be correct, but without problem defintion, cannot test it.
"""

def graphSearch(problem, fringe):
    #Generic Graph Search Algorithm Main Function
    closed = set()                          #Needed? 
    fringe.push(problem.getStartState())     #Structure is : [(item), (item), ...], priority where each item is (state, direction, total Cumulative Cost)
    
    while 1:
        if fringe.isEmpty():
            return []
            
        node = fringe.pop()
        #print "Node", node
        
        lastItem = node[-1]
        
        if problem.isGoalState(itemState):
            return lastItem
        
        if itemState not in closed:
            closed.add(itemState)
            
            state = problem.getSuccessors(lastItem)

            #If conflict, pop the state
            """if state == None:
                fringe.pop()
            #Else, push the new state
            else:
                fringe.push(state)
            """
        
        #raw_input()

def dfs(problem):
    fringe = []
    return graphSearch(problem, fringe)
