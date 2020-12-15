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
                (self.distanceToGap > 0) == (other.distanceToGap > 0) and
                self.isDead == other.isDead and
                self.zone == other.zone and
                self.similarVelocity(other) # chequear esto
                # and self.counter == other.counter no se si necesito esto
            )
        return False

    def similarVelocity(self, other):
        def first(vel):
            return vel >= 6
        def second(vel):
            return 6 > vel >= 2
        def third(vel):
            return 2 > vel >= -2
        def fourth(vel):
            return -2 > vel >= -6
        def fifth(vel):
            return -6 > vel

        return (
            first(self.velocity) == first(other.velocity) or
            second(self.velocity) == second(other.velocity) or 
            third(self.velocity) == third(other.velocity) or 
            fourth(self.velocity) == fourth(other.velocity) or 
            fifth(self.velocity) == fifth(other.velocity)
        )


        # def isSlowVelocity(vel):
        #     if abs(vel) < 4:
        #         True
        #     else:
        #         False

        # return isSlowVelocity(self.velocity) == isSlowVelocity(other.velocity)

        # if (self.velocity > 0) == (other.velocity > 0) and abs(self.velocity - other.velocity) < 0.5:
        #     return True
        # elif (self.velocity < 0) == (other.velocity < 0) and abs(self.velocity - other.velocity) < 0.5:
        #     return True
        # else:
        #     False
