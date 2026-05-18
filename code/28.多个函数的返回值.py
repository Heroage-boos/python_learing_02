


def calc(a,b):
    a+=1
    b+=1
    return a,b

r=calc(1,2)
r1,r2=calc(1,2)
print (r)


#如果我只需要返回值的其中一部分怎么办  位置参数
r1, _ = calc(1,2)
print (r1)


#不定长参数
def  func(*args):
    print(args)

func(1,2,3,4,5)
func("a","b","c")
func([1,2,3],[4,5,6])

#可变参数
def func1(**kwargs):
    print(kwargs)
print("可变参数")
func1(a=1,b=2)
func1(name="tom",age=20)
func1(a=[1,2,3],b=[4,5,6])
