from __future__ import division
from __future__ import print_function

from psychopy import visual, core, gui, data,event,sound,monitors
from psychopy.hardware import keyboard
import os
from os import path
import numpy as np
from psychopy import logging
import random
from random import randint, choice, shuffle
import csv
from datetime import datetime
import subprocess
from genTrials import genTrials
from demo_trials import demo_trials
from params import params
from task_master import task_master
import pandas as pd
import copy
import json

############ Eyelink Stuff ########################
# from psychopy.iohub.client import launchHubServer
# import pylink
# import platform
# import time
# import sys
# from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
# from PIL import Image  # for preparing the Host backdrop image
# from string import ascii_letters, digits
########### import rest of functions ############


# Main script to run experiment
# CHECK BEFORE YOU START
# Bose speaker turned on to max
# Computer volume at 50
# Chin rest - distance at 57cm
# param.audioDelay = -0.115 (set on 2022 Dell Computer 60Hz empirically  )

# Important variables to CHECK
dummymode = True
lowvision = False
showTrace = False

# Ask for subject details
myDlg = gui.Dlg(title='Input')
myDlg.addField('Initials:')
myDlg.addField('Age and sex (e.g. 23F):')
myDlg.addField('Which eye (L/R):')
myDlg.addField('Glasses (with/without/na):')
myDlg.addField('Show demo? (0/1):')
myDlg.addField('Task (vf/bdf):')
myDlg.show()

if not myDlg.OK:
    print('User cancelled the dialog box')
    core.quit()

initials = myDlg.data[0]
demographic = myDlg.data[1]
eye = myDlg.data[2]
glasses = myDlg.data[3]
showDemo = bool(int(myDlg.data[4]))
task = myDlg.data[5]

# check for exit conditions
if task != 'vf' and task != 'bdf':
    print("ERROR: Wrong task.")
    core.quit()
    sys.exit()




# # initialize Eyelink 1000
# ################################
# edf_fname = "expt0"
# edf_file = edf_fname + ".EDF"

# if not os.path.exists("EDF_Files"):
#     os.makedirs("EDF_Files")

# if dummymode == False:
#     try:
#         el_tracker = pylink.Eyelink("100.1.1.1") #Change to IP Address of Host PC
#     except:
#         print("Could not init eyelink")
#         core.quit()

# try:
#     el_tracker.openDataFile(edf_file)
# except:
#     print("Could not open eyelink data file")
#     core.quit()
#     sys.exit()




# el_tracker.doTrackerSetup()
# el_tracker.doDriftCorrect()
# el_tracker.startRecording()
# ################################
el_tracker = 0


# initial parameters
env,param,stim,circLoc,win,deg = params()



# # Configure a graphics environment (genv) for tracker calibration
# # Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# # see the EyeLink Installation Guide, "Customizing Screen Settings"
# el_coords = "screen_pixel_coords = 0 0 %d %d" % (env['screenXpixels'] - 1, env['screenYpixels'] - 1)
# el_tracker.sendCommand(el_coords)

# # Write a DISPLAY_COORDS message to the EDF file
# # Data Viewer needs this piece of info for proper visualization, see Data
# # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
# dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (env['screenXpixels'] - 1, env['screenYpixels'] - 1)
# el_tracker.sendMessage(dv_coords)

# genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win)
# print(genv)  # print out the version number of the CoreGraphics library
# foreground_color = (-1, -1, -1)
# background_color = win.color
# genv.setCalibrationColors(foreground_color, background_color)
# genv.setTargetType('circle')
# genv.setTargetSize(24)

# # Beeps to play during calibration, validation and drift correction
# # parameters: target, good, error
# #     target -- sound to play when target moves
# #     good -- sound to play on successful operation
# #     error -- sound to play on failure or interruption
# # Each parameter could be ''--default sound, 'off'--no sound, or a wav file
# genv.setCalibrationSounds('', '', '')
# pylink.openGraphicsEx(genv)




trials = genTrials(task,env,param,stim,circLoc,win,deg)

fileList = os.listdir("C:\\Users\\achan2\\Box\\SURF2023\\doubleFlashPython\\Data") #checks inside the data
foundFiles = [file for file in fileList if file.startswith(initials) and file.endswith(f'{task}_{eye}_{glasses}.json')]
    
path1 = os.path.join(os.getcwd(), 'Data', '')

if foundFiles: #check if file exists
    with open(os.path.join(path1,foundFiles[0])) as f:
        Data = json.load(f)
        if Data["Complete"] == 1:
            print("ERROR: Subject did this already.")
            core.quit()
        
        else: #start from last
            filePath = os.path.join(path1,foundFiles[0])
else:
    Data = {}
    Data["SubjectID"] = initials
    Data["Demographic"] = demographic
    Data["Eye"] = eye
    Data["glasses"] = glasses
    Data["Task"] = task
    Data["Conditions"] = []
    Data["Responses"] = []
    Data["RT"] = []
    Data["Catch"] = [] #catch trials
    Data["Present"] = {} #normal present trials
    Data["Complete"] = 0
    
    
    Data["Conditions"] = trials
    
    date = datetime.now().strftime('%d-%m-%Y %H_%M_%S')
    filePath = f'{path1}{initials}_{date}_{task}_{eye}_{glasses}.json' #C:\Users\achan2\Box\SURF2023\doubleFlashPython\Data\CZ_date_task_eye_glasses.py
    


# show demo
if showDemo:
    demo_trials(task,env,param,stim,circLoc,win,deg)

num_flashes, num_beeps, playBeep, Data = task_master(trials,task,env,param,stim,circLoc,win,deg,Data,filePath,eye,el_tracker)


# Save data
# if str(task) == "vf":
    
Data["Conditions"] = [condition + [resp, r] for condition, resp, r in zip(Data["Conditions"], Data["Responses"], Data["RT"])]
cop = copy.deepcopy(Data["Conditions"])
temp = sorted(cop, key=lambda x: x[1]) #sorts arr based on 2nd element, which indicated catch vs normal trials \
Data["Catch"] = [row[-2:] for row in temp[0:24]] #take only the catch trials rows, and only the Resp & RT of each


for j in range(24): #for each location
    count = 0
    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(24, len(temp)): #for the rest... "Present" trials
        if temp[i][0] == j and temp[i][2] <= 3:
            count += 1
            if temp[i][2] == 0:
                count0 += 1
            elif temp[i][2] == 1:
                count1 += 1
            elif temp[i][2] == 2:
                count2 += 1
            elif temp[i][2] == 3:
                count3 += 1
    Data['Present'][j] = {
        'nValid': count,
        'zero': count0,
        'one': count1,
        'two': count2,
        'three': count3,
        'zerop': count0 / count,
        'onep': count1 / count,
        'twop': count2 / count,
        'threep': count3 / count
    }


Data["Complete"] = 1

with open(filePath, "w") as file:
    json.dump(Data, file)
    print("All Trials Completed!")


