#return
# def func():
#     return 1
# a=func()
# print(1)


# yield 生成器
from multiprocessing import process
from typing import Any, Generator, Literal


def func_2():
    print("开始执行")
    yield 1
    print("执行完毕")
    yield 3
a=func_2()
print('aaaa',a)
# print(a.__next__())
# print(a.__next__())

for i in a:
    print(i)
# print(a.__next__())  #停止迭代




def func_3():
    num = yield 1
    # print('num1',num)
    num1 = yield num + 10
    # print('num2',num1)

f3=func_3();
print(f3)
r1=f3.send(None)
print('None',r1)
r2=f3.send(10)
print('f3.send2',r2)
# r3=f3.send(3)
# print('f3.send3',r3)


#生产者与消费者的案例
def customer():
    while True:
       n: Any=yield 
       if not n:
            return 
       print(f'消费了{n}号包子')

# 生产者代码
def product(c):
    # 消费者的生成器
    c.send(None)
    #假设 每天生产5个包子
    for i in range(5):
        print(f'生产了{i+1}号包子')
       #我们告诉新消费者可以消费了
        c.send(str(i+1))

c = customer()
product(c)
