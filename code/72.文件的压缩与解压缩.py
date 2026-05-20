'''文件压缩与解压缩
from shutil import make_archive

def compress_file(file_path, output_path):
    make_archive(output_path, 'zip', root_dir=file_path)

#压缩
make_archive(压缩之后的文件名，压缩后缀，希望压缩的文件或者目录)

#解压缩
import shutil import unpack_archive

unpack_archive(压缩文件路径，解压后的位置) 
'''

from shutil import make_archive, unpack_archive
from zipfile import ZipFile

#要压缩/解压的文件路径
from os  import path
import os

abs_path=path.dirname(path.abspath(__file__))
in_pack_path: str=path.join(abs_path,"hello")

# 压缩
make_archive(in_pack_path, 'zip',abs_path)

# 解压缩
unpack_path_target=path.join(abs_path,"hello.zip")
unpack_path=path.join(os.getcwd(),'hello')  
unpack_archive(unpack_path_target, unpack_path)

#删除
os.remove(unpack_path_target)

