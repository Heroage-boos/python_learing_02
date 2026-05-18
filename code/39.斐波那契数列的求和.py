'''
生成一个1000以内的斐波那契数列
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
然后求列表里所有数字的和
'''

#reduce函数
from functools import reduce
#import functools
#functools.reduce

arr=[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
sum=0;
# for i in arr : 
#     sum=i+sum
# print("sum=%d" % sum)


#使用reduce函数解决
def add(x,y):
    print("%d+%d" % (x,y))
    return x+y

#reduce返回的是一个值
result = reduce(add, arr,10) #2583
print("sum=%d" % result)
print(reduce(lambda x, y: x + y, arr))

# reduce使用场景：计算总和 ； 计算乘积  ；找最大值/最小值  ；字符串连接等
#计算乘积
print(reduce(lambda  x,y:x*y,arr))
#找最大值
print(reduce(lambda x,y:x if x>y else y, arr))
#找最小值
print(reduce(lambda x,y:x if x<y else y, arr))




