from app.libs.http_helper import HTTP

# from fisher import app 不要这样导入，会形成循环依赖
from flask import current_app  # 指代创建app的对象


class YuShuBook:
    # 模型层 MVC M层
    isbn_url = "http://t.talelin.com/v2/book/isbn/{}"
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn_no):
        url: str = self.isbn_url.format(isbn_no)
        result = HTTP.get(url)
        self.__fill_single(result) 

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(
            keyword, current_app.config["PRE_PAGE"], self.calculate_start(page)
        )
        result = HTTP.get(url)
        self.__fill_collection(result) 

    def calculate_start(self, page):
        """
        计算开始页
        """
        return (page - 1) * current_app.config["PRE_PAGE"]
