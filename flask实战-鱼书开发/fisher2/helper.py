
#来判断是q还是关键字
def is_isnm_or_key(word):
    isbn_or_key = "key"
    #ISBN数据查询 通过请求10位或13位的ISBN码可以反馈给用户相应的书籍信息和推荐指数
    if len(word) == 13 and word.isdigit():
        isbn_or_key = "isbn"
    short_1=word.replace('-','')
    if '-' in word and len(short_1) == 10 and short_1.isdigit:
        isbn_or_key = "isbn"
    return isbn_or_key