# 数据库与 ORM — Flask-SQLAlchemy 完整指南

> 基于 fisher_end 和 flask-cloudBook 两个项目的 SQLAlchemy ORM 实践

---

## 一、SQLAlchemy 初始化

### 1.1 模块级声明 + init_app 绑定

两个项目都采用相同的初始化模式：

```python
# app/models/base.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()    # 模块级声明，未绑定任何 Flask app

# app/__init__.py
def create_app():
    app = Flask(__name__)
    db.init_app(app)       # 在工厂函数中绑定
    with app.app_context():
        db.create_all()    # 自动建表
    return app
```

**为什么要分两步**：
- `db = SQLAlchemy()` 创建的是未绑定的实例，其他模块可以 `from app.models.base import db` 使用它定义模型
- `db.init_app(app)` 在 `create_app()` 中将数据库 URI 等配置绑定到具体应用
- 两步分离解决了 Application Factory 模式的循环导入问题

### 1.2 数据库连接配置

```python
# fisher_end: app/secure.py
SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:root@localhost:3306/fisher"

# cloudBook: config.py
SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:mysql6339575953@127.0.0.1:3306/cloud_book"
```

**URI 格式**：`dialect+driver://username:password@host:port/database`

| 部分 | 说明 | 常用值 |
|------|------|--------|
| `dialect` | 数据库类型 | `mysql`, `postgresql`, `sqlite` |
| `driver` | Python 驱动 | `cymysql`(mysql), `psycopg2`(postgres), `pysqlite`(sqlite) |
| `host:port` | 服务器地址 | `127.0.0.1:3306` |
| `database` | 数据库名 | `fisher`, `cloud_book` |

### 1.3 db.create_all() — Code First 自动建表

```python
def create_app():
    app = Flask(__name__)
    db.init_app(app)
    with app.app_context():
        db.create_all()    # 遍历所有 db.Model 子类，创建不存在的表
```

**工作机制**：
- SQLAlchemy 检查所有继承 `db.Model` 的类
- 通过反射检查数据库中是否已有同名表
- 不存在 → 生成 CREATE TABLE 语句并执行
- 已存在 → 跳过

**重要限制**：
- 只会**创建**新表，不会**修改**已有表结构
- 删除字段 → create_all 不处理
- 修改字段类型 → create_all 不处理
- 生产环境应使用 Alembic / Flask-Migrate

---

## 二、Base 基类设计

### 2.1 __abstract__ 抽象基类

两个项目都采用这种模式：

**fisher_end**（`fisher/app/models/base.py`）：
```python
class Base(db.Model):
    __abstract__ = True              # 不创建 base 表
    create_time = Column(Integer)    # Unix 时间戳
    status = Column(SmallInteger, default=1)  # 软删除标记

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0   # 软删除

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
```

**cloudBook**（`app/models/base.py`）：
```python
class Base(db.Model):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now)  # DateTime 类型
    status = Column(Integer, default=1)

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)
```

### 2.2 两个项目 Base 的差异

| 特性 | fisher_end | cloudBook |
|------|-----------|-----------|
| 时间字段类型 | `Integer` (Unix 时间戳) | `DateTime` (Python datetime) |
| 时间自动赋值 | `__init__` 中手动赋值 | `default=datetime.now` |
| 转换属性 | `create_datetime` property | 无 |
| 自定义 Query | `class Query(BaseQuery)` | 无（使用默认 Query） |
| `auto_commit` | `class SQLAlchemy` 扩展 | 无（直接 `db.session.commit()`） |
| `delete()` 方法 | 有 | 无 |

### 2.3 set_attrs 方法

```python
def set_attrs(self, attrs_dict):
    for k, v in attrs_dict.items():
        if hasattr(self, k) and k != 'id':
            setattr(self, k, v)
```

**用途**：将表单/JSON 数据批量赋值到模型实例。

**安全设计点**：
- `hasattr(self, k)`：只能赋值模型中定义的字段，防止注入不存在的属性
- `k != 'id'`：防止客户端覆盖主键值（避免越权修改其他用户的数据）

**使用示例**：
```python
user = User()
user.set_attrs(form.data)
# form.data = {"email": "test@qq.com", "nickname": "test", "password": "123"}
# 结果：user.email="test@qq.com", user.nickname="test", user.password=哈希值
```

---

## 三、Model 定义

### 3.1 User 模型对比

**fisher_end**（完整版）：
```python
class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(128))
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    # 业务方法：can_save_to_list(), can_send_drifts(), has_in_gifts()...

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
```

