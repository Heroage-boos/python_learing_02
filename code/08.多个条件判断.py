'''
and（和） 和    or（或） 的使用
'''
from this import d


a=2
b=3
c=10
d=10

if a>=b and c==d:
    print("a 等于 b 并且 c 等于 d")
elif a>=b or c==d:
    print("a 大于等于 b 或者 c 等于 d")
else:
    print("没有匹配到条件")

print("程序运行结束")