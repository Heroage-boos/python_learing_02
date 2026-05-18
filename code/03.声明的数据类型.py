a:int =1 # 整数类型
print("a is",type(a)) # type函数可以用来获取变量的数据类型

b=1.1
print("b is",type(b))

c=True
print("c is",type(c))

d='hello world'
print(f"d is {d[0]}{d[1]}{d[2]}{d[3]}{d[4]}",type(d))


e=None
print("e is",type(e))

# 打印类型的具体 比如  <class 'NoneType'>  输出  NoneType， <class 'bool'> 输出 bool ...
print(type(None),type(False),type(True),type(1),type('str'),type(1.1),type([1,2]))
# <class 'bool'>  输出  bool
print(type(None).__name__,type(False).__name__,type(True).__name__,type(1).__name__,type('str').__name__,type(1.1).__name__,type([1,2]).__name__)
