# 类方法的动态添加

class Person():
    def __init__(self, a,b):
        self.a = a
        self.b = b

    def run(self):
        print('run method')

def eat(number):
    print('eat method',number)

person = Person(1,2)

#第一种添加方法的方法 魔术方法，可以用户自定义
person.__setattr__("eat1",eat)
e=person.__getattribute__("eat1")  
e(1) #'eat method'

print("=======查看类的所有属性和方法",dir(person))

#第二种添加方法的方法
person.eat2=eat
print(dir(person))
person.eat2(2)