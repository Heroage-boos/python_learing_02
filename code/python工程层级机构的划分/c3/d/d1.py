class DC():
    def __init__(self):
        print("我是DC的构造函数")

    def fc_fun1(self):
        print("我是D1中fun1的实例方法")

    def fc_fun2(self):
        print("我是D1中fun2的实例方法")
        
    @staticmethod
    def fc_fun2():
        print("我是d1的静态方法")
        
    @classmethod
    def fc_fun3(cls):
        print("我是DC的类方法"), cls


def df():
    print("我是d1,中的dd函数")