class BookViewModel:
    pass


class BookCollection:

    @classmethod
    def package_single(cls, data, keyword):
        # 处理返回数据
        returned = {"books": [], "keyword": keyword, "total": 0}
        if data:
            returned["total"] = 1
            # 推导式
            returned["books"] = cls.__cut__book_data(data)
        return returned
        
    @classmethod
    def package_collection(cls, data, keyword):
        returned = {"books": [], "keyword": keyword, "total": 0}
        if data:
            returned["total"] = len(data["books"])
            returned["books"] = [cls.__cut__book_data(book) for book in data["books"]]
        return returned

    @classmethod
    def __cut__book_data(cls, data):
        book = {
            "title": data["title"],  # 书名
            "publisher": data["publisher"],  # 出版社
            "pages": data["pages"] or "",  # 页数
            "author": "、".join(
                data["author"]
            ),  # 作者  join在这里能够将list中的元素连接成一个字符串，例如将['a','b','c']连接成'a、b、c'
            "price": data["price"],  # 价格
            # 这里如果None就输出空字符串
            "summary": (data["summary"] or "")[:100],  # 摘要
            "image": data["images"],  # 图书封面
        }
        return book

""" 拓展推导式的其他用法
    # 只处理价格低于100的书籍
[cls.__cut__book_data(book) for book in data['books'] if book.get('price', 0) < 100]

# 处理并添加索引
[{**cls.__cut__book_data(book), 'index': i} for i, book in enumerate(data['books'])]

"""
