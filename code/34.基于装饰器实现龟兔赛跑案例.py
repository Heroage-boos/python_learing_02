"""
使用装饰器统计兔子函数和乌龟函数的运行时间

兔子每跑5米则随机休息1到10秒乌龟每跑1米则固定休息1秒
最后统计兔子函数和乌龟函数的运行时间:

"""

# 导入一个随机的工具，这里是导入随机模块
import random

# 导入时间工具
import time

# 定义一个跑道的长度
track_length = 10


# 定义装饰器
def runtime_log(type):
    def runtime(func):
        def inner():
            print("开始运行%s" % type)
            # 开始时间
            start_time = time.time()
            func()
            end_time = time.time()
            print("%s运行了%.2fs" % (type, end_time - start_time))

        return inner

    return runtime

@runtime_log("乌龟")
def wugui():
    for i in range(1, track_length + 1):
        print("乌龟跑到了第%d米" % i)
        time.sleep(1)
    print("乌龟跑完啦！")


@runtime_log("兔子")
def defiba():
    for i in range(1, track_length + 1):
        if i % 5 == 0:
            time.sleep(random.randint(1, 10))
        print("兔子跑到了第%d米" % i)
    print("兔子跑完啦")

wugui();
defiba();