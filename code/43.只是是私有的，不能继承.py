# 继承


# object类是所有类的祖宗，无论你是否有明确的指定是否继承他，都会默认的继承object
class Father(object):
    _c="这是一个私有属性c" #私有属性
    def __init__(self) :
        print("父类的构造函数运行了!!!")
    
    #写在类中的函数我们叫方法
    def many_money(self) :
        print("dad钱很多")

    def run(self) :
        print("dad会跑")


    __name='layi'
    #私有方法
    def __knowleger(self):
        print("dad的知识")

#继承  
class Son(Father): #多继承使用逗号分隔 相同方法或属性子类会继承写在前面的
    def __init__(self) :
        Father.__init__(self) # 显式调用第一个父类的构造函数
        print("子类的构造函数运行了!!!")


father = Father()

# 在子类没有明确调用自己的构造函数时，那么默认会调用父类的构造函数
son = Son()
son.many_money()

print(Son._c)
son.__knowleger()# 父类的私有方法不能被子类继承
print(Son.__name)# 父类的私有属性不能被子类继承