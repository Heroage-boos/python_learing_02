# 关键字搜索
# from flask import jsonify

# 正确导入方式，无法导入flask
# from fisher import app

#使用蓝图注册flask
from flask import Blueprint,jsonify

from helper import is_isnm_or_key
from yushu_book import YuShuBook

# print('ipapp-33333333',id(app))

# 蓝图 blueprint 蓝本
# 参数：蓝图名称，导入名称，URL前缀
web=Blueprint('web', import_name=__name__)

@web.route("/book/search/<q>")
def search(q):
    """
    q: 关键字   isbn
    page: 页码
    """
    # 用来判断是q还是关键字
    isbn_or_key= is_isnm_or_key(q)
    if isbn_or_key == "isbn":
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)
    #flask提供的简写方法
    return jsonify(result)