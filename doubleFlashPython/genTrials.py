from psychopy import core
import random

#generates random trials for experiements

def genTrials(task,env,param,stim,circLoc,win,deg):
    if str(task) == "vf":
        nRep = 5
        normalTrial = 1 #1 flash
        catchTrial = 0 #0 flash
        
    elif str(task) == "bdf":
        nRep = 10
        normalTrial = 2 #1 flash
        catchTrial = 1 #0 flash
    
    else:
        print("ERROR: Wrong task.")
        core.quit()
        

    # Create trials
    nLoc = 24
    trialspr = []

    for i in range(nLoc):
        for j in range(nRep):
            trialspr.append([i, normalTrial])  # Determine location
    # Append catch trials
    for i in range(nLoc):
        trialspr.append([i, catchTrial])

    # Shuffle trials
    random.shuffle(trialspr)

    return trialspr