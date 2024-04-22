# -*- coding: utf-8 -*-
"""

Determine stimulus set across conditions

@author: Anne.K
"""

import numpy as np 
from numpy import matlib
 
def concatstr(string,length):
    outputarray = np.empty([length,1], dtype='object')
    for i in range(len(outputarray)):
        outputarray[i] = string         
    return outputarray;    
    
def concatstrimg(string,ext,length):
    outputarray = np.empty([length,1], dtype='object')
    for i in range(len(outputarray)):
        if i< length/4:
            outputarray[i] = string + '1'+ ext
        elif i >= length/4 and i< length/2:
            outputarray[i] = string + '2'+ ext
        elif i >= length/2 and i< 3*length/4:
            outputarray[i] = string + '3'+ ext
        elif i >= 3*length/4:     
            outputarray[i] = string + '4'+ ext           
    return outputarray;    

def savestimsetfile_run(filename, task, flickposrun, stimT, stimNT, freq, timetarg, nb_trials_freq):
    header = 'run_task,imagetarget,imagescrambled,freq,timetarget,flickerpos,targetpos,targetpres,resp'
    imagetarget = np.array([[]])
    Resp = np.array([[]])
    Maincsvfile = []

    imagetarget = stimT[0:nb_trials_freq*3]
    imagescrambled = stimNT[0:nb_trials_freq*3]
    
    # par sequence freq: 1 essai de chaque side et de chaque time periode, egalite entre stim/ non stim 80 essais
    # par run : 80 essais * 3 frequences, ordre randomise

    freqr = np.concatenate((np.ones((nb_trials_freq,1))*freq[0],np.ones((nb_trials_freq,1))*freq[1],np.ones((nb_trials_freq,1))*freq[2]),axis=0)
    timetarget = matlib.repmat(timetarg,1,np.int(nb_trials_freq/len(timetarg)*3))
    targetpos = matlib.repmat(targetp,1,np.int(nb_trials_freq/(len(timetarg)*2))*3)
    
    #pour l'instant on randomize aleatoirement la présence ou l'absence de cible, il faudra voir si la randomization est correcte
    #targetpres = (np.random.rand(1,240)>0.5)*1
    targetpres = matlib.repmat(np.reshape([np.zeros([1,40]),np.ones([1,40])],-1),1,3)
    
    
    len(targetpres)
    len(targetpos)
    Resp = np.array(targetpres==1)
    Resp = Resp*1


    #### COMMENT RANDOMISER FLICKER POSE ??
    
    print(len(imagetarget[0]))
    Maincsvfile = np.concatenate((task,imagetarget, imagescrambled,freqr, np.transpose(timetarget),flickposrun, np.transpose(targetpos), np.transpose(targetpres),np.transpose(Resp)),axis=1)

    #### RANDOMIZATION
    # RANDOMIZE ORDER OF FREQUENCY BLOCKS
    # RANDOMIZE TRIALS WITHIN A FREQUENCY BLOCK
    randomblocks = np.random.permutation(3)
    randomtrials = [np.random.permutation(nb_trials_freq)+ randomblocks[0]*nb_trials_freq, np.random.permutation(nb_trials_freq)+ randomblocks[1]*nb_trials_freq, np.random.permutation(nb_trials_freq)+ randomblocks[2]*nb_trials_freq]
    Maincsvfile = Maincsvfile[np.reshape(randomtrials,-1)]
    np.savetxt(filename+'.csv', Maincsvfile, fmt= '%s,%s,%s,%i,%f,%s,%s,%i,%i', header = header,comments = "")
 
 


##########   PARAMETERS
ppt = 'gregory'

#for main experiment
timetarg = np.array([16.7, 33.3, 50, 66.7, 83.3, 100, 116.7, 133.3, 150, 166.7, 183.3, 200, 216.7, 233.3, 250, 266.7, 283.3, 300, 316.7, 333.3])
freq = np.array([6, 10, 60]) # 60 Hz is control without flicker
targetp = np.reshape([concatstr('l',len(timetarg)), concatstr('r',len(timetarg))],-1)

nb_rep_cond = 10; #corresponds to number of repeated trials per cond
nb_runs = nb_rep_cond; #(adding condition Face vs gratings)
nb_trials_freq = len(timetarg)*4 #per freq sequences, on target on each side and time period, and pres/absent 
nb_trials_run = nb_trials_freq * 3 
flickerpos = np.reshape([np.zeros(int(nb_rep_cond/2)), np.ones(int(nb_rep_cond/2))],-1)
rand_face = np.random.permutation(nb_rep_cond);
rand_gabor = np.random.permutation(nb_rep_cond);



##########

run_order = np.random.permutation(nb_runs);

# Face stim condition

flickerpos_face = flickerpos[rand_face]
face = concatstrimg('face_neutral_','.jpg',240)
randomize = np.random.permutation(240)
face = face[randomize]
facescrambled = concatstrimg('scrambled_diff_','.jpg', 240)
randomize = np.random.permutation(240)
facescrambled = facescrambled[randomize]
task = concatstr('face_task', nb_trials_run)

for i in range(0,np.int(nb_runs/2)):

    # determine position of flicker for the run
    if flickerpos_face[i]:
        flickpos = 'f_r'
    else: 
        flickpos = 'f_l'
   
    flickposrun = concatstr(flickpos,nb_trials_run)

    # save main stim sets
    savestimsetfile_run("ppt"+ppt+"_StimulusSet_FlickerFace_Behavior_main_run"+str(run_order[i]), task, flickposrun, face, facescrambled, freq, timetarg, nb_trials_freq)

########
# Gabor stim conditions
flickerpos_gabor = flickerpos[rand_gabor]    
gabor = concatstrimg('Gabor','.png',240)
randomize = np.random.permutation(240)
gabor = gabor[randomize]
gaborscrambled = concatstrimg('scrambled_diff_Gabor','.png', 240)
randomize = np.random.permutation(240)
gaborscrambled = gaborscrambled[randomize]
task = concatstr('gabor_task', nb_trials_run)

for i in range(np.int(nb_runs/2),nb_runs):
    
    # determine position of flicker for the run
    if flickerpos_gabor[i-int(nb_runs/2)]:
        flickpos = 'f_r'
    else: 
        flickpos = 'f_l'
   
    flickposrun = concatstr(flickpos ,nb_trials_run)
       
    savestimsetfile_run("ppt"+ppt+"_StimulusSet_FlickerFace_Behavior_main_run"+str(run_order[i]), task, flickposrun, gabor, gaborscrambled, freq, timetarg, nb_trials_freq)




