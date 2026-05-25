
from http_helper import HTTP

class YuShuBook:
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&count={}&start={}"

    @classmethod
    def search_by_isbn(cls,isbn_no):
        url = cls.isbn_url.format(isbn_no)
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_keyword(cls,keyword,count=15,start=0):
        url = cls.keyword_url.format(keyword)
        result = HTTP.get(url)
        return result