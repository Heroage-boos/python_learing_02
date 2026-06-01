# Flask 实战 - 鱼书开发：步骤与思路方法总结

## 一、项目概述

鱼书是一个基于 Flask 的图书搜索应用，通过调用鱼书 API 实现按 ISBN 或关键字搜索图书信息。项目从单文件逐步重构为蓝图(Blueprint)架构，经历了 4 个版本的演进，完整展示了 Flask 项目的开发思路和重构方法。

---

## 二、开发步骤与演进路线

### 第一步：单文件起步 (fisher/)

**目标**：快速跑通一个 Flask 应用，理解核心概念。

**关键文件**：`fisher.py` → `fisher2.py`

**核心代码**：
```python
from flask import Flask
app = Flask(__name__)
app.config.from_object("config")

@app.route("/book/search/<q>")
def search(q):
    isbn_or_key = is_isnm_or_key(q)
    if isbn_or_key == "isbn":
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=app.config["DEBUG"], port=81)
```

**学到的知识点**：
1. **Flask 应用创建**：`Flask(__name__)` 创建实例
2. **配置管理**：`app.config.from_object("config")` 从模块加载配置，配置变量约定大写
3. **路由注册**：`@app.route()` 装饰器绑定 URL 与视图函数
4. **URL 参数**：`<q>` 捕获 URL 中的动态部分
5. **响应处理**：`jsonify()` 自动将字典转为 JSON 响应（对比 `json.dumps()` 需手动设置 Content-Type）
6. **启动方式**：`app.run()` 启动开发服务器

**辅助模块的设计思路**：

| 模块 | 职责 | 设计要点 |
|------|------|---------|
| `helper.py` | 判断输入是 ISBN 还是关键字 | ISBN-13 为13位纯数字；ISBN-10 为含 `-` 的10位数字 |
| `http_helper.py` | 封装 HTTP 请求 | 命名避免与标准库 `http` 冲突；处理非200状态码和 JSON 解码异常 |
| `yushu_book.py` | 封装鱼书 API 调用 | 使用 `@classmethod`，URL 作为类变量，不实例化即可调用 |
| `config.py` | 集中管理配置 | 变量大写（常量风格），`from_object()` 按名加载 |

**这一步的问题**：所有路由写在一个文件，代码量增大后难以维护。

---

### 第二步：尝试拆分 — 遇到循环导入 (fisher2/)

**目标**：将路由拆分到 `app/web/book.py`，实现代码分层。

**遇到的核心问题 — 循环导入**：

```
fisher.py 中: app = Flask(__name__)
                ↓ 需要在 book.py 中使用 app
app/web/book.py 中: @app.route(...)  ← app 未定义！
                ↑ 如果 from fisher import app，又会导致循环导入
```

**为什么循环导入？**
- `fisher.py` 定义了 `app`，要导入 `book` 模块来注册路由
- `book.py` 要导入 `fisher.py` 中的 `app` 来使用 `@app.route()`
- 两者互相依赖，形成循环

**关键认知**：直接在视图模块中使用 `@app.route()` 是行不通的，因为 `app` 对象无法安全地传递到子模块。这正是 Blueprint 存在的意义。

---

### 第三步：蓝图 + 应用工厂模式 (fisher3/)

**目标**：用 Blueprint 解决循环导入，用应用工厂模式规范 app 创建。

**核心架构**：

```
fisher3/
├── fisher.py              # 入口：调用 create_app()
├── config.py              # 配置
├── helper.py              # 辅助函数
├── http_helper.py         # HTTP 封装
├── yushu_book.py          # API 封装
└── app/
    ├── __init__.py         # 应用工厂：create_app() + register_blueprints()
    └── web/
        ├── __init__.py     # 空文件（包标识）
        ├── book.py         # web 蓝图 — 图书路由
        └── user.py         # user 蓝图 — 用户路由
```

**应用工厂模式** (`app/__init__.py`)：
```python
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(obj="config")
    register_blueprints(app)
    return app

def register_blueprints(app):
    from app.web.book import web    # 延迟导入，避免循环
    from app.web.user import user
    app.register_blueprint(web)
    app.register_blueprint(user)
```

**蓝图使用** (`app/web/book.py`)：
```python
from flask import Blueprint, jsonify
web = Blueprint('web', import_name=__name__)

@web.route("/book/search/<q>")
def search(q):
    ...
```

**关键设计点**：
1. **延迟导入**：蓝图在 `register_blueprints()` 函数内部导入，而非模块顶层，避免循环导入
2. **Blueprint 替代 app**：每个视图模块创建自己的 Blueprint 实例，用 `@web.route()` 代替 `@app.route()`
3. **应用工厂**：`create_app()` 封装了 app 的创建、配置和蓝图注册，入口文件 `fisher.py` 只需调用它
4. **多蓝图注册**：`book.py` 创建 `web` 蓝图，`user.py` 创建 `user` 蓝图，分别注册

**这一步的问题**：每新增一个视图模块就要新建一个 Blueprint，`app/__init__.py` 也要同步添加注册代码，扩展不够方便。

