from psychopy import visual, core, sound
import numpy as np
import math
import copy

def params():
    # Set up the window
    #win = visual.Window(size=(800, 800), units='pix', color=(-1, -1, -1)) #None for testing purposes) 
    win = visual.Window(size = (3840,2160),fullscr=True, units='pix', color=(-1, -1, -1)) #black scree


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
    
    
    env['sampleRate'] = sound.AudioDeviceStatus().sampleRate #48000Hz aka number of samples in one second
    param['beepDuration'] = 0.007  # seconds (7 ms)
    param['audioDelay'] = -0.115 # in ms
    param['audioDelaySamps'] = int(param['audioDelay'] * env['sampleRate']) # in Hz
    param['beepOneBalance'] = 0.5
    param['beepTwoBalance'] = 0.5
    param['beepGap'] = 0.10 # 58 ms on paper
    
    param['preFlashTiming'] = 0.023 - param['audioDelay']
    param['postFlashTiming'] = param['beepDuration'] + param['beepGap'] - param['preFlashTiming']
    
    param['beepOneT'] = 0.170 - param['preFlashTiming']
    param['beepTwoT'] = 0.170 + param['postFlashTiming']
    param['beepThreeT'] = 0.170 + param['beepDuration'] + param['beepGap'] + param['postFlashTiming']
   
    beepOneSamps = int(param['beepOneT'] * env['sampleRate'])  # in Hz #ONSET TIME FOR BEEP (BEEP1 START PLAYING)
    beepTwoSamps = int(param['beepTwoT'] * env['sampleRate'])  # in Hz (BEEP2 START PLAYING)
    beepThreeSamps = int(param['beepThreeT'] * env['sampleRate'])   


    param['beep_array'] = np.sin(2 * np.pi * 800 * np.arange(0,param['beepDuration']*env['sampleRate']-1)/env['sampleRate']) #CONVERTS BEEP TO SIN WAVE = 335 samples per beeps
    param["beep_samps"] = np.size(param['beep_array']) #7 ms beep = array of 335 elements 

    # start time in ms
    # beepOneStartT = 0 - param['audioDelay']
    # beepTwoStartT = param['beepDuration'] + param['beepGap'] - param['audioDelay']
    # beepThreeStartT = param['beepDuration']*2 + param['beepGap']*2 - param['audioDelay']
    
    # start time in Hz
    # beepOneStartSamps = int(beepOneStartT * env['sampleRate'])
    # beepTwoStartSamps = int(beepTwoStartT * env['sampleRate'])
    # beepThreeStartSamps = int(beepThreeStartT * env['sampleRate'])
    
    # Entire stimulus is 200 ms long
    param['beep_nSamps'] = int(env['sampleRate'] * 0.300)  # 9600 samples in entire stimulus
    param['left_singleBeep_array'] = np.zeros(param['beep_nSamps']) #initialize zeros array for each 200ms stimulus
    param['right_singleBeep_array'] = np.zeros(param['beep_nSamps'])
    
    
    ###############
    #param.left_singleBeep_array(1, param.beepOneSamps:param.beepOneSamps + param.beep_samps - 1) = param.beep_array * (1 - param.beepOneBalance);
    #param.right_singleBeep_array(1, param.beepOneSamps:param.beepOneSamps + param.beep_samps - 1) = param.beep_array * param.beepOneBalance;
    #################
    
    #putting in the sound into the array start:end
    param["left_singleBeep_array"][beepOneSamps:beepOneSamps + len(param["beep_array"])] = param["beep_array"] * (1- param["beepOneBalance"]) #last part just splits between two audio channels
    param["right_singleBeep_array"][beepOneSamps:beepOneSamps + len(param["beep_array"])] = param["beep_array"] * param["beepOneBalance"]

    # add in second beep
    param['left_doubleBeep_array'] = copy.deepcopy(param['left_singleBeep_array'])   
    param['right_doubleBeep_array'] = copy.deepcopy(param['right_singleBeep_array'])
    
    param["left_doubleBeep_array"][beepTwoSamps:beepTwoSamps + len(param["beep_array"])]= param["beep_array"] * (1 - param["beepTwoBalance"])
    param["right_doubleBeep_array"][beepTwoSamps:beepTwoSamps + len(param["beep_array"])] = param["beep_array"] * param["beepTwoBalance"]

    # add in third beep
    param['left_tripleBeep_array'] = copy.deepcopy(param["left_doubleBeep_array"])
    param['right_tripleBeep_array'] = copy.deepcopy(param["right_doubleBeep_array"])
    
    param['left_tripleBeep_array'][beepThreeSamps:beepThreeSamps + len(param["beep_array"])] =  param["beep_array"] * (1- param["beepOneBalance"])
    param['right_tripleBeep_array'][beepThreeSamps:beepThreeSamps + len(param["beep_array"])] =  param["beep_array"] * param["beepOneBalance"]

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
    deg['one_42'] = (math.tan(math.radians(1.42))/2*param['viewDist'])/param['pixSize'] #1.42 degrees 
    deg["one"] = (math.tan(math.radians(1))/2*param['viewDist'])/param['pixSize']
    deg['two'] = (math.tan(math.radians(2))/2*param['viewDist'])/param['pixSize'] 
    deg['bar_width'] = (math.tan(math.radians(0.28))/2*param['viewDist'])/param['pixSize']
    deg['bar_length'] = (math.tan(math.radians(1.2))/2*param['viewDist'])/param['pixSize']
    # deg['five'] = (math.tan(math.radians(5))/2*param['viewDist'])/param['pixSize']
    # deg['ten'] = (math.tan(math.radians(10))/2*param['viewDist'])/param['pixSize']
    deg['fifteen'] = (math.tan(math.radians(15))/2*param['viewDist'])/param['pixSize']
    deg['fourteen'] = (math.tan(math.radians(14))/2*param['viewDist'])/param['pixSize']
    deg['sixteen'] = (math.tan(math.radians(16))/2*param['viewDist'])/param['pixSize']
    
    deg['one_diag'] = math.sqrt(math.pow(deg['one_42'], 2)/2)
    # deg['five_diag'] = math.sqrt(math.pow(deg['five'], 2)/2)
    # deg['ten_diag'] = math.sqrt(math.pow(deg['ten'], 2)/2)
    # deg['fifteen_diag'] = math.sqrt(math.pow(deg['fifteen'], 2)/2)

