'''
有数据如下:
student_name=["李元修"，"李建国""白敬亭"，"莫怀雨"，"谢起云"，"夏亭晚"，"徐时芳"，"李清安"，"李元斐"，"李拥军"]
请将所有姓李的同学筛选出来
'''

from typing import Any


student_name=["李元修","李建国","白敬亭","莫怀雨","谢起云","夏亭晚","徐时芳","李清安","李元斐","李拥军"]

has_in_name=[]

# for  name in student_name:
#     if name[0]=="李":
#         has_in_name.append(name)
        
# print(has_in_name)

#使用 startswith 方法   startswith字符串的开始判断
for name in student_name:
    if name.startswith("李"):
        has_in_name.append(name)
print(has_in_name)

#filter 过滤
has_in_name_2=filter(lambda x:x.startswith("李"),student_name)
print(list(has_in_name_2))