---

### 第四步：单蓝图多模块拆分 (fisher4/)

**目标**：用一个共享 Blueprint 组织同一层级下的多个视图模块，简化扩展。

**核心架构**：

```
fisher4/
├── fisher.py              # 入口：仅调用 create_app()
├── config.py
├── helper.py
├── http_helper.py
├── yushu_book.py
├── 说明.txt               # "4-3 单蓝图多模块拆分视图函数"
└── app/
    ├── __init__.py         # 应用工厂 + 注册单个 web 蓝图
    ├── api/                # 占位：API 模块（待扩展）
    ├── cms/                # 占位：CMS 模块（待扩展）
    └── web/
        ├── __init__.py     # ★ 核心：创建共享 web 蓝图，导入子模块
        ├── book.py         # from . import web → @web.route(...)
        └── user.py         # from . import web → @web.route(...)
```

**共享蓝图的关键** (`app/web/__init__.py`)：
```python
from flask import Blueprint

web = Blueprint("web", __name__)

# 导入子模块，触发 @web.route() 装饰器执行，注册路由
from app.web import book
from app.web import user
```

**视图模块使用共享蓝图** (`app/web/book.py`)：
```python
from . import web    # 从包的 __init__.py 导入共享蓝图

@web.route("/book/search/<q>")
def search(q):
    ...
```

**应用工厂简化** (`app/__init__.py`)：
```python
def register_blueprints(app):
    from .web.book import web    # 相对导入
    app.register_blueprint(web)  # 只注册一个蓝图！
```

**fisher3 vs fisher4 对比**：

| 方面 | fisher3 | fisher4 |
|------|---------|---------|
| 蓝图数量 | 多个：`web` + `user` | 单个共享 `web` 蓝图 |
| 蓝图定义位置 | 各视图模块自行创建 | `app/web/__init__.py` 集中创建 |
| 视图模块导入方式 | 各自 `Blueprint(...)` | `from . import web` 共享导入 |
| 新增模块时 | 改 `__init__.py` 注册 + 改 `app/__init__.py` 注册 | 只改 `app/web/__init__.py` 导入 |
| 导入风格 | 绝对导入 `from app.web.book` | 相对导入 `from .web.book` |

**为什么这样更好？**
- 新增视图模块（如 `gift.py`、`drift.py`），只需在 `app/web/__init__.py` 添加一行 `from app.web import gift`
- `app/__init__.py` 无需修改，蓝图注册保持稳定
- 同一层级的视图函数共享一个蓝图，URL 前缀统一管理

---

## 三、核心思路与方法论

### 1. 循序渐进的重构思路

```
单文件能跑 → 尝试拆分发现循环导入 → 用蓝图解决 → 优化蓝图使用方式
```

每次重构都是为了解决上一步暴露的具体问题，而非提前设计。

### 2. Flask 解决循环导入的两种策略

| 策略 | 做法 | 适用场景 |
|------|------|---------|
| **延迟导入** | 在函数内部 `from xxx import yyy`，而非模块顶层 | 应用工厂中注册蓝图 |
| **蓝图** | 视图模块使用 Blueprint 代替 app 对象 | 视图函数路由注册 |

### 3. 模块职责划分原则

```
入口文件(fisher.py)  → 只负责创建 app 和启动
应用工厂(__init__.py) → 封装 app 创建、配置加载、蓝图注册
视图模块(book/user)   → 只定义路由和视图函数
辅助模块(helper)      → 纯函数，无 Flask 依赖
HTTP模块(http_helper) → 封装第三方请求库
API模块(yushu_book)   → 封装外部 API 调用逻辑
配置模块(config)      → 集中管理配置常量
```

### 4. Blueprint 的本质理解

- Blueprint 是一个 **路由的容器**，可以独立定义路由，之后注册到 app 上
- Blueprint 解决了 `app` 对象在子模块中不可用的问题
- 一个 Blueprint 可以被多个模块共享使用
- Blueprint 支持设置 `url_prefix`，统一 URL 前缀

### 5. 应用工厂模式的好处

- `create_app()` 延迟到调用时才创建 app，方便测试时创建不同配置的实例
- 配置、蓝图注册等初始化逻辑集中管理
- 支持生产环境部署（nginx + uwsgi）

---

## 四、项目中值得注意的细节

1. **helper.py 的 `.isdigit` 遗漏**：`short_1.isdigit` 缺少括号 `()`，应为 `short_1.isdigit()`。这个 bug 在 4 个版本中一直存在。

2. **http_helper.py 命名**：故意不叫 `http.py`，因为 Python 标准库有 `http` 模块，同名会导致导入冲突。

3. **yushu_book.py 的 URL 演变**：
   - fisher/：ISBN 用 `t.yushu.im`，关键字用 `api.yushu.com`（两个不同域名）
   - fisher2~4/：统一改为 `t.talelin.com`（API 迁移到新域名）

