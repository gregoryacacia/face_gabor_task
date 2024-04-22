# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 12:07:11 2020

@author: Anne.K
"""

import glob
import imageio
import numpy as np


     
from diffeomorph import diffeomorph_face


img = imageio.imread("Gabor4.png")[:,:,0]
imgn = diffeomorph_face(img, max_offset=30, iterations=10, aggressive=True)
        
imageio.imwrite("scrambled_diff_Gabor4.png",imgn)
    
     