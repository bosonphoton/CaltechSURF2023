import os
import json
from psychopy import visual,core,event

#Script To Extract BS Data

initials = 'SV006'


win = visual.Window(
    size=(3840, 2160), winType='pyglet', allowGUI=False, allowStencil=False, colorSpace='rgb255', color='gray', 
    blendMode='avg', useFBO=True, 
    units='pix')


fileList = os.listdir("C:\\Users\\achan2\\Box\\SURF2023\\BlindSpotMapping-master\\BlindSpot_Mapping\\data") 
filePath = "C:\\Users\\achan2\\Box\\SURF2023\\BlindSpotMapping-master\\BlindSpot_Mapping\\data"
foundFilesL = [file for file in fileList if file.startswith(f'{initials}_L') and file.endswith('json')] 
foundFilesR = [file for file in fileList if file.startswith(f'{initials}_R') and file.endswith('json')]

if foundFilesL and foundFilesR: #check if file exists
    with open(os.path.join(filePath,foundFilesR[0])) as R:
        BS_R = json.load(R)
    with open(os.path.join(filePath,foundFilesL[0])) as L:
        BS_L = json.load(L)
else: 
    print("ERROR FILE NOT FOUND")
    win.close()
    core.quit()

left_vertices = tuple(BS_L["BS_Vertices"]) 
right_vertices = tuple(BS_R["BS_Vertices"]) 
left_center = tuple(BS_L["BS_Center"]) 
right_center = tuple(BS_R["BS_Center"]) 


line1 = visual.Line(win,lineColor='white',lineWidth=5)
line2 = visual.Line(win,lineColor='white',lineWidth=5)
line1.start = [-20,0]
line1.end =  [20,0]
line2.start = [0,-20]
line2.end = [0,20]
line1.draw()
line2.draw()


# left_center = tuple([-400.0, -63.5])
# right_center = tuple([400.0, -63.5])
# left_vertices = tuple([[-473.0, 132.0], [-600.0, -63.5], [-400.0, -259.0], [-300.0, -63.5]]) 
# right_vertices = tuple([[473.0, 132.0], [600.0, -63.5], [400.0, -259.0], [300.0, -63.5]])

leftBSborder = visual.shape.ShapeStim(win,units='pix',fillColor= 'black', fillColorSpace= 'black', vertices = left_vertices)
rightBSborder = visual.shape.ShapeStim(win,units='pix',fillColor= 'black', fillColorSpace= 'black', vertices = right_vertices)
leftBS = visual.Circle(win, units='pix', radius=20, pos=left_center, lineColor=None, fillColor="white")
rightBS = visual.Circle(win, units='pix', radius=20, pos=right_center, lineColor=None, fillColor="white")

leftBSborder.draw()
rightBSborder.draw()
leftBS.draw()
rightBS.draw()
win.flip()

screenshot = win.getMovieFrame()
screenshot.save(f'{initials}_blindspot.png')
win.close()
core.quit()