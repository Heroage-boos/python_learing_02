# CRUD 实战 — Flask + SQLAlchemy 数据库操作完整指南

> 基于 fisher_end 和 flask-cloudBook 两个项目的 CRUD 最佳实践

---

## 一、Create（创建）

### 1.1 基本创建流程

```python
# 模式：实例化 → 批量赋值 → add → commit
user = User()
user.set_attrs(form.data)       # 批量赋值（密码自动哈希）
db.session.add(user)
db.session.commit()
```

**逐步解读**：

```python
# 第一步：创建模型实例
user = User()
# 此时 user 是一个未持久化的 Python 对象，id 为 None

# 第二步：批量赋值属性
user.set_attrs(form.data)
# form.data 示例：{"email": "test@qq.com", "nickname": "测试", "password": "123456"}
# set_attrs 遍历字典，对每个 key 调用 setattr
# password 的赋值触发 @password.setter，自动哈希

# 第三步：加入会话
db.session.add(user)
# 此时 user 进入 SQLAlchemy 的会话（Session），处于 pending 状态

# 第四步：提交
db.session.commit()
# SQLAlchemy 生成 INSERT 语句并执行，user.id 被填充
```

### 1.2 fisher_end 独有的 auto_commit 模式

fisher_end 对 `SQLAlchemy` 类做了扩展，增加了上下文管理器：

**定义**（`fisher/app/models/base.py`）：

```python
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

db = SQLAlchemy()
```

**使用方式**：

```python
# fisher_end 中的视图函数写法
with db.auto_commit():
    user = User()
    user.set_attrs(form.data)
    db.session.add(user)
# 退出 with 块时自动 commit，异常时自动 rollback
```

**对比直接 commit**：

```python
# cloudBook 的直接 commit 方式
db.session.add(user)
db.session.commit()
# 如果中间抛异常，commit 不会执行，但 session 处于 dirty 状态
# auto_commit 模式更安全：任何异常都会触发 rollback
```

### 1.3 创建时密码自动加密

不需要在视图函数中手动调用 `generate_password_hash`：

```python
# 不需要这样做：
user.password = generate_password_hash(form.password.data)

# 因为 Model 的 setter 自动处理：
user.set_attrs(form.data)
# form.data 中包含 password，赋值时自动触发加密
```

---

## 二、Read（读取）

### 2.1 主键查询 — get()

```python
# 按主键查询，最快的方式
user = User.query.get(int(uid))

# 用于 flask_login 的 user_loader
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
```

`get()` 只适用于主键查询，先查一级缓存（identity map），缓存未命中才查数据库。

### 2.2 条件查询 — filter_by() / filter()

```python
# filter_by：关键字参数，简洁但不能用 > < != 等操作符
user = User.query.filter_by(email='test@qq.com').first()

# filter：表达式参数，功能更强大
users = User.query.filter(User.email == 'test@qq.com').all()
users = User.query.filter(User.id > 10).all()
```

**first() vs all()**：
- `first()`：返回单个对象或 None
- `all()`：返回列表（可能为空列表 `[]`）

### 2.3 链式查询

```python
# 按创建时间降序取最新的一本书
recent = Book.query\
    .filter_by(status=1)\
    .order_by(Book.created_at.desc())\
    .first()
```

**链式方法一览**：

| 方法 | 作用 | 示例 |
|------|------|------|
| `filter_by(**kwargs)` | 等值过滤 | `.filter_by(status=1)` |
| `filter(expression)` | 表达式过滤 | `.filter(Book.price > 0)` |
| `order_by(column)` | 排序 | `.order_by(Book.created_at.desc())` |
| `limit(n)` | 限制数量 | `.limit(10)` |
| `offset(n)` | 跳过前 n 条 | `.offset(20)` |
| `group_by(column)` | 分组 | `.group_by(Gift.isbn)` |
| `distinct()` | 去重 | 配合 group_by 使用 |

### 2.4 自定义 Query 类 — 软删除过滤（fisher 独占）

fisher_end 定义了自定义 `Query` 类来自动过滤软删除记录：

```python
from flask_sqlalchemy import BaseQuery

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 1    # 自动补充 status=1
        return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)
```

**效果**：

```python
# 你写的代码：
User.query.filter_by(email='test@qq.com').first()

# 实际执行的 SQL：
# SELECT * FROM user WHERE email='test@qq.com' AND status=1
```

这样所有 `filter_by()` 调用**自动**只查询 `status=1`（未删除）的记录，无需每次手动加条件。如需查询已删除记录，需显式传入 `status=0`。

### 2.5 列表推导式转换查询结果

```python
# 将 ORM 对象列表转为字典列表
from app.view_models.book import BookViewModel

self.books = [BookViewModel(b) for b in books_info.books]

# 带条件过滤
[BookViewModel(b) for b in books_info.books if b.get('price', 0) < 100]
```

### 2.6 前端 API 调用（flask-cloudBook）

```typescript
// 获取书籍列表
const res = await api.books.list({ q: 'python' })
// → GET /api/book/search?q=python

// 获取书籍详情
const book = await api.books.detail('9787544291163')
// → GET /api/book/details/9787544291163

// 检查登录状态
const isLoggedIn = await api.user.checkSession()
// → GET /api/user/home（静默检查，不触发 401 跳转）
```

### 2.7 Fisher 的高级查询模式

