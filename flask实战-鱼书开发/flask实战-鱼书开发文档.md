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

## WTForms参数校验

## 拆分config配置文件

## 如何减少第三方接口请求数据
-每一次查询将数据存储到数据库中去，下一次查询，先本地查询数据库如果有，不需要再次请求第三方。
-用redis来存储，key为查询的书籍名，value为书籍信息，设置好过期时间。


## Model First, Database First 与 Code First 
- Model First：先有模型，再建数据库 （数据库管理员经常使用，使用图表连转转换成数据库）
- Database First：先有数据库，再写代码（对应ORM）
- Code First：先写代码，再建数据库  (专注业务模型的设计，而不是专注数据库设计)

## Code First 创建数据库
- 使用flask-sqlalchemy来创建数据库
    - 安装：pip install flask-sqlalchemy
    - 在config中配置数据库
    - 在app中初始化db

## 将模型映射到数据库中

## MVC,ORM
- MVC：模型，视图，控制器 
- ORM：对象关系映射，将类和对象转换为数据库中的表和记录
