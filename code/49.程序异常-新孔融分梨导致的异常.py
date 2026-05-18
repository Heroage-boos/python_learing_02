# 异常
'''
什么是异常：
异常指的是程序在执行过程中遇到的问题

每个特定 错误都对应一个异常类对象
'''

def division():
    print("孔融开始分梨了")
    count=int(input("请输入一共有几个梨:\n"))
    person=int(input("请输入要分给几个人:\n"))
    #异常1 如果都输入0 ZeroDivisionError: division by zero
    if person==0 and count==0:
        print("小朋友的数量不能小于等于0")
        exit(0)  #退出程序
        # raise ZeroDivisionError

    #异常2 如果总数梨或人数是小数 ValueError: invalid literal for int() with base 10: '4.5'
    elif isinstance(person,float) or isinstance(count,float):
        print("人和梨必须是整数")
        exit(0)
    result=count/person  

    print("每个人平均分{}个梨".format(result))

division()
