# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 04:27:33 2017

@author: 傳衛
"""

"""
10/18 HW#02
1. 濾色: 
>  皮膚 (10%)  #show 出 mask＋濾出後的圖即可
>  白色 (10%)  #show 出 mask＋濾出後的圖即可
>  背景 (20%)  #show 出 mask＋濾出後的圖即可
2. 改色
> 皮膚變"亮" (15%)
> 白變紅 (15%)
> 背景變白 (15%)
> 三張整合起來  (10%)
>加分：將小精靈的眼睛改成黃色，但帽子和褲子還是紅色（20%）#難題
3. 美觀 
>沒雜訊, 線條乾淨  (5%)
(共120%)
input圖:  Blue.jpg
output圖（存）: 整合改色後final的圖.jpg＋(加分題圖.jpg)＋程式.py

p.s. 用python寫（盡量用python3）
繳交期限 10/25 中午12:00
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

'''
以白色遮罩和已拜訪像素的bool map建立遞迴搜尋 查詢並回傳每個白色區塊面積
'''
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

'''
以白色遮罩和已拜訪像素的bool map建立遞迴搜尋 更改一個白色區塊的顏色
'''
def space_colorer(boolmap,visitmap,colormap,in_x,in_y):
    if 0<=in_x<pic_w and 0<=in_y<pic_h:
        if boolmap[in_y,in_x] and not visitmap[in_y,in_x] :
            visitmap[in_y,in_x] = 255
            colormap[in_y,in_x] = (0,255,255)
            space_colorer(boolmap,visitmap,colormap,in_x,in_y-1)
            space_colorer(boolmap,visitmap,colormap,in_x+1,in_y)
            space_colorer(boolmap,visitmap,colormap,in_x,in_y+1)
            space_colorer(boolmap,visitmap,colormap,in_x-1,in_y)

"""
3. 美觀 
>沒雜訊, 線條乾淨  (5%)
新版優化數值 白色取值幾乎完整 藍色與背景可以取得邊緣以外的大多訊號 並新增 back_mask 取樣範圍
"""
BGRrange = [([0,40,0], [255,255,112]),
             ([190,190,180], [255,255,255]),
             ([0,40,0], [185,135,112])]

"""
1. 濾色: 
>  皮膚 (10%)
>  白色 (10%)
>  背景 (20%)
迴圈採樣 利用inRange函數 分別取出像素位置並建立 藍色遮罩 與  白色遮罩  和  背景遮罩
"""
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
3. 美觀 
>沒雜訊, 線條乾淨  (5%)
將back_mask 再做處理
使用類濾波遮罩 建立過濾雜訊的bg_mask
一次濾波就可以過濾掉絕大多數的雜訊
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
            
"""
利用藍色遮罩與背景遮罩的XOR可以得到皮膚遮罩
(但此程式並未使用此遮罩  僅為作業標準方便而使用)
"""
skin_mask =  cv2.bitwise_xor(blue_mask,bg_mask)
            
'''
1. 濾色: 
>  皮膚 (10%)  #show 出 mask＋濾出後的圖即可
>  白色 (10%)  #show 出 mask＋濾出後的圖即可
>  背景 (20%)  #show 出 mask＋濾出後的圖即可
測試遮罩模樣
'''             
"""
>  白色 (10%)  #show 出 mask＋濾出後的圖即可
"""
cv2.imshow("white-mask", white_mask)
cv2.imshow("white-mask-output", cv2.bitwise_and(src_pic, src_pic, mask=white_mask))
"""
>  皮膚 (10%)  #show 出 mask＋濾出後的圖即可
"""
cv2.imshow("blueSkin-mask",skin_mask )
cv2.imshow("blueSkin-mask-output", cv2.bitwise_and(src_pic, src_pic, mask=skin_mask))
"""
>  背景 (20%)  #show 出 mask＋濾出後的圖即可
"""
cv2.imshow("deepBlueBackground-mask", bg_mask)
cv2.imshow("deepBlueBackground-mask-output", cv2.bitwise_and(src_pic, src_pic, mask=bg_mask))
key = cv2.waitKey(0)
cv2.destroyAllWindows()


