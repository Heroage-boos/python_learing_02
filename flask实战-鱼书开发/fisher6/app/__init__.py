from flask import Flask
from app.models.book import db

# 创建app对象
def create_app():
    # static_folder 不写默认就是static，写全是为了方便修改,作用：告诉flask静态文件存哪
    # 某些情况下，可能会把静态文件夹名字改成其他名字，这时候路径中static要加s为 statics
    app = Flask(__name__,static_folder='static',static_url_path='/statics')  # static_url_path优先级高于static_folder
    # 导入方式1读取DEBUG
    # app.config.from_object(obj="config")
    app.config.from_object("app.secure")
    app.config.from_object("app.setting")

    #注册蓝图到app
    register_blueprints(app)

    # 初始化db
    db.init_app(app)
    # 创建表
    with app.app_context():
        db.create_all()
    return app

def register_blueprints(app):
    """
    注册蓝图
    """
    from .web.book import web
    
    app.register_blueprint(web)