4. **`from_object("config")` vs `from_object(obj="config")`**：后者使用了关键字参数 `obj`，两种写法效果相同。

5. **生产环境启动**：注释提到 `nginx + uwsgi` 必须加 `if __name__ == "__main__":` 保护，避免 uwsgi 导入时执行 `app.run()`。

6. **Pipfile 依赖**：核心只需 `flask` 和 `requests` 两个包。

---

## 五、Flask 开发步骤速查

```
1. 安装 Flask          → pip install flask
2. 创建应用实例        → app = Flask(__name__)
3. 加载配置            → app.config.from_object("config")
4. 定义路由            → @app.route("/path") 或 @blueprint.route("/path")
5. 编写视图函数        → def view_func(): return jsonify(data)
6. 创建蓝图            → web = Blueprint("web", __name__)
7. 注册蓝图            → app.register_blueprint(web)
8. 应用工厂封装        → def create_app(): ... return app
9. 启动运行            → app.run(host, port, debug)
```

---

## 六、项目目录结构演进图

```
fisher/                          # v1: 单文件，所有路由在一起
├── fisher.py / fisher2.py
├── helper.py
├── http_helper.py
└── yushu_book.py

fisher2/                         # v2: 尝试拆分，循环导入失败
├── fisher.py
├── app/web/book.py              ← @app.route() 但 app 未定义！
└── ...

fisher3/                         # v3: 蓝图 + 应用工厂
├── fisher.py                    → create_app()
├── app/__init__.py              → 工厂 + 注册多蓝图
└── app/web/
    ├── book.py                  → web = Blueprint('web')
    └── user.py                  → user = Blueprint('user')

fisher4/                         # v4: 单蓝图多模块
├── fisher.py                    → create_app()
├── app/__init__.py              → 工厂 + 注册单蓝图
└── app/web/
    ├── __init__.py              → web = Blueprint('web') + 导入子模块
    ├── book.py                  → from . import web
    └── user.py                  → from . import web
```

## request对象

Flask 的 `request` 对象封装了客户端发来的 HTTP 请求信息，最常用的属性：

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `request.args` | ImmutableMultiDict | URL 查询字符串参数 | `?q=python&page=2` |
| `request.form` | ImmutableMultiDict | POST 表单数据 | 提交表单 |
| `request.json` | dict | JSON 请求体 | API 请求 |
| `request.method` | str | 请求方法 | `'GET'`, `'POST'` |
| `request.url` | str | 完整请求 URL | `http://localhost/book/search2/?q=python` |

### URL 路径参数 vs 查询字符串参数

项目中的演进对比（fisher4 `app/web/book.py`）：

**方式1：URL 路径参数** — 参数嵌入 URL 中：
```python
@web.route("/book/search/<q>")
def search(q):
    # q 直接从 URL 路径提取
    isbn_or_key = is_isnm_or_key(q)
    ...
```
访问：`GET /book/search/python`

**方式2：查询字符串参数** — 通过 `request.args` 获取：
```python
@web.route("/book/search2/")
def search2():
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        ...
```
访问：`GET /book/search2/?q=python&page=2`

### request.args 的三种访问方式

```python
# 方式1：直接下标访问 — 参数不存在时抛出 KeyError
q = request.args['q']            # ❌ 缺少 q 时报错

# 方式2：get 方法 — 参数不存在时返回默认值
q = request.args.get('q', '')    # ✅ 安全，但无类型/范围校验

# 方式3：WTForms 绑定 — 推荐
form = SearchForm(request.args)  # ✅ 安全 + 自动校验 + 类型转换
if form.validate():
    q = form.q.data              # 经过校验和转换的数据
```

`request.args` 是 `ImmutableMultiDict`，支持 `.to_dict()` 转为普通字典：
```python
a = request.args.to_dict()  # {'q': 'python', 'page': '2'}
```

## WTForms参数校验

### 安装与基本用法

```bash
pip install wtforms
```

### 定义表单类（fisher4/5/6 `app/forms/book.py`）

```python
from wtforms import Form, IntegerField, StringField
from wtforms.validators import Length, NumberRange

class SearchForm(Form):
    q = StringField(validators=[Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
```

| 字段 | 类型 | 验证器 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `q` | StringField | Length(1, 30) | 无 | 搜索关键词，1-30字符 |
| `page` | IntegerField | NumberRange(1, 99) | 1 | 页码，1-99的整数 |

### 在视图函数中使用（fisher4 `app/web/book.py`）

```python
from flask import request, jsonify
from app.forms.book import SearchForm

@web.route("/book/search2/")
def search2():
    form = SearchForm(request.args)    # 1. 绑定查询字符串到表单
    if form.validate():                # 2. 执行校验
        q = form.q.data.strip()        # 3. 获取校验后的数据
        page = form.page.data          #    page 缺失时返回 default=1
        isbn_or_key = is_isnm_or_key(q)
        if isbn_or_key == "isbn":
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(keyword=q, page=page)
        return jsonify(result)
    else:
        return jsonify(form.errors)    # 4. 校验失败，返回错误信息
```

