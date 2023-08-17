import numpy as np

def getGazeCircle(xCenter, yCenter, visualAngle):
    r = visualAngle  # radius
    C = [xCenter, yCenter]  # center
    theta = np.linspace(0, 2 * np.pi, 100)  # angles for generating points
    xGazeCircle = xCenter + r * np.cos(theta)  # x-coordinates of points
    yGazeCircle = yCenter + r * np.sin(theta)  # y-coordinates of points
    return xGazeCircle, yGazeCircle

