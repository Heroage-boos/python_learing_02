# from flask import Flask, jsonify
from app import create_app,register_blueprints

app= create_app();

# 注册蓝图到app中 
# register_blueprints(app);

# 生产环境 nginx + uwsgi 必须加 
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=app.config["DEBUG"], port=81)
