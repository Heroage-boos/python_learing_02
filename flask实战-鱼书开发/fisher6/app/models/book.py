
# sqlalchemy 第三方，
# Flask_SQALAlchemy flask改造的，
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy 
 
db = SQLAlchemy()

class Book (db.Model):
     # primary_key 是否是主键？？  autoincrement 是否自增？？ 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    # 字符串类型，长度50，nullable不能为空 
    title = Column(String(50), nullable=False)
    author = Column(String(20),default="未命名")
    binding = Column(String(20))
    price = Column(String(20))
    isbn = Column(String(20))
    image = Column(String(50))

    def sample(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'binding': self.binding,
            'price': self.price,
            'image': self.image,
            'isbn': self.isbn
        }