### 校验流程图

```
GET /book/search2/?q=python&page=2
         │
         ▼
SearchForm(request.args)   ← 将查询参数绑定到表单字段
         │
         ▼
form.validate()
    ├── q: Length(1,30)     → "python" 长度6 ✅
    └── page: NumberRange(1,99) → 2 在范围内 ✅
         │
    全部通过 → form.q.data = "python", form.page.data = 2
    有失败   → form.errors = {"q": ["Field must be between 1 and 30 characters long."]}
```

### 常用验证器

| 验证器 | 作用 | 示例 |
|--------|------|------|
| `Length(min, max)` | 字符串长度限制 | `Length(min=1, max=30)` |
| `NumberRange(min, max)` | 数值范围限制 | `NumberRange(min=1, max=99)` |
| `DataRequired()` | 必填（不允许空值） | `DataRequired(message='关键词不能为空')` |
| `Email()` | 邮箱格式 | `Email()` |
| `Regexp(pattern)` | 正则匹配 | `Regexp(r'^\d{13}$')` |

自定义错误消息：`Length(min=1, max=30, message='搜索关键词长度须在1-30之间')`

## 拆分config配置文件

### 拆分原因

原始项目使用单个 `config.py`，问题：
- 数据库密码等敏感信息与公共配置混在一起
- 上传 GitHub 时会泄露敏感信息

### 拆分方案（fisher4/5/6）

```
config.py（单文件）
       ↓ 拆分
secure.py（敏感配置，不上传 GitHub） + setting.py（公共配置，可上传 GitHub）
```

**secure.py** — 敏感数据，添加到 `.gitignore`：
```python
'''secure.py 保存一些敏感数据，不应该上传到github（远程仓库）
生产环境和测试环境配置也不同
'''
DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:password@127.0.0.1:3306/fisher"
```

**setting.py** — 公共配置，可安全上传：
```python
'''setting.py 保存一些公共不敏感配置数据，可以上传到公共远程仓库比如github
'''
PRE_PAGE = 12
```

### 在应用工厂中加载

```python
# app/__init__.py
def create_app():
    app = Flask(__name__)
    app.config.from_object("app.secure")    # 先加载敏感配置
    app.config.from_object("app.setting")   # 再加载公共配置
    ...
```

`from_object()` 读取目标模块中所有**大写**变量，合并到 `app.config`。后加载的同名变量会覆盖先加载的。

### .gitignore 配置

```gitignore
# 忽略敏感配置
app/secure.py
```

## 如何减少第三方接口请求数据
-每一次查询将数据存储到数据库中去，下一次查询，先本地查询数据库如果有，不需要再次请求第三方。
-用redis来存储，key为查询的书籍名，value为书籍信息，设置好过期时间。
-ViewModel 数据裁剪：只保留前端需要的字段，减少传输量和暴露的风险。`__cut__book_data` 方法就是做数据裁剪。


## Model First, Database First 与 Code First 
- Model First：先有模型，再建数据库 （数据库管理员经常使用，使用图表连转转换成数据库）
- Database First：先有数据库，再写代码（对应ORM）
- Code First：先写代码，再建数据库  (专注业务模型的设计，而不是专注数据库设计)

## Code First 创建数据库
- 使用flask-sqlalchemy来创建数据库
    - 安装：pip install flask-sqlalchemy
    - 在config中配置数据库
    - 在app中初始化db

### 安装依赖

```bash
pip install flask-sqlalchemy
pip install cymysql   # MySQL 数据库驱动（SQLALCHEMY_DATABASE_URI 中的 mysql+cymysql）
```

### 配置数据库连接

在 `secure.py` 中配置：
```python
SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:password@127.0.0.1:3306/fisher"
```

URI 格式：`数据库类型+驱动://用户名:密码@主机:端口/数据库名`

### 初始化 SQLAlchemy

关键：`db` 对象在模块级别创建，在应用工厂中绑定 app：

```python
# app/models/book.py — 模块级别创建 db 实例
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# app/__init__.py — 应用工厂中绑定
from app.models.book import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.secure")
    app.config.from_object("app.setting")
    ...
    db.init_app(app)              # 将 db 绑定到 app
    with app.app_context():       # 必须在应用上下文中操作
        db.create_all()           # 根据模型创建数据库表
    return app
```

**为什么 `db` 不能在 `create_app()` 内部创建？** 因为 models 和 views 都需要导入 `db`，如果在 `create_app()` 内创建，会导致循环导入。先在模块级创建，再通过 `init_app()` 延迟绑定，是 Flask 扩展的标准模式。

## 将模型映射到数据库中

### 定义模型类（fisher5/6 `app/models/book.py`）

```python
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(20), default="未命名")
    binding = Column(String(20))
    price = Column(String(20))
    isbn = Column(String(20))
    image = Column(String(50))

    def sample(self):
        return {
            'id': self.id, 'title': self.title, 'author': self.author,
            'binding': self.binding, 'price': self.price,
            'image': self.image, 'isbn': self.isbn
        }
```

