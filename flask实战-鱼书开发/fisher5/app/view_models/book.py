class BookViewModel:
    pass

class BookCollection:

    @classmethod
    def package_single(cls,data,keyword):
        #处理返回数据
        returned = {
            "books":[],
            'keyword': keyword,
            'total': 0
        }
        if data:
            returned['total'] = 1
            returned['books'] = cls.__cut__book_data(data)
        return returned

    @classmethod
    def package_collection(cls,data,keyword):
        pass
    
    @classmethod
    def __cut__book_data(cls,data):
        book = {
            "title": data["title"], # 书名
            "publisher": data["publisher"], #出版社
            "pages": data["pages"] or "", # 页数
            "author": '、'.join(data["author"]), #作者  join在这里能够将list中的元素连接成一个字符串，例如将['a','b','c']连接成'a、b、c'
            "price": data["price"], # 价格
            "summary": data["summary"][:100] or "", # 摘要
            "image": data["images"]["medium"], # 图书封面
        }
        return book