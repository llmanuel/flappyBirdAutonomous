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
    if (bottomWallPosition.top < birdPosition.bottom):
      distance = bottomWallPosition.top + 15 - birdPosition.bottom # el punto mas lejano del pajaro
    elif (bottomWallPosition.top > birdPosition.bottom):
      distance = bottomWallPosition.top + 15 - birdPosition.bottom # el punto mas lejano del pajaro
    else:
      distance = 0

    # gapZonesSize = gapSize / 3
    gapLimitBottom = gapSize * 0.3
    gapLimitMiddle = gapSize * 0.5

    if distance >= 40 + gapSize or distance < -40:
      return Zones.FAR
    elif 40 + gapSize >= distance > 20 + gapSize or -40 <= distance < -20 :
      return Zones.MIDDLE
    elif gapSize < distance <= 20 + gapSize or 0 > distance >= -20:
      return Zones.BORDER
    elif gapSize >= distance > gapLimitMiddle:
      return Zones.GAP_TOP
    elif gapLimitMiddle >= distance > gapLimitBottom:
      return Zones.GAP_MIDDLE
    elif gapLimitBottom >= distance >= 0:
      return Zones.GAP_BOTTOM
    else:
      n = input("hola wacho")
      print(n)

  def inGapZones(self, zone):
    return zone == Zones.GAP_TOP or zone == Zones.GAP_MIDDLE or zone == Zones.GAP_BOTTOM