### 字段类型与约束

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | Integer | primary_key, autoincrement | 主键自增 |
| `title` | String(50) | nullable=False | 不允许为空 |
| `author` | String(20) | default="未命名" | 默认值 |
| `binding` | String(20) | 无 | 装帧方式 |
| `price` | String(20) | 无 | 价格（用 String 而非 Float，避免浮点精度问题） |
| `isbn` | String(20) | 无 | ISBN 编号 |
| `image` | String(50) | 无 | 封面图片 URL |

### Code First 工作流程

```
1. 编写 Python 模型类（Book）
2. db.init_app(app) 绑定数据库
3. db.create_all() 自动生成 CREATE TABLE 语句
4. Flask 在 app_context() 中执行建表
```

**注意**：`db.create_all()` 不会更新已存在的表结构。如果修改了模型字段，需要先删除表再重建，或使用 Flask-Migrate（Alembic）做数据库迁移。

## 将模型映射到数据库中

## MVC,ORM
- MVC：模型，视图，控制器 
- ORM：对象关系映射，将类和对象转换为数据库中的表和记录

### MVC 在鱼书项目中的体现

```
M (Model)       → app/models/book.py — Book 模型，数据库操作
V (View)        → app/templates/ — Jinja2 模板，页面展示
C (Controller)  → app/web/book.py — 视图函数，业务逻辑调度
```

项目还引入了 **ViewModel**（app/view_models/）作为 M 和 V 之间的数据塑形层：

```
Model → ViewModel → Template
(原始数据)  (塑形后数据)   (页面展示)
```

### ORM 的核心映射关系

| Python | 数据库 |
|--------|--------|
| 类（Book） | 表（book） |
| 属性（title） | 字段（title VARCHAR(50)） |
| 实例（book1） | 记录（一行数据） |

ORM 的优势：用 Python 代码操作数据库，不需要手写 SQL。例如 `Book.query.filter_by(isbn='9787544291163').first()` 替代 `SELECT * FROM book WHERE isbn='9787544291163'`。

## flask核心机制

### 两种上下文

Flask 有两种上下文，都是在请求处理期间存在，请求结束后销毁：

| 上下文 | 包含对象 | 作用 |
|--------|---------|------|
| **应用上下文** (App Context) | `current_app`, `g` | 应用级别的数据和配置 |
| **请求上下文** (Request Context) | `request`, `session` | 请求级别的数据 |

### 上下文的生命周期

```
请求到达
  │
  ▼
Flask 创建 App Context → push 到 _app_ctx_stack
  │
  ▼
Flask 创建 Request Context → push 到 _request_ctx_stack
  │
  ▼
视图函数执行（可访问 current_app, request 等）
  │
  ▼
请求结束 → pop 两个上下文
```

### current_app 是线程隔离的代理

```python
from flask import current_app

# ❌ 在应用上下文之外访问 → RuntimeError!
d = current_app.config["DEBUG"]

# ✅ 在应用上下文中访问
with app.app_context():
    d = current_app.config["DEBUG"]
```

`current_app` 不是真正的 app 对象，而是一个代理（Proxy），它指向当前线程中栈顶的 app 实例。每个线程看到的 `current_app` 可以不同。

### 在鱼书项目中的使用

```python
# app/spider/yushu_book.py — 通过 current_app 读取配置
from flask import current_app

class YuShuBook:
    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        url = cls.keyword_url.format(
            keyword,
            current_app.config['PRE_PAGE'],          # 通过代理访问配置
            (page - 1) * current_app.config['PRE_PAGE']
        )
        result = HTTP.get(url)
        return result
```

**为什么用 `current_app` 而不直接 `from app import app`？** 避免循环导入，且支持多 app 实例（测试时创建不同配置的 app）。

## flask中出现 RuntimeError: Working outside of application context. 原因

### 错误原因

`current_app`、`db` 等 Flask 对象依赖应用上下文。在以下场景中会触发此错误：

1. **脚本直接运行**，不在请求处理流程中
2. **在模块顶层**使用 `current_app`
3. **db 操作**没有在应用上下文中执行

```python
# ❌ 错误：模块顶层没有应用上下文
from flask import current_app
d = current_app.config["DEBUG"]  # RuntimeError!
```

### 解决方案

**方式1：使用 `with app.app_context()`**（推荐）
```python
with app.app_context():
    d = current_app.config["DEBUG"]  # ✅ 正常
```

**方式2：手动 push/pop**
```python
ctx = app.app_context()
ctx.push()
d = current_app.config["DEBUG"]  # ✅ 正常
ctx.pop()
```

### 鱼书项目中的实际应用

```python
# app/__init__.py — db.create_all() 必须在应用上下文中
def create_app():
    app = Flask(__name__)
    ...
    db.init_app(app)
    with app.app_context():    # ← 必须加上
        db.create_all()        # 操作数据库需要应用上下文
    return app
```

## with语句与上下文管理器
-连接数据库
-文件读写

### Python 上下文管理器协议

