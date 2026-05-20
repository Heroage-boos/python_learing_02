from flask import Flask, make_response 
from helper import is_isnm_or_key

app=Flask(__name__)
#导入方式1读取DEBUG
app.config.from_object("config")

#路由注册方式1
#flask支持通过添加路由装饰器，指定网址访问对应的函数
'''/hello 和 /hello/ 如果同时存在，那么
/hello/ 会被优先匹配
'''
@app.route('/hello')
def hello():
    # 基于类的视图 （即插视图）
    return 'Hello World!'
#假如在浏览器中输入：http://127.0.0.1:8000/hello/abc
@app.route('/hello/<name>/')
def hello_name(name):
    return f'Hello {name}!'

#视图函数里面到底返回了什么
@app.route("/hello_html/")
def hello_html():
    # status/code 
    # message 
    # response  
    headers= {
        # "content-type":"text/plain",  # 告诉浏览器返回的数据是什么类型
        "content-type":"application/json",
        "location":"http://www.bing.com" #告诉浏览器去哪里  重定向
    }
    # flask 中不用自己创建response
    # response= make_response("<html></html>",301)
    # response.headers= headers
    # return response
    return "<html></html>",301,headers #返回tuple (response,status,headers)
    # return "<h1>Hello World</h1>" #直接返回页面空白

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


# isbn搜索
@app.route("/book/isbn/<isbn>")
def book_isbn(isbn):
    return isbn,200

#路由注册方式二
app.add_url_rule('/hello2','hello2',hello)

#生产环境 nginx + uwsgi 必须加
if __name__ == '__main__':
    #导入方式2读取DEBUG 
    app.run(host="0.0.0.0",debug=app.config["DEBUG"],port=81)



