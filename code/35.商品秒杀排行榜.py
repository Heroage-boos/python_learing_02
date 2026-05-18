'''
需求理解
有列表结构如下:goods_info=[("水杯",12.5,25),("西装",1280,3689),("电脑",7800,13800),("摄像头",248.8,349)]
第一列代表商品名称，第二列代表商品折扣价格，第三列代表商品原价

请按照商品折扣数进行从小到大排序
'''

goods_info=[("水杯",12.5,25),("西装",1280,3689),("电脑",7800,13800),("摄像头",248.8,349)]

#商品折扣率 =  商品原价/商品折扣价格 


#比如我们要计算一个圆形的面积   π*r*r
#方式1：
import math
def circle_area(r):
    return math.pi*r*r

print(circle_area(10))

#使用lambda 表达式 格式1
circle_area2 = lambda r:math.pi*r*r
print(circle_area2(10))

def calc_func(o):
    if o=='+':
        return lambda x,y:x+y
    elif o=='-':
        return lambda x,y:x-y
    elif o=='*':
        return lambda x,y:x*y
    elif o=='/':
        return lambda x,y:x/y
    else:
        raise Exception('不支持的运算')

#格式2
f=calc_func("+")
print(f) #<function calc_func.<locals>.<lambda> at 0x00000234762EB530>
print(f(10,20)) #30


#排序
l=[1,2,3,-1,4,3]
l.sort()
print("正序排序",l)
l.sort(reverse=True)
print("倒序排序",l)

l2= [(1,-3),(2,0),(2,-2),(1,1)]
l2.sort()
print(l2)

def func(p):
    return  p[1]

#从小到大排序 key按照函数返回值来排序
l2.sort(key=func)
print(l2)

#从大到小排序
l2.sort(key=func,reverse=True)
print(l2)