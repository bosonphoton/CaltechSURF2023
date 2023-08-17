# stops audio playback
# stops eye tracking recording
# retrieves the recorded eye movement data file
# displays the file transfer status
# shuts down the connection to the eye tracker
# closes any open figure windows
# closes screen

from psychopy import core, sound, visual
import os
from params import params
import json
import copy
import pylink

def cleanup(Data,filePath,el_tracker,win):
    
    ######################################################################################################

###COPY FROM GET INPUT
    
    ######################################################################################################
    with open(filePath, "w") as file:
        json.dump(Data, file)
        print("Some Trials Completed")
    
    win.close()
    core.quit()
    

    
    
