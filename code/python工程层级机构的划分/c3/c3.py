print("我是c3的入口")

#没有找到包  说明imort导入的时候，最后边只能写到模块
# import f.f1.ff  #ModuleNotFoundError: No module named 'f.f1.ff'; 'f.f1' is not a package
# ff()

#导入f1模块
import f.f1 as f1
#使用模块去调用函数
f1.ff()
#使用模块去调用类
ff1=f1.FC()
ff1.fc_fun1()

#当我们使用from导入的时候
#from后面是模块中的属性或者方法
#后面再跟上import 关键字
#在import 后面可以跟多个属性或者方法，用逗号隔开 类的名称或者是函数的名称
from f.f1 import FC,ff
fc=FC()
fc.fc_fun1()
ff()
