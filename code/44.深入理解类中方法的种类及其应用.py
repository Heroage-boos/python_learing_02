#类中的一些方法和的应用
class  person():

    def __init__(self):
        self.name="long"
        self.age=20

    def runing(self):
        print("人正在跑步")

    #类方法  类方法可以使用类名直接调用，一般的方法必须使用实例化对象进行调用
    @classmethod
    def eat(cls,food):
        print("吃{}".format(food))
    
    #静态方法   静态方法实际上是与这个类没有什么关系的一个方法
    @staticmethod
    def sleep(inf):
        print("睡觉")

    #比如我们在一个类中有一个私有变量，我想要外部可以操作这个变量，但是不能直接操作，我们就需要用到property
    __age=18
    @property  #property装饰器会使一个方法变为一个变量 man.age访问
    def age(self):
        return self.__age
    @age.setter
    def age(self,value):
        if value<18:
            raise ValueError("年龄太小了")
        else:
            self.__age=value
    @age.getter
    def age(self):
        if(self.__age<18):
           print("太小了")
        else:
            return self.__age


man=person()
man.runing()
man.eat("大米") 

print(man.age)
man.sleep("晚安")