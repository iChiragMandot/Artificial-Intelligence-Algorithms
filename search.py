# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""
from spade import pyxf

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  f=open('maze','w')
#  print("startstate"+str(problem.getStartState())+".\n")
#  print("goal"+str(problem.goal)+".\n")
#  print f

#  f.write("Hello World")

  walls=problem.walls

  for x in range(0,walls.width):
      for y in range(0,walls.height):
          if (walls[x][y]== False):
              f.write("space("+str(x)+","+str(y)+").\n")


  f.close()

  myswipl = pyxf.xsb('/home/shakespeare/Downloads/XSB/bin/xsb')
  myswipl.load("/home/shakespeare/search/maze")
  myswipl.load("/home/shakespeare/Downloads/XSB/bin/dfs_new")

  result = myswipl.query("dfscall("+ str(problem.getStartState()) + "," + str(problem.goal) +")." )
  print result

  myswipl.load("/home/shakespeare/search/dfstree")
  myswipl.load("/home/shakespeare/Downloads/XSB/bin/path")
  result = myswipl.query("pathcall("+ str(problem.getStartState()) + "," + str(problem.goal) +")." )

  print result
  with open('/home/shakespeare/search/output') as f:
    content = f.readlines()

  from game import Directions
  ret = []
  for i in content:
      if i[0] is '1':
        ret.append(Directions.NORTH)
      if i[0] is '2':
        ret.append(Directions.EAST)
      if i[0] is '3':
        ret.append(Directions.SOUTH)
      if i[0] is '4':
        ret.append(Directions.WEST)

  return ret


  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  f=open('maze','w')
  print("startstate"+str(problem.getStartState())+".\n")
  print("goal"+str(problem.goal)+".\n")
#  print f

#  f.write("Hello World")

  walls=problem.walls

  for x in range(0,walls.width):
      for y in range(0,walls.height):
          if (walls[x][y]== False):
              f.write("space("+str(x)+","+str(y)+").\n")


  f.close()

  myswipl = pyxf.xsb('/home/shakespeare/Downloads/XSB/bin/xsb')
  myswipl.load("/home/shakespeare/search/maze")
  myswipl.load("/home/shakespeare/Downloads/XSB/bin/bfs_new")

  result = myswipl.query("bfscall("+ str(problem.getStartState()) + "," + str(problem.goal) +")." )
  print result

  myswipl.load("/home/shakespeare/search/bfstree")
  myswipl.load("/home/shakespeare/Downloads/XSB/bin/path")
  result = myswipl.query("pathcall("+ str(problem.getStartState()) + "," + str(problem.goal) +")." )

  print result
  with open('/home/shakespeare/search/output') as f:
    content = f.readlines()

  from game import Directions
  ret = []
  for i in content:
      if i[0] is '1':
        ret.append(Directions.NORTH)
      if i[0] is '2':
        ret.append(Directions.EAST)
      if i[0] is '3':
        ret.append(Directions.SOUTH)
      if i[0] is '4':
        ret.append(Directions.WEST)

  return ret
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  f=open('maze','w')
  print("startstate"+str(problem.getStartState())+".\n")
  print("goal"+str(problem.goal)+".\n")
#  print f

#  f.write("Hello World")

  walls=problem.walls

  for x in range(0,walls.width):
      for y in range(0,walls.height):
          if (walls[x][y]== False):
              f.write("space("+str(x)+","+str(y)+").\n")
              f.write("h((" + str(x) + "," + str(y) + ")," + str(heuristic((x,y),problem)) + ").\n")

  f.close()


  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch