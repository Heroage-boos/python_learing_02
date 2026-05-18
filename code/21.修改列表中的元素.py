'''
列表的CRUD
'''

arr=["1",2,3,'4']

#给列表中增加元素
arr.append('ADAS')
print(arr)

#更新到列表中元素  想要更新得先访问 例如：arr[X]
arr[0] = 'ADAS'
print(arr)

#删除列表中的元素  
#根据值删除
arr.remove("ADAS")
print(arr)
#根据下标(索引)删除
del arr[0]
print(arr)

#清空列表
arr.clear()
print(arr)