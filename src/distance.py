import pygame

class Distance:
  SAFE = 'safe'
  CAREFUL = 'careful'
  DANGER = 'danger'

class Zones:
  FAR = 'far'
  MIDDLE = 'middle'
  BORDER = 'border'
  GAP_TOP = 'gapTop'
  GAP_MIDDLE = 'gapMiddle'
  GAP_BOTTOM = 'gapBottom'

  def __init__(self):
    pass

  def getZoneAccordingToWalls(self, currentPositions):
    birdPosition = pygame.Rect(currentPositions[2])
    topWallPosition = pygame.Rect([birdPosition.left, *currentPositions[1][-3:]])
    bottomWallPosition = pygame.Rect([birdPosition.left, *currentPositions[0][-3:]])
    gapSize = bottomWallPosition.top - topWallPosition.bottom
    distance = 0
    if (bottomWallPosition.top > birdPosition.bottom):
      distance = bottomWallPosition.top - birdPosition.bottom
    else:
      distance = bottomWallPosition.top - birdPosition.top

    gapZonesSize = gapSize / 3

    if distance >= 40 + gapSize or distance < -40:
      return Zones.FAR
    elif 40 + gapSize > distance > 20 + gapSize or -40 < distance < -20 :
      return Zones.MIDDLE
    elif gapSize < distance <= 20 + gapSize or 0 > distance > -20:
      return Zones.BORDER
    elif gapSize > distance > gapZonesSize * 2:
      return Zones.GAP_TOP
    elif gapZonesSize * 2 > distance > gapZonesSize:
      return Zones.GAP_MIDDLE
    elif gapZonesSize > distance > 0:
      return Zones.GAP_BOTTOM