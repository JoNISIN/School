# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 04:27:33 2017

@author: 傳衛
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
"""
鬆綁預設遞迴限制
"""
sys.setrecursionlimit(10000000)

"""設置原始圖片名稱"""
file_name = "blue.jpg"

"""開啟圖片並讀取寬高"""
src_pic = cv2.imread("blue.jpg")
pic_w = src_pic.shape[1]
pic_h = src_pic.shape[0]

vis_mask = np.zeros([pic_h,pic_w], dtype="uint8")
def space_counter(boolmap,visitmap,in_x,in_y):
    counter = 0
    if 0<=in_x<pic_w and 0<=in_y<pic_h:
        if boolmap[in_y,in_x] and not visitmap[in_y,in_x] :
            visitmap[in_y,in_x] = 255
            counter += space_counter(boolmap,visitmap,in_x,in_y-1)
            counter += space_counter(boolmap,visitmap,in_x+1,in_y)
            counter += space_counter(boolmap,visitmap,in_x,in_y+1)
            counter += space_counter(boolmap,visitmap,in_x-1,in_y)
            return counter+1
        else:
            return 0
    else :
        return 0
    
def space_colorer(boolmap,visitmap,colormap,in_x,in_y):
    counter = 0
    if 0<=in_x<pic_w and 0<=in_y<pic_h:
        if boolmap[in_y,in_x] and not visitmap[in_y,in_x] :
            visitmap[in_y,in_x] = 255
            colormap[in_y,in_x] = (0,255,255)
            counter += space_colorer(boolmap,visitmap,colormap,in_x,in_y-1)
            counter += space_colorer(boolmap,visitmap,colormap,in_x+1,in_y)
            counter += space_colorer(boolmap,visitmap,colormap,in_x,in_y+1)
            counter += space_colorer(boolmap,visitmap,colormap,in_x-1,in_y)
            return counter+1
        else:
            return 0
    else :
        return 0

"""新版優化數值 白色取值幾乎完整 藍色與背景可以取得邊緣以外的大多訊號 並新增 back_mask 取樣範圍"""
BGRrange = [([0,40,0], [255,255,112]),
             ([190,190,180], [255,255,255]),
             ([0,40,0], [185,135,112])]

"""迴圈採樣 利用inRange函數 分別取出 藍色遮罩 與  白色遮罩  和  背景遮罩"""
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

'''
將back_mask 再做處理
使用類濾波遮罩 建立過濾雜訊的bg_mask
'''
bg_mask = np.zeros([pic_h,pic_w], dtype="uint8")
for ih in range(0,pic_h):
    for iw in range(0,pic_w):
        '''使用權值白&權值黑'''
        price_w = 0
        price_b = 0
        '''迴圈取得黑白權值'''
        for of_y in range(-1,1):
            for of_x in range(-1,1):
                if 0 <= ih+of_y < pic_h and 0 <= ih+of_x < pic_w :
                    if back_mask[ih+of_y,iw+of_x] :
                        price_w += 1
                    else :
                        price_b += 1
        '''使用權值做出過濾'''
        if  price_w < 4 :
            bg_mask[ih,iw] = 0
        else :
            bg_mask[ih,iw] = 255
            
'''測試遮罩模樣   '''             
cv2.imshow("output-bg", bg_mask)
cv2.imshow("output-bk", back_mask)
key = cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("mask-bg.jpg",bg_mask)


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
                ''' 
                未建立濾波器前所使用的舊方法  使用4格範圍的取樣濾波過濾數值
                if back_mask[ih,iw] and back_mask[ih+1,iw] and back_mask[ih+1,iw+1] and back_mask[ih,iw+1]:
                    src_pic[ih,iw] = 255
                '''
                '''
                新方法使用濾波器所建立的bg_mask遮罩做為過濾標準 方便控制參數
                '''
                if bg_mask[ih,iw] :
                    src_pic[ih,iw] = 255   
                else :
                    for i in range(0,3):
                        c = int(src_pic[ih,iw,i])
                        c = c*bright_rate+bright_plus
                        if c > 255 :
                            c = 255
                        src_pic[ih,iw,i] = c
"""
顯示圖片
按s儲存並覆蓋原圖(已被註解)
按o儲存並另外輸出
其他按鍵不動作
最後關閉所有視窗
"""
cv2.imshow("output", src_pic)
key = cv2.waitKey(0)
'''按s儲存並覆蓋原圖(已被註解)
if key == 115:
    cv2.imwrite(file_name,src_pic)
'''
'''按o儲存並另外輸出(已被註解)
if key == 111:
    cv2.imwrite("output.jpg",src_pic)
'''
cv2.imwrite("output.jpg",src_pic)
cv2.destroyAllWindows()

eye_mask = np.zeros([pic_h,pic_w], dtype="uint8")
for ih in range(0,pic_h):
    for iw in range(0,pic_w):
        if white_mask[ih,iw] and not vis_mask[ih,iw]:
            AreaNum = space_counter(white_mask,vis_mask,iw,ih)
            print(format("%d(%d,%d)"%(AreaNum,iw,ih)))
            if 203 < AreaNum < 320 :
                space_colorer(white_mask,eye_mask,src_pic,iw,ih)

cv2.imshow("white_mask", white_mask)
cv2.imshow("eye_mask", eye_mask)
cv2.imshow("output", src_pic)
cv2.imwrite("output-plus.jpg",src_pic)
key = cv2.waitKey(0)
cv2.destroyAllWindows()