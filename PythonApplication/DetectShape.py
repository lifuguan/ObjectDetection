# -*- coding: utf-8 -*-
'''
Time: 2018.7.19
author: lifuguan 
E-mail:1002732355@qq.com
'''

from time import sleep
import cv2
import argparse
import numpy as np 

import imutils  #OpenCV辅助（改进）lib

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
    image = cv2.imread("sample.jpg", cv2.IMREAD_COLOR)
    
    #emmmm, 我觉得这段代码可以使用以下一行带过
    #image = cv2.imread("image")

    #初始化要调整大小的图像的尺寸并获取图像大小 (有什么用吗)
    '''
    @param: 第二个参数是关键
    '''
    resized_image = imutils.resize(image, width = 300) #, width=300
    cv2.imshow("hello world", resized_image)
    cv2.waitKey(0)

    ratio = image.shape[0] / float(resized_image.shape[0])
     
    #灰度化图片
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("hello world", gray_image)
    cv2.waitKey(0)

    #对灰度图进行二值化操作，突出显示特征   （选择30，200为阀值）  (哈哈哈， 我不要这个玩意)
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY)[1]
    print thresh
    
    cv2.imshow("hello world", thresh)
    cv2.waitKey(0)
    
    #在二值化图像中寻找识别出的图形
    #cnts[0]对应opencv2.x，   cnts[1]对应opnecv3.x
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #给cnts降维，对应相应版本的opencv
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    #实例化标识模块对象
    sd = ShapeDetector()

    #循环标识
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c = ratio * c
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 2)
 
	    # show the output image
        cv2.imshow("Image", image)

        cv2.waitKey(0)


