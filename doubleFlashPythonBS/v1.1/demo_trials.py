from psychopy import visual, core, event, sound
from drawStim import drawStim
from params import params
from playAudio import playAudio
from checkGaze import checkGaze
import numpy as np
import copy

def demo_trials(task,env,param,stim,circLoc,win,deg):
    showTrace = True
    
    # Draw fixation################################ Debug
    # drawStim("fixation", win, stim, env)
    # win.flip()
    # t0 = core.getTime()
    #############################################
    
    while not event.getKeys(): 
        drawStim("fixation", win, stim, env)
        #fix_success = checkGaze(env,param,stim,circLoc,win,deg)
        win.flip()
        # t1 = core.getTime()
        # print("TIME DELAY" + str(t1-t0))
        # t0 = copy.deepcopy(t1)
    
    # First show flash
    core.wait(0.2)  # so it doesn't return true immediately
    while not event.getKeys():
        line1 = 'For the following experiment '
        line2 = 'you will see flash(es) like this.'
        drawStim(line1 + line2, win, stim, env)
        #checkGaze(env,param,stim,circLoc,win,deg)
        win.flip()

    core.wait(0.2)
    while not event.getKeys():
        drawStim("flash", win, stim, env)
        #checkGaze(env,param,stim,circLoc,win,deg)
        win.flip()

    # Second show beep
    if str(task) == "bdf":
        drawStim('You will also hear beep(s) like this.', win, stim, env)
        win.flip()
        core.wait(1)
        event.waitKeys()

        ############# PsychPortAudio('FillBuffer', env.audio_handle, [param.left_singleBeep_array; param.right_singleBeep_array]);
        a = np.reshape(param["left_singleBeep_array"],(1,9600))
        b = np.reshape(param["right_singleBeep_array"],(1,9600))
        sound_arr = np.transpose(np.concatenate((a,b)))
        sound1 = sound.Sound(value=sound_arr,sampleRate=env['sampleRate'],volume = 1,stereo = True)
        
        win.flip()
        clock = core.Clock()
        StimOnsetTimePre = clock.getTime()
        t0 = StimOnsetTimePre + 0.016777
        core.wait(1)
        sound1.play(when = t0)
        core.wait(1)

    # Third play beep that indicates question prompt
    drawStim('The following tone indicates that it is time to respond', win, stim, env)
    win.flip()
    event.waitKeys()
    core.wait(1)
    win.flip()
    playAudio('resp', env) 
    core.wait(1)
