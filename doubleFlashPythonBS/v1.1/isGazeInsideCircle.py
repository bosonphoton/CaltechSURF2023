import math

#returns True or False
def isGazeInsideCircle(nowCoords, xCenter, yCenter, visualAngle):
    distance = math.sqrt((nowCoords[0] - xCenter)**2 + (nowCoords[1] - yCenter)**2)
    isInside = (distance <= visualAngle)
    return isInside
