from psychopy import visual, core, sound
import numpy as np
import math
import copy

def params():
    # Set up the window
    #win = visual.Window(size=(800, 800), units='pix', color=(-1, -1, -1)) #None for testing purposes) 
    win = visual.Window(fullscr=True, units='pix', color=(-1, -1, -1)) #black scree

    env = {}
    env['screenXpixels'], env['screenYpixels'] = win.size
    env["xCenter"], env["yCenter"] = (0,0)    
    env['frameRate'] = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
    
    if env['frameRate'] is not None:
        env['ifi'] = 1 / env['frameRate']
    else:
        env['ifi'] = 1/60

    param = {}
    param["viewDist"] = 570 * 2
    param['nchannels'] = 2
    param['startCue'] = 0
    param['repetitions'] = 1
    param['waitForDeviceStart'] = 1

    #audio_handle = sound.Sound(value=0, sampleRate=env['sampleRate'], channels=param['nchannels'])
    env['sampleRate'] = sound.AudioDeviceStatus().sampleRate
    param['beepDuration'] = 0.007  # seconds (7 ms)
    param['audioDelay'] = -0.105
    param['beepOneBalance'] = 0.5
    param['beepTwoBalance'] = 0.5
    param['preFlashBeepT'] = 0.023 - param['audioDelay']  # From double flash paper
    param['postFlashBeepT'] = 0.064 - (0.023 - param['audioDelay'])  # From double flash paper

    # flash will begin at t = 50ms
    param['beepOneT'] = 0.170 - param['preFlashBeepT']  # in sec
    param['beepTwoT'] = 0.170 + param['postFlashBeepT']  # in sec
    param['beepOneSamps'] = int(param['beepOneT'] * env['sampleRate'])  # in Hz #ONSET TIME FOR BEEP (BEEP1 START PLAYING)
    param['beepTwoSamps'] = int(param['beepTwoT'] * env['sampleRate'])  # in Hz (BEEP2 START PLAYING)
    
    #############?????###################### Unsure About This ###############################################
    # sin(2*pi*freq*(0:duration*samplingRate-1)/samplingRate)
    param['beep_array'] = np.sin(2 * np.pi * 800 * np.arange(0,param['beepDuration']*env['sampleRate']-1)/env['sampleRate']) #CONVERTS TO SIN WAVE 
    param["beep_samps"] = np.size(param['beep_array']) #How many samples there are in a beep (sample = single datapoint on a sound wave)
    #############?????###################### Unsure About This ###############################################
    
    
    # Entire stimulus is 200 ms long
    param['beep_nSamps'] = int(env['sampleRate'] * 0.200)  # 9600
    param['left_singleBeep_array'] = np.zeros(param['beep_nSamps']) #initialize zeros array for each 200ms stimulus
    param['right_singleBeep_array'] = np.zeros(param['beep_nSamps'])
    
    
    ###############
    #param.left_singleBeep_array(1, param.beepOneSamps:param.beepOneSamps + param.beep_samps - 1) = param.beep_array * (1 - param.beepOneBalance);
    #param.right_singleBeep_array(1, param.beepOneSamps:param.beepOneSamps + param.beep_samps - 1) = param.beep_array * param.beepOneBalance;
    #################
    
    #putting in the sound into the array start:end
    param["left_singleBeep_array"][param["beepOneSamps"]:param["beepOneSamps"] + param["beep_samps"]]  = param["beep_array"] * (1- param["beepOneBalance"]) #last part just splits between two audio channels
    param["right_singleBeep_array"][param["beepOneSamps"]:param["beepOneSamps"] + param["beep_samps"]] = param["beep_array"] * param["beepOneBalance"]

    # add in second beep
    param['left_doubleBeep_array'] = copy.deepcopy(param['left_singleBeep_array'])   
    param['right_doubleBeep_array'] = copy.deepcopy(param['right_singleBeep_array'])
    
    param["left_doubleBeep_array"][param["beepTwoSamps"]:param["beepTwoSamps"] + param["beep_samps"]] = param["beep_array"] * (1 - param["beepTwoBalance"])
    param["right_doubleBeep_array"][param["beepTwoSamps"]:param["beepTwoSamps"] + param["beep_samps"]] = param["beep_array"] * param["beepTwoBalance"]


    # Keys
    ##################

    # eccentricity
    param['eccs'] = 600
    param['shift'] = 0
