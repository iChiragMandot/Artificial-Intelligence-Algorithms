# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
    self.policy = {}
    self.values1 = util.Counter()
    self.qval = util.Counter()

    for k in mdp.getPossibleActions((3,1)):
           for (l,m) in mdp.getTransitionStatesAndProbs((3,1),k):
                print k , l , m , mdp.getReward((3,1),k,l)


    for i in range(self.iterations):
        for j in mdp.getStates():

            if mdp.isTerminal(j):
                self.values[j]=0
                self.policy[j]=None
                continue

            mval=-10000
            mxa = None
            for k in mdp.getPossibleActions(j):
                    cval=0.0
                    for (l,m) in mdp.getTransitionStatesAndProbs(j,k):
                        cval+= m*(mdp.getReward(j,k,l) + self.discount*self.values[l])
                        self.qval[j,k]= m*(mdp.getReward(j,k,l) + self.discount*self.values[l])
                    if cval > mval:
                        mval=cval
                        mxa=k
            self.values1[j]=mval
            self.policy[j]=mxa
        for j in self.values.keys():
            self.values[j]=self.values1[j]


  #  print self.values[(3,1)]
    "*** YOUR CODE HERE ***"
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    return self.qval[state,action]
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    return self.policy[state]
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
