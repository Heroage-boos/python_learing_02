
#字符串 ↔ 数字转换
num_str=   "123.5555555555"
num_str2=   "123"
# num_int=int(num_str) #会报错 ValueError: invalid literal for int() with base 10: '123.55555'
num_int = int(float(num_str2))
num_float= float(num_str)
print(f"字符串{num_str}转数字",num_int,num_float)

num=111
str_num=str(num)
print(f"数字{num}转字符串",str_num)

# 字符串转列表
text = "hello world"
words = text.split()          # ["hello", "world"]
chars = list(text)            # ["h", "e", "l", "l", "o", " ", "w", "o", "r", "l", "d"]

# 列表转字符串
words = ["hello", "world"]
text = " ".join(words)        # "hello world"
text = ",".join(words)        # "hello,world"

# 列表转集合去重
numbers = [1, 2, 2, 3, 3, 4]
unique_numbers = list(set(numbers))  # [1, 2, 3, 4]

# 字典转列表
data = {"a": 1, "b": 2}
keys = list(data.keys())      # ["a", "b"]
values = list(data.values())  # [1, 2]
items = list(data.items())    # [("a", 1), ("b", 2)]

# 列表转字典
keys = ["a", "b"]
values = [1, 2]
data = dict(zip(keys, values))  # {"a": 1, "b": 2}

import json

# Python对象 → JSON字符串
data = {"name": "张三", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)  # 中文不转义

# JSON字符串 → Python对象
json_str = '{"name": "张三", "age": 25}'
data = json.loads(json_str)

# 各种类型转布尔值
print(bool(""))        # False
print(bool(" "))       # True
print(bool([]))        # False
print(bool([0]))       # True
print(bool(0))         # False
print(bool(None))      # False

# float → int（向下取整）
x = 3.9
y = int(x)             # 3

# 字符串保留小数位
num = 3.14159
formatted = round(num, 2)  # 3.14


# 十进制 → 其他进制
num = 255
hex_str = hex(num)     # "0xff"
bin_str = bin(num)     # "0b11111111"
oct_str = oct(num)     # "0o377"

# 其他进制 → 十进制
int("ff", 16)          # 255
int("11111111", 2)     # 255

from datetime import datetime
import time

# 时间戳 → 日期字符串
timestamp = 1713273600
date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

# 日期字符串 → 时间戳
date_str = "2024-04-16 12:00:00"
timestamp = int(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp())