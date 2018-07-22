## -*- coding:utf-8 -*-

#import cv2
#import numpy as np

#"""
#功能：读取一张图片，显示出来，转化为HSV色彩空间
#     并通过滑块调节HSV阈值，实时显示
#"""

#image = cv2.imread('C:\\Users\\10027\\source\\repos\\ObjectDetection\\PythonApplication\\RoboSample\\mix\\real1.jpg') # 根据路径读取一张图片
#cv2.imshow("BGR", image) # 显示图片

#hsv_low =  np.array([100,43, 125])
#hsv_high = np.array([124,255,155])

## 下面几个函数，写得有点冗余

#def h_low(value):
#    hsv_low[0] = value

#def h_high(value):
#    hsv_high[0] = value

#def s_low(value):
#    hsv_low[1] = value

#def s_high(value):
#    hsv_high[1] = value

#def v_low(value):
#    hsv_low[2] = value

#def v_high(value):
#    hsv_high[2] = value

#cv2.namedWindow('image')
#cv2.createTrackbar('H low', 'image', 0, 255, h_low) 
#cv2.createTrackbar('H high', 'image', 0, 255, h_high)
#cv2.createTrackbar('S low', 'image', 0, 255, s_low)
#cv2.createTrackbar('S high', 'image', 0, 255, s_high)
#cv2.createTrackbar('V low', 'image', 0, 255, v_low)
#cv2.createTrackbar('V high', 'image', 0, 255, v_high)

#while True:
#    dst = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # BGR转HSV
#    dst = cv2.inRange(dst, hsv_low, hsv_high) # 通过HSV的高低阈值，提取图像部分区域
#    cv2.imshow('dst', dst)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#cv2.destroyAllWindows()

import cv2
import numpy as np
import imutils

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


cap = cv2.VideoCapture(1)
while(1):
    # get a frame
    ret, frame = cap.read()
    image = frame
    
    ratio = image.shape[0] / float(image.shape[0])

    # #将格式从BGR——>HSV  HSV颜色区度:https://blog.csdn.net/taily_duan/article/details/51506776
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
   
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
    #分割图像
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    kernel = np.ones((5,5),np.uint8)  
    erosion = cv2.erode(mask,kernel,iterations = 1)
    img = cv2.dilate(erosion, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=16)

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


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   