任何实现了 `__enter__` 和 `__exit__` 方法的对象都可以用 `with` 语句：

```python
class MyResource:
    def __enter__(self):
        print("connect to resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("disconnect to resource")
        return False  # True 表示抑制异常，False 表示正常抛出

with MyResource() as resource:
    resource.query()
# 无论是否发生异常，__exit__ 都会被执行
```

### __exit__ 的异常处理

```python
# return True  → 异常被吞掉，不抛出
# return False → 异常正常抛出（默认行为）

def __exit__(self, exc_type, exc_val, exc_tb):
    print("cleanup")        # 即使 with 块中有异常，这里也会执行
    return False            # 异常继续向上传播
```

### Flask 中的应用

```python
# 1. 应用上下文
with app.app_context():
    d = current_app.config["DEBUG"]

# 2. 文件读写
with open('data.txt') as f:
    content = f.read()
# with 结束后自动关闭文件，无需手动 f.close()

# 3. 数据库操作（伪代码）
with db.session:
    user = User(name='test')
    db.session.add(user)
# with 结束后自动 commit 或 rollback
```

### with 的本质

```
with expr as var:
    # 等价于：
    manager = expr
    var = manager.__enter__()
    try:
        ...  # with 块中的代码
    finally:
        manager.__exit__(...)
```

`with` 保证 `__exit__` 一定被调用，即使发生异常——这是资源清理（关闭连接、释放锁）的可靠方式。

## with语句与上下文管理器（补充）
-连接数据库
-文件读写

（详细内容见上方「flask核心机制」和「RuntimeError」章节中的 with 语句部分）
- 进程：独立的内存空间，独立的运行环境，独立的文件描述符（打开文件）
- 线程：同一块内存空间，不同的执行单元（CPU时间片）
- 协程：同一块内存空间，不同的执行单元（CPU时间片），协程切换成本极低


# 线程
- 多线程
- 主线程和子线程的执行顺序
- 多线程的优势与好处
- 全局解释器锁GIL
- 对于IO密集型程序，多线程是有意义的
- 对于CPU密集型程序，多线程是没有意义的
- 开启flask多线程所带来的问题
- 线程隔离
-flask中的线程隔离对象Local
-flask中的线程隔离对象栈：LocalStack
-flask中被线程隔离的对象
-梳理串接flask的一些名词

### 多线程与 GIL

```python
import threading

def worker():
    print('i am thread')
    t = threading.current_thread()
    time.sleep(10)
    print(t.getName())

new_t = threading.Thread(target=worker)
new_t.start()   # 子线程开始执行
```

**GIL（全局解释器锁）**：Python 解释器的锁，同一时刻只允许一个线程执行 Python 字节码。这意味着：
- 多线程无法利用多核 CPU 的并行计算能力
- 但 IO 操作（网络请求、数据库查询、文件读写）时会释放 GIL，所以 IO 密集型程序多线程仍有意义

**主线程和子线程的执行顺序**：子线程在 `start()` 后开始执行，但与主线程是并发的，执行顺序由操作系统调度。

### 开启 Flask 多线程

```python
# 默认：单线程，请求排队处理
app.run(host='0.0.0.0', debug=True, port=81)

# 开启多线程：可同时处理多个请求
app.run(host='0.0.0.0', debug=True, port=81, threaded=True)
```

**多线程带来的问题**：多个线程共享同一块内存空间，如果全局对象（如 `current_app`、`request`）不是线程隔离的，并发请求会互相覆盖数据。

### 线程隔离

**问题演示**（test4.py）— 普通对象不线程隔离：
```python
class A:
    b = 1

my_obj = A()

def worker():
    my_obj.b = 2   # 子线程修改

new_t = threading.Thread(target=worker)
new_t.start()
time.sleep(1)
print(my_obj.b)    # 主线程看到 2！共享状态被修改
```

**解决方案** — werkzeug.local.Local 实现线程隔离（test5.py）：
```python
from werkzeug.local import Local

my_obj = Local()
my_obj.b = 1

def worker():
    my_obj.b = 2
    print("in new thread b is:" + str(my_obj.b))  # 2

new_t = threading.Thread(target=worker)
new_t.start()
time.sleep(1)
print('in main thread b is:' + str(my_obj.b))  # 1 — 主线程不受影响！
```

原理：`Local` 内部用线程 ID 作为 key，为每个线程维护独立的数据字典。

### LocalStack（test6.py）

```python
from werkzeug.local import LocalStack

s = LocalStack()
s.push(1)
print(s.top)   # 1
print(s.top)   # 1（top 不弹出）
print(s.pop()) # 1（pop 弹出）
print(s.top)   # None（栈空）

s.push(1)
s.push(2)
print(s.top)   # 2（后进先出）
print(s.pop()) # 2
print(s.top)   # 1
```

`LocalStack` = 线程隔离 + 栈结构。Flask 用栈而非简单 Local，是为了支持**嵌套上下文**（如一个 app 调用另一个 app 时，多个上下文共存于栈中）。

