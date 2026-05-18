dict_book={
    "name":"西游记",
    "price":99,
    "author":"吴承恩",
    "publish":"人民出版社",
    "isbn":"1-23456789-X"
}

#使用 for in 遍历了字典的键盘
for d in dict_book:
    print(d) # name price author  publish isbn

#变通一下 遍历键
for key in dict_book.keys():
    print(key)
    print(dict_book[key]) # 根据键 访问值


#遍历值
for value in dict_book.values():
    print(value)


#遍历键值对
for key,value in dict_book.items():
    print(key,value)
    






