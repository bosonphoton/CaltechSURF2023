import math
from params import params

# Screen width:          60 cm = 600 mm
# Horizontal resolution: 3840
# pixel size:            600/3840 = 0.1562
# Viewing distance:      57 cm = 570 mm
# VA formula:            2 * atand ( size in mm / viewDist*2)

def visual_angle(env,param,stim,circLoc,win,deg):
    
    param["pixSize"] = 600 / win.size[0]
    param["viewDist"] = 570 * 2

    deg = {}

    deg['one'] = (math.degrees(math.atan(1) / 2 * param["viewDist"]) / param["pixSize"])
    deg['two'] = (math.degrees(math.atan(2) / 2 * param["viewDist"]) / param["pixSize"])
    deg['three'] = (math.degrees(math.atan(3) / 2 * param["viewDist"]) / param["pixSize"])

    deg['five'] = (math.degrees(math.atan(5) / 2 * param["viewDist"]) / param["pixSize"])
    deg['ten'] = (math.degrees(math.atan(10) / 2 * param["viewDist"]) / param["pixSize"])
    deg['fifteen'] = (math.degrees(math.atan(15) / 2 * param["viewDist"]) / param["pixSize"])

    deg['five_diag'] = math.sqrt((deg['five'] ** 2) / 2)
    deg['ten_diag'] = math.sqrt((deg['ten'] ** 2) / 2)
    deg['fifteen_diag'] = math.sqrt((deg['fifteen'] ** 2) / 2)
    
    return deg
