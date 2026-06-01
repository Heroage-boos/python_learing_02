
from flask import jsonify

#导入蓝图
from . import web

@web.route("/user/get")
def user_get():
    return jsonify({"test":"hello fisher!"})