# -*- coding: utf-8 -*-

'''
@All right reserved.
@summary: used to track the black line to correct the diretion of the car
@author: LiHao
@date: 2018.7.22
@refer: https://www.opencv-python-tutroals.readthedocs.io
@location: DJI
'''


import cv2
import numpy as np
import imutils


#用于识别
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
            #return shape , approx[0][0], approx[1][0], approx[2][0], approx[3][0]

        elif len(approx) == 5:
            shape = "pentagon"
        else:
            shape = "circle"
        return shape

#初始化， 
cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 480)
while(1):
    # get a frame
    ret, frame = cap.read()
    image = frame
    
    ratio = image.shape[0] / float(image.shape[0])

    # #将格式从BGR——>HSV  HSV颜色区度:https://blog.csdn.net/taily_duan/article/details/51506776
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = hsv[0: 480, 0: 640]

    #设置黑色
    lower_black = np.array([0,0,0])
    upper_black = np.array([180,255,46])
    #分割图像
    mask = cv2.inRange(hsv, lower_black, upper_black)

    kernel = np.ones((5,5),np.uint8)  
    erosion = cv2.erode(mask,kernel,iterations = 1)
    img = cv2.dilate(erosion, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)

    cv2.imshow("oengzhang", img)

    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #给cnts降维，对应相应版本的opencv
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    sd = ShapeDetector()
    for c in cnts:
        #以下为垃圾代码
        M = cv2.moments(c)
        #返回得到名字
        shape = sd.detect(c)

        if M["m10"] != 0:
        #表示图像重心
            cX_ = int((M["m10"] / M["m00"]) * ratio)
            cY_ = int((M["m01"] / M["m00"]) * ratio)
        else :
            cX = cY = 0

        #处理一下图片
        c = c.astype("float")
        c = ratio * c
        c = c.astype("int")
        #滤掉噪声 (利用面积大小)
        if c.size > 150 :
            
            cv2.putText(image, shape, (cX_, cY_), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)
            # show the output image
        cv2.imshow("Image", image)


    if cv2.waitKey(50) & 0xFF == ord(' '):
        break
   
