goods_info=[
    ("水杯",12.5,25),
    ("西装",1280,3689),
    ("电脑",7800,13800),
    ("摄像头",248.8,349)
]

for  i in goods_info:
    #打印 获取具体折扣
    print(i[0],"商品的折扣率为:",i[1]/i[2]*100,"%")

#使用 lambda 结合排序 打印
goods_info.sort(key=lambda i:i[1]/i[2] )
print(goods_info)