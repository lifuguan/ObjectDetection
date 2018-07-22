class Detect_Thread:
    def detect_blue():
        time.sleep(1)
        print("the current threading %s is ended"%(threading.current_thread().name))
        pass

    def detect_yellow():
        time.sleep(2)
        print("the current threading %s is ended"%(threading.current_thread().name))
        pass

    def detect_red():
        time.sleep(6)
        print("the current threading %s is ended"%(threading.current_thread().name))
        pass

    def detect_grren():
        time.sleep(4)
        print("the current threading %s is ended"%(threading.current_thread().name))
        pass
