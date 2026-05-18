"""
定义以下变量并赋值:
鸡肉饭(20.5元)，鱿鱼饭(235元)，番茄鸣蛋汤(2元)，牛肉汤(2元)，酸菜米线(16元)，橙汁(15元)，草莓汁(20元)，苹案(15元)，西瓜汁(20元)

为每个变量添加相应注释，并根据以下效果图及代码区的提示完成该习题:
鱿鱼饭比鸡肉饭贵:True
酸菜米线比鸡肉饭便宜: True
番茄鸡蛋汤与牛肉价格相等:True
鸡肉饭的价格不等于鱿鱼饭:True
草莓汁比橙汁贵:True
草莓汁与西瓜汁价格相等:True
橙汁的价格比草莓便宜:True
草莓汁与西瓜汁的价格相等 True
"""

chiken_rice = 20.5  # 鸡肉饭(20.5元)，

fish_rice = 235  # 鱿鱼饭(235元)，

tomato_eggsoup = 2  # 番茄鸣蛋汤(2元)，

beef_rice = 2  # 牛肉汤(2元)，

mixed_noodles = 16  # 酸菜米线(16元)

orange_juice = 15  # 橙汁(15元)

strawberry_juice = 20  # 草莓汁(20元)，

apple_juice = 15  # 苹案(15元)，

watermelon_juice = 20  # 西瓜汁(20元)

# 鱿鱼饭比鸡肉饭贵:True
print(fish_rice > chiken_rice)
# 酸菜米线比鸡肉饭便宜: True
print(mixed_noodles < chiken_rice)
# 番茄鸡蛋汤与牛肉价格相等:True
print(tomato_eggsoup == beef_rice)
# 鸡肉饭的价格不等于鱿鱼饭:True
print(chiken_rice != fish_rice)
# 草莓汁比橙汁贵:True
print(strawberry_juice > orange_juice)
# 草莓汁与西瓜汁价格相等:True
print(strawberry_juice == watermelon_juice)
# 橙汁的价格比草莓便宜:True
print(orange_juice < strawberry_juice)
# 草莓汁与西瓜汁的价格相等 True
print(strawberry_juice == watermelon_juice)


"""
出门在外乘坐出租车必不可少，那么你知出租车计价表的程吗?
下面是某城市出租车收费标准:起步价13元，3公里以内收费13元; 
超过3公里，基本单价23元/公里; 

超过10公里，基本单价加收20%的费用，即2.76元/公里;燃油加费1元/次;
请根据该标准编写出租车的计费程序。
"""

# 计算总公里
# 计算前三公里（起步价+总公里-3）*13
# 判断是否超过3km ，超过则计算超过部分
# 判断是否超过10km，

# 设定乘车总公里数
frist_price = 13  # 起步价
total_kilometers: float = float(input("请输入乘车总公里数："))
count_price = 0  # 总车费
fuel_price = 1  # 燃油加费
fuel_num = 0  # 燃油加费次数

# 计算前三公里
if total_kilometers > 10:
    count_price: float = frist_price + (total_kilometers - 3) *23 + (total_kilometers - 10) * (23 + 2.6)
elif total_kilometers > 3 and total_kilometers <= 10:
    count_price: float = frist_price +(total_kilometers - 3) * 23
elif total_kilometers <= 3:
    count_price = frist_price

print("总车费为：", count_price, "元")
