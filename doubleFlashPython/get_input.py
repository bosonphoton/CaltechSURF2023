from psychopy import visual, core, event, sound
from params import params
from drawStim import drawStim
from playAudio import playAudio
import json
import copy

def get_input(env,param,stim,circLoc,win,deg,task,responded,Data,filePath):
    if task == "bdf":
        prompt = 'How many flashes did you see?\n\n 0: Zero\n\n 1: One\n\n 2: Two\n\n 3: Three'
    elif task == "vf":
        prompt = 'Did you see a flash?\n\n <== Yes        No ==>'

    num = 99

    drawStim(prompt,win,stim,env)
    win.flip()
    playAudio("resp",env)
    
    while not responded: #wait 0.01 seconds before executing loop
        core.wait(0.01)
        a = event.waitKeys(timeStamped=True)
        keys = [row[0] for row in a]
        secs = [row[1] for row in a][-1]

        for key in keys:
            if key in ['escape', 'q']:

######################################################################################################                
                #Data["Conditions"] = [condition + [resp, r] for condition, resp, r in zip(Data["Conditions"], Data["Responses"], Data["RT"])]
                #cop = copy.deepcopy(Data["Conditions"])
                #temp = sorted(cop, key=lambda x: x[1]) #sorts arr based on 2nd element, which indicated catch vs normal trials \
                #Data["Catch"] = [row[-2:] for row in temp[0:5]] #take only the catch trials rows, and only the Resp & RT of each


                # for j in range(24): #for each location
                #     count = 0
                #     count0 = 0
                #     count1 = 0
                #     count2 = 0
                #     count3 = 0
                #     for i in range(24, len(cop)): #for the rest... "Present" trials
                #         if cop[i, 0] == j and cop[i, 2] <= 3:
                #             count += 1
                #             if cop[i, 2] == 0:
                #                 count0 += 1
                #             elif cop[i, 2] == 1:
                #                 count1 += 1
                #             elif cop[i, 2] == 2:
                #                 count2 += 1
                #             elif cop[i, 2] == 3:
                #                 count3 += 1
                #     Data['Present'][j] = {
                #         'nValid': count,
                #         'zero': count0,
                #         'one': count1,
                #         'two': count2,
                #         'three': count3,
                #         #'zerop': count0 / count, bc count may be  0
                #         #'onep': count1 / count,
                #         #'twop': count2 / count,
                #         #'threep': count3 / count
                #     }
######################################################################################################
    
                
                with open(filePath, "w") as file:
                    json.dump(Data, file)
                    print("Some Trials Completed")
                responded = True
                win.close()
                core.quit()
            elif key in ['1', 'num_1']:
                num = 1
            elif key in ['2', 'num_2']:
                num = 2
            elif key in ['3', 'num_3']:
                num = 3
            elif key in ['0', 'num_0']:
                num = 0
            elif key in ['left', 'left arrow']:
                num = 1
            elif key in ['right', 'right arrow']:
                num = 0

        if num <= 3:
            responded = True

        drawStim(prompt,win,stim,env)
        win.flip()
    
    return num,secs,responded