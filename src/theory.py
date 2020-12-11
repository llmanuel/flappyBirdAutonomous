import pygame
from src.worldState import WorldState
from src.utilityCalculator import UtilityCalculator
from src.distance import Distance

CRITICAL_DISTANCE = 180
DANGER_DISTANCE = 60
class Theory:
    def __init__(self, currentPositions, velocity, counter, action):
        self.currentWorldState = WorldState(
            self.isInTheGapHeight(currentPositions),
            self.isCrossingTheGap(currentPositions),
            self.isFarAwayFormWall(currentPositions),
            self.calculateDistanceToGap(currentPositions),
            velocity,
            currentPositions,
            counter
        )
        self.action = action
        self.expectedResult = None
        self.successCount = 0
        self.useCount = 0
        self.utility = None

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Theory):
            return (
                self.currentWorldState == other.currentWorldState and
                self.expectedResult == other.expectedResult and
                self.action == other.action
            )
        return False

    def getAction(self):
        return self.action

    def setAction(self, action):
        self.action = action

    def setExpectedResult(self, worldResultPositions, velocity, counter, isDead):
        self.expectedResult = WorldState(
            self.isInTheGapHeight(worldResultPositions),
            self.isCrossingTheGap(worldResultPositions),
            self.isFarAwayFormWall(worldResultPositions),
            self.calculateDistanceToGap(worldResultPositions),
            velocity,
            worldResultPositions,
            counter,
            isDead
        )
        self.utility = UtilityCalculator(self.currentWorldState, self.expectedResult, self.action).getUtility()

    def verifyResult(self, worldResultPositions, velocity, counter, isDead):
        if self.action == 'holdKey' and self.calculateDistanceToGap(worldResultPositions) < self.currentWorldState.distanceToGap:
            isDead = True
        if not self.expectedResult:
            self.setExpectedResult(worldResultPositions, velocity, counter, isDead)
            return True
        else:
            worldResult = WorldState(
                self.isInTheGapHeight(worldResultPositions),
                self.isCrossingTheGap(worldResultPositions),
                self.isFarAwayFormWall(worldResultPositions),
                self.calculateDistanceToGap(worldResultPositions),
                velocity,
                worldResultPositions,
                counter,
                isDead
            )
            newUtility = UtilityCalculator(self.currentWorldState, worldResult, self.action).getUtility()
            # comparar resultados
            self.useCount += 1
            if worldResult == self.expectedResult and newUtility == self.utility:
                self.successCount += 1
                return True
            else:
                return False # crear una nueva teoria si retorna False

    def getTheoryValue(self):
        if not self.useCount or self.useCount < 5:
            return self.utility
        
        return self.utility * (self.successCount / self.useCount)
    
    def isInTheGapHeight(self, currentPositions):
        birdPosition = pygame.Rect(currentPositions[2])
        topWallPosition = pygame.Rect([birdPosition.left, currentPositions[1][1] + 20, *currentPositions[1][-2:]])
        bottomWallPosition = pygame.Rect([birdPosition.left, currentPositions[0][1] - 20, *currentPositions[0][-2:]])
        
        return not bool(topWallPosition.colliderect(birdPosition)) and not bool(bottomWallPosition.colliderect(birdPosition))
        
    def calculateDistanceToGap(self, currentPositions):
        birdPosition = pygame.Rect(currentPositions[2])
        topWallPosition = pygame.Rect([birdPosition.left, *currentPositions[1][-3:]])
        bottomWallPosition = pygame.Rect([birdPosition.left, *currentPositions[0][-3:]])
        gapCenter = int((bottomWallPosition.top + topWallPosition.bottom) / 2) + 10
        if (gapCenter > birdPosition.bottom):
            return gapCenter - birdPosition.bottom
        elif (gapCenter < birdPosition.top):
            return gapCenter - birdPosition.top # si me paso es negativo
        else:
            return 0

    def isCrossingTheGap(self, currentPositions):
        wallsPosition = pygame.Rect(currentPositions[1][0], 0, 90, 720)
        topWallPosition = pygame.Rect(currentPositions[1])
        bottomWallPosition = pygame.Rect(currentPositions[0])
        birdPosition = pygame.Rect(currentPositions[2])

        return (not bool(topWallPosition.colliderect(birdPosition)) or not bool(bottomWallPosition.colliderect(birdPosition))) and bool(wallsPosition.colliderect(birdPosition))
        
    def isFarAwayFormWall(self, currentPositions):
        leftSideOfWall = int(currentPositions[1][0])
        rightSideOfBird = int(currentPositions[2][0] + currentPositions[2][2])

        print(f"Distance to wall: {leftSideOfWall - rightSideOfBird}")
        if CRITICAL_DISTANCE < leftSideOfWall - rightSideOfBird:
            return Distance.SAFE
        elif CRITICAL_DISTANCE > leftSideOfWall - rightSideOfBird > DANGER_DISTANCE:
            return Distance.CAREFUL
        else:
            return Distance.DANGER



        # distancia en x a los tubos -> dado un X si x > X no es tan grave. Si x < X todo importa mas
        # 1. Estoy chocando el tubo de arriba
        # 2. Estoy chocando el tubo de abajo
        # 3. Estoy a la altura del gap
        # Fucionar 1, 2 y 3 en estoy chocando el tubo


        # Estoy en el gap

        # self.topWallPosition = currentPositions[1]
        # self.bottomWallPosition = currentPositions[0]
        # self.birdPosition = currentPositions[2]
        # self.turnsSinceHoldKey = turnsSinceHoldKey
        # self.action = None
        # distancia al tubo
        # estoy chocando en el rango del tubo de arriba
        # estoy chocando el tubo de abajo
        # estoy pasando por el medio 
        # estoy atravesando el caño
        # estoy en medio del aire



# si la teoria falla entonces creas una nueva teoria con la utilidad nueva
# Funcion de utilidad:
# fijate si estas mas cerca del hueco 1
# si pasaste el tubo Max
# si moriste, creas una teoria que tenga una utilidad distinta. Entonces despues podrias hacer una teoria mutante que abarca ambas teorias