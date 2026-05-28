''' 线程隔离
python中如何进行线程隔离？
使用字典来实现线程隔离，每个线程都有自己的字典(使用线程id进行区分)
'''

class A:
    b = 1

my_obj = A()

def  worker():
    print('worker')
    my_obj.b = 2

import threading
import time

new_t = threading.Thread(target=worker, name= "qiyue_thread")
new_t.start()
time.sleep(1)
# new_t.join()
#主线程
print(my_obj.b)  # 2