### Flask 中被线程隔离的对象

| 对象 | 所在上下文 | 栈 |
|------|-----------|-----|
| `current_app` | 应用上下文 | `_app_ctx_stack` |
| `g` | 应用上下文 | `_app_ctx_stack` |
| `request` | 请求上下文 | `_request_ctx_stack` |
| `session` | 请求上下文 | `_request_ctx_stack` |

### 梳理串接 Flask 的核心名词

```
请求到达
  │
  ▼
Request Context 创建 → push 到 LocalStack（_request_ctx_stack）
  │
  ▼
App Context 创建 → push 到 LocalStack（_app_ctx_stack）
  │
  ▼
视图函数执行
  ├── current_app → _app_ctx_stack.top.app（线程隔离的应用实例）
  ├── request     → _request_ctx_stack.top.request（线程隔离的请求对象）
  ├── g           → _app_ctx_stack.top.g（线程隔离的临时存储）
  └── session     → _request_ctx_stack.top.session（线程隔离的会话）
  │
  ▼
请求结束 → pop 两个上下文
```


## python 中的锁
- 锁的目的：保证多线程之间的数据同步
- 常用锁：Lock, RLock, Semaphore, BoundedSemaphore, Condition


## ViewModel的基本概念

### 什么是 ViewModel

ViewModel 是 Model 和 View 之间的数据塑形层。原始 API 返回的数据字段多、格式不统一，ViewModel 将其裁剪、转换为前端需要的格式。

```
API 原始数据 → ViewModel 塑形 → 模板/JSON 展示
（字段多、格式乱）   （精简、统一）    （干净、可读）
```

### fisher5 实现：@classmethod 模式

```python
# app/view_models/book.py (fisher5)
class BookCollection:
    @classmethod
    def package_single(cls, data, keyword):
        """处理单本书（ISBN 搜索）"""
        returned = {"books": [], "keyword": keyword, "total": 0}
        if data:
            returned["total"] = 1
            returned["books"] = cls.__cut__book_data(data)
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        """处理多本书（关键字搜索）"""
        returned = {"books": [], "keyword": keyword, "total": 0}
        if data:
            returned["total"] = len(data["books"])
            returned["books"] = [cls.__cut__book_data(book) for book in data["books"]]
        return returned

    @classmethod
    def __cut__book_data(cls, data):
        """数据裁剪：只保留需要的字段"""
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "pages": data["pages"] or "",
            "author": "、".join(data["author"]),   # 列表 → 字符串
            "price": data["price"],
            "summary": (data["summary"] or "")[:100],  # None → ""，截取前100字
            "image": data["images"],
        }
        return book
```

调用方式：`BookCollection.package_single(data, q)` — 直接返回字典，可被 `jsonify` 序列化。

### fisher6 实现：实例方法模式

```python
# app/view_models/book.py (fisher6)
class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = "、".join(book['author'])
        self.price = book['price']
        self.summary = (book['summary'] or "")[:100]
        self.image = book['images']

class BookCollection:
    def __init__(self):
        self.keyword = ""
        self.total = 0
        self.books = []

    def fill(self, yushu_book, keyword):
        self.keyword = keyword
        self.total = 1
        self.books = [BookViewModel(book) for book in yushu_book.books]
```

调用方式：`books.fill(yushu_book, q)` — 结果保存在实例上，需用 `json.dumps(books, default=lambda o: o.__dict__)` 序列化。

### 两种模式对比

| 方面 | fisher5（@classmethod） | fisher6（实例方法） |
|------|------------------------|-------------------|
| 调用方式 | `BookCollection.package_single(data, q)` | `books.fill(yushu_book, q)` |
| 状态保存 | 无，每次返回新字典 | 有，结果存在实例属性上 |
| 序列化 | 直接 `jsonify()` | 需 `json.dumps(default=...)` |
| 适用场景 | 简单的数据转换 | 需要保存状态或多个方法操作同一数据 |

## 全局静态资源访问 和 蓝图静态资源访问

### 全局静态资源（Flask 应用级别）

```python
# app/__init__.py
app = Flask(__name__, static_folder='static', static_url_path='/statics')
```

| 参数 | 作用 | 默认值 | 说明 |
|------|------|--------|------|
| `static_folder` | 磁盘上静态文件目录（物理路径） | `'static'` | 文件夹在 `app/static/` |
| `static_url_path` | URL 中的访问前缀 | 同 `static_folder` | `static_url_path` 优先级更高 |

**示例**：`static_folder='static'` + `static_url_path='/statics'` → 文件在 `app/static/test_user_info.css`，URL 为 `/statics/test_user_info.css`。

### 蓝图静态资源（Blueprint 级别）

```python
# app/web/__init__.py
web = Blueprint("web", __name__, template_folder="templates")
```

蓝图可独立设置 `template_folder` 和 `static_folder`，路径相对于蓝图所在目录。

**模板查找顺序**：先查应用级 `app/templates/`，再查蓝图级。

### 模板中引用静态文件

