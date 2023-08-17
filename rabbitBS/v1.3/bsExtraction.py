# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:28:49 2023

@author: achan2
"""
import os
import json

#Script To Extract BS Data

def bsExtraction(initials):
    fileList = os.listdir("C:\\Users\\achan2\\Box\\SURF2023\\BlindSpotMapping-master\\BlindSpot_Mapping\\data") 
    filePath = "C:\\Users\\achan2\\Box\\SURF2023\\BlindSpotMapping-master\\BlindSpot_Mapping\\data"
    foundFilesL = [file for file in fileList if file.startswith(f'{initials}_L') and file.endswith('json')] 
    foundFilesR = [file for file in fileList if file.startswith(f'{initials}_R') and file.endswith('json')]
    
    if foundFilesL and foundFilesR: #check if file exists
        with open(os.path.join(filePath,foundFilesR[0])) as R:
            BS_R = json.load(R)
        with open(os.path.join(filePath,foundFilesL[0])) as L:
            BS_L = json.load(L)
            
        BS = {}
        BS['leftBS_center'] = tuple(BS_L["BS_Center"]) #[x,y] float
        leftBS_width = BS_L["BS_width"]
        leftBS_height = BS_L["BS_height"]
        BS['leftBS_x'] = leftBS_width/2    #radius values of ellipse for convinience
        BS['leftBS_y'] = leftBS_height/2
        
        BS['rightBS_center'] = tuple(BS_R["BS_Center"]) #[x,y] float
        rightBS_width = BS_R["BS_width"]
        rightBS_height = BS_R["BS_height"]
        BS['rightBS_x'] = rightBS_width/2    #radius values of ellipse for convinience
        BS['rightBS_y'] = rightBS_height/2
        
        return BS

    else:
        print("ERROR!!! BS DATA DNE YET")
        return None
    
    

