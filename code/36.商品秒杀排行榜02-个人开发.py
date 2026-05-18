'''
需求理解
有列表结构如下:goods_info=[("水杯",12.5,25),("西装",1280,3689),("电脑",7800,13800),("摄像头",248.8,349)]
第一列代表商品名称，第二列代表商品折扣价格，第三列代表商品原价

请按照商品折扣数进行从小到大排序
'''

from typing import Any


goods_info=[("水杯",12.5,25),("西装",1280,3689),("电脑",7800,13800),("摄像头",248.8,349)]
new_goods_info=[]

#计算每一个元组的折扣率返回  折扣率= 商品折扣价格/商品原价 * 100%
def calc_1(goods_info=goods_info):
    for item in goods_info:
        new_goods_info.append((item[0],item[1],item[2],round(item[1]/item[2]*100,2)))
calc_1()
print(new_goods_info)

#进行排序
def sort_calc_1(p):
    return p[3]

new_goods_info.sort(key=sort_calc_1)

print(new_goods_info)