**cloudBook**（精简版）：
```python
class User(UserMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), default='无名之辈xxx')
    nickname = Column(String(256))
    phone_number = Column(String(11), unique=True)
    email = Column(String(256), unique=True)
    _password = Column('password', String(length=256), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
```

**关键差异**：
- fisher_end 有 `confirmed`、`beans`、`send_counter` 等业务字段（鱼书赠送相关）
- cloudBook 更精简，聚焦电子书商城核心功能
- cloudBook 有 `name` 字段（`default='无名之辈xxx'`）

### 3.2 Book 模型（cloudBook）

```python
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    image = Column(String(50))
    summary = Column(String(100))
    isbn = Column(String(13))

    def sample(self):
        return {
            "id": self.id, "title": self.title,
            "author": self.author, "binding": self.binding,
            "publisher": self.publisher, "price": self.price,
            "image": self.image, "summary": self.summary,
            "isbn": self.isbn
        }
```

### 3.3 BookList — 用户自定义书单（cloudBook）

```python
class BookList(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    list_name = Column(String(100), nullable=False)
    is_public = Column(Boolean, default=False)
```

### 3.4 Fisher 的 Gift/Wish 模型

```python
# Gift（赠送）
class Gift(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

# Wish（心愿）
class Wish(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)
```

### 3.5 常用列类型与约束

| Column 参数 | 说明 | 示例 |
|-------------|------|------|
| `primary_key=True` | 主键 | `id = Column(Integer, primary_key=True)` |
| `autoincrement=True` | 自增 | 配合主键使用 |
| `nullable=False` | 不允许空 | `title = Column(String(50), nullable=False)` |
| `unique=True` | 唯一约束 | `email = Column(String(50), unique=True)` |
| `default=xxx` | 默认值 | `status = Column(Integer, default=1)` |
| `ForeignKey('table.col')` | 外键 | `user_id = Column(Integer, ForeignKey('user.id'))` |

**列类型**：`Integer`, `String(n)`, `Float`, `Boolean`, `DateTime`, `SmallInteger`, `Text`

### 3.6 relationship 关系映射

```python
# 定义在 Gift 模型中
uid = Column(Integer, ForeignKey('user.id'), nullable=False)
user = relationship('User')
```

**效果**：
```python
gift = Gift.query.first()
print(gift.user.nickname)    # 通过 gift.user 直接访问关联的 User 对象
```

SQLAlchemy 会自动根据外键生成 JOIN 查询，加载关联对象。`relationship` 的加载策略默认为 `lazy='select'`（访问时才查询）。

---

## 四、自定义 Query — 软删除自动过滤（fisher 独有）

### 4.1 实现

```python
from flask_sqlalchemy import BaseQuery

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 1     # 自动附加 status=1
        return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)
```

### 4.2 效果

```python
# 你写的
User.query.filter_by(email='test@qq.com').first()

# 实际执行的 SQL
# SELECT * FROM user WHERE email='test@qq.com' AND status=1

# 如果你想查已删除的
User.query.filter_by(email='test@qq.com', status=0).first()
# SQL: SELECT * FROM user WHERE email='test@qq.com' AND status=0
```

**优势**：对所有 `filter_by()` 调用透明生效，不需要每次手动加 `status=1`。业务代码可以像操作普通表一样操作（已删除记录自动不可见）。

**注意**：如果用 `filter()`（表达式形式）替代 `filter_by()`（关键字形式），则不受此自动过滤影响，需要手动加条件。

---

## 五、auto_commit 上下文管理器（fisher 独有）

### 5.1 扩展 SQLAlchemy 类

```python
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()          # 无异常 → 提交
        except Exception as e:
            self.session.rollback()         # 有异常 → 回滚
            raise e

db = SQLAlchemy(query_class=Query)
```

### 5.2 使用方式

```python
# 在视图函数中，所有写操作包裹在 with db.auto_commit() 中
@web.route('/my/gift/create', methods=['POST'])
@login_required
def create_gift():
    form = GiftForm(request.form)
    if form.validate():
        with db.auto_commit():
            gift = Gift()
            gift.set_attrs(form.data)
            gift.uid = current_user.id
            db.session.add(gift)
        # 退出 with 块 → 自动 commit
        return redirect(url_for('web.my_gifts'))
    return render_template('gift_create.html', form=form)
```

### 5.3 与直接 commit 的对比

```python
# cloudBook 的直接 commit 方式
db.session.add(user)
db.session.commit()
# 如果 commit 前抛异常，不执行 commit，但 session 状态可能脏污

# fisher 的 auto_commit 方式
with db.auto_commit():
    db.session.add(gift)
    # 可能抛异常的代码...
# 异常 → 自动 rollback，session 恢复干净状态
```

