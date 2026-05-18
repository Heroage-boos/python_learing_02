# 异常
"""
什么是异常：
异常指的是程序在执行过程中遇到的问题

每个特定 错误都对应一个异常类对象
"""





def division():
    while True:
        print("孔融开始分梨了")
        try:
            count = int(input("请输入一共有几个梨:\n"))
            person = int(input("请输入要分给几个人:\n"))
            result = count / person
            print("每个人平均分{}个梨".format(result))

        # except Exception as e:  #捕获所有异常
        #     print("发生异常了!",e)

        except ValueError:  # 明确捕获异常
            print("输入有误，请输入数字！")
            break  # 结束循环

        except ZeroDivisionError:  # 明确捕获异常
            print("不能除以0")

division()
