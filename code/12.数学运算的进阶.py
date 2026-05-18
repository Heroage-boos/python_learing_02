#数学运算符的进阶
# % 取余数
# ** 幂运算 平方
# //取整除

j=5
i= 7

print(j%i)
print(j/i)
print(j//i)
print(j**i)


#取出100以内的奇数
i=0
while i<=100:
    i+=1
    if i%2==1:
        print(i,end=" ")
        continue
    if i>99:
        break
    