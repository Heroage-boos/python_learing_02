#日志的打印

#演变1
'''
def print_log(func):
    print("装饰器",func.__name__)
    def inner(x,y):
        print("开始执行函数",x,y)
        return func(x,y)
    return inner

@print_log
def func_1(a,b):
    print("函数1运行")


func_1(1,2)
'''

'''
# 演变2
def print_log(func):
    print("装饰器",func.__name__)
    def inner(x,y):
        print("参数的列表是",x,y)
        return func(x,y)  #如果不返回值，外部无法获取到函数的返回值
    return inner

@print_log
def func_1(a,b):
    print("函数1运行")
    return a+b


value1= func_1(10,20)
print(value1)
'''

'''
# 演变3  需要支持任意变换装饰器都不会报错
def print_log(func):
    print("装饰器",func.__name__)
    def inner(*args,**kwargs):  #一个*表示可以传入任意个位置参数，*args表示位置参数的tuple，**kwargs表示关键字参数的dict
        print("参数的列表是",args,kwargs)
        return func(*args,**kwargs)  #如果不返回值，外部无法获取到函数的返回值
    return inner

@print_log
def func_1(a,b,c,d,e=2,f=2):
    print("函数1运行")
    return a+b+c+d

value1= func_1(10,20,30,40,e=1,f=2)
print(value1)
'''


# 演变4  
def print_log(func):
    print("装饰器222",func)
    def inner(*args,**kwargs):  #一个*表示可以传入任意个位置参数，*args表示位置参数的tuple，**kwargs表示关键字参数的dict
        print("参数的列表是",args,kwargs)
        return func(*args,**kwargs)  #如果不返回值，外部无法获取到函数的返回值
    return inner
def  print_log(type):
    print("装饰器",type)
    def decorator(func):
        print("装饰器",func)
        def inner(*args,**kwargs):  #一个*表示可以传入任意个位置参数，*args表示位置参数的tuple，**kwargs表示关键字参数的dict
            print("参数的列表是",args,kwargs)
            return func(*args,**kwargs)  #如果不返回值，外部无法获取到函数的返回值
        return inner
    return decorator

@print_log("控制台")
def func_1(a,b,c,d,e=2,f=2):
    print("函数1运行")
    return a+b+c+d

value1= func_1(10,20,30,40,e=1,f=2)
print(value1)