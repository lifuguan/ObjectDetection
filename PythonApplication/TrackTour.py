# -*- coding: utf-8 -*-

'''
@All right reserved.
@summary: used to track the black line to correct the diretion of the car
@author: LiHao
@date: 2018.7.22
@refer: https://www.opencv-python-tutroals.readthedocs.io
@location: DJI
'''

# -*- coding: utf-8 -*-

import cv2
import math
import numpy as np
import imutils

class ShapeDetector:
    def __init__(self):
        pass

    #位置分析函数
    def pos_calc(self, pt1, pt2, pt3, pt4, center_point) :
        slope_up = 0
        height  = 0.1
        width   = 0.1
        if pt2[1] + 10 > 200 :
            cv2.putText(image, "p1 ", (pt1[0], pt1[1] + 10) , cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p1位置
            cv2.putText(image, "p2 ", (pt2[0], pt2[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p2位置 
            cv2.putText(image, "p3 ", (pt3[0], pt3[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p3位置 
            cv2.putText(image, "p4 ", (pt4[0], pt4[1] + 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p4位置 
            height = float(pt1[1]-pt2[1])  
            width = float(-pt1[0]+pt2[0])
        elif pt2[1] + 10 < 100 :
            #修正摄像头左移
            cv2.putText(image, "p1 ", (pt1[0], pt1[1] + 10) , cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p1位置
            cv2.putText(image, "p2 ", (pt2[0], pt2[1] + 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p2位置 
            cv2.putText(image, "p3 ", (pt3[0], pt3[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p3位置 
            cv2.putText(image, "p4 ", (pt4[0], pt4[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #p4位置
            height = float(pt2[1]-pt3[1])  
            width = float(-pt2[0]+pt3[0])
        #初中数学斜率法
        if not height!=0 or width!=0:
            slope_up = float(height/width)
        elif height :
            slope_up = 50 #让斜率大于阀值

        x = math.pow(abs(320 - center_point[0]), 2) #获取镜头中心与质点的横距离，并开平方
        y = math.pow(abs(slope_up *(320 - center_point[0])) , 2)  #获取镜头中心与质点的纵距离，并开平方
        dst = math.sqrt(int(+y))
        
        #根据角度分析行进方向
        status = ["true", "left", "right"]
        if slope_up >= 13 or slope_up <= -13:
            #print  slope_up
            return status[0], dst
        elif slope_up > 0:
            #print slope_up
            return status[2], dst
        elif slope_up < 0:
            #print slope_up
            return status[1], dst

        pass

    def drawLine(self, shape, approx):
                #三角形有三个角

        if shape == "rectangle" or shape == "sqaure":
            #嵌套array
            pt1 = tuple(approx[0][0])
            pt2 = tuple(approx[1][0])
            pt3 = tuple(approx[2][0])
            pt4 = tuple(approx[3][0])
            cv2.line(image, pt1, pt2, (0, 255, 0), 3)
            cv2.line(image, pt3, pt2, (0, 255, 0), 3)
            cv2.line(image, pt4, pt3, (0, 255, 0), 3)
            cv2.line(image, pt4, pt1, (0, 255, 0), 3)

        elif shape == "pentagon" :
            #嵌套array
            pt1 = tuple(approx[0][0])
            pt2 = tuple(approx[1][0])
            pt3 = tuple(approx[2][0])
            pt4 = tuple(approx[3][0])
            pt5 = tuple(approx[3][0])
            cv2.line(image, pt1, pt2, (0, 255, 0), 3)
            cv2.line(image, pt3, pt2, (0, 255, 0), 3)
            cv2.line(image, pt4, pt3, (0, 255, 0), 3)
            cv2.line(image, pt4, pt5, (0, 255, 0), 3)
            cv2.line(image, pt5, pt1, (0, 255, 0), 3)

        elif shape == "cross" :
            pt1 = tuple(approx[0][0])
            pt2 = tuple(approx[1][0])
            pt3 = tuple(approx[2][0])
            pt4 = tuple(approx[3][0])
            pt5 = tuple(approx[4][0])
            pt6 = tuple(approx[5][0])
            pt7 = tuple(approx[6][0])
            pt8 = tuple(approx[7][0])
            pt9 = tuple(approx[8][0])
            pt10 = tuple(approx[9][0])
            pt11 = tuple(approx[10][0])
            pt12 = tuple(approx[11][0])
            cv2.line(image, pt1, pt2, (0, 255, 0), 3)
            cv2.line(image, pt3, pt2, (0, 255, 0), 3)
            cv2.line(image, pt4, pt3, (0, 255, 0), 3)
            cv2.line(image, pt4, pt5, (0, 255, 0), 3)
            cv2.line(image, pt5, pt6, (0, 255, 0), 3)
            cv2.line(image, pt7, pt6, (0, 255, 0), 3)
            cv2.line(image, pt7, pt8, (0, 255, 0), 3)
            cv2.line(image, pt9, pt8, (0, 255, 0), 3)
            cv2.line(image, pt10, pt9, (0, 255, 0), 3)
            cv2.line(image, pt11, pt10, (0, 255, 0), 3)
            cv2.line(image, pt12, pt11, (0, 255, 0), 3)
            pass
            pass

    #初始化图形名字并且圈出
    def detect(self, c):
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
            #return shape , approx[0][0], approx[1][0], approx[2][0], approx[3][0]

        elif len(approx) == 5:
            shape = "pentagon"
        else:
            shape = "circle"
        return shape, approx




cap = cv2.VideoCapture(2)
cap.set(3, 640)
cap.set(4, 480)
while(1):
    # get a frame
    ret, frame = cap.read()
    image = frame
    

    # #将格式从BGR——>HSV  HSV颜色区度:https://blog.csdn.net/taily_duan/article/details/51506776
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = hsv[0: 480, 0: 640]

    #设置黑色
    lower_black = np.array([0,0,0])
    upper_black = np.array([255,255,46])
    #分割图像
    kernel = np.ones((2,2),np.uint8)  
    erosion = cv2.erode(hsv,kernel,iterations = 1)
    img = cv2.dilate(erosion, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=4)
    mask = cv2.inRange(img, lower_black, upper_black)



    cv2.imshow("oengzhang", mask)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #给cnts降维，对应相应版本的opencv
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    sd = ShapeDetector()
    for c in cnts:
        #滤掉噪声 (利用面积大小)
        if c.size > 150 :
            print "size: ", c.size
            #以下为垃圾代码
            M = cv2.moments(c)
            #返回得到名字
            shape, approx = sd.detect(c)

            if M["m10"] != 0:
            #表示图像重心
                cX_ = int((M["m10"] / M["m00"]) )
                cY_ = int((M["m01"] / M["m00"]) )
            else :
                cX = cY = 0


            cv2.line(image, (320, 0) , (320, 480) , (0, 0 , 200), 4) 
            #圈出黑线
            sd.drawLine(shape, approx)
            #质心辅助线
            cv2.line(image, (cX_, cY_) , (0, cY_) , (255, 255 , 255), 1) 
            cv2.line(image, (cX_, cY_) , (cX_, 0) , (255, 255 , 255), 1) 
            
            cv2.putText(image, "black line " + shape, (cX_, cY_), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #线的形状
            cv2.line(image, (cX_, cY_) , (cX_, cY_) , (255, 255 , 255), 5)  #描绘出质心
            cv2.putText(image, "position " + str((cX_, cY_)), (cX_, cY_+20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #质心位置


            #避免出现三角形时pos_calc()报错
            if shape == "rectangle" or shape == "square":
                pos_status = ["true", "left", "right"]
                angle_status, dst = sd.pos_calc(approx[0][0], approx[1][0], approx[2][0], approx[3][0], (cX_, cY_))
                #小车跑到右边去啦
                if cX_>340:
                    cv2.putText(image, "Left Off", (340, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  4)  #线的形状
                    cv2.putText(image, "distance " + str(dst), (cX_, cY_+40), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #打印偏移距离
                #小车跑到左边去啦                                                                                                   
                elif cX_ <300:                                                                                                     
                    cv2.putText(image, "Right Off", (340, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  4)  #线的形状       
                    cv2.putText(image, "distance " + str(dst), (cX_, cY_+40), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #打印偏移距离
                else :                                                                                                             
                    #在小车位置未偏离的情况下, 传入数据进行位置分析                                                                    
                    cv2.putText(image, "distance " + str(dst), (cX_, cY_+40), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  2)  #打印偏移距离
                    if angle_status == "true":
                        cv2.putText(image, "Correct direction!", (320, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  4)  
                    elif angle_status == "left":
                        cv2.putText(image, "Go right!", (320, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  4)  
                    elif angle_status == "right":
                        cv2.putText(image, "Go left!", (320, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),  4)  
            else:
                print "None rectangle"
        else:
            print "too fucking small", c.size
        #图像显示
        cv2.imshow("Image", image)

    #cv2.waitKey(0)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
   
