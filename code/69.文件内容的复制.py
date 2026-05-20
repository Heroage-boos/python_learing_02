'''文件内容复制
使用方法  copyfile('file1', 'target_url')  copyfile(来源文件，目标文件)
'''

#导入包和模块
from shutil import copyfile


#设置路径
import os
#获取到当前目录的地址
abs_path=os.path.dirname(os.path.abspath(__file__))
print('========path',abs_path)  #========path d:\python-app\code

path: str=os.path.join(abs_path,'hello.py')
print('====path',path)
target_path=os.path.join(abs_path,'hello2.py')
print('====target_path',path)

#使用方法  
copyfile(path, target_path)

print('文件内容复制成功')