"""設置亮度線性變化  rate比率變化  plus固定變化"""
bright_rate = 1
bright_plus = 70

"""
2. 改色
> 皮膚變"亮" (15%)
> 白變紅 (15%)
> 背景變白 (15%)
> 三張整合起來  (10%)

以遮罩(mask)作為判斷依據 迴圈對判斷為true的向速做出變化
對藍色做出亮度變化(預設比率增加)
對白色做出轉變為紅色的變化

註:(> 三張整合起來  (10%)):
    當初實作時為了降低時間與空間複雜度沒有再做先分開再疊合
    而是直接透過遮罩的布林含意直接疊回原圖進行操作
    在發布成作業之前便已經完成了此項作業也經過老師的同意
    效果也沒有改變請多多包涵QAQ
"""
for ih in range(0,pic_h):
    for iw in range(0,pic_w):
        """
        > 白變紅 (15%)
        此elif為對於部分灰階雜訊的處理方式
        """
        if white_mask[ih,iw] :
            src_pic[ih,iw,0:2] = src_pic[ih,iw,0:2]/10
        elif abs(int(src_pic[ih,iw,0])- src_pic[ih,iw,1]) < 20 and abs(int(src_pic[ih,iw,0])- src_pic[ih,iw,2]) < 20 :
            src_pic[ih,iw,0:2] = src_pic[ih,iw,0:2]/2
            
        """
        > 皮膚變"亮" (15%)
        > 背景變白 (15%)
        先使用藍色遮罩免去額外的處理
        再透過背景遮罩的if...else...分開兩種不同的藍色區域做出相應變換
        """
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
顯示圖片並輸出
按s儲存並覆蓋原圖(已被註解)
按o儲存並另外輸出(已被註解)
所以現在只會直接儲存
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

"""
output圖（存）: 整合改色後final的圖.jpg
更改結果輸出為output.jpg
"""
cv2.imwrite("output.jpg",src_pic)
cv2.destroyAllWindows()


'''
以上基礎作業完成
'''

"""
>加分：將小精靈的眼睛改成黃色，但帽子和褲子還是紅色（20%）#難題
"""
'''
此程式算法以白色區域的面積大小大致區分眼睛與其他部分
'''
'''建立眼部遮罩'''
eye_mask = np.zeros([pic_h,pic_w], dtype="uint8")
for ih in range(0,pic_h):
    for iw in range(0,pic_w):
        """尋找每一個未被使用過的白色像素作為起點 進行遞迴搜尋"""
        if white_mask[ih,iw] and not vis_mask[ih,iw]:
            """計算出面積大小"""
            AreaNum = space_counter(white_mask,vis_mask,iw,ih)
            """輸出每個白色區塊的大小和起點(測試用)
            print(format("%d(%d,%d)"%(AreaNum,iw,ih)))
            """
            
            """眼部主要介於蔗面積之中 但唯一有一個例外(被多偵測以為是眼睛) 但這例外形狀和大小都幾乎無法用單一算法排除"""
            if 203 < AreaNum < 320 :
                """利用地回搜尋將整個區塊的眼部著色"""
                space_colorer(white_mask,eye_mask,src_pic,iw,ih)

""" 用圖片表示所有用到的MASK方便比對(測試用)
cv2.imshow("white_mask", white_mask)
cv2.imshow("eye_mask", eye_mask)
"""
cv2.imshow("output-plus", src_pic)
key = cv2.waitKey(0)
cv2.destroyAllWindows()

"""
output圖（存）: 加分題圖.jpg
儲存為output-plus.jpg
"""
cv2.imwrite("output-plus.jpg",src_pic)