**auto_commit 的优点**：
- 任何异常都触发 rollback，不会残留脏数据
- 代码更整洁，不需要重复写 try/except
- 与 Python `with` 语句自然集成

---

## 六、数据库操作完整示例

### 6.1 单条插入

```python
# cloudBook 风格
user = User()
user.set_attrs(register_form.data)
db.session.add(user)
db.session.commit()

# fisher 风格
with db.auto_commit():
    user = User()
    user.set_attrs(form.data)
    db.session.add(user)
```

### 6.2 批量插入

```python
with db.auto_commit():
    for isbn in isbn_list:
        wish = Wish()
        wish.uid = current_user.id
        wish.isbn = isbn
        db.session.add(wish)
# 退出 with 时统一 commit，只产生一次数据库写操作
```

### 6.3 更新单条

```python
with db.auto_commit():
    gift = Gift.query.filter_by(id=gid, uid=current_user.id).first_or_404()
    gift.launched = True
# 不需要显式 update，SQLAlchemy 自动跟踪 dirty 对象
```

### 6.4 软删除

```python
with db.auto_commit():
    gift = Gift.query.filter_by(id=gid, uid=current_user.id).first_or_404()
    gift.delete()     # 调用 Base.delete() → self.status = 0
```

### 6.5 复杂查询

```python
# 最近礼物（按 ISBN 去重，取 30 个）
recent_gifts = Gift.query\
    .filter_by(launched=False)\
    .group_by(Gift.isbn)\
    .order_by(Gift.create_time)\
    .limit(30)\
    .distinct()\
    .all()

# 统计每个 ISBN 的心愿数
from sqlalchemy import func
count_list = db.session.query(
    func.count(Wish.id), Wish.isbn
).filter(
    Wish.launched == False,
    Wish.isbn.in_(isbn_list),
    Wish.status == 1
).group_by(Wish.isbn).all()
```

---

## 七、Code First vs Migration

### 7.1 db.create_all() — 开发阶段

```python
with app.app_context():
    db.create_all()
```

| 优点 | 缺点 |
|------|------|
| 零配置，模型即表 | 不会修改已有表结构 |
| 适合快速原型开发 | 不处理字段改名/类型变更 |
| 适合小型个人项目 | 无版本管理，无法回滚 |

### 7.2 Flask-Migrate（Alembic）— 生产环境

```python
# 安装
pip install flask-migrate

# 初始化
from flask_migrate import Migrate
migrate = Migrate(app, db)

# 命令行
flask db init          # 初始化迁移目录
flask db migrate -m "描述"  # 自动生成迁移脚本
flask db upgrade       # 执行迁移
flask db downgrade     # 回滚迁移
```

**对比**：

| | db.create_all() | Flask-Migrate |
|---|---|---|
| 建表 | 自动 | 需手动执行 upgrade |
| 改表 | 不支持 | 自动检测并生成迁移脚本 |
| 版本管理 | 无 | 每次修改生成版本文件 |
| 回滚 | 不支持 | `downgrade` 回退 |
| 生产环境 | 不推荐 | 推荐 |
| 学习成本 | 零 | 中等 |

### 7.3 最佳实践

1. **开发阶段**用 `db.create_all()` 快速迭代
2. **上线前**切换到 Flask-Migrate
3. 两个项目的 `db.create_all()` 都放在 `create_app()` 中，每次启动都会执行——这在开发中很方便，但生产环境应移除

---

## 八、最佳实践总结

| 实践 | 来源 | 说明 |
|------|------|------|
| `db = SQLAlchemy()` 模块级 + `init_app()` 绑定 | 两个项目 | 解决循环导入 |
| `__abstract__` 基类 | 两个项目 | 公共字段复用，不创建表 |
| `set_attrs()` + `k != 'id'` | 两个项目 | 安全批量赋值 |
| `Column('password', ...)` 列别名 | 两个项目 | 配合 property setter 实现自动哈希 |
| 自定义 Query 自动过滤 | fisher_end | 软删除对业务透明 |
| `auto_commit` 上下文管理器 | fisher_end | 自动 commit/rollback |
| `relationship('Model')` 关联查询 | 两个项目 | 通过对象访问关联数据 |
| 模型上放置业务方法 | fisher_end | `can_send_drifts()` 等方法归属模型 |
| Code First 快速原型 | 两个项目 | `db.create_all()` 开发用 |
| 生产环境用 Flask-Migrate | 推荐 | 版本化数据库变更 |
