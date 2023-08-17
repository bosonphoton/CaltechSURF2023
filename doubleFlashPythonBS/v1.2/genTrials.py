from psychopy import core
import random

#generates random trials for experiements

def genTrials(task,env,param,stim,circLoc,win,deg):
    if str(task) == "vf":
        nRep = 5
        normalTrial = 1 #1 flash
        catchTrial = 0 #0 flash
        
        # Create trials
        nLoc = 6
        trialspr = []

        for i in range(nLoc):
            for j in range(nRep):
                trialspr.append([i, normalTrial])  # Determine location
        # Append catch trials
        for i in range(nLoc):
            for j in range(2): #2 catch trials
                trialspr.append([i, catchTrial])

        # Shuffle trials
        random.shuffle(trialspr)

        return trialspr
    
        
    elif str(task) == "bdf":
        nRep = 5
        nLoc = 6 # 0 = left, 1 = right
        zeroFlash = 0
        oneFlash = 1 #normal 2b1f
        twoFlash = 2
        oneBeep = 1
        twoBeep = 2 #normal 2b1f
        zeroBeep = 0
        catch = 0
        normal = 1
        
        trialspr = [] #[L/R, catch or not, num_flashes, num_beeps]
        
        for i in range(nLoc): #normal
            for j in range(nRep):
                trialspr.append([i, normal, oneFlash, twoBeep])
        
        # Append catch trials
        for i in range(nLoc):
            for j in range(2):
                trialspr.append([i, catch, zeroFlash, oneBeep])
                trialspr.append([i, catch, zeroFlash, twoBeep])
                trialspr.append([i, catch, oneFlash, oneBeep])
                trialspr.append([i, catch, twoFlash, oneBeep])
                trialspr.append([i, catch, twoFlash, twoBeep])
                trialspr.append([i, catch, oneFlash, zeroBeep])
                trialspr.append([i, catch, twoFlash, zeroBeep])
                trialspr.append([i, catch, zeroFlash, zeroBeep])
        
        random.shuffle(trialspr)
        
        return trialspr
        
    
    else:
        print("ERROR: Wrong task.")
        core.quit()
        
    
