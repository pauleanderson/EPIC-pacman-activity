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
    self.moves = []


  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    # ["North","South","East"]
    bestAction = None # This is what we have to return

    myState = gameState.getAgentState(self.index)

    if myState.numCarrying > 5: # go home safest way possible
        print(4)
        """print(4)
        minDistsOpps = []
        for action in actions: # let's explore the actions (North, South, etc)
            succ = self.getSuccessor(gameState, action)
            posSucc = succ.getAgentState(self.index).getPosition()

            opponents = self.getOpponents(succ)
            def getOpponentDistance(index):
                pos = succ.getAgentState(o).getPosition()
                if pos == None: # Not observable so set to 9999
                    return 9999
                return self.getMazeDistance(posSucc,pos)
            minDistsOpps.append(min([getOpponentDistance(o) for o in opponents]))
        ix = np.argmax(minDistsOpps)
        bestAction = actions[ix]
        """
        while bestAction is None:
            if len(self.moves) == 0:
                break
            lastMove = self.moves.pop()
            if lastMove == 'South':
                bestAction = "North"
                return bestAction
            elif lastMove == 'North':
                bestAction = 'South'
                return bestAction
            elif lastMove == "West":
                bestAction = "East"
                return bestAction
            elif lastMove == "East":
                bestAction = "West"
                return bestAction

    foodLeft = self.getFood(gameState).asList()
    opponents = self.getOpponents(gameState)
    # List of positions with food

    # where am I? pos = (x,y)
    pos = gameState.getAgentState(self.index).getPosition()
    # My assumption is you mean directly in front of us
    isFoodInFront = False
    for foodLeftPos in foodLeft: # repetition is big :)
        if self.getMazeDistance(pos,foodLeftPos) == 1:
            isFoodInFront = True

    if not isFoodInFront:
        print(1)
        # Pick a direction that moves us towards closest food
        # as long as that move keeps us 2 away from defenders
        # i.e., go in new direction
        minDist = 9999 # initialie to a high number

        minDists = []
        minDistsOpps = []
        for action in actions: # let's explore the actions (North, South, etc)
            succ = self.getSuccessor(gameState, action)
            posSucc = succ.getAgentState(self.index).getPosition()
            dists = []
            for foodLeftPos in foodLeft:
                dists.append(self.getMazeDistance(posSucc,foodLeftPos))
            minDists.append(min(dists))

            opponents = self.getOpponents(succ)
            def getOpponentDistance(index):
                pos = succ.getAgentState(o).getPosition()
                if pos == None: # Not observable so set to 9999
                    return 9999
                return self.getMazeDistance(posSucc,pos)
            minDistsOpps.append(min([getOpponentDistance(o) for o in opponents]))

        ix = np.argmin(minDists) # find the direction that takes us closest to food
        # We need this loop to make sure we aren't  violating your idea of staying away
        for _ in range(len(actions)):
            ix_ = np.argmin(minDists)
            if minDistsOpps[ix_] > 2:
                ix = ix_
                break
            minDists[ix_] = 9999 # Ghost too close
        bestAction = actions[ix]
        self.moves.append(bestAction)
        return bestAction
    else: # Yes there is food!
        # Find which action takes us towards the food
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

        # Now see if there is an opponent too close if we go that way
        succ = self.getSuccessor(gameState, bestAction)
        posSucc = succ.getAgentState(self.index).getPosition()
        opponents = self.getOpponents(succ)
        def getOpponentDistance(index):
            pos = gameState.getAgentState(o).getPosition()
            if pos == None: # Not observable so set to 9999
                return 9999
            return self.getMazeDistance(posSucc,pos)

        minDistOpps  = min([getOpponentDistance(o) for o in opponents])
        if minDistOpps <= 2: # run away
            print(2)
            ix = np.argmax(minDistsOpps) # change out best action to max of min
            bestAction = actions[ix]
            self.moves.append(bestAction)
            return bestAction

        #elif len(foodLeft) < 5:
        #    print(3)
        #    return bestAction # go after that food!
        else:
            self.moves.append(bestAction)
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
