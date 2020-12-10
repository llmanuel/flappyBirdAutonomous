import pygame

class UtilityCalculator:
    def __init__(self, currentWorldState, worldResult):
        self.currentWorldState = currentWorldState
        self.worldResult = worldResult

    def getUtility(self):
        if self.worldResult.isDead:
            return -1
        elif self.worldResult.counter > self.currentWorldState.counter:
            return 1000
        elif self.worldResult.farAwayFormWall:
            if abs(self.worldResult.distanceToGap) < abs(self.currentWorldState.distanceToGap) or self.worldResult.distanceToGap == 0:
                return 1
            elif self.isVelocityHelping():
                return 1
            else:
                return 0
        elif not self.worldResult.farAwayFormWall and not self.worldResult.crossingTheGap:
            if self.worldResult.distanceToGap < self.currentWorldState.distanceToGap:
                return 4
            elif self.isVelocityHelping():
                return 2
            else:
                return -1
        elif self.worldResult.crossingTheGap:
            # ver de ir sumando puntos si voy mas al medio y eso
            if self.isVelocityHelping():
                return 10
            else:
                return 2

    def isVelocityHelping(self):
        if self.worldResult.inGapHeight and abs(self.worldResult.velocity) < 9:
            return True
        elif not self.worldResult.inGapHeight:
            worldResultPositions = self.worldResult.currentPositions
            birdPosition = pygame.Rect(worldResultPositions[2])
            topWallPosition = pygame.Rect([birdPosition.left, *worldResultPositions[1][-3:]])
            bottomWallPosition = pygame.Rect([birdPosition.left, *worldResultPositions[0][-3:]])

            if topWallPosition.colliderect(birdPosition) and self.worldResult.velocity < self.currentWorldState.velocity:
                return True
            elif bottomWallPosition.colliderect(birdPosition) and self.worldResult.velocity > self.currentWorldState.velocity:
                return True
            else:
                False
            