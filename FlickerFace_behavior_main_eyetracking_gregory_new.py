           #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.0.2)

@authors: Anne K. & Grégory A.
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import csv

import copy
from copy import deepcopy

##EYETRACKING
eyetracking_record = False

if eyetracking_record:
    from iViewXAPI import  *
    from iViewXAPIReturnCodes import * 

    # ---------------------------------------------
    #---- connect to iViewX
    # ---------------------------------------------

    res = iViewXAPI.iV_SetLogger(c_int(1), c_char_p(b"iViewXSDK_Python_FlickerFace.txt"))
    res = iViewXAPI.iV_Connect(c_char_p(b'127.0.0.1'), c_int(4444), c_char_p(b'127.0.0.1'), c_int(5555))
    res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
    print("iV_GetSystemInfo: " + str(res))
    print("Samplerate: " + str(systemData.samplerate))
    print("iViewX Version: " + str(systemData.iV_MajorVersion) + "." + str(systemData.iV_MinorVersion) + "." + str(systemData.iV_Buildnumber))
    print("iViewX API Version: " + str(systemData.API_MajorVersion) + "." + str(systemData.API_MinorVersion) + "." + str(systemData.API_Buildnumber))

    def SampleCallback(sample):
        dataFile_eyedata.write('%i,%i,%.1f,%.1f,%.1f,%.1f\n' %(trials.thisN, sample.timestamp,sample.leftEye.gazeX, sample.leftEye.gazeY, sample.rightEye.gazeX, sample.rightEye.gazeY))
        return 0
        
    CMPFUNC = WINFUNCTYPE(c_int, CSample)
    smp_func = CMPFUNC(SampleCallback)
    sampleCB = False

       
    ###########################################
    # ---------------------------------------------
    #---- configure and start calibration
    # ---------------------------------------------

    calibrationData = CCalibration(5, 1, 0, 0, 1, 250, 220, 2, 20, b"") # (method (i.e.: number of points), visualization, display, speed, auto, fg, bg, shape, size, filename)
    res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
        
    res = iViewXAPI.iV_Calibrate()
    print("iV_Calibrate " + str(res))

    res = iViewXAPI.iV_Validate()
    print("iV_Validate " + str(res))

    res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), 0)
    print("iV_GetAccuracy " + str(res))
    print("deviationXLeft " + str(accuracyData.deviationLX) + " deviationYLeft " + str(accuracyData.deviationLY))
    print("deviationXRight " + str(accuracyData.deviationRX) + " deviationYRight " + str(accuracyData.deviationRY))

    ###########################


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.0.2'
expName = 'FlickerFace_Behavior_main'  # from the Builder filename that created this script
expInfo = {'session': '', 'participant': '', 'threshold_gabor':'', 'threshold_face':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

endExpNow = False  # flag for 'escape' or other condition => quit the exp



# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0,
    allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Instructions
Intructions_1Clock = core.Clock()
PauserunClock = core.Clock()

text_pauserun = visual.TextStim(win=win, name='text_4',
    text="Pause \n \n \n Presser 'flèche haute' ou 'flèche basse' pour continuer.",
    font='Arial',
    pos=[0, 0], height=0.04, wrapWidth=.8, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    depth=0.0);

text_faces = visual.TextStim(win=win, name='text_4',
    text="Détection de visages \n \n Presser 'flèche haute' si il y a un visage, \n Presser 'flèche basse' s'il n'y a pas de visage.\n \n Presser 'flèche haute' ou 'flèche basse' pour démarrer.",
    font='Arial',
    pos=[0, 0], height=0.04, wrapWidth=.8, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    depth=0.0);
    
text_gratings = visual.TextStim(win=win, name='text_4',
    text="Détection de Gabor  \n \n Presser 'flèche haute' si il y a un Gabor, \n Presser 'flèche basse' s'il n'y a pas de Gabor.\n \n Presser 'flèche haute' ou 'flèche basse' pour démarrer.",
    font='Arial',
    pos=[0, 0], height=0.04, wrapWidth=.8, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    depth=0.0);  




# Initialize components for Routine "pause_start", with fixation cross
pause_startClock = core.Clock()


# Initialize components for Routine "Trial"
TrialClock = core.Clock()
   

posf = 0.13
sizef = 0.18
post = 0.13
sizet = 0.18
    
image_flicker = visual.ImageStim(
    win=win, name='image_Lflicker',
    image='sin', mask='raisedCos',
    ori=0, pos=[-posf,-posf], size=[sizef,sizef],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
    
image_static = visual.ImageStim(
    win=win, name='image_Rstatic',
    image='sin', mask='raisedCos',
    ori=0, pos=[posf,-posf], size=[sizef,sizef],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
        
    
image_target = visual.ImageStim(
    win=win, name='image_target',
    image='sin', mask='raisedCos',
    ori=0, pos=[-post,-post], size=[sizet,sizet],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

image_target_mask = visual.ImageStim(
    win=win, name='image_target',
    image='sin', mask='raisedCos',
    ori=0, pos=[-post,-post], size=[sizet,sizet],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)   
    
image_scrambled = visual.ImageStim(
    win=win, name='image_scrambled',
    image='sin', mask='raisedCos',
    ori=0, pos=[post, -post], size=[sizet,sizet],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
           
      
image_instruc1 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[-0.4,-0.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

image_instruc2 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[-0.15,-.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=0.4,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

image_instruc3 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[0.15,-.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=0.4,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

image_instruc4 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[0.4,-.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=0.4,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

    
image_instruc5 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[-0.4,-0.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

image_instruc6 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[-0.15,-.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

image_instruc7 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[0.15,-.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)  

image_instruc8 = visual.ImageStim(
    win=win, name='image_instruc1',
    image='sin', mask='raisedCos',
    ori=0, pos=[0.4,-.3], size=[.16,.16],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)       
     
    
#fixation cross
disk = visual.Circle( win=win, pos=[0, 0], radius =.008,edges = 32,
    fillColor='white')  
    

line1 = visual.Line( win=win, start=(-.01, -0), end=(.01, 0),
    fillColor='black', lineWidth=2, lineColor='black')    
 
line2 = visual.Line( win=win, start=(0, -0.01), end=(0, 0.01),
    fillColor='black', lineWidth=2, lineColor='black') 
    
#trial count
trial_count = visual.TextStim(win=win, name='trial_count',
    text='default text',
    font='Arial',
    pos=[.4, -.4], height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    depth=-6.0);


# Initialize components for Routine "pause"
pauseClock = core.Clock()


# Initialize components for Routine "the_end"
the_endClock = core.Clock()

text_3 = visual.TextStim(win=win, name='text_3',
    text='Fin de la session. \n ',
    font='Arial',
    pos=[0, 0], height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    depth=0.0);



# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 




# START
if expInfo['session'] == str(1):
    run = 0;
    n_runs = 3
elif expInfo['session'] == str(2):
    run = 3;
    n_runs = 5
elif expInfo['session'] == str(3):
    run = 5;
    n_runs = 8
elif expInfo['session'] == str(4):
    run = 8;
    n_runs = 10    


scoretot = 0
while run <n_runs:
    
    ## parameters of run ##
    
    ## saving data
    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + 'data' + os.sep + expName + '_ppt%s_run%i_%s' % (expInfo['participant'], run, expInfo['date'])
    filename_eyedata = _thisDir + os.sep + 'data' + os.sep + expName + 'eyedata_ppt%s_run%i_%s' % (expInfo['participant'], run, expInfo['date'])

    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/annkos/Desktop/FlickerFace/Behavioral_study/FlickerFace_behavior.py',
        savePickle=True, saveWideText=True,
        dataFileName=filename)
    # save a log file for detail verbose info
    #logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    #logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file


    ## loading stim set
    stimulusset_filename = 'ppt%s' % (expInfo['participant'])+'_StimulusSet_FlickerFace_Behavior_main_run'+str(run)+'.csv'
    durationtarget = 0.050 # 50 ms
    timeflicker = 1.000; #time to wait before presentation of target

    trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(stimulusset_filename),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
            
    
   
    # ------Prepare to start Routine "Intructions_1"-------

    win.mouseVisible = False
    t = 0
    Intructions_1Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_4 = event.BuilderKeyResponse()
    
    ## define task
    if run_task == 'gabor_task': 
        
        Intructions_1Components = [text_gratings, image_instruc1, image_instruc2,image_instruc3,image_instruc4, image_instruc5, image_instruc6,image_instruc7,image_instruc8,key_resp_4]
                
        # keep track of which components have finished
        for thisComponent in Intructions_1Components:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "Intructions_1"-------
        while continueRoutine:
            # get current time
            t = Intructions_1Clock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            disk.setAutoDraw(False)
            line1.setAutoDraw(False)
            line2.setAutoDraw(False)
            
            # *text_4* updates
            if t >= 0.0 and text_gratings.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_gratings.tStart = t
                text_gratings.frameNStart = frameN  # exact frame index
                text_gratings.setAutoDraw(True)
            
                imageinstruc = 'stimuli_bmp_final/Gabor1.png'            
                imageinstrucb = 'stimuli_bmp_final/Gabor2.png'   
                imageinstrucc = 'stimuli_bmp_final/Gabor3.png'    
                
                image_instruc1.setImage(imageinstruc)
                image_instruc2.setImage(imageinstrucb)
                image_instruc3.setImage(imageinstrucc)
                image_instruc4.setImage(imageinstruc)

                imageinstruc = 'stimuli_bmp_final/scrambled_diff_Gabor1.png'            
                imageinstrucb = 'stimuli_bmp_final/scrambled_diff_Gabor2.png'  
                imageinstrucc = 'stimuli_bmp_final/scrambled_diff_Gabor3.png' 
                
                image_instruc5.setImage(imageinstruc)
                image_instruc6.setImage(imageinstrucb)
                image_instruc7.setImage(imageinstrucc)
                image_instruc8.setImage(imageinstruc)
                        
                image_instruc5.setAutoDraw(True) 
                image_instruc6.setAutoDraw(True)
                image_instruc7.setAutoDraw(True)
                image_instruc8.setAutoDraw(True)
                
                image_instruc1.opacity = 1               
                image_instruc2.opacity = 0.5
                image_instruc3.opacity = 0.3
                image_instruc4.opacity = 0                
                
                image_instruc1.setAutoDraw(True) 
                image_instruc2.setAutoDraw(True)
                image_instruc3.setAutoDraw(True)
                image_instruc4.setAutoDraw(True)
                
                
            # *key_resp_4* updates
            if t >= 0.0 and key_resp_4.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_4.tStart = t
                key_resp_4.frameNStart = frameN  # exact frame index
                key_resp_4.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
                
            if key_resp_4.status == STARTED:
                theseKeys = event.getKeys(keyList=['up','down'])
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_4.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_4.rt = key_resp_4.clock.getTime()
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Intructions_1Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
                    # refresh the screen
                    
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        
    elif run_task == 'face_task':
        
        Intructions_1Components = [text_faces, image_instruc1, image_instruc2,image_instruc3,image_instruc4, image_instruc5, image_instruc6,image_instruc7,image_instruc8, key_resp_4]

        # keep track of which components have finished
        for thisComponent in Intructions_1Components:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "Intructions_1"-------
        while continueRoutine:
            # get current time
            t = Intructions_1Clock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            disk.setAutoDraw(False)
            line1.setAutoDraw(False)
            line2.setAutoDraw(False)
            # *text_4* updates
            if t >= 0.0 and text_faces.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_faces.tStart = t
                text_faces.frameNStart = frameN  # exact frame index
                text_faces.setAutoDraw(True)
                
                imageinstruc = 'stimuli_faces_final/face_neutral_1.jpg'            
            
                image_instruc1.setImage(imageinstruc)
                image_instruc2.setImage(imageinstruc)
                image_instruc3.setImage(imageinstruc)
                image_instruc4.setImage(imageinstruc)

                imageinstruc = 'stimuli_faces_final/scrambled_diff_1.png'           
            
                image_instruc5.setImage(imageinstruc)
                image_instruc6.setImage(imageinstruc)
                image_instruc7.setImage(imageinstruc)
                image_instruc8.setImage(imageinstruc)
                        
                image_instruc5.setAutoDraw(True) 
                image_instruc6.setAutoDraw(True)
                image_instruc7.setAutoDraw(True)
                image_instruc8.setAutoDraw(True)
                
                image_instruc1.opacity = 1               
                image_instruc2.opacity = 0.8
                image_instruc3.opacity = 0.5
                image_instruc4.opacity = 0                
                
                image_instruc1.setAutoDraw(True) 
                image_instruc2.setAutoDraw(True)
                image_instruc3.setAutoDraw(True)
                image_instruc4.setAutoDraw(True)                
            
            # *key_resp_4* updates
            if t >= 0.0 and key_resp_4.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_4.tStart = t
                key_resp_4.frameNStart = frameN  # exact frame index
                key_resp_4.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_4.status == STARTED:
                theseKeys = event.getKeys(keyList=['up','down'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_4.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_4.rt = key_resp_4.clock.getTime()
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Intructions_1Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

    # -------Ending Routine "Intructions_1"-------
    for thisComponent in Intructions_1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_4.keys in ['', [], None]:  # No response was made
        key_resp_4.keys=None
    thisExp.addData('key_resp_4.keys',key_resp_4.keys)
    if key_resp_4.keys != None:  # we had a response
        thisExp.addData('key_resp_4.rt', key_resp_4.rt)
    thisExp.nextEntry()
    # the Routine "Intructions_1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()



    # ------Prepare to start Routine "pause_start"-------
    t = 0
    pause_startClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.500000)


    # -------Start Routine "pause_start"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = pause_startClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        
        # shopw fixation cross
        if t >= 0.0 :
            disk.setAutoDraw(True)
            line1.setAutoDraw(True)
            line2.setAutoDraw(True)            
        frameRemains = 0.0 + 1.5- win.monitorFramePeriod * 0.75  # most of one frame period left

        # check for quit (typically the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit() 

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()



    if eyetracking_record:
         #eyedata recording
         dataFile_eyedata = open(filename_eyedata+'-data.csv', 'w')  # a simple text file with 'comma-separated-values'
         dataFile_eyedata.write('Trial_number,Timestamp,LeftEyeX,LeftEyeY,RightEyeX,RightEyeY\n')

    trialsthisN = 0
    
    for thisTrial in trials:
        currentLoop = trials
        
        trialsthisN +=1
        
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Trial"-------
        t = 0
        TrialClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        
        # update component parameters for each repeat 
        # CHOSE FACE STIM for flicker, scrambles for static
        imN = np.random.permutation(4)+1
        imageflick = 'stimuli_faces_final/face_neutral_'+str(imN[0])+'.jpg'
        imagestatic = 'stimuli_faces_final/scrambled_diff_'+str(imN[0])+'.jpg'

        #CHOSE target and scrambled STIM
        imagetarget = 'stimuli_bmp_final/'+imagetarget            
        imagescrambled= 'stimuli_bmp_final/'+imagescrambled
        
        
        Response = event.BuilderKeyResponse()
        
        image_flicker.setImage(imageflick)
        image_static.setImage(imagestatic)
        image_target.setImage(imagetarget)
        image_scrambled.setImage(imagescrambled)

        # define opacity flicker and mask (random)
        if freq ==6:
            flicker_opacity = (np.arange(0,60) %10==0)* 1
            randp = np.random.permutation(59)
            flickrand = flicker_opacity[1::]
            mask_opacity = deepcopy(flicker_opacity)
            mask_opacity[1::] = flickrand[randp]            
        elif freq == 10:
            flicker_opacity = (np.arange(0,60) %6==0)* 1
            randp = np.random.permutation(59)
            flickrand = flicker_opacity[1::]
            mask_opacity = deepcopy(flicker_opacity)
            mask_opacity[1::] = flickrand[randp] 
            
        elif freq == 60:
            flicker_opacity = np.ones((1,60))[0]
            mask_opacity = np.ones((1,60))[0]
            
        
        # define flicker position
        if flickerpos == 'f_l':
            image_flicker.setPos([-posf,-posf])
            image_static.setPos([posf,-posf])
            
        else: 
            image_flicker.setPos([posf,-posf])
            image_static.setPos([-posf,-posf])
            
        
        if targetpos == 'l':
            image_target.setPos([-post,-post])
            image_scrambled.setPos([-post,-post])
            
        else: 
            image_target.setPos([post,-post])
            image_scrambled.setPos([post,-post])
        
        trial_count.setText(trials.thisN)
        # keep track of which components have finished
        TrialComponents = [Response, image_target, image_scrambled,  trial_count]
        for thisComponent in TrialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "Trial"-------
        while continueRoutine:
            # get current time
            
            if eyetracking_record:
                ##### record eye gaze
                res = iViewXAPI.iV_SetSampleCallback(smp_func)
                sampleCB = True
            
            # fixation cross 
            disk.setAutoDraw(True)
            line1.setAutoDraw(True)
            line2.setAutoDraw(True)               

            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            
            t = TrialClock.getTime()
            # Draw flicker image    
            if t < timeflicker:
                
                #flicker > set opacity and draw figure
                #(6  pour 10 Hz; 10 pour 6 Hz, 1 pour fixe)
                #image_flicker.opacity = np.cos((frameN % (60/freq))*np.pi*2/(60/freq))/2 + 0.5
                #image_flicker.opacity = np.float((np.cos((frameN % (60/freq))*np.pi*2/(60/freq)/2) >0.5)*1)
                image_flicker.opacity = np.float(flicker_opacity[frameN])
                image_static.opacity = np.float(mask_opacity[frameN])
                image_static.draw()
                image_flicker.draw()
            
            # target > presents stimulus after timeperiod                    
            if t >= timeflicker+timetarget/1000 and t <= timeflicker+timetarget/1000+durationtarget:
                if run_task == 'gabor_task': 
                    image_scrambled.draw()
                    if targetpres: #draw stim only if targetpres
                        image_target.opacity = np.float(expInfo['threshold_gabor'])
                        image_target.draw()
                    
                elif run_task == 'face_task':
                    image_scrambled.draw()
                    if targetpres: #draw stim only if targetpres
                        image_target.opacity = np.float(expInfo['threshold_face'])
                        image_target.draw()
                
                
            # *Response* updates, starts after presentation of target
            if t >= timeflicker+timetarget/1000 and Response.status == NOT_STARTED:
                # keep track of start time/frame for later
                Response.tStart = t
                Response.frameNStart = frameN  # exact frame index
                Response.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(Response.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if Response.status == STARTED:
                theseKeys = event.getKeys(keyList=['up','down'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    Response.keys = theseKeys[-1]  # just the last key pressed
                    Response.rt = Response.clock.getTime()
                    # was this 'correct'?
                    if (Response.keys == str(('up','down')[resp])) or (Response.keys == ('up','down')[resp]):
                        Response.corr = 0
                    else:
                        Response.corr = 1
                    # a response ends the routine
                    continueRoutine = False
                    scoretot += Response.corr 
                  
                if t > 4:  # end of trial
                    Response.corr = 0
                    Response.rt = Response.clock.getTime()
                    continueRoutine = False
                     
            # *trial_count* updates
            if t >= 0.0 and trial_count.status == NOT_STARTED:
                # keep track of start time/frame for later
                trial_count.tStart = t
                trial_count.frameNStart = frameN  # exact frame index
                trial_count.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in TrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Trial"-------
        for thisComponent in TrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
  
        # store data for trials (TrialHandler)
        trials.addData('Response.keys',Response.keys)
        trials.addData('Response.corr', Response.corr)
        if Response.keys != None:  # we had a response
            trials.addData('Response.rt', Response.rt)
        # the Routine "Trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
             
        
        if trialsthisN == 80 or trialsthisN == 160:
            continuePause = True
            #pause for ppt to rest
            while continuePause:
                text_pauserun.setAutoDraw(True)
                disk.setAutoDraw(False)
                line1.setAutoDraw(False)
                line2.setAutoDraw(False)
                win.flip()
                theseKeys = event.getKeys(keyList=['up','down'])
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_4.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_4.rt = key_resp_4.clock.getTime()
                    # a response ends the routine
                    continuePause = False
                    text_pauserun.setAutoDraw(False)
            
        # ------Pause of 800 ms before next trial
        win.flip()
        t = 0
        pauseClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(0.800000)
        
        
        # -------Start Routine "pause"-------
        while continueRoutine and routineTimer.getTime() > 0 :
            # get current time
            t = pauseClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *mini_pause* updates
            if t >= 0.0:
                disk.setAutoDraw(True)
                line1.setAutoDraw(True)
                line2.setAutoDraw(True)   

            
            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        thisExp.nextEntry()
        
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename+'.csv')    
     

    # next run
    run +=1 

# ------Prepare to start Routine "the_end"-------
t = 0
the_endClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()
# keep track of which components have finished
the_endComponents = [text_3, key_resp_2]
for thisComponent in the_endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "the_end"-------
while continueRoutine:
    # get current time
    t = the_endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
          
    # *text_3* updates
    if t        >= 0.0 and text_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_3.tStart = t
        text_3.setText("Score: "+ str(scoretot/(2*240)*100)+ "%, \n Fin de la session")
        text_3.frameNStart = frameN  # exact frame index
        text_3.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in the_endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "the_end"-------
for thisComponent in the_endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "the_end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


"""
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
"""
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
