from src.distance import Zones

class WorldState:
    def __init__(self, inGapHeight, crossingTheGap, farAwayFormWall, distanceToGap, velocity, currentPositions, counter, isDead = None):
        self.inGapHeight = inGapHeight
        self.crossingTheGap = crossingTheGap
        self.farAwayFormWall = farAwayFormWall
        self.distanceToGap = distanceToGap
        self.zone = Zones().getZoneAccordingToWalls(currentPositions)
        self.isDead = isDead
        self.counter = counter
        self.velocity = velocity
        self.currentPositions = currentPositions

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, WorldState):
            return (
                # self.inGapHeight == other.inGapHeight and
                # self.crossingTheGap == other.crossingTheGap and
                # self.farAwayFormWall == other.farAwayFormWall and
                # (self.distanceToGap > 0) == (other.distanceToGap > 0) and
                self.isDead == other.isDead and
                self.zone == other.zone and
                self.similarVelocity(other) # chequear esto
                # and self.counter == other.counter no se si necesito esto
            )
        return False

    def similarVelocity(self, other):
        if (self.velocity > 0) == (other.velocity > 0) and abs(self.velocity - other.velocity) < 0.5:
            return True
        elif (self.velocity < 0) == (other.velocity < 0) and abs(self.velocity - other.velocity) < 0.5:
            return True
        else:
            False
