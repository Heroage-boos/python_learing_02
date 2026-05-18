# 了解一下函数的基本特点
#在内存中开辟了一块独立的空间，一遍提供后续调用

#计算多个人的bim体重
def bmi_calculate(**weight_and_height):
    return_dict={} #期望返回 {"小白":18,"小明":20}
    print(weight_and_height)
    for name,args in weight_and_height.items():
        print(name,args)
        weight:float=args[0]
        height1=height2 = args[1]
        return_dict[name] = weight/(height1*height2)
    print("hello",return_dict)
    return return_dict
    #如果要从数组转元祖
    return tuple(result_List)

obj= bmi_calculate(xiaowang=[70,1.65],xiaobai=[80,180])
print(obj) 