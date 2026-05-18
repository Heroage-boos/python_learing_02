# 继承


# object类是所有类的祖宗，无论你是否有明确的指定是否继承他，都会默认的继承object
class Father(object):

    def __init__(self) :
        print("父类的构造函数运行了!!!")
    
    def many_money(self) :
        print("dad钱很多")

    def run(self) :
        print("dad会跑")

class Mather(object):
    # def __init__(self) :
    #     print("mather的构造函数运行了!!!")
    
    def face(self) :
        print("脸很漂亮")
    
    def run(self) :
        print("mom会跑")


#继承  
class Son(Father,Mather): #多继承使用逗号分隔 相同方法或属性子类会继承写在前面的
    def __init__(self) :
        Father.__init__(self) # 显式调用第一个父类的构造函数
        print("子类的构造函数运行了!!!")


father = Father()

# 在子类没有明确调用自己的构造函数时，那么默认会调用父类的构造函数
son = Son()
son.many_money()
son.face()
son.run()  #父类有同样的方法，子类会继承写在前面的

#属性和方法的继承是一样的