```python
# Gift 模型上的类方法 — recent()
@classmethod
def recent(cls):
    recent_gifts = Gift.query\
        .filter_by(launched=False)\
        .group_by(Gift.isbn)\
        .order_by(Gift.create_time)\
        .limit(30)\
        .distinct()\
        .all()
    return recent_gifts

# Wish 模型 — 统计每个 ISBN 的心愿数量
@classmethod
def get_wish_counts(cls, isbn_list):
    count_list = db.session.query(
        func.count(Wish.id), Wish.isbn
    ).filter(
        Wish.launched == False,
        Wish.isbn.in_(isbn_list),
        Wish.status == 1
    ).group_by(Wish.isbn).all()
    return [{'count': c, 'isbn': i} for c, i in count_list]
```

---

## 三、Update（更新）

### 3.1 set_attrs 批量更新

```python
# 定义在 Base 基类上
def set_attrs(self, attrs_dict):
    for k, v in attrs_dict.items():
        if hasattr(self, k) and k != 'id':
            setattr(self, k, v)

# 使用
user = User.query.get(uid)
user.set_attrs({"nickname": "新昵称", "email": "new@qq.com"})
db.session.commit()
```

**注意**：`k != 'id'` 防止更新主键。

### 3.2 通过 property setter 更新密码

```python
# 直接赋值触发了 setter → 自动哈希
user.password = 'new_password_123'
db.session.commit()
```

### 3.3 单字段更新

```python
# fishery_end: 在 auto_commit 上下文中更新
with db.auto_commit():
    gift = Gift.query.filter_by(id=gid, uid=current_user.id).first()
    gift.launched = True
# 自动 commit/rollback

# cloudBook: 直接更新
book = Book.query.get(book_id)
book.price = '39.90'
db.session.commit()
```

### 3.4 批量更新

```python
# 批量修改符合条件的记录
db.session.query(User)\
    .filter(User.email.endswith('@test.com'))\
    .update({User.status: 0}, synchronize_session=False)
db.session.commit()
```

`update()` 直接生成一条 SQL UPDATE，比逐条查询再修改高效得多。

---

## 四、Delete（删除）

### 4.1 软删除模式 — 两个项目共同采用

**定义**（Base 基类）：

```python
class Base(db.Model):
    __abstract__ = True
    status = Column(Integer, default=1)  # 1=正常, 0=删除

    def delete(self):
        self.status = 0   # 软删除：只改状态，不删记录
```

**使用**：

```python
# 业务代码中，删除只需调用 delete()
gift.delete()
db.session.commit()

# 而不是：
# db.session.delete(gift)   ← 这是硬删除，数据不可恢复
```

**优势**：
1. 数据可恢复
2. 保留审计记录
3. 用户关闭浏览器前可撤销操作
4. 配合自定义 Query 自动过滤，对查询代码透明

### 4.2 自定义 Query 自动过滤

```python
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 1
        return super().filter_by(**kwargs)
```

这样常规 `filter_by()` 查询自动只返回 `status=1` 的记录，已删除记录对业务代码不可见。

### 4.3 什么时候用硬删除

- 临时/测试数据
- 没有业务价值的日志数据
- 法律要求必须删除的敏感数据

### 4.4 Fisher 的 Gift/Wish 删除

```python
# fisher/app/models/gift.py
class Gift(Base):
    def delete(self):
        self.status = 0

# 视图中
@web.route('/my/gift/delete/<int:gid>')
@login_required
def delete_gift(gid):
    with db.auto_commit():
        gift = Gift.query.filter_by(id=gid, uid=current_user.id).first_or_404()
        gift.delete()
    return redirect(url_for('web.my_gifts'))
```

---

## 五、CREATE TABLE — Code First 自动建表

### 5.1 db.create_all()

```python
# 在 create_app() 中
def create_app():
    app = Flask(__name__)
    db.init_app(app)
    with app.app_context():
        db.create_all()    # 根据所有 db.Model 子类自动创建表
    return app
```

`db.create_all()` 会遍历所有继承自 `db.Model` 的类，为每个类创建对应的数据库表（如果表不存在）。

**限制**：
- 只会创建不存在的表，不会修改已有表结构
- 删除字段：无法通过 create_all 处理
- 修改字段类型：无法通过 create_all 处理
- 适合开发阶段，生产环境应使用 Alembic/Flask-Migrate

### 5.2 __abstract__ 基类

```python
class Base(db.Model):
    __abstract__ = True   # Base 本身不创建表
    created_at = Column(...)
    status = Column(Integer, default=1)

class User(Base):         # User 继承 Base 的字段，User 创建表
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24))
```

`__abstract__ = True` 告诉 SQLAlchemy 这个类不映射到表，只作为其他模型的基类。

---

## 六、最佳实践总结

| 模式 | 说明 | 项目来源 |
|------|------|---------|
| `set_attrs(form.data)` | 批量赋值，排除 id 字段 | 两个项目共用 |
| `with db.auto_commit()` | 自动 commit/rollback 上下文 | fisher_end 独有 |
| `@password.setter` 自动加密 | 赋值时自动哈希，不会遗漏 | 两个项目共用 |
| 软删除 + 自定义 Query | `status=0` 标记删除，`filter_by` 自动过滤 | fisher_end 独有 |
| `__abstract__` 基类 | 公共字段复用，不创建表 | 两个项目共用 |
| `db.create_all()` Code First | 开发阶段自动建表 | 两个项目共用 |
| `filter_by().order_by().first()` | 链式操作，代码清晰 | 两个项目共用 |
| 方法放在模型上 | `recent()`、`delete()` 等业务方法归属模型 | fisher_end |
| 列表推导式转换结果 | `[BookViewModel(b) for b in books]` | 两个项目共用 |
| `credentials: 'include'` | 前端 fetch 携带 cookie | cloudBook |
