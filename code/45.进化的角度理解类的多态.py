#多态
class  Animal():
    def action(self):
        print("动物有一些行为")
        pass

class Duck(Animal):
    def action(self):
        print("quack")

class Cat(Animal):
    def action(self):
        print("miao")

duck=Duck()
cat=Cat()
animal=Animal()

duck.action()
cat.action()
animal.action()

#多态的使用形式
i= [duck,cat]

for i in i:
    i.action()