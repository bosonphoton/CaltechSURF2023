from psychopy import visual, core, event, sound
from params import params
from drawStim import drawStim
from playAudio import playAudio
import json
import copy

def get_input_location(num,win,stim,env):
    # Different response identifier according to different tasks
    
    responded = False
    while not responded:   
        where = 'Where did you see the second flash?\n\n\n'
        if num == 2:
            t1 = "1: Same location as first flash\n\n"
            t2 = '2: Different from the first flash\n\n'  
            drawStim(where+t1+t2, win, stim, env)
            win.flip()
            b = event.waitKeys(timeStamped=True)
            keys2 = [row[0] for row in b]
            
            for key in keys2:
                if key in ['1', 'num_1']:
                    loc = 1
                    responded = True                   
                elif key in ['2', 'num_2']:
                    loc = 2
                    responded = True
                           
          
        elif num == 3: 
            t1 = "1: Same location as first flash\n\n"
            t2 = '2: Between first and last flash\n\n'
            t3 = '3: Same location as last flash'
            drawStim(where+t1+t2+t3, win, stim, env)
            win.flip()
            b = event.waitKeys(timeStamped=True)
            keys2 = [row[0] for row in b]
            
            for key in keys2:
                if key in ['1', 'num_1']:
                    loc = 3
                    responded = True
                elif key in ['2', 'num_2']:
                    loc = 4
                    responded = True
                elif key in ['3', 'num_3']:
                    loc = 5
                    responded = True
    
    return loc