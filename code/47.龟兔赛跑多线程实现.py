import random
import threading  #threading 线程

# from 导入的是一个类  import 导入的是一个模块


# 龟兔赛跑多线程实现
track_length = 100


# 兔子跑的函数
def rabbit_run():
    for i in range( track_length):
        # 兔子每跑五米休息一下 1-10秒
        if i % 5 == 0:
            sleep_time = random.randint(1, 10)
            print("兔子休息了{}秒".format(sleep_time))
        print("兔子跑到第{}米".format(i))
    print("rabbit完成比赛！")
        
# 乌龟跑的函数
def tortoise_run():
    for i in range( track_length):
        # 乌龟每跑三米休息一下 1-5秒
        if i % 3 == 0:
            sleep_time = random.randint(1, 5)
            print("乌龟休息了{}秒".format(sleep_time))
        print("乌龟跑到第{}米".format(i))
    print("乌龟完成比赛！")
 

rabbit_thread = threading.Thread(target=rabbit_run)
tortoise_thread = threading.Thread(target=tortoise_run)
#启动两个线程
rabbit_thread.start()
tortoise_thread.start()
#join 方法会阻塞主线程，直到括号中的子线程执行完毕
rabbit_thread.join()
tortoise_thread.join()