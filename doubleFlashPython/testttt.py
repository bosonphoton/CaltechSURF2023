# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:28:20 2023

@author: achan2
"""

from psychopy import visual, core, sound
import numpy as np
import math

# Set up the window
win = visual.Window(size=(800, 800), units='pix', color=(-1, -1, -1)) #None for testing purposes) 
# win = visual.Window(size = (3840, 2160), fullscr=True, units='pix', color=(-1, -1, -1)) #black scree

env = {}
env['screenXpixels'], env['screenYpixels'] = win.size
env["xCenter"], env["yCenter"] = (0,0)
# Set up sound

env['sampleRate'] = 48000  # or 44100

env['frameRate'] = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)

if env['frameRate'] is not None:
    env['ifi'] = 1 / env['frameRate']
else:
    env['ifi'] = 1/60

win.close()
param = {}
param["viewDist"] = 570 * 2
param['nchannels'] = 2
param['startCue'] = 0
param['repetitions'] = 1
param['waitForDeviceStart'] = 1

#audio_handle = sound.Sound(value=0, sampleRate=env['sampleRate'], channels=param['nchannels'])

param['beepDuration'] = 0.007  # seconds (7 ms)
param['audioDelay'] = -0.105
param['beepOneBalance'] = 0.5
param['beepTwoBalance'] = 0.5
param['preFlashBeepT'] = 0.023 - param['audioDelay']  # From double flash paper
param['postFlashBeepT'] = 0.064 - (0.023 - param['audioDelay'])  # From double flash paper

# flash will begin at t = 50ms
param['beepOneT'] = 0.170 - param['preFlashBeepT']  # in sec
param['beepTwoT'] = 0.170 + param['postFlashBeepT']  # in sec
param['beepOneSamps'] = int(param['beepOneT'] * env['sampleRate'])  # 1536


param['beepTwoSamps'] = int(param['beepTwoT'] * env['sampleRate'])  # in Hz

#############?????###################### Unsure About This ###############################################

param['beep_array'] = np.sin(2 * np.pi * param['beepOneBalance'] * np.arange(0,param['beepDuration']*env['sampleRate']-1)/env['sampleRate']) #(335,)
param["beep_samps"] = np.size(param['beep_array']) #335
#############?????###################### Unsure About This ###############################################


# Entire stimulus is 200 ms long
param['beep_nSamps'] = int(env['sampleRate'] * 0.200)  # 9600
param['left_singleBeep_array'] = np.zeros(param['beep_nSamps'])
param['right_singleBeep_array'] = np.zeros(param['beep_nSamps'])

param["left_singleBeep_array"][param["beepOneSamps"]:param["beepOneSamps"] + param["beep_samps"]] = param["beep_array"] * (1- param["beepOneBalance"])
param["right_singleBeep_array"][param["beepOneSamps"]:param["beepOneSamps"] + param["beep_samps"]] = param["beep_array"] * param["beepOneBalance"]

# add in second beep
param['left_doubleBeep_array'] = param['left_singleBeep_array']
param['right_doubleBeep_array'] = param['right_singleBeep_array']
param["left_doubleBeep_array"][param["beepTwoSamps"]:param["beepTwoSamps"] + param["beep_samps"]] = param["beep_array"] * (1 - param["beepTwoBalance"])
param["right_doubleBeep_array"][param["beepTwoSamps"]:param["beepTwoSamps"] + param["beep_samps"]] = param["beep_array"] * param["beepTwoBalance"]



# eccentricity
param['eccs'] = 600
param['shift'] = 0
#     % Screen width:          60 cm = 600 mm
# % Horizontal resolution: 3840
# % pixel size:            600/3840 = 0.1562
# % Viewing distance:      57 cm = 570 mm
# % VA formula:            2 * atand ( size in mm / viewDist*2)

# param.pixSize = 600/env.screenXpixels;
param["pixSize"] = 600/3840 


deg = {}

deg['one'] = (math.tan(math.radians(1))/2*param['viewDist'])/param['pixSize']
deg['two'] = (math.tan(math.radians(2))/2*param['viewDist'])/param['pixSize']
deg['three'] = (math.tan(math.radians(3))/2*param['viewDist'])/param['pixSize']

deg['five'] = (math.tan(math.radians(5))/2*param['viewDist'])/param['pixSize']
deg['ten'] = (math.tan(math.radians(10))/2*param['viewDist'])/param['pixSize']
deg['fifteen'] = (math.tan(math.radians(15))/2*param['viewDist'])/param['pixSize']

deg['five_diag'] = math.sqrt(math.pow(deg['five'], 2)/2)
deg['ten_diag'] = math.sqrt(math.pow(deg['ten'], 2)/2)
deg['fifteen_diag'] = math.sqrt(math.pow(deg['fifteen'], 2)/2)



param["cross"] = [deg["five"], deg["ten"],deg["fifteen"]]
param["diago"] = [deg["five_diag"], deg["ten_diag"], deg["fifteen_diag"]]

circLoc = {}

#################### ???? EDIT THIS ??? #######################################
for i in range(1,25):
    #case verticle 
    if i in range(1,4):
        circLoc[i] = (env["xCenter"], env["yCenter"] - param["cross"][i-1])
        circLoc[i+3] = (env["xCenter"], env["yCenter"] + param["cross"][i-1])
    #case horizon
    if i in range(7,10):
        circLoc[i] = (env["xCenter"] + param["cross"][i-7], env["yCenter"])
        circLoc[i+3] = (env["xCenter"] - param["cross"][i-7], env["yCenter"])
    #case diag
    if i in range(13,16):
        circLoc[i] = (env["xCenter"] + param["diago"][i-13], env["yCenter"] - param["diago"][i-13])
    if i in range(16,19):
        circLoc[i] = (env["xCenter"] - param["diago"][i%3-1], env["yCenter"] + param["diago"][i%3-1])
    if i in range(19,22):
        circLoc[i] = (env["xCenter"] + param["diago"][i%3-1], env["yCenter"] + param["diago"][i%3-1])
    if i in range(22,25):
        circLoc[i] = (env["xCenter"] - param["diago"][i%3-1], env["yCenter"] - param["diago"][i%3-1])
    
    
