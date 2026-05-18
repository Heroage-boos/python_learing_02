dict_1 = {"a": 1, "b": 2, "c": 3}

#如何向字典中添加元素
dict_1['d']=4

#修改字典中的元素
dict_1["a"]=10

#删除字典中的元素
#根据键来删除
del dict_1["a"]
dict_2=dict_1.pop("b")

#清空字典
# dict_1.clear();

print(dict_1)
