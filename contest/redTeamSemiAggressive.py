# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint
import numpy as np

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveAgent', second = 'DefensiveAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class MyAgent(CaptureAgent):
      def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
          # Only half a grid position was covered
          return successor.generateSuccessor(self.index, action)
        else:
          return successor

class OffensiveAgent(MyAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    bestAction = None # This is what we have to return
    foodLeft = self.getFood(gameState).asList()
    # total food = 20
    if 1-len(foodLeft)/20 >= 0.25: # Go home!
        minDistsOpps = []
        for action in actions:
            succ = self.getSuccessor(gameState, action)
            posSucc = succ.getAgentState(self.index).getPosition()
            opponents = self.getOpponents(succ)
            def getOpponentDistance(index):
                pos = gameState.getAgentState(o).getPosition()
                if pos == None: # Not observable so set to 9999
                    return 9999
                return self.getMazeDistance(posSucc,pos)
            minDistsOpps.append(min([getOpponentDistance(o) for o in opponents]))
        ix = np.argmax(minDistsOpps)
        bestAction = actions[ix]
        return bestAction

    pos = gameState.getAgentState(self.index).getPosition()
    opponents = self.getOpponents(gameState)
    def getOpponentDistance(index):
        p = gameState.getAgentState(o).getPosition()
        if p == None: # Not observable so set to 9999
            return 9999
        return self.getMazeDistance(p,pos)
    minDistOpps = min([getOpponentDistance(o) for o in opponents])

    isGhostNearby = False
    if minDistOpps <= 2:
        isGhostNearby = True

    if not isGhostNearby: # got get some food!
        minDists = []
        for action in actions:
            succ = self.getSuccessor(gameState, action)
            posSucc = succ.getAgentState(self.index).getPosition()
            dists = []
            for foodLeftPos in foodLeft:
                dists.append(self.getMazeDistance(posSucc,foodLeftPos))
            if len(dists) > 0:
                minDists.append(min(dists))
            else:
                minDists.append(0)
        ix = np.argmin(minDists)
        bestAction = actions[ix]
        return bestAction
    elif minDistOpps > 4: # kinda far?
        minDists = []
        for action in actions:
            succ = self.getSuccessor(gameState, action)
            posSucc = succ.getAgentState(self.index).getPosition()
            dists = []
            for foodLeftPos in foodLeft:
                dists.append(self.getMazeDistance(posSucc,foodLeftPos))
            minDists.append(min(dists))
        ix = np.argmin(minDists)
        bestAction = actions[ix]
        return bestAction
    else: # run away!
        minDistsOpps = []
        for action in actions:
            succ = self.getSuccessor(gameState, action)
            posSucc = succ.getAgentState(self.index).getPosition()
            opponents = self.getOpponents(succ)
            def getOpponentDistance(index):
                pos = gameState.getAgentState(o).getPosition()
                if pos == None: # Not observable so set to 9999
                    return 9999
                return self.getMazeDistance(posSucc,pos)
            minDistsOpps.append(min([getOpponentDistance(o) for o in opponents]))
        ix = np.argmax(minDistsOpps)
        bestAction = actions[ix]
        return bestAction


class DefensiveAgent(MyAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)

    # go after those opponents!
    minDistsOpps = []
    for action in actions:
        succ = self.getSuccessor(gameState, action)
        posSucc = succ.getAgentState(self.index).getPosition()
        opponents = self.getOpponents(succ)
        def getOpponentDistance(index):
            pos = gameState.getAgentState(o).getPosition()
            if pos == None: # Not observable so set to 9999
                return 9999
            return self.getMazeDistance(posSucc,pos)
        minDistsOpps.append(min([getOpponentDistance(o) for o in opponents]))
    ix = np.argmin(minDistsOpps)
    bestAction = actions[ix]
    return bestAction