#     % Screen width:          60 cm = 600 mm
# % Horizontal resolution: 3840
# % pixel size:            600/3840 = 0.1562
# % Viewing distance:      57 cm = 570 mm
# % VA formula:            2 * atand ( size in mm / viewDist*2)

# param.pixSize = 600/env.screenXpixels;
    param["pixSize"] = 600/env['screenXpixels']


    deg = {}
    
    deg['one'] = (math.tan(math.radians(1))/2*param['viewDist'])/param['pixSize']
    deg['two'] = (math.tan(math.radians(2))/2*param['viewDist'])/param['pixSize']
    deg['three'] = (math.tan(math.radians(3))/2*param['viewDist'])/param['pixSize']
    
    deg['five'] = (math.tan(math.radians(5))/2*param['viewDist'])/param['pixSize']
    deg['ten'] = (math.tan(math.radians(10))/2*param['viewDist'])/param['pixSize']
    deg['fifteen'] = (math.tan(math.radians(15))/2*param['viewDist'])/param['pixSize']
    
    deg['five_diag'] = math.sqrt(math.pow(deg['five'], 2)/2)
    deg['ten_diag'] = math.sqrt(math.pow(deg['ten'], 2)/2)
    deg['fifteen_diag'] = math.sqrt(math.pow(deg['fifteen'], 2)/2)



    param["cross"] = [deg["five"], deg["ten"],deg["fifteen"]]
    param["diago"] = [deg["five_diag"], deg["ten_diag"], deg["fifteen_diag"]]

    circLoc = {}

    #################### ???? EDIT THIS ??? #######################################
    for i in range(25):
        #case verticle 
        if i in range(4):
            circLoc[i] = (env["xCenter"], env["yCenter"] - param["cross"][i-1])
            circLoc[i+3] = (env["xCenter"], env["yCenter"] + param["cross"][i-1])
        #case horizon
        if i in range(7,10):
            circLoc[i] = (env["xCenter"] + param["cross"][i-7], env["yCenter"])
            circLoc[i+3] = (env["xCenter"] - param["cross"][i-7], env["yCenter"])
        #case diag
        if i in range(13,16):
            circLoc[i] = (env["xCenter"] + param["diago"][i-13], env["yCenter"] - param["diago"][i-13])
        if i in range(16,19):
            circLoc[i] = (env["xCenter"] - param["diago"][i%3-1], env["yCenter"] + param["diago"][i%3-1])
        if i in range(19,22):
            circLoc[i] = (env["xCenter"] + param["diago"][i%3-1], env["yCenter"] + param["diago"][i%3-1])
        if i in range(22,25):
            circLoc[i] = (env["xCenter"] - param["diago"][i%3-1], env["yCenter"] - param["diago"][i%3-1])
        
        
    # prep visual stimuli
    stim = {}
    stim["duration"] = 0.2  # 200 ms
    stim["nFrames"] = round(stim["duration"] / env["ifi"]) #should be 12
    stim["baseCircle"] = [0, 0, deg["two"], deg["two"]]

    # fixation
    stim["fix_size"] = 50
    stim["fix_lw"] = 10
    stim["fix_X"] = [-stim["fix_size"], stim["fix_size"], 0, 0]
    stim["fix_Y"] = [0, 0, -stim["fix_size"], stim["fix_size"]]
    stim["fix_coords"] = [stim["fix_X"], stim["fix_Y"]]
    stim["fix_dur"] = 1  # in sec
    stim["fix_nFrames"] = round(stim["fix_dur"] / env["ifi"]) #should be 60
    stim["fix_deg_allowed"] = deg["two"]
    stim["fix_circle"] = [env["xCenter"] - stim["fix_deg_allowed"],
                  env["yCenter"] - stim["fix_deg_allowed"],
                  env["xCenter"] + stim["fix_deg_allowed"],
                  env["yCenter"] + stim["fix_deg_allowed"]]
    stim["fix_circle_width"] = 30 
    stim["line_color"] = "white"

    stim["text_size"] = 100

    
    return env,param,stim,circLoc,win,deg

