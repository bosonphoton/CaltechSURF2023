from checkGaze import checkGaze
from psychopy import visual
from params import params
from drawStim import drawStim

def fixation_help(env,param,stim,circLoc,win,deg,flag,eye,el_tracker):
    
    showTrace = False
    
    if el_tracker == 0:
        pass
   
    else:
        while not flag:
            fixated = [False] * int(stim["fix_nFrames"]) #creates an array of F
            for iframe in range(int(stim["fix_nFrames"])):
                drawStim("fixation", win, stim, env)
                fix_success = checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                if not fix_success:
                    fix_circle_color = [255, 0, 0] #red
                else:
                    fix_circle_color = [0, 255, 0] #green
    
                fix_circle = visual.Circle(win, stim["fix_deg_allowed"], lineColor=fix_circle_color, lineWidth=stim["fix_circle_width"], fillColor = None)
                fix_circle.draw()
                win.flip()
    
                fixated[iframe] = fix_success
    
            if all(fixated):
                flag = True
                break
    
        showTrace = True
    
        # show fixation for another 200 ms
        for iframe in range(int(stim["nFrames"])):
            drawStim("fixation", win, stim, env)
            checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
            win.flip()
