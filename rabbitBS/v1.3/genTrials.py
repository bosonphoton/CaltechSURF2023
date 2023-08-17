from psychopy import core
import random

#generates random trials for experiements

def genTrials(task): #10L + 10R + 2catchL + 2catchR
    if str(task) == "dt": #detection task
        nRep = 5
        normalTrial = 1 #1 flash
        nLoc = 10
        numcatchTrials = 2
        catch = 0 #0 flash
        num_catch = numcatchTrials*nLoc
    
    if str(task) == "av": #40L + 40R + 16catchL + 16catchR = 112 trials 
        nRep = 5
        nLoc = 8 
        numcatchTrials = 2
        normalTrial = 3 #2 flashes 3 beeps 
        catch1 = 0 #2 flash 0 beep
        catch2 = 2 #2 flash 2 beep
        num_catch = numcatchTrials*nLoc*2
        
    trialspr = []

    for i in range(nLoc):
        for j in range(nRep):
            trialspr.append([i, normalTrial])  # Determine location
            
    if str(task) == "dt":
        for i in range(nLoc):
            for j in range(numcatchTrials):
                trialspr.append([i, catch])
    
    if str(task) == "av":
        for i in range(nLoc):
            for j in range(2):
                trialspr.append([i, catch1]) #one catch for 0 beeps
                trialspr.append([i, catch2]) #one catch for 2 beeps
            
    
    # Shuffle trials
    random.shuffle(trialspr)

    
    return trialspr, num_catch
