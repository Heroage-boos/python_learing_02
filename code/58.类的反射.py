'''
类的反射
反射指的是对象具有检测、访问、修改自身属性的能力

反射本质上就是在使用四个内置函数，然后对属性进行增删改查

'''
class Web:
    def index(self):
        print("我是首页")
        
    def login(self):
        print("我是登录页面")

web=Web();

#检测
hasattr(web,"index")
hasattr(web,"home")

print(hasattr(web,"index")) #True
print(hasattr(web,"home"))  #False
print(dir(web))

#访问
page=input("请输入你想要去的页面")
getattr(web,page)
if hasattr(web,page):
    getattr(web,page)()
else:
    print("不存在该页面")

#修改
setattr(web,'login',lambda :print('我是新的登录页'))

#删除
delattr(web,'login')