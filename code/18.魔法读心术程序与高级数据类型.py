"""
我有A、B、C、D、E、F1、你作为玩家，选好一个数字，然后告诉我这个数字存在在哪张
卡片上:2、我将会猜出你心里想的数字是什么
"""

# 调整数字不要重复
arr = {
    "A": [1, 9, 17, 25, 33, 41, 49, 57,3, 11, 19, 27, 35, 43, 51, 59,5, 13, 21, 29, 37, 45, 53, 61,7, 15, 23, 31, 39, 47, 55, 63],
    "B": [2, 10, 18, 26, 34, 42, 50, 58,3, 11, 19, 27, 35, 43, 51, 59,6, 14, 22, 30, 38, 46, 54, 62,7, 15, 23, 31, 39, 47, 55, 63],
    "C": [4, 12, 20, 28, 36, 44, 52, 60,5, 13, 21, 29, 37, 45, 53, 61,6, 14, 22, 30, 38, 46, 54, 62,7, 15, 23, 31, 39, 47, 55, 63],
    "D": [4, 12, 20, 28, 36, 44, 52, 60,5, 13, 21, 29, 37, 45, 53, 61,6, 14, 22, 30, 38, 46, 54, 62,7, 15, 23, 31, 39, 47, 55, 63],
    "E": [16, 20, 24, 28, 48, 52, 56, 60,17, 21, 25, 29, 49, 53, 57, 61,18, 22, 26, 30, 50, 54, 58, 62,19, 23, 27, 31, 51, 55, 59, 63],
    "F": [32, 36, 40, 44, 48, 52, 56, 60,33, 37, 41, 45, 49, 53,57, 61,34, 38,42, 46,50, 54,58,62,35, 39, 43, 47, 51, 55, 59, 63],
}

chiose_ticket = str(input("你心里想的数字都位于哪些卡片上，多张卡片使用 ,分隔\n"))

card_list = chiose_ticket.split(",")

# 记录用户输入的卡片
user_choose_card = []

# 根据卡片拿到数字
for card in card_list:
    # lower() 可以将所有字母变为小写 pper() 可以将所有字母变为大写
    upper_char = card.upper()

    if upper_char == "A":
        user_choose_card.append(arr["A"][0])
    elif upper_char == "B":
        user_choose_card.append(arr["B"][0])
    elif upper_char == "C":
        user_choose_card.append(arr["C"][0])
    elif upper_char == "D":
        user_choose_card.append(arr["D"][0])
    elif upper_char == "E":
        user_choose_card.append(arr["E"][0])
    elif upper_char == "F":
        user_choose_card.append(arr["F"][0])

#计算出所有数字的和
sum = 0
for num in user_choose_card:
    sum += num

print(card_list,user_choose_card)
print("你心里想的数字是:",sum)
