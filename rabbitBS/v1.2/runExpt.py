from __future__ import division
from __future__ import print_function

from psychopy import visual, core, gui, data,event,sound,monitors
from psychopy.hardware import keyboard
import os
import sys
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
from bsExtraction import bsExtraction

############ Eyelink Stuff ########################
# from psychopy.iohub.client import launchHubServer
# import pylink
# import platform
# import time
# import sys
# from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
# from PIL import Image  # for preparing the Host backdrop image
# from string import ascii_letters, digits
# ########### import rest of functions ############


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
stimshape = "bar" #bar or circle

# Ask for subject details
myDlg = gui.Dlg(title='Input')
myDlg.addField('Initials:')
myDlg.addField('Age and sex (e.g. 23F):')
myDlg.addField('Which eye (L/R):')
myDlg.addField('Glasses (with/without/na):')
myDlg.addField('Show demo? (0/1):')
myDlg.addField('Task (dt/av):') #detection task VS audio-visual
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
if task != 'dt' and task != 'av':
    print("ERROR: Wrong task.")
    core.quit()
    




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


BS = bsExtraction(initials) #Get BlindSpot Data

# initial parameters
env,param,stim,circLoc,win,deg,sequence = params(BS)
win.setMouseVisible(False)


# Configure a graphics environment (genv) for tracker calibration
# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# see the EyeLink Installation Guide, "Customizing Screen Settings"
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



trials, num_catch = genTrials(task)

fileList = os.listdir("C:\\Users\\achan2\\Box\\SURF2023\\rabbitBS\\v1.2\\Data") #checks inside the data
foundFiles = [file for file in fileList if file.startswith(initials) and file.endswith(f'{task}_{eye}_{glasses}.json')]
path1 = os.path.join(os.getcwd(), 'Data', '')

if foundFiles: #check if file exists
    with open(os.path.join(path1,foundFiles[0])) as f:
        Data = json.load(f)
        if Data["Complete"] == 1:
            print("ERROR: Subject did this already.")
            win.close()
            core.quit()
            sys.exit()
        
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
    demo_trials(stimshape,task,env,param,stim,circLoc,win,deg,eye,el_tracker,sequence,filePath,Data)

num_flashes, num_beeps, playBeep, Data = task_master(stimshape, trials,task,env,param,stim,circLoc,win,deg,Data,filePath,eye,el_tracker,sequence)


#DataConditions = [sequence/loc , flash or no flash, response, RT]
    
Data["Conditions"] = [condition + [resp, r] for condition, resp, r in zip(Data["Conditions"], Data["Responses"], Data["RT"])]
cop = copy.deepcopy(Data["Conditions"])
temp = sorted(cop, key=lambda x: x[1]) #sorts arr based on 2nd element, which indicated catch vs normal trials \
print(temp)
    
    
if str(task) =='av': #224 total trials, 64 catch
    Data["Catch"] = [row[-2:] for row in temp[0:num_catch]] #take only the catch trials rows, and only the Resp & RT of each
    for j in range(len(sequence)): #for each sequence
        count = 0
        count0 = 0
        count1 = 0
        count2 = 0
        count3 = 0
        for i in range(num_catch, len(temp)): #for the rest... "Present" trials
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
        
if str(task) =='dt': #216 total trials, 32 catch
    Data["Catch"] = [row[-2:] for row in temp[0:num_catch]] #take only the catch trials rows, and only the Resp & RT of each
    for j in range(len(circLoc)): #for each sequence
        count = 0
        count0 = 0
        count1 = 0
        for i in range(num_catch, len(temp)): #for the rest... "Present" trials
            if temp[i][0] == j and temp[i][2] <= 3:
                count += 1
                if temp[i][2] == 0:
                    count0 += 1
                elif temp[i][2] == 1:
                    count1 += 1

        Data['Present'][j] = {
            'nValid': count,
            'zero': count0,
            'one': count1,
            'zerop': count0 / count,
            'onep': count1 / count,
        }


Data["Complete"] = 1

with open(filePath, "w") as file:
    json.dump(Data, file)
    print("All Trials Completed!")


