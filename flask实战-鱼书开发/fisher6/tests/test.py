from flask import Flask, current_app

app = Flask(__name__)

'''

'''

'''RuntimeError: Working outside of application context. 出现原因
    1、没有在应用上下文中运行代码，比如：
        d   =  current_app.config["DEBUG"]
   修复：
    with app.app_context():
        d   =  current_app.config["DEBUG"]
'''
# ctx = app.app_context()
# ctx.push()  # 将应用上下文推入当前栈中
# a = current_app
# d   =  current_app.config["DEBUG"]

with app.app_context():
    d   =  current_app
    a   =  current_app.config["DEBUG"]
    print(a)
'''
1.连接数据库
2.sql
3.释放资源

方法1：
try 
expect
finally

方法2： 使用with语句
with app.app_context():
    d   =  current_app.config["DEBUG"]
'''

'''
实现上下文协议的对象使用with
with app.app_context():
    d   =  current_app.config["DEBUG"]
上下文表达式必须要返回一个上下文管理器
'''

# 文件读写
# f = open("D:\t.txt")
# print(f.read())
# 使用 with
with open('D:\t.txt') as f:
    print(f.read())

if __name__ == '__main__':
    # 单进程，但线程
    app.run(host='0.0.0.0',debug=a.config['DEBUG'],port=82)
