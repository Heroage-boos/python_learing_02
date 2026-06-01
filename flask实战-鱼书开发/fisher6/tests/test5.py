''' 线程隔离
python中如何进行线程隔离？
使用字典来实现线程隔离，每个线程都有自己的字典(使用线程id进行区分)
'''
import threading
import time

from werkzeug.local import Local

class A:
    b = 1

my_obj = Local()
my_obj.b = 1

def  worker():
    print('worker')
    my_obj.b = 2
    print("in new thread b is:" + str(my_obj.b)) #in new thread b is:2


new_t = threading.Thread(target=worker, name= "qiyue_thread")
new_t.start()
time.sleep(1)
# new_t.join()
#主线程
print('in main thread b is :' + str(my_obj.b))  # in main thread b is:1

''' 两次print的结果为什么不一样？
因为my_obj是线程本地对象，每个线程都有自己的my_obj
主线程和新线程是不同的线程，所以它们各自的my_obj是不同的
'''
