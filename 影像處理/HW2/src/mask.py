# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

image = cv2.imread("blue.jpg")

color = ('b', 'g', 'r')
for i, col in enumerate(color): # 列舉
    histr = cv2.calcHist([image], [i], None, [256], [0,256]) # 直方圖
    plt.plot(histr, color = col)
    plt.xlim([0,256])
    plt.show()
    
BGRrange = [([0,100,0], [255,255,100]), # range:([BGR]~[BGR])
             ([200,200,200], [255,255,255])]

index = 0
for (lower, upper) in BGRrange:
    #create NumPy arrays from the BGRrange
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask) # (底圖, 加了mask的圖)
    # show the images
    cv2.imshow("images", output)
    cv2.imwrite(str(index)+".jpg", output)
    index += 1
    # cv2.imshow("images", mask)
    cv2.waitKey(0)
cv2.destroyAllWindows()