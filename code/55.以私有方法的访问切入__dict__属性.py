# __dict__属性

class Father(object):
    __name__="Father"
    #私有方法  当我们在一个类中进行私有方法的声明，python默认对我们的私有方法进行了名称上的修改
    def __knowledge(self):
        print('父亲的知识')

father=Father();
# father.__knowledge();
print(Father.__dict__)

#我们想要获取到一个类中所有属性和方法，包括魔术方法，我们应该怎么办
print('大Father',dir(Father))
print('小Father',dir(father))

'''
['_Father__knowledge', '__class__', '__delattr__', '__dict__', 
'__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', 
'__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__name__',
 '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
 '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__']
'''


'''
演示魔术方法__add__的使用
对于一个类A，我们想要实现对类A的实例的加法运算，需要定义__add__方法
'''
a=1
b=2
# print(a+b)

class A():
    def __init__(self,a):
        self.a=a

    def __add__(self,other):
        print("调用了add方法，但是这里我把加法运算改成了减法运算")
        return self.a - other
        
a=A(a=3);
print(a+6) #-3
print(dir(int))