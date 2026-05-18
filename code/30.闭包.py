#闭包  函数嵌套函数,一个函数的返回值也可以是一个函数

def func_a():
    print("我是函数1")

    def func_b():
        print("我是函数2 内部函数")
        return 111
    return func_b()

# func_a= func_a()
print(func_a())


#闭包
#如果我们有一个函数，让它可以任意的计算一个值的任意次幂   a**b

def warpper(exponent):
    def exponent_of(base):
        return base**exponent
    return exponent_of

#计算一个函数的平方
square=warpper(2)
print(square(2))  # 2的二次方
print(square(3))  # 3的二次方
print(square(4))  # 4的二次方


