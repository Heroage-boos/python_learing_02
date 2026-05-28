
from app.libs.http_helper import HTTP
# from fisher import app 不要这样导入，会形成循环依赖
from flask import current_app  #指代创建app的对象

class YuShuBook:

    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&count={}&start={}"

    @classmethod
    def search_by_isbn(cls,isbn_no):
        url = cls.isbn_url.format(isbn_no)
        result = HTTP.get(url)

        # save(data)
        # if book_data:
        #     return book_data
        # else :
        #     return save(result)
        return result

    @classmethod
    def search_by_keyword(cls,keyword,page=1):
        # 
        url = cls.keyword_url.format(keyword,current_app.config['PRE_PAGE'], (page-1) * current_app.config['PRE_PAGE'])
        result = HTTP.get(url)
        return result