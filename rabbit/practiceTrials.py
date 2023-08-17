# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:12:45 2023

@author: achan2
"""

from psychopy import visual, event, core
from drawStim import drawStim
from playAudio import playAudio
from checkGaze import checkGaze
from dispStim import dispStim
from get_input import get_input
from params import params
from cleanup import cleanup
from isGazeInsideCircle import isGazeInsideCircle
import random


def practiceTrials(stimshape,trials,task,env,param,stim,circLoc,win,deg,Data,filePath,eye,el_tracker,sequence):
    
    flashes_list = [1] * 12
    beeps_list =  random.choices([0, 1, 2, 3], [3, 3, 3, 3], k=12)
    playBeep = True

    # Wait for key press to begin experiment
    line1 = 'Begin practice trials \n\n'
    line2 = 'Press any key to continue.'
    
    drawStim(line1 + line2, win, stim, env)
    win.flip()
    event.waitKeys()

    # Start showing stimuli
    core.wait(1)
    
    for n in range(11):
        print("Practice trial: " + str(n))
        responded = False
        while not responded:
            checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
            a = event.waitKeys(timeStamped=True)
            keys = [row[0] for row in a]
            secs = [row[1] for row in a][-1]
            for key in keys:
                if key in ['escape', 'q']:
                    cleanup(Data,filePath)
                  
            XYpositions = sequence[Data["Conditions"][n][0]] #((x,y),(x2,y2),(x3,y3))
            ori = sequence[Data["Conditions"][n][0]][3]
            

            num_flashes = flashes_list[n]
            num_beeps = beeps_list[n]
            
            ###### accuracy check
            # num_beeps = 3
            # num_flashes = 2

            dispStim(stimshape, task,XYpositions,env,param,stim,circLoc,win,deg,num_flashes,num_beeps,playBeep,eye,el_tracker,ori)

            # Response
            t0 = core.getTime()  # get RT
            num,secs,responded = get_input(env,param,stim,circLoc,win,deg,task,responded,Data,filePath)
            if num_beeps == 0 and num != 0:
                reminder = "Please respond to number of flashes only"
                drawStim(reminder,win,stim,env)
                win.flip()
    
    
    end = 'End of practice trials\n'
    drawStim(ends, win, stim, env)
    win.flip()   
    event.waitKeys()
    
    return num_flashes,num_beeps,playBeep,Data