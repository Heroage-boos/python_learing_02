class Person():
    def __init__(self, a,b):
        self.a = a
        self.b = b

    def say_hi(self):
        print('Hello, my name is', self.name)


p = Person(1,2)
print (p.a, p.b)

c=input("请输入你想要添加的属性名称")
d=input("请输入你想要添加的属性值")

p.__setattr__(c,d) #添加属性值
result=p.__getattribute__(c)  # 获取属性值
print(result)