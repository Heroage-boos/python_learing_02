# 重复即是循环
i = 1
target = 10
while i <= target:
    print(f"{i}")
    i += 1
    if i == 10:
        print(i)
        break


num = 8
# 循环的跳出
while True:  # 这个条件下永远会循环
    num += 1
    print(f"hello world{num}")
    if num == 10:
        break
        # 跳出 结束循环
    else:
        continue
        # 继续执行
