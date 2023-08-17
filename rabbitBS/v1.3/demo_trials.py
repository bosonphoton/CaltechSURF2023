from psychopy import visual, core, event, sound
from drawStim import drawStim
from params import params
from playAudio import playAudio
from checkGaze import checkGaze
import numpy as np
import copy
from get_input import get_input
import random
from dispStim import dispStim

def demo_trials(stimshape,task,env,param,stim,circLoc,win,deg,eye,el_tracker,sequence,filePath,Data):
    showTrace = False
    
    while not event.getKeys(): 
        line1 = 'Please keep your eyes on the\n\n fixation cross AT ALL TIMES\n\n throughout experiment'
        drawStim(line1, win, stim, env)
        #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
        win.flip()

    core.wait(0.2)  # so it doesn't return true immediately
    while not event.getKeys():
        drawStim("fixation", win, stim, env)
        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
        win.flip()
        
    # First show flash
    core.wait(0.2)  # so it doesn't return true immediately
    while not event.getKeys():
        line1 = 'For the following experiment\n\n '
        line2 = 'you will see the following flash(es)\n\n'
        line3 = "left and right of fixation cross\n"
        drawStim(line1 + line2 + line3, win, stim, env)
        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
        win.flip()

    core.wait(0.2)
    while not event.getKeys():
        if stimshape =="circle":
            drawStim("flash", win, stim, env)
        else: 
            circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(0,0), lineColor=None, fillColor="white")
            circle.draw()
        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
        win.flip()

    # Second show beep
    if str(task) == "av":
        drawStim('You will also hear beep(s) like this', win, stim, env)
        win.flip()
        event.waitKeys()
        sound1 = sound.Sound(value=param['beep_array'],sampleRate=env['sampleRate'],volume = 1,stereo = True)
        
        win.flip()
        clock = core.Clock()
        StimOnsetTimePre = clock.getTime()
        t0 = StimOnsetTimePre + env['ifi']
        # core.wait(1)
        sound1.play(when = t0)
        core.wait(1)

        drawStim('Make sure to only report the\n\n number of FLASHES you SEE', win, stim, env)
        win.flip()
        event.waitKeys()
        # core.wait(1)
        win.flip()
        core.wait(1)
    
    # Third play beep that indicates question prompt
    drawStim('The following tone indicates that it is time to respond', win, stim, env)
    win.flip()
    event.waitKeys()
    # core.wait(1)
    win.flip()
    playAudio('resp', env) 
    core.wait(1)
    
    if str(task) == 'av':
        flashes_list = [1] * 12
        beeps_list =  random.choices([0, 1, 2, 3], [3, 3, 3, 3], k=12)
        playBeep = True

        # Wait for key press to begin experiment
        line1 = 'Begin practice trials \n\n'
        line2 = 'Press any key to continue.'
        
        drawStim(line1 + line2, win, stim, env)
        win.flip()
        event.waitKeys()
        
        for n in range(11):
            responded = False
            while not responded:
                print("Practice trial: " + str(n))                  
                checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                ran = np.random.randint(9) 
                XYpositions = sequence[ran] #((x,y),(x2,y2),(x3,y3))
                ori = sequence[ran][3]
                num_flashes = flashes_list[n]
                num_beeps = beeps_list[n]
    
                dispStim(stimshape, task,XYpositions,env,param,stim,circLoc,win,deg,num_flashes,num_beeps,playBeep,eye,el_tracker,ori)
    
                # Response
                num,secs,responded = get_input(env,param,stim,circLoc,win,deg,task,responded,Data,filePath)
                if num_beeps == 0 and num == 0:
                    rem = "Please report only number\n\n of FLASHES you see"
                    drawStim(rem,win,stim,env)
                    win.flip()
                    event.waitKeys()
            
    
        
        end = 'End of practice trials\n'
        drawStim(end, win, stim, env)
        win.flip()   
        event.waitKeys()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
