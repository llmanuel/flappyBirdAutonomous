import pygame
import random
import numpy as np
from src.actions import Actions
from src.theory import Theory
from src.distance import Distance
from src.theoryDb import TheoryDb

class TheoryManager:
    def __init__(self):
        self.theoryList = []

    def loadSavedTheories(self):
        self.theoryList = TheoryDb().fetchTheories()

    def saveTheories(self):
        TheoryDb().saveTheories(self.theoryList)

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
        else:
            theoryWithMaxValue = max(theoriesForCurrentSituation, key=lambda theory: theory.utility)
            theoriesWithMaxValue = [th for th in theoriesForCurrentSituation if th.utility == theoryWithMaxValue.utility]
            maxValueTheory = max(theoriesWithMaxValue, key=lambda theory: theory.successCount)
            if thereIsHoldKey and thereIsRelease:
                if (maxValueTheory.getTheoryValue() < 0) or maxValueTheory.useCount < 5:
                    if(maxValueTheory.getTheoryValue() > 6 and random.randint(0, 10) < 7):
                        selectedTheory = maxValueTheory
                    else:
                        selectedTheory = self.explore(newTheory, random.randint(0, 10) < 4 or (self.newTheoryIsABadTheory(newTheory, maxValueTheory) and newTheory.getAction() == maxValueTheory.getAction()))  
                elif (maxValueTheory.getTheoryValue() < 0.4) and random.randint(0, 10) < 4 * abs(maxValueTheory.utility):
                    selectedTheory = self.explore(newTheory, self.newTheoryIsABadTheory(newTheory, maxValueTheory) and newTheory.getAction() == maxValueTheory.getAction())
                # if (maxValueTheory.getTheoryValue() < 0):
                    # if turns > 20000: 
                    #     name = input("Enter your name: ")
                #     selectedTheory = self.explore(newTheory, self.newTheoryIsABadTheory(newTheory, maxValueTheory) and newTheory.getAction() == maxValueTheory.getAction())
                # elif (maxValueTheory.getTheoryValue() == 0):
                #     selectedTheory = self.explore(newTheory, random.randint(0, 10) > 4)
                else:
                    selectedTheory = maxValueTheory
            elif (thereIsHoldKey and not thereIsRelease) and maxValueTheory.getTheoryValue() < 6:
                newTheory.setAction(Actions.RELEASE_KEY)
                selectedTheory = newTheory
                self.theoryList.append(selectedTheory)
            elif (not thereIsHoldKey and thereIsRelease):
                newTheory.setAction(Actions.HOlD_KEY)
                selectedTheory = newTheory
                self.theoryList.append(selectedTheory)
            else:
                selectedTheory = self.explore(newTheory, self.newTheoryIsABadTheory(newTheory, maxValueTheory) or (maxValueTheory.getTheoryValue() == 0 and random.randint(0, 10) > 4))

        # if turns > 500 and selectedTheory.currentWorldState.zone == 'gapTop' and selectedTheory.action == Actions.HOlD_KEY:
        #     m = input('alto gato')
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

        self.increaseUseCountOfSimilarTheoriesTo(self.theoryList[index], worldResultPositions, velocity, counter, isDead)
        if self.theoryList[index].utility is None:
            n = input("algo raro gato")
        removed = self.removeTheoryIfDeadByCrushingWall(index)
        # print("verify result: ", result)
        if not result and not removed:
            lastPositions = self.theoryList[index].currentWorldState.currentPositions
            lastVelocity = self.theoryList[index].currentWorldState.velocity
            newTheory = self.createNewTheory(lastPositions, lastVelocity, self.theoryList[index].currentWorldState.counter)
            newTheory.setAction(self.theoryList[index].action)
            newTheory.verifyResult(worldResultPositions, velocity, counter, isDead)
            if newTheory.utility is None:
                n = input("algo raro gato3")
            self.theoryList.append(newTheory)
        # cleaning similar or worthless theories
        self.removeUnsuccessfullTheories()
        # if turns % 500 == 0:
        for i, item in enumerate(self.theoryList):
            self.mergeSimilarTheoriesTo(item)


    def removeTheoryIfDeadByCrushingWall(self, index):
        expectedResult = self.theoryList[index].expectedResult
        currentWorldState = self.theoryList[index].currentWorldState
        if expectedResult.farAwayFormWall == Distance.SAFE and currentWorldState.farAwayFormWall == Distance.DANGER:
            self.theoryList.pop(index)
            return True
        
        return False

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

    def increaseUseCountOfSimilarTheoriesTo(self, theoryToCheck, worldResultPositions, velocity, counter, isDead):
        for i, theory in enumerate(self.theoryList):
            if theoryToCheck.similar(theory): # equal currentState, action
                theory.verifyResult(worldResultPositions, velocity, counter, isDead)
