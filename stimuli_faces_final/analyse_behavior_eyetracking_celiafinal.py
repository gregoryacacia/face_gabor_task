# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 15:10:58 2022

@author: Administrateur
"""

import csv
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
from matplotlib import patches
#import panda as pd

trial=[];
leftEyeX = [];
leftEyeY = [];
rightEyeX = [];
rightEyeY = [];
gazeX = [];
gazeY = [];
gazemeanX = [];
gazemeanY = [];
gazestdX = [];
gazestdY = [];
timetarget  = [];

currentTrial = 0
durflick = 1 #s
durtarg = 0.380 # period where target can appear
Fseye = 60 #sampling rate eyetracker

fld = ''
date = '*.csv'
tick = 0
reject_t = np.zeros(120)

## Exclusion parameters for saccades
width = 37* 2 # number of pixels per visual angle * # visual angle
height = 37* 2#20* np.nanmean(gazestdY)              

## rejection: 1 blink flicker, 2 blink target, 3 saccade, 4 trial too short, 5 bad fixation

prevvalue =1

#def skipLine(f, skip):
  #skip = skip-1  


For ppt == 'celia':
            
    fig = plt.figure(1)
    ax = fig.add_subplot(111, aspect='auto')
    for run in range(0,20):
        
        datafilename = glob(fld+"FlickerFace_Behavior_maineyedata_ppt"+str(ppt)+"_run"+str(run)+date)
        datafilename2 = glob(fld+"FlickerFace_Behavior_main_ppt"+str(ppt)+"_run"+str(run)+date)
        
        f= open(datafilename2[0])
        with f as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                next(csvReader, None)  # skip the headers 
                next(csvReader, None)  # skip the headers  
                for row in csvReader:
                    timetarget.append(int(float(row[4])))
                    
        
        f= open(datafilename[0])
        with f as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                next(csvReader, None)  # skip the headers 
                next(csvReader, None)  # skip the headers  

                
                for row in csvReader:
                    
                    if row != []: #and (int(float(row[2])) !=0): # on enleve les moments ou l'eyetracker ne captait plus
                        trialn = int(row[0]) 
                        #rejectstat = False
                        #rejectres = int(0)
                        if (trialn == currentTrial and tick < durflick*Fseye):
                            
                            tick+=1
                            
                            if float(row[2])*float(row[3])*float(row[4])*float(row[5])==0: # if one value equals zero> blink
                                leftEyeX.append(np.nan)
                                leftEyeY.append(np.nan)    
                                rightEyeX.append(np.nan)
                                rightEyeY.append(np.nan)  
                                gazeX.append(np.nan)
                                gazeY.append(np.nan) 
                                prevvalue =0 
                                
                                if currentTrial <120:
                                    reject_t[currentTrial] = int(1)
                                
                            elif  float(row[2])*float(row[3])*float(row[4])*float(row[5])!=0 and prevvalue == 0 :
                                next(csvReader)
                                next(csvReader)
                                #skipLine(f,row)
                                prevvalue = 1                            
                            
                            else:
                                leftEyeX.append(int(float(row[2])))
                                leftEyeY.append(int(float(row[3])))    
                                rightEyeX.append(int(float(row[4])))
                                rightEyeY.append(int(float(row[5])))    
                            
                                gazeX.append(int((float(row[2])+float(row[4]))/2)) 
                                gazeY.append(int((float(row[3])+float(row[5]))/2)) 
                                

                        elif (trialn == currentTrial and (tick >= durflick*Fseye and tick < (durflick+durtarg)*Fseye)):
                        
                            #target period
                            tick+=1
                            if float(row[2])*float(row[3])*float(row[4])*float(row[5])==0: # if one value equals zero> blink
                                if timetarget[trialn] > tick :    #if blink before the target
                                        leftEyeX.append(np.nan)
                                        leftEyeY.append(np.nan)    
                                        rightEyeX.append(np.nan)
                                        rightEyeY.append(np.nan)  
                                        gazeX.append(np.nan)
                                        gazeY.append(np.nan) 
                                        
                                        if currentTrial <120:
                                            reject_t[currentTrial] = int(2)   
    
                            else:
                                leftEyeX.append(int(float(row[2])))
                                leftEyeY.append(int(float(row[3])))    
                                rightEyeX.append(int(float(row[4])))
                                rightEyeY.append(int(float(row[5])))    
                                
                                gazeX.append(int((float(row[2])+float(row[4]))/2)) 
                                gazeY.append(int((float(row[3])+float(row[5]))/2)) 
                                
                                          
                        elif (trialn != currentTrial):  
                            # plot data trial 
                            if tick< (Fseye *1) and currentTrial <120:
                                reject_t[currentTrial] = int(4)
                             
                            #elif tick> (Fseye *1) and (np.max(gazeX)-np.min(gazeX))>width and currentTrial<120:
                                #reject_t[currentTrial] = int(3)
                               
                                
                            elif tick> (Fseye *1) and (((np.max(gazeX)-np.min(gazeX))**2/width**2 + (np.max(gazeY)-np.min(gazeY))**2/height**2) >1) and currentTrial<120:
                                reject_t[currentTrial] = int(3)    
                                #plt.plot(gazeX,gazeY,'k')
                                
                            elif (np.nanmean(gazeY)<465 or np.nanmean(gazeY)>615 or np.nanmean(gazeX)<885 or np.nanmean(gazeX)>1035) and currentTrial<120: #Non-fixation at the center
                                reject_t[currentTrial] = int(5)    
                                
                            
                            elif tick> (Fseye *1) and (((np.max(gazeX)-np.min(gazeX))**2/width**2 + (np.max(gazeY)-np.min(gazeY))**2/height**2) <1):
                                plt.plot(gazeX,gazeY)
                                gazemeanX.append(np.nanmean(gazeX))
                                gazemeanY.append(np.nanmean(gazeY))
                                gazestdX.append(np.nanstd(gazeX))
                                gazestdY.append(np.nanstd(gazeY))       
                                    
                                        
                                                
                            currentTrial = trialn  
                            leftEyeX = []
                            leftEyeY = []
                            rightEyeX = []
                            rightEyeY = []                            
                            gazeX = []
                            gazeY = [] 
                           # print(tick)
                            tick=0
                    
                       
        xcenter = np.nanmean(gazemeanX)
        ycenter = np.nanmean(gazemeanY)                              
             
        e1 = patches.Ellipse((xcenter, ycenter), width, height, angle=0, linewidth=2, fill=False, zorder=2)
        ax.add_patch(e1)
        gazemeanX = []
        gazemeanY = []  
        gazestdX = []
        gazestdY = []  
        np.savetxt(fld+"FlickerFace_Behavior_trialrejecteyedata_ppt"+str(ppt)+"_run"+str(run)+".csv",reject_t)
  
    #plt.xlim(900,1050)
    #plt.ylim(450,650) 
    plt.xlim(0,1920)
    plt.ylim(0,1080)
    
plt.show()
