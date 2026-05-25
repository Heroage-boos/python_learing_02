from typing import Any, Callable, Literal


from flask import Flask, jsonify
from helper import is_isnm_or_key
from yushu_book import YuShuBook

app = Flask(__name__)
# 导入方式1读取DEBUG
app.config.from_object("config")


# 关键字搜索
@app.route("/book/search/<q>")
def search(q):
    """
    q: 关键字   isbn
    page: 页码
    """
    # 用来判断是q还是关键字
    isbn_or_key= is_isnm_or_key(q)
    result = None
    if isbn_or_key == "isbn":
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)
    # return json.dumps(result), 200, {"Content-Type": "application/json"}
    #flask提供的简写方法
    return jsonify(result)


# 生产环境 nginx + uwsgi 必须加
if __name__ == "__main__":
    # 导入方式2读取DEBUG
    app.run(host="0.0.0.0", debug=app.config["DEBUG"], port=81)
