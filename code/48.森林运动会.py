# 森林运动会
import threading
import time
import random

# 声明一个变量，存储最终的名名次
ranking = []
# 声明一个变量，用来存储比赛的距离
distance = 100

def run_method(run_distance, max_sleep_time):
    for i in range(distance):
        # 获取当前线程
        current_thread = threading.current_thread()
        # 每一个动物休息的时间都不同
        if i % run_distance == 0 and i != 0:
            sleep_time = random.randint(1, max_sleep_time)
            print(f"{current_thread.name}休息了{sleep_time}秒")
            time.sleep(sleep_time)
        print(f"{current_thread.name}跑到了第{i+1}步")
    ranking.append(current_thread.name)
    print(f"{current_thread.name}完成比赛！")

#定义兔子线程类
class RabbitThread(threading.Thread):
    def run(self):
        run_method(5, 10)

#乌龟
class TortoiseThread(threading.Thread):
    def run(self):
        run_method(1, 2)

#大象
class ElephantThread(threading.Thread):
    def run(self):
        run_method(3, 6)

if __name__ == "__main__":
    rabbit = RabbitThread(name="兔子")
    tortoise = TortoiseThread(name="乌龟")
    elephant = ElephantThread(name="大象")
    rabbit.start()
    tortoise.start()
    elephant.start()

    rabbit.join()
    tortoise.join()
    elephant.join()
    
    print("比赛结束")
    print(f"最终排名：{ranking}")


