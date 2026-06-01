from flask import Blueprint

# template_folder 指定模板文件夹，相对于 __file__ 的相对路径
web = Blueprint("web", __name__,template_folder="templates")

from app.web import book
from app.web import user


