'''文件的复制

'''

#导入包与模块
from shutil import copy
# 导入os模块
import os

#设置路径 相对路径
# path = r'./hello.py'

# 设置路径 绝对路径  getcwd() os.getcwd() 返回的是 D:\python-app
path = os.path.join(os.getcwd(), 'hello.py')
print('path.getcwd()======',path)  # D:\python-app\hello.py

# 使用脚本所在目录作为基础路径，而不是当前工作目录
script_dir = os.path.dirname(os.path.abspath(__file__))
print('script_dir========',script_dir)  #d:\python-app\code

abc_path = os.path.join(script_dir, 'hello.py')
print('abc_path========',abc_path)  #d:\python-app\code\hello.py
target_path = os.path.join(script_dir, 'hello2.py')
print('target_path========',target_path)  #d:\python-app\code\hello2.py

#使用方法
# copy('file1', 'target_url')  copy(目标文件，目标地址)
#返回x的浅拷贝。
copy(abc_path, target_path)

#提示
print('文件复制成功！')


