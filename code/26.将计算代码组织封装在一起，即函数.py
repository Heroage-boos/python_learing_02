# 了解一下函数的基本特点
#在内存中开辟了一块独立的空间，一遍提供后续调用

#我们自己声明一个函数

def fun_1():
    print("hello world")

fun_1()

#尝试封装BMI体重计算
def bmi_calculate(stong,height_1):
    #让输入体重 身高
    #类型转换  考虑单位，校验是否是数字类型
    stong: float=float(stong)

    # 考虑单位，校验是否是数字类型
    if float(stong) < 5 or float(height_1)<0.3:
        print("体重或身高不符合要求")

    height_2=height_1
    #类型转换  考虑单位，校验是否是数字类型
    height_1=float(height_1)
    height_2=float(height_2)

    #计算出BMI指数
    BMI=stong / (height_1*height_2)
    print(f"BMI值为{BMI}")

    #根据需求考虑使用if if 还是 elif
    # 1、当测量者的BMI指数小于18.5时，认为他的体重过轻
    if BMI < 18.5:
        print("体重过轻")
    # 2、当测量者的BMI指数大于等于18.5，且小于24时，认为他的体重正常
    elif(BMI>=18.5 and BMI<24):
        print("体重正常")
    # 3、当测量者的BMI指数大于等于24，且小于等于28时，认为他的体重过重
    elif BMI >=24 and BMI <=28:
        print("体重过重")
    # 4、当测量者的BMI指数大于28时，认为他的体重属于肥胖行列
    elif BMI > 28:
        print("体重肥胖")
    else:
        print("计算失败！请重新输入!")


stong=input("请输入体重，单位千克\n")
height_1=input("请输入您的身高，单位米")
bmi_calculate(stong,height_1)
