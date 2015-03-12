# Backtrack
Implement Backtrack search for Problems

# Backtracking

Inspired by CS 188 course on Artificial Intelligence (https://courses.edx.org/courses/BerkeleyX/CS188.1x-4/1T2015/info) 
This is not homework, so it does not violate any Honor Policy.

Designed and Implemented by Kush Jain (https://github.com/kushjain) and Abhishek Rose (https://github.com/rawcoder)

###Problems we are trying to solve
Currently we are focusing on :

* Sudoku : Solving for NxN board. Fill the numbers 1-N such that each row and each column must have all numbers 1-N. Also , the board is divided into N square regions, which alo must contain unique numbers.

All Problem Definitions could be found in problems.py file

### Algorithms we Are Implementing
Implemented:

* Backtrack : In backtrack, we try to solve the constraints by trying out different values for decision variables. If at any point, we find that we cannot make any further decision without violating any constraint, we backtrack from that set of decision variables, and try different set. http://en.wikipedia.org/wiki/Backtracking 
It is augmented by several important additions
* Forward Checking: In addition to backtracking, we propogate the constraints further, so that we may find inconsistency earlier. http://en.wikipedia.org/wiki/Look-ahead_%28backtracking%29
* Picking Most Conflicted/constrained variable: This can shorten the search space considerably. 

In addition, there are algorithms which 
* Enforce arc consistency.
* Try to pick optimal value for given variable. [Least Constrained Value]
We may implement them in future.

All algorithms could be found in solveAgents.py
