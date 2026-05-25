
from http_helper import HTTP

class YuShuBook:
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = "http://api.yushu.com/book/search?q={}&count={}&start={}"

    @classmethod
    def search_by_isbn(cls,isbn_no):
        # url = YuShuBook.isbn_url.format(isbn_no)
        url = cls.isbn_url.format(isbn_no)
        # url = self.isbn_url
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_keyword(cls,keyword,count=15,start=0):
        # url: str = YuShuBook.keyword_url.format(keyword)
        url = cls.keyword_url.format(keyword)
        result = HTTP.get(url)
        return result