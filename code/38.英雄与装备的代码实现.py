"""
有一个变量叫hero equip是列表，代表英雄所穿的装备，当我们把hero_equip传入到一个计算装备属性的函数calc_equip_properties中，
这个函数可以返回对应的装备属性。最后通过代码实现把这些装备的属性全部放入到一个列表中
"""

# 使用map函数实现

hero_equip = ["刀", "盾", "枪", "护手"]

def calc_equip_properties(equip):
    if "刀" == equip:
        return "攻击+120"
    elif "盾" == equip:
        return "防御+200"
    elif "枪" == equip:
        return "攻击+250"
    elif "护手" == equip:
        return "攻击+100"
    else:
        return 0

r = map(calc_equip_properties, hero_equip)
print(list(r))