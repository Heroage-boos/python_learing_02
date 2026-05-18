#自定义异常

class Person():
    pass

person=Person();

print(person) #<__main__.Person object at 0x0000029FD1848AD0>


#比如我们有一个系统，对系统年龄的设置限制到必须18岁以上，如果不是这样我们将抛出以下异常
class AgeError(Exception):# 自定义异常
    def __init__(self, msg):
        self.message = msg
        super().__init__(self.message) # python3.6以上 必须要继承Exception，否则会报错

age_error=AgeError("年龄错误")
print(age_error)  # 空白  