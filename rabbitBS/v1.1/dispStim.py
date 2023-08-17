from psychopy import core, event, sound, visual
from fixation_help import fixation_help
from params import params
from drawStim import drawStim
from checkGaze import checkGaze
import numpy as np

def dispStim(stimshape,task,XYpositions,env,param,stim,circLoc,win,deg,num_flashes,num_beeps,playBeep,eye,el_tracker,ori):
    
    # if int(ori) in [0,1,8,9]:
    #     orientation = 90
    # elif int(ori) in [2,3,14,15]:
    #     orientation = -45    
    # elif int(ori) in [10,11,6,7]:
    #     orientation = 45
    # else:
    #     orientation = 180
    orientation = ori
    
    showTrace = False

    # Prepare beep here
    if playBeep:
        # Fill buffer
        if num_beeps == 0: 
            a = np.zeros((1,param['beep_nSamps']))
            b = np.zeros((1,param['beep_nSamps']))
            sound_arr = np.transpose(np.concatenate((a,b)))
            sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
        if num_beeps == 1:
            ###################################################### EDIT FILL BUFFER ##########################
            a = np.reshape(param["left_singleBeep_array"],(1,param['beep_nSamps']))
            b = np.reshape(param["right_singleBeep_array"],(1,param['beep_nSamps']))
            sound_arr = np.transpose(np.concatenate((a,b)))
            sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
        elif num_beeps == 2:
            a = np.reshape(param["left_doubleBeep_array"],(1,param['beep_nSamps']))
            b = np.reshape(param["right_doubleBeep_array"],(1,param['beep_nSamps']))
            sound_arr = np.transpose(np.concatenate((a,b)))
            sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
        elif num_beeps == 3:
            a = np.reshape(param["left_tripleBeep_array"],(1,param['beep_nSamps']))
            b = np.reshape(param["right_tripleBeep_array"],(1,param['beep_nSamps']))
            sound_arr = np.transpose(np.concatenate((a,b)))
            sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
            ###################################################### EDIT FILL BUFFER #########################


    # Fixation - won't start trial until successful fixation
    fail_count = 0
    flag = False
    while not flag:
        fixated = [False] * int(stim["fix_nFrames"])
        for iframe in range(int(stim["fix_nFrames"])):
            drawStim("fixation", win, stim, env)
            fix_success = checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
            win.flip()
            fixated[iframe] = fix_success
        if all(fixated):
            flag = True
            break
        else:
            fail_count += 1
            if fail_count >= 3:
                fixation_help(env,param,stim,circLoc,win,deg,flag, eye,el_tracker)

    ######## Actual stimulus ##########
    if num_flashes >= 1: 
        # Pre-flip, t approx -0.0167
        drawStim("fixation", win, stim, env)
        win.flip()
        clock = core.Clock()
        StimOnsetTimePre = clock.getTime()
        t0 = StimOnsetTimePre + env["ifi"]

        if playBeep:
            sound1.play(when = t0)
        
        
        for iframe in range(int(stim["nFrames"])):  # 200 ms / 12 frames
            if str(task) == "av":
                x1 = XYpositions[0][0]
                y1 = XYpositions[0][1]
                x2 = XYpositions[1][0]
                y2 = XYpositions[1][1]
                x3 = XYpositions[2][0]
                y3 = XYpositions[2][1]
                
                ####### accuracy check
                # x3 = XYpositions[0][0]
                # y3 = XYpositions[0][1]
                
                if stimshape == "circle":
                    ####################################### Circle Stim ################################################################
                    if iframe == stim['flashOneFrame']: #present stim on 3,6,9th frame
                        drawStim("fixation", win, stim, env)                
                        circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(x1,y1), lineColor=None, fillColor="white")
                        circle.draw()
                        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                        win.flip()
                    # if iframe == 6: #present stim on 3,6,9th frame
                    #     drawStim("fixation", win, stim, env)                
                    #     circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(x2,y2), lineColor=None, fillColor="white")
                    #     circle.draw()
                    #     checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                    #     win.flip()
                    if iframe == stim['flashTwoFrame']: #present stim on 3,6,9th frame
                        drawStim("fixation", win, stim, env)                
                        circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(x3,y3), lineColor=None, fillColor="white")
                        circle.draw()
                        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                        win.flip()            
                    else:
                        # Fixation for 3 frames before flash
                        drawStim("fixation", win, stim, env)
                        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                        win.flip()

                    ####################################### Circle Stim ################################################################
                
                elif stimshape == "bar":
                    ####################################### Bar Stim ################################################################
                    if iframe == stim['flashOneFrame']: #present stim on 3,6,9th frame
                        drawStim("fixation", win, stim, env)
                        circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(x1,y1), lineColor=None, fillColor="white", ori = orientation)
                        circle.draw()
                        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                        win.flip()
                    # if iframe == 6: #present stim on 3,6,9th frame
                    #     drawStim("fixation", win, stim, env)                
                    #     circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(x1,y1), lineColor=None, fillColor="white")
                    #     circle.draw()
                    #     checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                    #     win.flip()
                    if iframe == stim['flashTwoFrame']: #present stim on 3,6,9th frame
                        drawStim("fixation", win, stim, env)                
                        circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(x3,y3), lineColor=None, fillColor="white", ori = orientation)
                        circle.draw()
                        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                        win.flip()            
                    else:
                        # Fixation for 3 frames before flash
                        drawStim("fixation", win, stim, env)
                        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                        win.flip()
                        
            else: #if task is detection task
                x1 = XYpositions[0]
                y1 = XYpositions[1]
                if iframe == 3: #present stim on 3rd frame
                    drawStim("fixation", win, stim, env)  
                    if stimshape == "circle":
                        circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(x1,y1), lineColor=None, fillColor="white")
                    else:
                        circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(x1,y1), lineColor=None, fillColor="white", ori = orientation)
                    circle.draw()
                    checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                    win.flip()     
                else:
                    # Fixation for 3 frames before flash
                    drawStim("fixation", win, stim, env)
                    checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                    win.flip()
                    ####################################### Bar Stim ################################################################
                    


    else:  # No flash, keep drawing fixation
        for iframe in range(int(stim["nFrames"])):
            drawStim("fixation", win, stim, env)
            checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
            win.flip()

    # Fixation
    for iframe in range(int(stim["fix_nFrames"])):
        drawStim("fixation", win, stim, env)
        checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
        win.flip()
        