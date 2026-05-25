from flask import Flask

# 创建app对象
def create_app():
    app = Flask(__name__)
    # 导入方式1读取DEBUG
    app.config.from_object(obj="config")
    #注册蓝图到app
    register_blueprints(app)
    return app

def register_blueprints(app):
    """
    注册蓝图
    """
    from .web.book import web
    
    app.register_blueprint(web)