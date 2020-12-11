import pygame
from src.distance import Distance, Zones
from src.actions import Actions

GAP_SIZE = 130

class UtilityCalculator:
    def __init__(self, currentWorldState, worldResult, action):
        self.currentWorldState = currentWorldState
        self.worldResult = worldResult
        self.action = action

    def getUtility(self):
        if self.worldResult.isDead:
            return -8
        elif self.worldResult.counter > self.currentWorldState.counter:
            return 1000
        elif self.worldResult.farAwayFormWall == Distance.SAFE:
            if self.worldResult.zone == Zones.BORDER and self.isVelocityHelping(self.action):
                return 3
            elif self.worldResult.zone == Zones.MIDDLE and self.isVelocityHelping(self.action):
                return 2
            elif abs(self.worldResult.distanceToGap) < abs(self.currentWorldState.distanceToGap):
                return 1
            elif self.isVelocityHelping(self.action):
                return 1
            else:
                return -1
        elif self.worldResult.farAwayFormWall == Distance.CAREFUL:
            if self.worldResult.zone == Zones.MIDDLE and self.isVelocityHelping(self.action):
                return 1
            elif self.worldResult.zone == Zones.MIDDLE and not self.isVelocityHelping(self.action):
                return -4
            elif not self.worldResult.inGapHeight and self.worldResult.zone == Zones.BORDER and self.isVelocityHelping(self.action):
                return 2
            elif not self.worldResult.inGapHeight and self.worldResult.zone == Zones.BORDER and not self.isVelocityHelping(self.action):
                return -1
            elif self.worldResult.inGapHeight:
                if self.worldResult.zone == Zones.GAP_BOTTOM and self.isVelocityHelping(self.action):
                    return 5
                elif self.worldResult.zone == Zones.GAP_MIDDLE and self.isVelocityHelping(self.action):
                    return 4
                elif self.worldResult.zone == Zones.GAP_TOP and self.isVelocityHelping(self.action):
                    return 2
                elif not self.isVelocityHelping(self.action):
                    return 0
                else:
                    return 1
            elif self.worldResult.zone == Zones.FAR and self.isVelocityHelping(self.action): # if zone is far
                return -3
            elif self.worldResult.zone == Zones.FAR and not self.isVelocityHelping(self.action):
                return -5
        elif self.worldResult.crossingTheGap:
            # ver de ir sumando puntos si voy mas al medio y eso
            if self.worldResult.zone == Zones.GAP_BOTTOM and self.isVelocityHelping(self.action):
                return 10
            elif self.worldResult.zone == Zones.GAP_MIDDLE and self.isVelocityHelping(self.action):
                return 7
            elif self.worldResult.zone == Zones.GAP_TOP and self.isVelocityHelping(self.action):
                return 4
            elif not self.isVelocityHelping(self.action):
                return 0
            else:
                return 2
        elif self.worldResult.farAwayFormWall == Distance.DANGER:
            if self.worldResult.zone == Zones.MIDDLE and self.isVelocityHelping(self.action):
                return -2
            elif self.worldResult.zone == Zones.FAR and not self.isVelocityHelping(self.action):
                return -8
            if self.worldResult.zone == Zones.BORDER and self.isVelocityHelping(self.action):
                return 2
            elif self.worldResult.zone == Zones.BORDER and not self.isVelocityHelping(self.action):
                return -8
            # elif not self.worldResult.inGapHeight and abs(self.worldResult.distanceToGap) < 20 and self.isVelocityHelping(self.action):
            #     return 2
            # elif not self.worldResult.inGapHeight:
            #     return -8
            elif self.worldResult.inGapHeight:
                if self.worldResult.zone == Zones.GAP_BOTTOM and self.isVelocityHelping(self.action):
                    return 9
                elif self.worldResult.zone == Zones.GAP_MIDDLE and self.isVelocityHelping(self.action):
                    return 7
                elif self.worldResult.zone == Zones.GAP_TOP and self.isVelocityHelping(self.action):
                    return 2
                elif not self.isVelocityHelping(self.action):
                    return 0
                else:
                    return 1

    def isVelocityHelping(self, action):
        if self.worldResult.inGapHeight and abs(self.worldResult.velocity) < 6:
            return True
        elif not self.worldResult.inGapHeight:
            worldResultPositions = self.worldResult.currentPositions
            birdPosition = pygame.Rect(worldResultPositions[2])
            topWallPosition = pygame.Rect([birdPosition.left, *worldResultPositions[1][-3:]])
            bottomWallPosition = pygame.Rect([birdPosition.left, *worldResultPositions[0][-3:]])

            furtherZones = self.worldResult.zone == Zones.FAR or self.worldResult.zone == Zones.MIDDLE or self.worldResult.zone == Zones.BORDER

            if topWallPosition.colliderect(birdPosition):
                if action == Actions.HOlD_KEY:
                    return False
                elif furtherZones and self.worldResult.velocity < self.currentWorldState.velocity:
                    return True
                elif self.worldResult.velocity < 0 or (self.worldResult.velocity < self.currentWorldState.velocity and self.worldResult.velocity < 5):
                    return True
                else:
                    False
            elif bottomWallPosition.colliderect(birdPosition):
                if action == Actions.RELEASE_KEY:
                    return False
                if furtherZones and self.worldResult.velocity > self.currentWorldState.velocity:
                    return True
                elif self.worldResult.velocity > 0 or (self.worldResult.velocity > self.currentWorldState.velocity and self.worldResult.velocity > -5):
                    return True
                else:
                    False
            elif self.worldResult.crossingTheGap or self.worldResult.inGapHeight:
                if action == Actions.RELEASE_KEY and self.worldResult.zone == Zones.GAP_TOP:
                    return True
                elif action == Actions.HOlD_KEY and self.worldResult.zone == Zones.GAP_BOTTOM:
                    return True
                elif -8 < self.worldResult.velocity < 8:
                    return True
                else:
                    False
            else:
                False
            