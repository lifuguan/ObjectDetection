#-*- coding:utf-8 -*-
import cv2
import threading
import time
def target():
    print("the current threading %s is runing"%(threading.current_thread().name))
    time.sleep(1)
    print("the current threading %s is ended"%(threading.current_thread().name))
print("the current threading %s is runing"%(threading.current_thread().name))
## 属于线程t的部分
t = threading.Thread(target=target)
t.start()
## 属于线程t的部分
t.join() # join是阻塞当前线程(此处的当前线程时主线程) 主线程直到Thread-1结束之后才结束


def target1():
    print("the current threading %s is runing"%(threading.current_thread().name))
    time.sleep(3)
    print("the current threading %s is ended"%(threading.current_thread().name))
t1 = threading.Thread(target=target1)
t1.start()
t1.join()

print("the current threading %s is ended"%(threading.current_thread().name))