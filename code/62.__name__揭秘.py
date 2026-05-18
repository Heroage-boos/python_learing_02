
if __name__ == '__main__':
    print("你好世界!")


#__main __一般来说代表找一个程序运行的入口 main.PY
print(__name__)

from time_utils import my_time
print(__name__)  # time_utils

from db_utils.db import my_db
my_db() #db_utils.db

# 当我们直接运行__name__ 这个变量所在的文件（模块）的时候，__name__ 为 __main__
# 当我们把__name__ 这个变量所在的文件（模块）作为别人的包导入的时候，__name__ 为 文件（模块）的名称



#我们一般在主入口文件（模块）中写一些测试代码或示例代码，然后在主入口文件（模块）中将__name__ == __main__ 括起来
#这样别人如果只导入我们的模块而不运行的时候，就不会执行到测试代码,判断这个文件是不是主入口文件
if __name__ == '__main__':
    print('hello world')