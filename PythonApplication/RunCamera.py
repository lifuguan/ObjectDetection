# -*- coding: utf-8 -*- 

import cv2



if __name__=='__main__':
    cap = cv2.VideoCapture(1)
    force = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter()
    while True:
        if cap.isOpened() == True: 
            ret, frame = cap.read()
            if ret == True:
                out.write(frame)
                cv2.imshow("Video", frame)

        else :
            print "can not found"




