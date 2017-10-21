# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 04:27:33 2017

@author: 傳衛
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

"""設置原始圖片名稱"""
file_name = "blue.jpg"

"""開啟圖片並讀取寬高"""
src_pic = cv2.imread("blue.jpg")
pic_w = src_pic.shape[1]
pic_h = src_pic.shape[0]

"""設置色彩取樣範圍  藍([0,40,0], [255,255,100])  白([200,200,200], [255,255,255])"""
"""新版優化數值 並新增 back_mask 取樣範圍"""
BGRrange = [([0,40,0], [255,255,100]),
             ([190,190,180], [255,255,255]),
             ([0,40,0], [185,135,100])]

"""迴圈採樣 利用inRange函數 分別取出 藍色遮罩 與  白色遮罩"""
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

"""設置亮度線性變化  rate比率變化  plus固定變化"""
bright_rate = 1
bright_plus = 70

"""
以遮罩(mask)作為判斷依據 迴圈對判斷為true的向速做出變化
對藍色做出亮度變化(預設比率增加)
對白色做出轉變為紅色的變化
"""
for ih in range(0,pic_h):
    for iw in range(0,pic_w):
                
        if white_mask[ih,iw] :
            src_pic[ih,iw,0:2] = src_pic[ih,iw,0:2]/10
            
        elif abs(int(src_pic[ih,iw,0])- src_pic[ih,iw,1]) < 20 and abs(int(src_pic[ih,iw,0])- src_pic[ih,iw,2]) < 20 :
            src_pic[ih,iw,0:2] = src_pic[ih,iw,0:2]/2
            
        if blue_mask[ih,iw] :
            if ih+1 < pic_h and iw+1 < pic_w :
                if back_mask[ih,iw] and back_mask[ih+1,iw] and back_mask[ih+1,iw+1] and back_mask[ih,iw+1]:
                    src_pic[ih,iw] = 255
                    
                else:
                    for i in range(0,3):
                        c = int(src_pic[ih,iw,i])
                        c = c*bright_rate+bright_plus
                        if c > 255 :
                            c = 255
                        src_pic[ih,iw,i] = c
"""
顯示圖片
按s儲存並覆蓋原圖
按o儲存並另外輸出
其他按鍵不動作
最後關閉所有視窗
"""
cv2.imshow("output", src_pic)
key = cv2.waitKey(0)
if key == 115:
    cv2.imwrite(file_name,src_pic)
if key == 111:
    cv2.imwrite("output.jpg",src_pic)
cv2.destroyAllWindows()
