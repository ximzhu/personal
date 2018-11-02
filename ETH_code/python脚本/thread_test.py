import threading
import time
class mythread(threading.Thread):
    def __init__(self,threadname):
        threading.Thread.__init__(self,name=threadname)
        #self.threadname = threadname
    def run(self):
        global x
        lock.acquire()
        x = x+1
        print x
        #time.sleep(1)
        lock.release()

if __name__ == '__main__':
    lock = threading.RLock()
    t1 = []
    x = 0
    
    for i in range(5):
        t = mythread(str(i))
        t1.append(t)
        
    for i in t1:
        i.start()
