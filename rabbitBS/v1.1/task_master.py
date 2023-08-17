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

def task_master(stimshape,trials,task,env,param,stim,circLoc,win,deg,Data,filePath,eye,el_tracker,sequence):
    
    if task == "dt":  # detection flash
        flashes_list = [trial[1] for trial in Data["Conditions"]]
        beeps_list = [0] * len(trials)
        playBeep = False

    elif task == "av":  # audio visual
        flashes_list = [1] * len(trials)
        beeps_list =  [trial[1] for trial in Data["Conditions"]]
        playBeep = True

    # Wait for key press to begin experiment
    line1 = 'The experiment will begin as soon as you are ready\n\n'
    line2 = 'Press any key to continue.'
    
    drawStim(line1 + line2, win, stim, env)
    win.flip()
    event.waitKeys()


    # Start showing stimuli
    core.wait(1)
    
    for n in range(len(Data["Responses"]),len(trials)):
        print("n trial" + str(n))
        responded = False
        while not responded:
            checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker)
            if n % 20 == 0 and n != 0:  # break every 20 trials
                leftover = len(trials) - n
                l1 = 'Please take a break if needed\n'
                l2 = '\n Press any key to continue\n'
                l3 = f'\n{leftover} more trials to go'
                drawStim(l1 + l2 + l3, win, stim, env)
                win.flip()
                playAudio('break', env)
                a = event.waitKeys(timeStamped=True)
                keys = [row[0] for row in a]
                secs = [row[1] for row in a][-1]
                for key in keys:
                    if key in ['escape', 'q']:
                        cleanup(Data,filePath)
                  
            if str(task) == "av":
                XYpositions = sequence[Data["Conditions"][n][0]] #((x,y),(x2,y2),(x3,y3))
                ############### accuracy check
                # XYpositions = sequence[Data["Conditions"][0][0]]
                ori = sequence[Data["Conditions"][n][0]][3]
                
                #XYpositions = (())
                print("POSITIONS" + str(XYpositions))
                
            elif str(task) == "dt":
                XYpositions = circLoc[Data["Conditions"][n][0]] # stim[0] is left eye, stim[1] is right eye                
                ori = XYpositions[2]
                print(ori)

            num_flashes = flashes_list[n]
            num_beeps = beeps_list[n]
            
            ###### accuracy check
            # num_beeps = 3
            # num_flashes = 2

            dispStim(stimshape, task,XYpositions,env,param,stim,circLoc,win,deg,num_flashes,num_beeps,playBeep,eye,el_tracker,ori)

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
    
    
    