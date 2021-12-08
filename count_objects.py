# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 22:16:01 2021

@author: PankK
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.ndimage import morphology
from skimage.measure import regionprops,label

def area(LB, label=1):  #Считаем площадь, берем маркированную фигуру
    pxs = np.where( LB == label) #список координат по всем осям, позиции всех пикселей (1- по строкамб 2 по столбцам)
   
    return [len(pxs[0]),pxs] # достаточно посчитать кол-во пикселей по 1 оси

def get_mask(labeled, pxs, label=1):
    max_x = max(pxs[0])+1
    min_x = min(pxs[0])
    max_y = max(pxs[1])+1
    min_y = min(pxs[1])
   # print(max_x,min_x,max_y,min_y)
    mask = labeled[min_x:max_x,min_y:max_y]
    #print(cur_area == label)
    return mask
 
def all_areas(labeled):
    areas = []
    for i in range(1,len(labeled)):
        if(area(labeled,i)[0] in areas):
            pass
        else:
            areas.append(area(labeled,i)[0])
            print(areas[-1])
    
    
image = np.load("ps.npy")
labeled = label(image)
counting_masks = [[]]
num = 0
count_masks = 0
print(len(labeled))
while(np.count_nonzero(image) != 0):

    plt.subplot(121)
    plt.imshow(image)
    #cur_area = area(labeled,1)[0]
    if count_masks<4:
        for i in range(1,len(labeled)):
            
            cur_area = area(labeled,i)[0]
            if cur_area > 10:
                pxs = area(labeled,i)[1]
                break
    else:   
       cur_area = area(labeled,1)[0]     
       pxs = area(labeled,1)[1]
       
    found_mask = get_mask(labeled, pxs)
    count_masks+=1
    print(found_mask)
    result_mask = morphology.binary_opening(labeled,found_mask)
    count = np.count_nonzero(morphology.binary_erosion(labeled,found_mask))
    counting_masks.append([found_mask,count])
    num+=count
    print("Figure amount: ",count)
    image = image - result_mask
    labeled = label(image)
       

    plt.subplot(122)
    plt.imshow(image)
    plt.show()
print("Common amount: ",num)
