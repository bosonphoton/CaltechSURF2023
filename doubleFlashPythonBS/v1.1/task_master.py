# Script for BOTH visual flash detection AND double flash tasks
from psychopy import visual, event, core
from drawStim import drawStim
from playAudio import playAudio
from checkGaze import checkGaze
from dispStim import dispStim
from get_input import get_input
from params import params
from cleanup import cleanup
from isGazeInsideCircle import isGazeInsideCircle

def task_master(trials,task,env,param,stim,circLoc,win,deg,Data,filePath,eye,el_tracker):
    
    if task == "vf":  # Visual flash detection
        flashes_list = [trial[1] for trial in Data["Conditions"]]
        beeps_list = [0] * len(trials)
        playBeep = False

    elif task == "bdf":  # Double flash
        flashes_list = [trial[2] for trial in Data["Conditions"]]
        beeps_list =  [trial[3] for trial in Data["Conditions"]]
        playBeep = True

    # Wait for key press to begin experiment
    line1 = 'The experiment will begin as soon as you are ready\n\n'
    line2 = 'Press any key to continue.'
    
    drawStim(line1 + line2, win, stim, env)
    win.flip()
    event.waitKeys()


    # Start showing stimuli
    core.wait(1)
    win.mouseVisible = False
    
    for n in range(len(Data["Responses"]),len(trials)):
        print("n trial" + str(n))
        responded = False
        while not responded:
            #checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
            if n % 20 == 0 and n != 0:  # break every 20 trials
                l1 = 'Please take a break if needed\n'
                l2 = '\n Press any key to continue'
                drawStim(l1 + l2, win, stim, env)
                win.flip()
                playAudio('break', env)
                a = event.waitKeys(timeStamped=True)
                keys = [row[0] for row in a]
                secs = [row[1] for row in a][-1]
                for key in keys:
                    if key in ['escape', 'q']:
                        cleanup(Data,filePath, el_tracker) #EDIT 
                  
            if task == "vf":
                Xposition = circLoc[Data["Conditions"][n][0]][0]
                Yposition = circLoc[Data["Conditions"][n][0]][1]
                
                print("POSITIONS" + str(Xposition)  + " " + str(Yposition))
            else:
                Xposition = stim[Data["Conditions"][n][0]][0]
                Yposition = stim[Data["Conditions"][n][0]][1]
                # Xposition = stim[0][0]
                # Yposition = stim[0][1]
                

            num_flashes = flashes_list[n]
            num_beeps = beeps_list[n]
            # num_flashes = 2
            # num_beeps = 2

            dispStim(Xposition,Yposition,env,param,stim,circLoc,win,deg,num_flashes,num_beeps,playBeep,eye,el_tracker)

            # Response
            t0 = core.getTime()  # get RT
            num,secs,responded = get_input(env,param,stim,circLoc,win,deg,task,responded,Data,filePath)
            Data["Responses"].append(num)  #stores key response into data struc
            Data["RT"].append(secs - t0) 
    
    
    a = 'You are now finished with this run.\n'
    b = '\n Please ring the bell and notify the experimenter. '
    c = '\n\n Thank you for your time! '
    d = ''

    drawStim(a+b+c+d, win, stim, env)
    win.flip()
    playAudio('outro',env)
    event.waitKeys()
    win.close()
    
    return num_flashes,num_beeps,playBeep,Data
    
    
    