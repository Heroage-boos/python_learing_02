# 关键字搜索
# from flask import jsonify

# 正确导入方式，无法导入flask
# from fisher import app

# 使用蓝图注册flask
# from flask实战-鱼书开发.fisher6.app.spider.yushu_book import YuShuBook


from typing import Literal


import json
from flask import jsonify, render_template, request
from app.libs.helper import is_isnm_or_key
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm  
from app.view_models.book import BookViewModel,BookCollection

# 导入蓝图
from . import web


@web.route("/book/search/<q>")
def search(q):
    """
    q: 关键字   isbn
    page: 页码
    """
    # 用来判断是q还是关键字
    isbn_or_key: Literal['isbn', 'key'] = is_isnm_or_key(q)
    yushu_book: YuShuBook = YuShuBook()
    books    = BookCollection()
    if isbn_or_key == "isbn":
        yushu_book.search_by_isbn(q)
    else:
        yushu_book.search_by_keyword(q)
    books.fill(yushu_book,q)
    # data = books.fill(yushu_book.books,q)
    # flask提供的简写方法
    return json.dumps(obj=books,default=lambda o:o.__dict__)
    # return jsonify(data)   # TypeError: Object of type BookViewModel is not JSON serializable 


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
        yushu_book = YuShuBook()
        books: BookCollection = BookCollection()

        if isbn_or_key == "isbn":
            yushu_book.search_by_isbn(q)
            data = BookViewModel(book=yushu_book.books)
        else:
            yushu_book.search_by_keyword(q)
            # data = books.fill(yushu_book.books,q)
        books.fill(yushu_book,q)
        # flask提供的简写方法
        return json.dumps(books,default = lambda o:o.__dict__)
        # return jsonify(data)   # TypeError: Object of type BookViewModel is not JSON serializable 
    else:
        return jsonify(form.errors)

#  假如之后有文件需要积分下载
# def download():
#     if  user.jifen > 0:
#          send_static_file =  request.send_static_file()
#         pass
#     else:
#         return jsonify({"errcode":1})

@web.route("/test")
def test():
    user_info = {
        'name': "name",
        'age': 25,
    }
    
    return render_template("test_user_info.html", data=user_info)