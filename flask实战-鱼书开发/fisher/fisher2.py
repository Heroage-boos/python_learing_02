from flask import Flask, make_response 
from helper import is_isnm_or_key

app=Flask(__name__)
#导入方式1读取DEBUG
app.config.from_object("config")

#关键字搜索  http://t.yushu.im/v2/book/search/search?q={}&start={}&count={}
@app.route("/book/search/<q>/<page>")
def search(q,page):
    '''
        q: 关键字   isbn
        page: 页码
    '''
    # 用来判断是q还是关键字
    isbn_or_key = is_isnm_or_key(q)
    return isbn_or_key,200


#生产环境 nginx + uwsgi 必须加
if __name__ == '__main__':
    #导入方式2读取DEBUG 
    app.run(host="0.0.0.0",debug=app.config["DEBUG"],port=81)



