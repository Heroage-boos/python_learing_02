from flask import Flask
from app.models.book import db

# 创建app对象
def create_app():
    app = Flask(__name__)
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