#抛出异常
#raise

class AgeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        msg=args[0]
        self._msg=msg
        print(msg)
    

class Person():
    __age=0

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self,value):
        if value<0 or value>120:
            # raise ValueError('年龄不合法')
            raise AgeError('年龄不合法')
        else:
            self.__age=value
    
    @age.getter
    def age(self):
        if(self.__age<0 or self.__age>120):
            # print('非法年龄')
            raise AgeError('非法年龄')
        else:
            return self.__age

try:
    p=Person()
    p.age=-9
    print(p.age)
# except Exception as e:
#     print(e)
except AgeError as a:
    print(a)
# except UserError as e:  #可以设置其他异常抛出
#     print(e)
finally: #无论代码是否发生异常都会执行
    print('资源清除')