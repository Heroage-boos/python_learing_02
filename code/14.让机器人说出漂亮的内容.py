# 字符串的格式化
# i = "python web开发"
from pickletools import read_uint2


i: str=input("请输入你想要学习的课程名称：")
s ="我来学习**%s**课程" % i   #字符串使用%s
print(s)
'''
字符串使用%s
字符串使用%d
字符串使用%f
'''
s2 ="我来学习**%s**课程，课程编号为**%d**" % (i,1)
print(s2)

r="跟着{0}学{1},{0}学习了{2}小时".format('小明同学','python',20)
r2=f"跟着{0}学{1},{0}学习了{2}小时".format('小明同学','python',20)

print(r)
print(r2)


#保留小数点后两位
x=3.1415926
print(f"保留小数点后两位：{x:.2f}")
print("保留小数点后两位：{:.2f}".format(x))

print("保留小数点后两位和正数符号：{:+.2f}".format(+3.55555))


