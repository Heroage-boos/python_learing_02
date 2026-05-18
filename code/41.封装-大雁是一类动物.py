# 定义类 注意：类的名字使用大驼峰命名法
class WildGoose:
    neck = "长长的脖子"
    wing = "宽厚的翅膀"
    leg = "健壮的腿"

    # 实例函数 self是实例对象
    def __init__(self, name):
        self.name = name
        print("大雁的构造函数运行了", self.neck)
    
    
    def fly(self):
        print(self.name,"大雁在飞翔")

print(WildGoose.neck)

# 这样的调用是错误的，一般不这么做
# print(WildGoose.__init__(1))
goose = WildGoose("胖小鹅")  # 胖小鹅 是实例的属性
print(goose.name)
goose.fly()

