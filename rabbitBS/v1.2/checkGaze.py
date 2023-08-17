from psychopy import visual,event
from params import params
from isGazeInsideCircle import isGazeInsideCircle
####Displays green in upper left corner if gaze within field
####Otherise displays red


def checkGaze(env,param,stim,circLoc,win,deg,eye,el_tracker):
    if el_tracker == 0: #hide the fixation helper
        return True
    
    else:
        
        dummymode = True ######## temporary, fix the functions
        if dummymode: #get mouse coords
            mouse = event.Mouse()
            nowCoords = mouse.getPos() 
    
        else:  # we are actually tracking eyes
        # # Main loop for eye tracking
        #     while True:
        #         # Check if new eye data is available
        #         if el_tracker.sampleAvailable():
        #             # Get the newest eye sample
        #             sample = el_tracker.getNewestSample()          
        #             if eye in ["L","l"]:
        #                 nowCoords = tuple(sample.getLeftEye().getGaze())
        #             else:
        #                 nowCoords = tuple(sample.getRightEye().getGaze())
            nowCoords = (0,0) #for now
    
    
        topleft = (-win.size[0]/2, win.size[1]/2)
    
        # draw indicator at top left corner
        if isGazeInsideCircle(nowCoords, env["xCenter"], env["yCenter"], stim["fix_deg_allowed"]):
            dotColor = [0, 255, 0]  # green
            dot = visual.Rect(win,size = 30, color = dotColor, pos = topleft) #modify to indicate upper left hand corner
            dot.draw()
            fix_success = True 
        else:
            dotColor = [255, 0, 0]  # red
            dot = visual.Rect(win,size = 30, color = dotColor, pos = topleft)
            dot.draw()
            fix_success = False
        
        showTrace = False ######temporary fix 
        if showTrace: 
            dotColorTrace = [0.5, 0.5, 0.5]
            stim = visual.Rect(win, size = 10, color = dotColorTrace, pos = (nowCoords)) 
            stim.draw()
        
    
        return fix_success
        #return None