```html
<!-- url_for('static', ...) 依据 static_url_path 生成 URL -->
<link rel="stylesheet" href="{{ url_for('static', filename='test_user_info.css') }}">
<!-- 渲染结果：href="/statics/test_user_info.css" -->

<img src="{{ url_for('static', filename='测试图片-1.png') }}">
```

**常见坑**：href 值必须用引号包裹，否则浏览器无法正确解析：
```html
<!-- ❌ 错误 -->
<link rel="stylesheet" href={{ url_for('static',filename="test_user_info.css")}}">

<!-- ✅ 正确 -->
<link rel="stylesheet" href="{{ url_for('static', filename='test_user_info.css') }}">
```

## flask中的templates

### render_template 渲染模板

Flask 使用 Jinja2 作为模板引擎，`render_template()` 函数将模板和数据结合生成 HTML：

```python
# app/web/book.py (fisher6)
from flask import render_template

@web.route("/test")
def test():
    user_info = {'name': "name", 'age': 25}
    return render_template("test_user_info.html", data=user_info)
```

**模板查找路径**：
1. 应用级：`app/templates/`
2. 蓝图级：Blueprint 的 `template_folder` 指定的目录

### 内联 style vs 外部 CSS

项目中 `test_user_info.html` 同时展示了两种方式：

**方式1：`<style>` 内联样式**（适合样式少、仅当前页面使用）：
```html
<style>
    .user-info {
        font-size: 28px;
        font-weight: bolder;
    }
</style>
```

**方式2：`<link>` 外部 CSS**（推荐，样式可复用、可缓存）：
```html
<link rel="stylesheet" href="{{ url_for('static', filename='test_user_info.css') }}">
```

## 模板引擎
- Jinja2

Jinja2 是 Flask 默认的模板引擎，特点：
- 模板文件放在 `templates/` 目录下
- 使用 `{{ }}` 输出变量，`{% %}` 执行逻辑
- 支持继承、包含、宏等高级功能
- 自动 HTML 转义，防止 XSS 攻击

## 如何在flask中使用Jinja2模板

### 1. 使用 render_template 函数渲染模板

```python
from flask import render_template

@web.route("/test")
def test():
    user_info = {'name': "name", 'age': 25}
    # 第一个参数是模板文件名，后续是传递给模板的变量
    return render_template("test_user_info.html", data=user_info)
```

### 2. 在模板中定义变量

```html
<!-- 输出变量 -->
<span>{{ data.name }}, {{ data.age }}</span>
```

### 3. 在模板中循环遍历数据

```html
<ul>
{% for book in books %}
    <li>{{ book.title }} - {{ book.author }}</li>
{% endfor %}
</ul>
```

### 4. 在模板中继承其他模板

**基模板 `base.html`**：
```html
<html>
<head><title>{% block title %}{% endblock %}</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

**子模板**：
```html
{% extends "base.html" %}

{% block title %}图书搜索{% endblock %}

{% block content %}
    <h1>搜索结果</h1>
{% endblock %}
```

### 5. 在模板中包含其他模板

```html
<!-- 将公共部分抽取为独立模板，在多处复用 -->
{% include "header.html" %}
<div>页面内容</div>
{% include "footer.html" %}
```

### 6. 在模板中引入静态文件

```html
<!-- CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

<!-- JavaScript -->
<script src="{{ url_for('static', filename='app.js') }}"></script>

<!-- 图片 -->
<img src="{{ url_for('static', filename='logo.png') }}">
```

### 7. 条件判断

```html
{% if data.age > 18 %}
    <span>成年人</span>
{% elif data.age > 12 %}
    <span>青少年</span>
{% else %}
    <span>儿童</span>
{% endif %}
```

## Jinjia2中读取字典和对象
- 访问字典值：通过[]方式
- 访问对象属性：通过.方式

### 字典访问

```python
# 视图函数传递字典
user_info = {'name': "张三", 'age': 25}
return render_template("test.html", data=user_info)
```

```html
<!-- 方式1：点号访问（推荐） -->
{{ data.name }}   → 张三
{{ data.age }}    → 25

<!-- 方式2：方括号访问 -->
{{ data['name'] }} → 张三
{{ data['age'] }}  → 25
```

### 对象属性访问

```python
# 视图函数传递对象
book = BookViewModel(book_data)
return render_template("test.html", book=book)
```

```html
<!-- 只能用点号访问属性 -->
{{ book.title }}    → 书名
{{ book.author }}   → 作者

<!-- 方括号不适用于对象属性 -->
{{ book['title'] }} → ❌ 不推荐
```

### 两种方式的选择

| 数据类型 | 访问方式 | 示例 |
|---------|---------|------|
| 字典 dict | `.` 或 `[]` 均可 | `data.name` 或 `data['name']` |
| 对象 object | 只用 `.` | `book.title` |
| 列表 list | `[]` 索引 | `books[0].title` |

Jinja2 的 `.` 语法会依次尝试：字典键 → 属性 → 方法调用，所以 `data.name` 对字典和对象都能工作。



