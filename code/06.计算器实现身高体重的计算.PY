'''
需求描述：孩子的身高=(父亲的身高+母亲的身高)*0.54
'''

#让用户输入父亲的身高
father_height=input("输入父亲的身高：")
#校验输入的内容是否为数字
try:
    float(father_height)
except ValueError:
    print("输入的不是数字，请重新输入")
    exit()

#输入母亲的身高
mom_height=input("输入母亲的身高：")

#计算孩子的身高
child_height=float(father_height)+float(mom_height)*0.54

#输出结果
print("孩子的身高是：",child_height)

