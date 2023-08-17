from psychopy import visual
from params import params

###############
from psychopy import visual,event
from params import params
from isGazeInsideCircle import isGazeInsideCircle

def drawStim(target, win, stim, env):
    
    if str(target) == "fixation":
        line1 = visual.Line(win,lineColor=stim["line_color"],lineWidth=stim["fix_lw"])
        line2 = visual.Line(win,lineColor=stim["line_color"],lineWidth=stim["fix_lw"])
        line1.start = [-stim["fix_size"],0]
        line1.end =  [stim["fix_size"],0]
        line2.start = [0,-stim["fix_size"]]
        line2.end = [0,stim["fix_size"]]
        line1.draw()
        line2.draw()
        
        # #############################################
        # dummymode = True ######## temporary, fix the functions
        # if dummymode: #get mouse coords
        #     mouse = event.Mouse()
        #     nowCoords = mouse.getPos() 

        # else:  # we are actually tracking eyes
        #     nowCoords = (0,0) #for now
            
        # topleft = (-win.size[0]/2, win.size[1]/2)

        # # draw indicator at top left corner
        # if isGazeInsideCircle(nowCoords, env["xCenter"], env["yCenter"], stim["fix_deg_allowed"]):
        #     dotColor = [0, 255, 0]  # green
        #     dot = visual.DotStim(win,dotSize = 30, fieldShape = "sqr", color = dotColor, fieldPos = topleft) #modify to indicate upper left hand corner
        #     dot.draw()
        #     fix_success = True 
        # else:
        #     dotColor = [255, 0, 0]  # red
        #     dot = visual.DotStim(win,dotSize = 30, fieldShape = "sqr", color = dotColor, fieldPos = topleft)
        #     dot.draw()
        #     fix_success = False
        
        # showTrace = False ######temporary fix 
        # if showTrace: 
        #     dotColorTrace = [0.5, 0.5, 0.5]
        #     stim = visual.DotStim(win,dotSize = 10, fieldShape = "sqr",color = dotColorTrace, fieldPos = (nowCoords)) 
        #     stim.draw()
        
    
    elif str(target) == "flash":
        #circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2] - stim["baseCircle"][0]) / 2, pos=(env["xCenter"], env["yCenter"]), lineColor=None, fillColor="white")
        circle = visual.Circle(win, units='pix', radius=(stim["baseCircle"][2]/2), pos=(0,0), lineColor=None, fillColor="white")
        circle.draw()

    else:
        #text_stim = visual.TextStim(win, text=target, pos=(env["xCenter"], env["yCenter"]), color="white")
        text_stim = visual.TextStim(win, text=target, pos=(0,0), color="white", height = stim["text_size"],wrapWidth = env['screenXpixels']) #allow wrapWidth to be full size of screen
        text_stim.draw()





