"""
第一次输入一个数字，然后输入一个操作费 ，然后输入一个数字
然后输出结果
"""

operator_num = 0
input_num = 0
while True:
    if operator_num > 0 and input_num != 0:
        print("输入c,计算器清零，重新开始计算:")
        print("输入d,基于上一次计算结果，进行计算:")
        print("输入n,结束:")
        operator = input("请输入选择：\n")
        if operator == "c":
            input_num = 0
            continue
        if operator == "d":
            op: str = input("请输入一个操作符：")
            reset_num_2 = float(input("请输入第二个数字:"))
            if op == "+":
                input_num += reset_num_2
            elif op == "-":
                input_num -= reset_num_2
            elif op == "*":
                input_num = input_num * reset_num_2
            elif op == "/":
                input_num = input_num / reset_num_2
            else:
                print("输入错误")
                continue
            print(f"结果为{input_num}")
            operator_num += 1
        if operator == "n":
            break

    else:
        # 记录上一次的计算结果
        num_1: float = float(input("请输入第一个数字:"))
        op: str = input("请输入一个操作符：")
        num_2 = float(input("请输入第二个数字:"))
        if op == "+":
            input_num = num_1 + num_2
        elif op == "-":
            input_num = num_1 - num_2
        elif op == "*":
            input_num = num_1 * num_2
        elif op == "/":
            input_num = num_1 / num_2
        else:
            print("输入错误")
            continue
        print(f"结果为{input_num}")
        operator_num += 1
