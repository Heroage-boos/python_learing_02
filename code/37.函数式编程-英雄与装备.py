"""
有一个变量叫hero equip是列表，代表英雄所穿的装备，当我们把hero_equip传入到一个计算装备属性的函数calc_equip_properties中，
这个函数可以返回对应的装备属性。最后通过代码实现把这些装备的属性全部放入到一个列表中
"""

# 使用map函数实现

hero_equip = [
    {"name": "剑", "value": 1},
    {"name": "盾", "value": 5},
    {"name": "弓", "value": 3},
]


def calc_equip_properties(e):
    return e['value'] + 2

#经过一个计算返回一个值给r
r = map(calc_equip_properties, hero_equip)
print(list(r))


#结合lamdba表达式
r = map(lambda x: int(x['value'])+1, hero_equip)
print(list(r))

print (list(map(lambda x: int(x['value'])+1, hero_equip)))

r = map(lambda x: x, hero_equip)
print(list(r))