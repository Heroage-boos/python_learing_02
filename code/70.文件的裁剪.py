'''文件的的裁剪
使用方法  move('file1', 'target_url')  splitfile(来源文件，目标文件)
'''

#导入包和模块
from shutil import move

#获取路径
import os

abs_path=os.path.dirname(os.path.abspath(__file__))
print('========path',abs_path)  #========path d:\python-app\code

path=os.path.join(abs_path, 'hello3.py')
print('====path',path)
to_path=os.path.join(abs_path,'hello.py')
print('====to_path',to_path)

move(path,to_path)

#提示
print('文件裁剪成功')