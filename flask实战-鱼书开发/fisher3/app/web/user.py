
import json
from flask import Blueprint, jsonify

#使用user蓝图
user=Blueprint("user",__name__)

@user.route("/user/get")
def user_get():
    return jsonify({"test":"hello fisher!"}),200,{'Content-Type': 'application/json'}