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

import imutils  
#OpenCV辅助（改进）lib



class ShapeDetector:
    def __init__(self):
        pass

    #位置分析函数
    def pos_calc(self, pt1, pt2, pt3, pt4):
        a = pt1[1]-pt2[1]
     
        sclope_up = float(float(pt1[1]-pt2[1])/float(pt1[0]-pt2[0]))
        sclope_down = float(float(pt4[1]-pt3[1])/float(pt4[0]-pt3[0]))
        sclope_average = float((sclope_down + sclope_up) / 2)
        point_average = ((pt1[0]+pt2[0]+pt3[0]+pt4[0]) / 4, (pt1[1]+pt2[1]+pt3[1]+pt4[1]) / 4)
        #显示该物块斜率
        print  sclope_average
        #显示该物块中心点
        print  point_average

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
            #嵌套array
            pt1 = tuple(approx[0][0])
            pt2 = tuple(approx[1][0])
            pt3 = tuple(approx[2][0])
            pt4 = tuple(approx[3][0])
            cv2.line(image, pt1, pt2, (0, 255, 0), 3)
            cv2.line(image, pt3, pt2, (0, 255, 0), 3)
            cv2.line(image, pt4, pt3, (0, 255, 0), 3)
            cv2.line(image, pt4, pt1, (0, 255, 0), 3)

            #传入数据进行位置分析
            #self.pos_calc(approx[0][0], approx[1][0], approx[2][0], approx[3][0])

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

    #emmmm, 我觉得这段代码可以使用以下一行带过
    #image = cv2.imread("image")
    cap = cv2.VideoCapture(2)
    cap.set(3, 1280) #设置长
    cap.set(4, 480)  #设置短
    while True:

        ret, frame = cap.read()
        image = frame
        #初始化要调整大小的图像的尺寸并获取图像大小 (有什么用吗)
        resized_image = imutils.resize(image) #, width=300


        ratio = image.shape[0] / float(resized_image.shape[0])
     
       # #将格式从BGR——>HSV  HSV颜色区度:https://blog.csdn.net/taily_duan/article/details/51506776
        hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
   
        #根据上篇博文和比赛情况，设置一个蓝色的区间
        lower_blue = np.array([100,43, 46])
        upper_blue = np.array([124,255,255])
        #设置红色区间
        lower_red = np.array([156,43,46])
        upper_red = np.array([180,255,255])
        #设置绿色区间
        lower_green = np.array([35,43,77])
        upper_green = np.array([96,255,255])
        #设置黄色区间
        lower_yellow = np.array([13,43,46])
        upper_yellow = np.array([42,255,255])


        #集体分割图像，分步骤检测颜色色块
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        kernel = np.ones((5,5),np.uint8)  
        erosion_blue = cv2.erode(mask_blue,kernel,iterations = 1)
        kernel = np.ones((5,5),np.uint8)  
        erosion_red = cv2.erode(mask_red,kernel,iterations = 1)
        kernel = np.ones((5,5),np.uint8)  
        erosion_green = cv2.erode(mask_green,kernel,iterations = 1)
        kernel = np.ones((5,5),np.uint8)  
        erosion_yellow = cv2.erode(mask_yellow,kernel,iterations = 1)


        #集体膨胀，消除噪点，（顺便填充一下）
        dilate_blue  = cv2.dilate(erosion_blue, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)    
        dilate_red   = cv2.dilate(erosion_red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)    
        dilate_green = cv2.dilate(erosion_green, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=16)    
        dilate_yellow = cv2.dilate(erosion_yellow, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=16)    
        cv2.imshow("blue",   dilate_blue  )
        cv2.imshow("green",  dilate_red   )
        cv2.imshow("red",    dilate_green )
        cv2.imshow("yellow", dilate_yellow)

        #在二值化图像中寻找识别出的图形
        #cnts[0]对应opencv2.x，   cnts[1]对应opnecv3.x
        cnts_blue   = cv2.findContours(dilate_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_red    = cv2.findContours(dilate_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_green  = cv2.findContours(dilate_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_yellow = cv2.findContours(dilate_yellow.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        #给cnts降维，对应相应版本的opencv
        cnts_blue   = cnts_blue[0] if imutils.is_cv2() else cnts_blue[1]
        cnts_red    = cnts_red[0] if imutils.is_cv2() else cnts_red[1]
        cnts_green  = cnts_green[0] if imutils.is_cv2() else cnts_green[1]
        cnts_yellow = cnts_yellow[0] if imutils.is_cv2() else cnts_yellow[1]


        #实例化标识模块对象
        sd_blue   = ShapeDetector()
        sd_red    = ShapeDetector()
        sd_green  = ShapeDetector()
        sd_yellow = ShapeDetector()

        #循环标识
        for c in cnts_blue:
            #以下为垃圾代码
            M = cv2.moments(c)
            if M["m10"] != 0:
            #表示图像重心
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            else :
                cX = cY = 0
            #返回得到名字
            shape = sd_blue.detect(c)
            #处理一下图片
            c = c.astype("float")
            c = ratio * c
            c = c.astype("int")
            #滤掉噪声 (利用面积大小)
            if c.size > 100 :
                cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)




        for c in cnts_red:
            #以下为垃圾代码
            M = cv2.moments(c)
            if M["m10"] != 0:
            #表示图像重心
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            else :
                cX = cY = 0
            #返回得到名字
            shape = sd_red.detect(c)
            #处理一下图片
            c = c.astype("float")
            c = ratio * c
            c = c.astype("int")
            #滤掉噪声 (利用面积大小)
            if c.size > 100 :
                cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)



        for c in cnts_green:
            #以下为垃圾代码
            M = cv2.moments(c)
            if M["m10"] != 0:
            #表示图像重心
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            else :
                cX = cY = 0
            #返回得到名字
            shape = sd_green.detect(c)
            #处理一下图片
            c = c.astype("float")
            c = ratio * c
            c = c.astype("int")
            #滤掉噪声 (利用面积大小)
            if c.size > 100 :
                cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)


        for c in cnts_yellow:
            #以下为垃圾代码
            M = cv2.moments(c)
            if M["m10"] != 0:
            #表示图像重心
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            else :
                cX = cY = 0
            #返回得到名字
            shape = sd_yellow.detect(c)
            #处理一下图片
            c = c.astype("float")
            c = ratio * c
            c = c.astype("int")
            #滤掉噪声 (利用面积大小)
            if c.size > 150 :
                cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)
                # show the output image
                cv2.imshow("Image", image)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

