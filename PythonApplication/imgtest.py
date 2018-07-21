# -*- coding: utf-8 -*-

#import cv2
#import numpy as np 

#img = cv2.imread("sample5.jpg", cv2.IMREAD_COLOR)
#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

##set blue thresh
#lower_blue=np.array([60,43,46])
#upper_blue=np.array([300,255,255])

#mask = cv2.inRange(hsv, lower_blue, upper_blue)
##res = cv2.bitwise_and(img, img, mask=mask)
#cv2.imshow('Mask', mask)
#cv2.waitKey(0)

'''
Time: 2018.7.19
author: lifuguan 
E-mail:1002732355@qq.com
'''

from time import sleep
import cv2
import argparse
import numpy as np 

import imutils  
#OpenCV辅助（改进）lib

class ShapeDetector:
    def __init__(self):
        pass
    def detect(self, c):
        #初始化图形名字并且圈出
        shape = "undentifed"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        #三角形有三个角
        if len(approx) == 3:
            shape = "triangle"
        #四边形有四个角  (我是真不知道他怎么分辨四边形和矩形，和ar有关吗)
        elif len(approx) == 4:
            (x,y ,w, h) = cv2.boundingRect(approx)
            #在已经为矩形的前提下，近似判断长宽比
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        elif len(approx) == 5:
            shape = "pentagon"
        else:
            shape = "circle"
        return shape

#brief: 主函数
if __name__=='__main__':
    image = cv2.imread("C:\\Users\\10027\\source\\repos\\ObjectDetection\\PythonApplication\\RoboSample\\green\\green1.jpg", cv2.IMREAD_COLOR)
    
    #emmmm, 我觉得这段代码可以使用以下一行带过
    #image = cv2.imread("image")

    #初始化要调整大小的图像的尺寸并获取图像大小 (有什么用吗)
    resized_image = imutils.resize(image, width = 300) #, width=300
    cv2.imshow("hello world", resized_image)
    cv2.waitKey(0)

    ratio = image.shape[0] / float(resized_image.shape[0])
     
   # #将格式从BGR——>HSV  HSV颜色区度:https://blog.csdn.net/taily_duan/article/details/51506776
    hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
   
    #根据上篇博文和比赛情况，设置一个蓝色的区间
    lower_blue = np.array([40,43,46])
    upper_blue = np.array([255,255,255])
    #设置红色区间
    lower_red = np.array([0,43,46])
    upper_red = np.array([10,255,255])
    #设置绿色区间
    lower_green = np.array([35,43,46])
    upper_green = np.array([110,255,255])
    #设置黄色区间
    lower_yellow = np.array([26,43,46])
    upper_yellow = np.array([34,255,255])

    #分割图像
    mask = cv2.inRange(hsv, lower_green, upper_green)
    cv2.imshow("hello", mask)
    cv2.waitKey(0)
    #膨胀，消除噪点，（顺便填充一下）
    img = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    cv2.imshow("hello1", img)
    cv2.waitKey(0)
    
    #在二值化图像中寻找识别出的图形
    #cnts[0]对应opencv2.x，   cnts[1]对应opnecv3.x
    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #给cnts降维，对应相应版本的opencv
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    #实例化标识模块对象
    sd = ShapeDetector()

    #循环标识
    for c in cnts:
        #以下为垃圾代码
        M = cv2.moments(c)
        if M["m10"] != 0:
        #表示图像重心
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
        else :
            cX = cY = 0
        shape = sd.detect(c)
        #处理一下图片
        c = c.astype("float")
        c = ratio * c
        c = c.astype("int")
        #滤掉噪声 (利用面积大小)
        if c.size > 100 :
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
	        # show the output image
            cv2.imshow("Image", image)

            cv2.waitKey(0)


