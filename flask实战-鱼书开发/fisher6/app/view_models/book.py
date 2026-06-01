class BookViewModel:

    def __init__(self,book) :
         self.title = book["title"]
         self.publisher = book["publisher"]
         self.pages = book["pages"]
         self.author = "、".join(book["author"])
         self.price = book["price"]
         self.summary = book["summary"]
         self.image = book["image"]

class BookCollection:
    def __init__(self) :
        self.total = 0
        self.books = []
        self.keyword = ""

    def fill(self,yushu_book,keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


""" 拓展推导式的其他用法
    # 只处理价格低于100的书籍
[cls.__cut__book_data(book) for book in data['books'] if book.get('price', 0) < 100]

# 处理并添加索引
[{**cls.__cut__book_data(book), 'index': i} for i, book in enumerate(data['books'])]

"""
