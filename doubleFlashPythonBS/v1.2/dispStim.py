from psychopy import core, event, sound, visual
from fixation_help import fixation_help
from params import params
from drawStim import drawStim
from checkGaze import checkGaze
import numpy as np

def dispStim(Xposition,Yposition,env,param,stim,circLoc,win,deg,num_flashes,num_beeps,playBeep,eye,el_tracker):
    showTrace = False

    # Prepare beep here
    if playBeep:
        if num_beeps == 0:
            a = np.zeros((1,9600))
            b = np.zeros((1,9600))
            sound_arr = np.transpose(np.concatenate((a,b)))
            sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
        elif num_beeps == 1:
            ###################################################### EDIT FILL BUFFER ##########################
            a = np.reshape(param["left_singleBeep_array"],(1,9600))
            b = np.reshape(param["right_singleBeep_array"],(1,9600))
            sound_arr = np.transpose(np.concatenate((a,b)))
            sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
        elif num_beeps == 2:
            a = np.reshape(param["left_doubleBeep_array"],(1,9600))
            b = np.reshape(param["right_doubleBeep_array"],(1,9600))
            sound_arr = np.transpose(np.concatenate((a,b)))
            sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
            ###################################################### EDIT FILL BUFFER #########################


    # # Fixation - won't start trial until successful fixation
    # fail_count = 0
    # flag = False
    # while not flag:
    #     fixated = [False] * int(stim["fix_nFrames"])
    #     for iframe in range(int(stim["fix_nFrames"])):
    #         drawStim("fixation", win, stim, env)
    #         fix_success = checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
    #         win.flip()
    #         fixated[iframe] = fix_success
    #     if all(fixated):
    #         flag = True
    #         break
    #     else:
    #         fail_count += 1
    #         if fail_count >= 3:
    #             pass
    #             fixation_help(env,param,stim,circLoc,win,deg,flag)
    
    # Fixation
    for iframe in range(int(stim["fix_nFrames"])):
        drawStim("fixation", win, stim, env)
        #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
        win.flip()


    ######## Actual stimulus ##########
    if num_flashes == 1:
        # Pre-flip, t approx -0.0167
        drawStim("fixation", win, stim, env)
        win.flip()
        clock = core.Clock()
        StimOnsetTimePre = clock.getTime()
        t0 = StimOnsetTimePre + env["ifi"]

        if playBeep:
            sound1.play(when = t0)
        
        for iframe in range(int(stim["nFrames"])):  # 200 ms / 12 frames
            if iframe == 3:
                drawStim("fixation", win, stim, env)                
                # circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(), lineColor=None, fillColor="white")
                # circle.draw()
                circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(Xposition,Yposition), ori = stim['ori'], lineColor=None, fillColor="white")
                circle.draw()
                #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                win.flip()
            else:
                # Fixation for 3 frames before flash
                drawStim("fixation", win, stim, env)
                #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                win.flip()
                
    if num_flashes == 2:
        # Pre-flip, t approx -0.0167
        drawStim("fixation", win, stim, env)
        win.flip()
        clock = core.Clock()
        StimOnsetTimePre = clock.getTime()
        t0 = StimOnsetTimePre + env["ifi"]

        if playBeep:
            sound1.play(when = t0)
        
        for iframe in range(int(stim["nFrames"])):  # 200 ms / 12 frames
            if iframe == 3:
                drawStim("fixation", win, stim, env)                
                # circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(Xposition,Yposition), lineColor=None, fillColor="white")
                # circle.draw()
                circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(Xposition,Yposition),ori = stim['ori'], lineColor=None, fillColor="white")
                circle.draw()
                #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                win.flip()
            if iframe == 6:
                drawStim("fixation", win, stim, env)                
                # circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(Xposition,Yposition), lineColor=None, fillColor="white")
                # circle.draw()
                circle = visual.Rect(win, width = deg["bar_width"] , height=deg["bar_length"], pos=(Xposition,Yposition),ori = stim['ori'], lineColor=None, fillColor="white")
                circle.draw()
                #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                win.flip()
            else:
                # Fixation for 3 frames before flash
                drawStim("fixation", win, stim, env)
                #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
                win.flip()

    else:  # No flash, keep drawing fixation
        clock = core.Clock()
        StimOnsetTimePre = clock.getTime()
        t0 = StimOnsetTimePre + env["ifi"]

        if playBeep:
            sound1.play(when = t0)
            
        for iframe in range(int(stim["nFrames"])):
            drawStim("fixation", win, stim, env)
            #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
            win.flip()

    # Fixation
    for iframe in range(int(stim["fix_nFrames"])):
        drawStim("fixation", win, stim, env)
        #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
        win.flip()
