# -*- coding: utf-8 -*-

'''
@All right resevrsed
@smmary:used to detect different shapes and different color in a video stream
@Time: 2018.7.19
@author: lifuguan 
@E-mail:1002732355@qq.com
'''

import threading
from time import sleep
import cv2
import argparse
import numpy as np 

import imutils  
#OpenCV辅助（改进）lib

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




class ShapeDetector:
    def __init__(self):
        pass

    def drawRetangle(self, color):
        pass    
    #初始化图形名字并且圈出
    def detect(self, c):
        shape = "undentifed"
        peri = cv2.arcLength(c, True)
        #@param 2: 精度调整
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        #三角形有三个角
        if len(approx) == 3:
            shape = "triangle"
        #四边形有四个角  (我是真不知道怎么分辨四边形和矩形，和ar有关吗)
        elif len(approx) == 4:
            (x,y ,w, h) = cv2.boundingRect(approx)
            #嵌套array
            pt1 = tuple(approx[0][0])
            pt2 = tuple(approx[1][0])
            pt3 = tuple(approx[2][0])
            pt4 = tuple(approx[3][0])
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)
            cv2.line(frame, pt3, pt2, (0, 255, 0), 3)
            cv2.line(frame, pt4, pt3, (0, 255, 0), 3)
            cv2.line(frame, pt4, pt1, (0, 255, 0), 3)
            
            #传入数据进行位置分析
            #self.pos_calc(approx[0][0], approx[1][0], approx[2][0], approx[3][0])

            #在已经为矩形的前提下，近似判断长宽比
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
            #return shape , approx[0][0], approx[1][0], approx[2][0], approx[3][0]

        elif len(approx) == 5:
            shape = "pentagon"
            pt1 = tuple(approx[0][0])
            pt2 = tuple(approx[1][0])
            pt3 = tuple(approx[2][0])
            pt4 = tuple(approx[3][0])
            pt5 = tuple(approx[4][0])
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)
            cv2.line(frame, pt3, pt2, (0, 255, 0), 3)
            cv2.line(frame, pt4, pt3, (0, 255, 0), 3)
            cv2.line(frame, pt4, pt5, (0, 255, 0), 3)
            cv2.line(frame, pt1, pt5, (0, 255, 0), 3)
        elif len(approx) == 6:
            shape = "Hexagon"
            pt1 = tuple(approx[0][0])
            pt2 = tuple(approx[1][0])
            pt3 = tuple(approx[2][0])
            pt4 = tuple(approx[3][0])
            pt5 = tuple(approx[4][0])
            pt6 = tuple(approx[5][0])
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)
            cv2.line(frame, pt3, pt2, (0, 255, 0), 3)
            cv2.line(frame, pt4, pt3, (0, 255, 0), 3)
            cv2.line(frame, pt4, pt5, (0, 255, 0), 3)
            cv2.line(frame, pt6, pt5, (0, 255, 0), 3)
            cv2.line(frame, pt1, pt6, (0, 255, 0), 3)
        else:
            shape = "circle"
        return shape
        pass




class Detect_Thread:
    def __init__(self):
        pass
    
    img_blue   = cv2.imread("sample.jpg")
    img_yellow = cv2.imread("sample.jpg")
    img_red    = cv2.imread("sample.jpg")
    img_green  = cv2.imread("sample.jpg")
    


    def detect_blue(self, mask):
        kernel = np.ones((3,3),np.uint8)  
        erosion = cv2.erode(mask,kernel,iterations = 2)
        dilate_blue = cv2.dilate(erosion, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=15)
        cnts_blue   = cv2.findContours(dilate_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sd_blue   = ShapeDetector()
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
            if c.size > 150 :
                cv2.putText(origin_img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)
                self.img_blue = c
        pass

    def detect_yellow(self, mask):
        kernel_yellow = np.ones((5,5),np.uint8)  
        erosion_yellow = cv2.erode(mask,kernel_yellow,iterations = 1)
        dilate_yellow = cv2.dilate(erosion_yellow, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=16)
        cnts_yellow = cv2.findContours(dilate_yellow.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
            if c.size > 100 :
                
                cv2.putText(origin_img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)
        self.img_red = c
        pass

    #红色待定
    def detect_red(self, mask):
        kernel = np.ones((3,3),np.uint8)  
        erosion = cv2.erode(mask,kernel,iterations = 2)
        dilate_red = cv2.dilate(erosion, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=15)
        cnts_red    = cv2.findContours(dilate_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
            if c.size > 150 :
                cv2.putText(origin_img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)
                self.img_red =  c
        pass

    def detect_green(self, mask):
        kernel_green = np.ones((5,5),np.uint8)  
        erosion_green = cv2.erode(mask,kernel_green,iterations = 2)
        dilate_green = cv2.dilate(erosion_green, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=18)
        cnts_green  = cv2.findContours(dilate_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
                cv2.putText(origin_img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)
                self.img_green = c
        pass



#brief: 主函数
if __name__=='__main__':
    cap = cv2.VideoCapture(2)
    cap.set(3, 1280) #设置长
    cap.set(4, 480)  #设置短
    while True:
        global frame
        ret, frame = cap.read()
        resized_image = imutils.resize(frame)
        ratio = frame.shape[0] / float(frame.shape[0])
        #将格式从BGR——>HSV  HSV颜色区度:https://blog.csdn.net/taily_duan/article/details/51506776
        hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
        #多线程节省运算时间
        th_blue = threading.Thread(target=Detect_Thread.detect_blue, args=(hsv, ))
        th_blue.start()
        th_blue.join()

        th_yellow = threading.Thread(target=Detect_Thread.detect_yellow, args=(hsv, ))
        th_yellow.start()
        th_yellow.join()

        th_red = threading.Thread(target=Detect_Thread.detect_red, args=(hsv, ))
        th_red.start()
        th_red.join()

        th_green = threading.Thread(target=Detect_Thread.detect_green, args=(hsv, ))
        th_green.start()
        th_green.join()
        
        '''确保子线程全部结束才结束主线程'''

        df = Detect_Thread()
        img_blue    = df.img_blue
        img_yellow  = df.img_yellow
        img_red     = df.img_red
        img_green   = df.img_green
        cv2.imshow("Detect Frame", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        

        pass

