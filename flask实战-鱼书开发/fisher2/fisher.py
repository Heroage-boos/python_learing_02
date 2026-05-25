from flask import Flask

app = Flask(__name__)
# 导入方式1读取DEBUG
app.config.from_object(obj="config")


# from app.web import Book  #这种导入方式不行
print('ipapp-1111111',id(app))
# 使用蓝图 blueprint 蓝本


# 生产环境 nginx + uwsgi 必须加
if __name__ == "__main__":
    # 如果和上面的id(app)值一样，说明是同一个app,如果不同说明不是同一个app对象
    print('ipapp-222222',id(app))
    # 导入方式2读取DEBUG
    app.run(host="0.0.0.0", debug=app.config["DEBUG"], port=81)
