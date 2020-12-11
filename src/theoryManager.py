import pygame
import random
import numpy as np
from src.actions import Actions
from src.theory import Theory
from src.distance import Distance

class TheoryManager:
    def __init__(self):
        self.theoryList = []

    def getTheoriesForSituation(self, newTheory, turns):
        # read theories and check for one similar to this situation
        if len(self.theoryList) == 0:
            self.theoryList.append(newTheory)
            return newTheory
        
        print(f"Number of theories: {len(self.theoryList)}")
        thereIsHoldKey = False
        thereIsRelease = False
        theoriesForCurrentSituation = []
        for i, theory in enumerate(self.theoryList):
            if theory.currentWorldState == newTheory.currentWorldState and (theory.utility is not None):
                if (theory.action == Actions.HOlD_KEY):
                    thereIsHoldKey = True
                if (theory.action == Actions.RELEASE_KEY):
                    thereIsRelease = True
                theoriesForCurrentSituation.append(theory)

        selectedTheory = None
        if len(theoriesForCurrentSituation) == 0:
            self.theoryList.append(newTheory)
            selectedTheory = newTheory
        elif thereIsHoldKey and thereIsRelease:
            maxValueTheory = max(theoriesForCurrentSituation, key=lambda theory: theory.getTheoryValue())
            if (maxValueTheory.getTheoryValue() < 0) and random.randint(0, 10) < 1 * abs(maxValueTheory.utility):
                selectedTheory = self.explore(newTheory, self.newTheoryIsABadTheory(newTheory, maxValueTheory) and newTheory.getAction() == maxValueTheory.getAction())
            # if (maxValueTheory.getTheoryValue() < 0):
                # if turns > 20000: 
                #     name = input("Enter your name: ")
            #     selectedTheory = self.explore(newTheory, self.newTheoryIsABadTheory(newTheory, maxValueTheory) and newTheory.getAction() == maxValueTheory.getAction())
            # elif (maxValueTheory.getTheoryValue() == 0):
            #     selectedTheory = self.explore(newTheory, random.randint(0, 10) > 4)
            else:
                selectedTheory = maxValueTheory
        elif ((thereIsHoldKey and not thereIsRelease) or (not thereIsHoldKey and thereIsRelease)) and random.randint(0, 10) <= 4:
            selectedTheory = self.explore(newTheory, self.newTheoryIsABadTheory(newTheory, max(theoriesForCurrentSituation, key=lambda theory: theory.getTheoryValue())))
        else:
            maxValueTheory = max(theoriesForCurrentSituation, key=lambda theory: theory.getTheoryValue())
            selectedTheory = self.explore(newTheory, self.newTheoryIsABadTheory(newTheory, maxValueTheory) or (maxValueTheory.getTheoryValue() == 0 and random.randint(0, 10) > 4))

        return selectedTheory

    def explore(self, newTheory, condition):
        if condition:
            newAction = Actions().getAnother(newTheory.action)
            newTheory.setAction(newAction)

        self.theoryList.append(newTheory)
        return newTheory

    def newTheoryIsABadTheory(self, newTheory, maxValueTheory):
        return (maxValueTheory.getTheoryValue() < 0) and newTheory.currentWorldState == maxValueTheory.currentWorldState


    def createNewTheory(self, currentPositions, velocity, counter):
        if random.randint(0, 2) == 2:
            return Theory(currentPositions, velocity, counter, Actions.HOlD_KEY)
        else:
            return Theory(currentPositions, velocity, counter, Actions.RELEASE_KEY)

    def getTheory(self, currentPositions, velocity, counter, turns):
        newTheory = self.createNewTheory(currentPositions, velocity, counter)
        return self.getTheoriesForSituation(newTheory, turns)

    def verifyTheory(self, theory, worldResultPositions, velocity, counter, isDead, turns):
        index = 0
        for i, item in enumerate(self.theoryList):
            if id(item) == id(theory):
                index = i
                break

        result = self.theoryList[index].verifyResult(worldResultPositions, velocity, counter, isDead)

        self.removeTheoryIfDeadByCrushingWall(index)
        print("verify result: ", result)
        if not result:
            lastPositions = self.theoryList[index].currentWorldState.currentPositions
            lastVelocity = self.theoryList[index].currentWorldState.velocity
            newTheory = self.createNewTheory(lastPositions, lastVelocity, self.theoryList[index].currentWorldState.counter)
            newTheory.setAction(self.theoryList[index].action)
            newTheory.verifyResult(worldResultPositions, velocity, counter, isDead)
            self.theoryList.append(newTheory)
        # cleaning similar or worthless theories
        self.removeUnsuccessfullTheories()
        if turns % 5000 == 0:
            for i, item in enumerate(self.theoryList):
                self.mergeSimilarTheoriesTo(item)


    def removeTheoryIfDeadByCrushingWall(self, index):
        expectedResult = self.theoryList[index].expectedResult
        currentWorldState = self.theoryList[index].currentWorldState
        if expectedResult.farAwayFormWall == Distance.SAFE and currentWorldState.farAwayFormWall == Distance.DANGER:
            self.theoryList.pop(index)

    def removeUnsuccessfullTheories(self):
        def successPercentage(theory):
            if theory.useCount == 0:
                return 1
            return theory.successCount/theory.useCount
            
        usefullTheories = [theory for theory in self.theoryList if successPercentage(theory) > 0.1]
        self.theoryList = usefullTheories

    def mergeSimilarTheoriesTo(self, theoryToCheck):
        restOfTheories = []
        similarTheories = []
        similarTheoriesUtilityValues = set()
        for i, theory in enumerate(self.theoryList):
            if theoryToCheck == theory: # equal currentState, action and expectedResult
                similarTheoriesUtilityValues.add(theory.utility)
                similarTheories.append(theory)
            else:
                restOfTheories.append(theory)

        mergedTheories = []
        commonTheory = theoryToCheck
        for i, utility in enumerate(similarTheoriesUtilityValues):
            theoriesWithUtility = [theory for theory in similarTheories if theory.utility == utility]
            commonTheory = theoriesWithUtility[0]
            for i, theory in enumerate(theoriesWithUtility):
                if theory.useCount > commonTheory.useCount and theory.successCount > commonTheory.successCount:
                    commonTheory = theory
            
            mergedTheories.append(commonTheory)
        
        self.theoryList = [*restOfTheories, *mergedTheories]

