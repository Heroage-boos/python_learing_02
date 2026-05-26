# 关键字搜索
# from flask import jsonify

# 正确导入方式，无法导入flask
# from fisher import app

# 使用蓝图注册flask
from flask.blueprints import Blueprint
from flask import jsonify, request
from helper import is_isnm_or_key
from yushu_book import YuShuBook
from app.forms.book import SearchForm  

# 导入蓝图
from . import web


@web.route("/book/search/<q>")
def search(q):
    """
    q: 关键字   isbn
    page: 页码
    """
    # 用来判断是q还是关键字
    isbn_or_key = is_isnm_or_key(q)
    if isbn_or_key == "isbn":
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)
    # flask提供的简写方法
    return jsonify(result)


# 带参数的路由
@web.route("/book/search2/")
def search2():
    """
    q: 关键字   isbn
    page: 页码
    page_size: 每页显示的条目数
    count = 15
    """
    # Request Response
    # HTTP 的请求信息
    # 查询参数 POST参数 remote ip
    # request = Request()
    # response = make_response()

    # q= request.args['q']
    # page= request.args['page']
    # a = request.args.to_dict()  #将不可变的字典转换为可变

    form = SearchForm(request.args)
    # WTForms参数校验
    if form.validate():
        # 验证通过，获取表单数据
        q = form.q.data.strip()  #首尾去除空格
        page = form.page.data  #如果通过form.page.data获取如果没传会返回默认值1，下面同理

        isbn_or_key = is_isnm_or_key(q)
        if isbn_or_key == "isbn":
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(keyword=q)
        # flask提供的简写方法
        return jsonify(result)
    else:
        return jsonify(form.errors), 400
