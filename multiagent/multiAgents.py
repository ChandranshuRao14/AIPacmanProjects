# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # raw_input("Press enter to continue")
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # High Score should depend on the following:
        # Distance to food
        # Distance to ghost
        # Amount of scared time left

        # This is the next position we have to check
        newX,newY = newPos
        currX, currY = currentGameState.getPacmanPosition()

        # First we have to check the food
        foodScore = 0
        if currentGameState.getFood()[newX][newY] == True:
          foodScore = 150 # There is a food next to us
        else:
          # Check all of the food distances
          foodDistances = []
          for x in range(0,newFood.width):
            for y in range(0,newFood.height):
              if newFood[x][y] == True:
                foodDistances.append(manhattanDistance((x,y),newPos))
          foodScore = int(float(1)/float(min(foodDistances)) * 100) # Closer the food, the higher the score

        maxScaredTime = max(newScaredTimes)

        # Check all ghosts
        ghostDistances = []
        ghostScore = 0
        for i in newGhostStates:
          ghostX, ghostY = i.getPosition()
          # If it's in the same row or column, decrease the score
          if ghostX == newX:
            ghostScore = -20
          elif ghostY == newY:
            ghostScore = -20
          else:
            ghostDistances.append(manhattanDistance(newPos,i.getPosition()))
        if ghostScore != -20:
          ghostScore = max(ghostDistances) # Farther away the ghost, the higher the score

        score = foodScore + 3*ghostScore + 5*maxScaredTime
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        actionToTake = ""
        v = -100000
        # Loop through the actions available
        for action in gameState.getLegalActions():
          newV = self.minValue(gameState.generateSuccessor(0,action), 0, 1)
          # Check if this v is better
          if newV > v and newV != 100000:
            v = newV
            actionToTake = action
        # print("BEST action: " + actionToTake)
        # raw_input("Continue")
        # print("")
        return actionToTake

    def value(self, gameState, depth, agentIndex):
      # Base case: check if depth has been reached or if we won or lost
      if depth == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      if agentIndex == 0: # This is pacman!!
        return self.maxValue(gameState, depth, agentIndex)
      else: # This is a ghost
        return self.minValue(gameState, depth, agentIndex)
    
    def maxValue(self, gameState, depth, agentIndex):
      v = -100000
      legalMoves = gameState.getLegalActions(0)
      # Loop through children
      for action in legalMoves:
        v = max(v, self.value(gameState.generateSuccessor(0, action),depth,1))
      return v

    def minValue(self, gameState, depth, agentIndex):
      v = 100000
      legalMoves = gameState.getLegalActions(agentIndex)
      # Loop through children
      for action in legalMoves:
        if agentIndex == gameState.getNumAgents() -1:
          v = min(v, self.value(gameState.generateSuccessor(agentIndex, action),depth+1,0)) # That's the last min level, switch back to max
        else:
          v = min(v, self.value(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1)) # Go to the next min level
      return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        actionToTake = ""
        # Set alpha and beta values
        v = a = -100000
        b = 100000
        for action in gameState.getLegalActions():
          newV = self.minValue(gameState.generateSuccessor(0,action), 0, 1, a, b)
          if newV > v:
            v = newV
            actionToTake = action
          if newV > b:
            return actionToTake
          a = max(a, newV)
        #print("BEST action: " + actionToTake)
        #raw_input("Continue")
        #print("")
        return actionToTake

    def value(self, gameState, depth, agentIndex, a, b):
      # Base case: check if depth has been reached or if we won or lost
      if depth == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      if agentIndex == 0: # Agent is pacman
        return self.maxValue(gameState, depth, agentIndex, a, b)
      else:
        return self.minValue(gameState, depth, agentIndex, a, b)
    
    def maxValue(self, gameState, depth, agentIndex, a, b):
      v = -100000
      legalMoves = gameState.getLegalActions(0)
      # Loop through children
      for action in legalMoves:
        v = max(v, self.value(gameState.generateSuccessor(0, action),depth,1, a ,b))
        if v > b:
          return v
        a = max(a,v)
      if v == -100000:
        return self.evaluationFunction(gameState)
      return v

    def minValue(self, gameState, depth, agentIndex, a, b):
      v = 100000
      legalMoves = gameState.getLegalActions(agentIndex)
      # Loop through children
      for action in legalMoves:
        if agentIndex == gameState.getNumAgents() -1:
          v = min(v, self.value(gameState.generateSuccessor(agentIndex, action),depth+1,0, a, b)) # That's the last min level
        else:
          v = min(v, self.value(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1, a, b)) # There are more min levels
        if v < a:
          return v
        b = min(b,v)
      if v == 100000:
        return self.evaluationFunction(gameState)
      return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        actionToTake = ""
        v = -100000
        for action in gameState.getLegalActions():
          newV = self.expValue(gameState.generateSuccessor(0,action), 0, 1)
          # Check if this is a better move
          if newV > v and newV != 100000:
            v = newV
            actionToTake = action
        return actionToTake
    
    def value(self, gameState, depth, agentIndex):
      # Base case: check if depth has been reached or if we won or lost
      if depth == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      if agentIndex == 0: # Agent is pacman
        return self.maxValue(gameState, depth, agentIndex)
      else: # Agent is ghost
        return self.expValue(gameState, depth, agentIndex)

    def maxValue(self, gameState, depth, agentIndex):
      v = -100000
      legalMoves = gameState.getLegalActions(0)
      # Loop through children
      for action in legalMoves:
        v = max(v, self.value(gameState.generateSuccessor(0, action),depth,1))
      return v

    def expValue(self, gameState, depth, agentIndex):
      v = [0] # create a new empty list and add each probability
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
        if agentIndex == gameState.getNumAgents() -1:
          v.append(self.value(gameState.generateSuccessor(agentIndex, action),depth+1,0)) # That's the last min level
        else:
          v.append(self.value(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1))
      # Calculate expected value
      total = float(sum(v))
      num = float(len(v)-1)
      if num == 0: # Check if the denominator is not 0
        return self.evaluationFunction(gameState)
      return total/num

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Get necessary information
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()
    scared = [ghostState.scaredTimer for ghostState in ghosts]
    capsules = currentGameState.getCapsules()

    currX, currY = pos

    # Check all of the food distances
    foodDistances = []
    if len(food.asList()) != 0:
      for x in range(0,food.width):
        for y in range(0,food.height):
          if food[x][y] == True:
            foodDistances.append(manhattanDistance((x,y),pos))
      foodScore = int(float(1)/float(min(foodDistances)) * 10) # Inverse of closest food
    else:
      foodScore = 0
    
    # Check all ghosts
    ghostScore = 0
    for i in ghosts:
      ghostX, ghostY = i.getPosition()
      ghostDistance = manhattanDistance(pos,(ghostX,ghostY))
      if ghostDistance != 0:
          # Check if the ghost is scared
          if i.scaredTimer > 0:  # Ghost is scared, we must attack it
              ghostScore += float(20)/float(ghostDistance)
          else:
              ghostScore -= float(10)/float(ghostDistance)

    score = currentGameState.getScore() + foodScore + ghostScore

    return score
# Abbreviation
better = betterEvaluationFunction

