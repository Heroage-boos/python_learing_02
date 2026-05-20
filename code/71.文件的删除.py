'''导入包与模块
from os import remove

def delete_file(file_path):
    try:
        remove(file_path)   # remove(目标文件)
    except FileNotFoundError:
        pass
'''