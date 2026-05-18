#字典
# 字典的key必须是唯一的，但是value可以重复，key可以是任意类型 常用数字和字符串 其他不提倡,不能用[],{}
d= {
    "name":"张三",
    "age":18,
    1:1 ,
    True:123,
    (1,2):1,
}

print(d)
print(type(d))

#单独访问字典所有的键
print(d.keys())

#单独访问字典所有的值
print(d.values())

#单独访问字典所有的键值对
print(d.items())

#判断某个元素是否在字典中存在
print(1 in d)
print(True in d)
print((1,2) in d)

#在对象调用的时候，方法加括号，属性不加括号
print(len(d))
print(d["name"])
print(d[(1,2)])

#新增一个键值对
d["sex"]="男"
print(d)

#修改一个键值对
d["name"]="李四"
print(d)

#删除一个键值对
del d["sex"]
print(d)