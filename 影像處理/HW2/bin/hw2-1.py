# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 04:27:33 2017

@author: 傳衛
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

file_name = "blue.jpg"

src_pic = cv2.imread("blue.jpg")
cpy_pic = cv2.imread("blue.jpg")
pic_w = src_pic.shape[1]
pic_h = src_pic.shape[0]

BGRrange = [([0,40,0], [255,255,112]),
             ([190,190,180], [255,255,255]),
             ([0,40,0], [185,135,112])]

index = 0
for (lower, upper) in BGRrange:
    
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    
    if(index==0):
        blue_mask = cv2.inRange(src_pic, lower, upper)
    elif index==1 :
        white_mask = cv2.inRange(src_pic, lower, upper)
    elif index==2 :
        back_mask = cv2.inRange(src_pic, lower, upper)
    index+=1

cv2.imshow("src", src_pic)
cv2.imshow("mask_b", blue_mask)
cv2.imwrite("mask_b.jpg",blue_mask)
cv2.imshow("mask_w", white_mask)
cv2.imwrite("mask_w.jpg",white_mask)
cv2.imshow("mask_back", back_mask)
cv2.imwrite("mask_back.jpg",back_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

bright_rate = 1.5
bright_plus = 0

for ih in range(0,pic_h):
    for iw in range(0,pic_w):
        
        if blue_mask[ih,iw] :
            for i in range(0,3):
                c = int(src_pic[ih,iw,i])
                c = c*bright_rate+bright_plus
                if c > 255 :
                    c = 255
                src_pic[ih,iw,i] = c
                
        if white_mask[ih,iw] :
            src_pic[ih,iw,0:2] = src_pic[ih,iw,0:2]/10
            
        elif abs(int(src_pic[ih,iw,0])- src_pic[ih,iw,1]) < 20 and abs(int(src_pic[ih,iw,0])- src_pic[ih,iw,2]) < 20 :
        #elif 160<abs(int(src_pic[ih,iw,0])/3+int(src_pic[ih,iw,1])/3+int(src_pic[ih,iw,2])/3) < 200 :
            src_pic[ih,iw,0:2] = src_pic[ih,iw,0:2]/2

cv2.imshow("output", src_pic)
cv2.imshow("output-src", cpy_pic)
key = cv2.waitKey(0)
'''if key == 115:
    cv2.imwrite(file_name,src_pic)'''
if key == 111:
    cv2.imwrite("output.jpg",src_pic)
cv2.destroyAllWindows()
