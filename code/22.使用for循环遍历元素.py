
arr =  ['1','222','333','444','555']
for i in arr:
    if i =='1':
        continue
    if i == '333':
       print('存在')
       break
else:
   print('不存在')