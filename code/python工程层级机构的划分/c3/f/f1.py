class FC():
    def __init__(self):
        print("我是FC的构造函数")

    def fc_fun1(self):
        print("我是F1中fc的实例方法")
        
    @staticmethod
    def fc_fun2():
        print("我是FC的静态方法")
        
    @classmethod
    def fc_fun3(cls):
        print("我是FC的类方法"), 


def ff():
    print("我是f1,中的ff函数")