#法定结婚年龄的限制，比如男22岁，女20岁

class AgeError(Exception):...
    # pass

class Person():
    def set_age(self,age):
        raise AgeError("你必须覆盖set_age方法,进行你自己的年龄控制")

class boy(Person):
    def set_age(self,age):
        if age<22:
            raise AgeError("男孩的法定结婚年龄是22岁")
        else:
            self.age=age

class girl(Person):
    def set_age(self,age):
        if age<20:
            raise AgeError("女孩的法定结婚年龄是20岁")
        else:
            self.age=age


b=boy()
b.set_age(18)
g: girl=girl()
g.set_age(age=19)