# if int(ori) in [0,1,8,9]: #horizontal
#     orientation = 90
# elif int(ori) in [2,3,14,15]: #-45
#     orientation = -45    
# elif int(ori) in [10,11,6,7]: #45
#     orientation = 45
# else:
#     orientation = 180 # vertical


    circLoc = {} #starts from N going clockwise 8 positions
    #For right eye
    circLoc[0] = (env["xCenter"] + deg['fifteen'], env["yCenter"] + deg['one_42'],90)
    circLoc[1] = (env["xCenter"] + deg['fifteen'] + deg['one_diag'], env["yCenter"] + deg['one_diag'],-45)
    circLoc[2] = (env["xCenter"] + deg['sixteen'], env["yCenter"],180)
    circLoc[3] = (env["xCenter"] + deg['fifteen'] + deg['one_diag'], env["yCenter"] - deg['one_diag'],45)
    circLoc[4] = (env["xCenter"] + deg['fifteen'], env["yCenter"] - deg['one_42'], 90)
    circLoc[5] = (env["xCenter"] + deg['fifteen'] - deg['one_diag'], env["yCenter"] - deg['one_diag'],-45 )
    circLoc[6] = (env["xCenter"] + deg['fourteen'], env["yCenter"], 180)
    circLoc[7] = (env["xCenter"] + deg['fifteen'] - deg['one_diag'], env["yCenter"] + deg['one_diag'], 45)
    #For left eye
    circLoc[8] = (env["xCenter"] - deg['fifteen'], env["yCenter"] + deg['one_42'], 90)
    circLoc[9] = (env["xCenter"] - deg['fifteen'] - deg['one_diag'], env["yCenter"] + deg['one_diag'],45)
    circLoc[10] = (env["xCenter"] - deg['sixteen'], env["yCenter"],180)
    circLoc[11] = (env["xCenter"] - deg['fifteen'] - deg['one_diag'], env["yCenter"] - deg['one_diag'],-45)
    circLoc[12] = (env["xCenter"] - deg['fifteen'], env["yCenter"] - deg['one_42'],90)
    circLoc[13] = (env["xCenter"] - deg['fifteen'] + deg['one_diag'], env["yCenter"] - deg['one_diag'],45)
    circLoc[14] = (env["xCenter"] - deg['fourteen'], env["yCenter"],180)
    circLoc[15] = (env["xCenter"] - deg['fifteen'] + deg['one_diag'], env["yCenter"] + deg['one_diag'],-45)    
    
    circLoc[16] = (env["xCenter"] - deg['fifteen'], env["yCenter"],180) # blind left
    circLoc[17] = (env["xCenter"] + deg['fifteen'], env["yCenter"],180) # blind right
    
    
    
    ########################################  REAL BLINDSPOTS  ##########################################################  TO DO: EDIT THE DIAGONALS (1,3,5,7) (15,13,11,9)!!!!!!
    #epsilon =  deg['one'] # just to make sure it is beyond blindspot

    #For right eye (starts at (0,1) going clockwise)
    # circLoc[0] = (BS['rightBS_center'][0], BS['rightBS_center'][1] + (BS['rightBS_y'] + epsilon),90)
    # circLoc[1] = (BS['rightBS_center'][0]  + deg['one_diag'], env["yCenter"] + deg['one_diag'],-45)
    # circLoc[2] = (BS['rightBS_center'][0] + BS['rightBS_x'] + epsilon, BS['rightBS_center'][1],180)
    # circLoc[3] = (BS['rightBS_center'][0]  + deg['one_diag'], env["yCenter"] - deg['one_diag'],45)
    # circLoc[4] = (BS['rightBS_center'][0], (BS['rightBS_center'][1] - (BS['rightBS_y'] + epsilon)), 90)
    # circLoc[5] = (BS['rightBS_center'][0] - deg['one_diag'], env["yCenter"] - deg['one_diag'],-45 )
    # circLoc[6] = (BS['rightBS_center'][0] - (BS['rightBS_x'] + epsilon), BS['rightBS_center'][1], 180)
    # circLoc[7] = (BS['rightBS_center'][0] - deg['one_diag'], env["yCenter"] + deg['one_diag'], 45)
    
    # #For left eye (going counterclockwise)
    # circLoc[8] = (BS['leftBS_center'][0], BS['leftBS_center'][1] + (BS['leftBS_y'] + epsilon), 90)
    # circLoc[9] = (BS['leftBS_center'][0]  - deg['one_diag'], BS['leftBS_center'][1] + deg['one_diag'],45)
    # circLoc[10] = (BS['leftBS_center'][0] - (BS['leftBS_x'] + epsilon), BS['leftBS_center'][1],180)
    # circLoc[11] = (BS['leftBS_center'][0]  - deg['one_diag'], env["yCenter"] - deg['one_diag'],-45)
    # circLoc[12] = (BS['leftBS_center'][0], BS['leftBS_center'][1] - (BS['leftBS_y'] + epsilon), 90)
    # circLoc[13] = (BS['leftBS_center'][0]  + deg['one_diag'], env["yCenter"] - deg['one_diag'],45)
    # circLoc[14] = (BS['leftBS_center'][0] + (BS['leftBS_x'] + epsilon), BS['leftBS_center'][1] ,180)
    # circLoc[15] = (BS['leftBS_center'][0]  + deg['one_diag'], env["yCenter"] + deg['one_diag'],-45)        
    
    # circLoc[16] = (BS['leftBS_center'],180) # blind left
    # circLoc[17] = (BS['rightBS_center'],180) # blind right    
    
    #####################################################################################################################
    
    
    sequence ={}
    stim = {}
    stim["blind_left"] = (env["xCenter"] - deg['fifteen'], env["yCenter"]) #replace with users blind spots
    stim["blind_right"] = (env["xCenter"] + deg['fifteen'], env["yCenter"]) #replace with users blind spots
    
    ############# (flashOnePos, BSpos, flashTwopos, ori)
    sequence[0] = (circLoc[0], stim["blind_right"], circLoc[4], circLoc[0][2]) #horiz
    sequence[1] = (circLoc[4], stim["blind_right"], circLoc[0], circLoc[0][2]) #horiz
    sequence[2] = (circLoc[1], stim["blind_right"], circLoc[5], circLoc[5][2]) #-45
    sequence[3] = (circLoc[5], stim["blind_right"], circLoc[1], circLoc[1][2]) #-45
    sequence[4] = (circLoc[6], stim["blind_right"], circLoc[2], circLoc[2][2]) 
    sequence[5] = (circLoc[2], stim["blind_right"], circLoc[6], circLoc[6][2])
    sequence[6] = (circLoc[7], stim["blind_right"], circLoc[3], circLoc[3][2]) #+45
    sequence[7] = (circLoc[3], stim["blind_right"], circLoc[7], circLoc[7][2]) #+45

    sequence[8] = (circLoc[8], stim["blind_left"], circLoc[12], circLoc[12][2]) #horiz
    sequence[9] = (circLoc[12], stim["blind_left"], circLoc[8], circLoc[8][2]) #horiz
    sequence[10] = (circLoc[9], stim["blind_left"], circLoc[13], circLoc[13][2]) #+45
    sequence[11] = (circLoc[13], stim["blind_left"], circLoc[9], circLoc[9][2]) #+45
    sequence[12] = (circLoc[10], stim["blind_left"], circLoc[14], circLoc[14][2])
    sequence[13] = (circLoc[14], stim["blind_left"], circLoc[10], circLoc[10][2])
    sequence[14] = (circLoc[11], stim["blind_left"], circLoc[15], circLoc[15][2]) #-45
    sequence[15] = (circLoc[15],stim["blind_left"], circLoc[11], circLoc[11][2]) #-45

    
    # prep visual stimuli
    stim["duration"] = 0.2  # 200 ms
    
    stim["nFrames"] = round(stim["duration"] / env["ifi"]) #should be 12
    #stim["baseCircle"] = [0, 0, deg["two"], deg["two"]]
    stim["baseCircle"] = [0, 0, deg["two"]*2, 2*deg["two"]]
    stim['flashOneFrame'] = 3
    stim['flashTwoFrame'] = 11

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
    
    stim[0] = stim["blind_left"]
    stim[1] = stim["blind_right"]

    

    
    return env,param,stim,circLoc,win,deg,sequence

