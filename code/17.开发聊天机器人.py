# 我们是基于关键字搜索做的聊天机器人

robot = "大黄蜂"

while True:
    user_input = input("请输入你的问题：")
    if "你叫什么名字" in user_input:
        print(f"我叫{robot}，我是一个聊天机器人")
    elif "你好" in user_input:
        print("你好！")
    elif "玩儿" in user_input:
        print("玩儿什么？")
    elif user_input in "退出":
        print("好的，再见")
        break
    else:
        print("对不起, 我不懂你在说啥")
