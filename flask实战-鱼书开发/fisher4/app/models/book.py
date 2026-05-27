
# sqlalchemy 第三方，
# Flask_SQALAlchemy flask改造的，
from flask_sqlalchemy import SQLAlchemy 
 
class Book ():
    id = None
    title = ''
    author = None
    binding = None
    price = None
    isbn = None
    image = None

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