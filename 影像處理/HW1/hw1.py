# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 16:35:17 2017

@author: 卓傳衛
"""

import cv2


"""除了標準輸出有寬高資訊外  視窗開啟圖檔的名稱後也有圖片寬高尺寸"""
"""
9/27 HW#01 
1. 視窗看圖 (10%)
2. 長寬各縮小一半 (30%)
3. 中間放字--"淡江資工" (綠色的, 粗體) (30%)
4.  **影像其他特效 (20%額外加分)
     Input: 讀入"任意"一張圖片
     Output:（1）存新檔圖 (20%）
            （2）顯示影像寬和高 (10%)
"""

"""讀取並縮小圖片"""
#圖片名稱
pic_name = "cutecat.jpg"
pic = cv2.imread(pic_name)
small_pic = cv2.resize(pic,(int(pic.shape[1]/2),int(pic.shape[0]/2)))
small_pic_name = "small-"+pic_name

'''印出縮小後的圖片'''
cv2.imshow(format(small_pic_name+"(%d x %d)"%(small_pic.shape[1],small_pic.shape[0])),small_pic)
print(format("寬:%d 長:%d"%(small_pic.shape[1],small_pic.shape[0])))
key = cv2.waitKey(0)

'''按下S儲存縮小的照片'''
if(key == 115):
    cv2.imwrite(small_pic_name,small_pic)

"""影像其他特效(使圖片線性增亮)"""
bright_rate = 1.5
bright_plus = 0
for ih in range(0,small_pic.shape[0]):
    for iw in range(0,small_pic.shape[1]):
        for i in range(0,3):
            b = int(small_pic[ih,iw,i])
            b = b*bright_rate+bright_plus
            if b > 255 :
                b = 255
            small_pic[ih,iw,i] = b
"""印出變亮的圖片"""
cv2.imshow(format("bright-"+small_pic_name+"(%d x %d)"%(small_pic.shape[1],small_pic.shape[0])),small_pic)
print(format("寬:%d 長:%d"%(small_pic.shape[1],small_pic.shape[0])))
key = cv2.waitKey(0)

'''按下S儲存變亮的照片'''
if(key == 115):
    cv2.imwrite("bright"+small_pic_name,small_pic)


"加入文字"
font = cv2.FONT_HERSHEY_TRIPLEX
"""cv2.putText並不直接支援中文 故使用英文 'TKU CSIE' """
text = 'TKU CSIE'
Big = 2
hoz_offset = 10
ver_offset = 5
text_on_pic = cv2.putText(small_pic,text,(int(small_pic.shape[1]/2)-len(text)*Big*hoz_offset,int(small_pic.shape[0]/2)+Big*ver_offset),font,Big,(0,255,0),10)
cv2.imshow(format("text-"+small_pic_name+"(%d x %d)"%(small_pic.shape[1],small_pic.shape[0])),small_pic)
print(format("寬:%d 長:%d"%(small_pic.shape[1],small_pic.shape[0])))
key =cv2.waitKey(0)

"""儲存(輸出)最終結果"""
cv2.imwrite("Output-"+small_pic_name,small_pic)
cv2.destroyAllWindows()

