# ViewModel 与数据塑形 — 解耦数据获取与展示

> 基于 fisher_end 和 flask-cloudBook 两个项目的 ViewModel 实践

---

## 一、为什么需要 ViewModel

### 1.1 问题场景

外部 API 返回的原始数据结构往往不符合前端需求：

```json
// YuShuBook API 返回的原始数据
{
  "author": ["鲁迅", "朱自清"],    // 列表，前端需要字符串
  "pages": null,                    // 可能为 None
  "summary": "很长很长的摘要...",   // 可能太长
  "images": {...},                  // 结构复杂
  "price": "39.00",
  "binding": "精装",
  "_internal_field": "xxx"          // 内部字段不应暴露
}
```

直接返回原始数据的问题：
1. **前端展示逻辑散落**：每次都要处理 `None` → `""`、`list` → `str` 等转换
2. **暴露内部字段**：API 返回值可能包含不应该传给前端的字段
3. **重复代码**：多个页面用到同一数据时需要重复编写转换逻辑
4. **测试困难**：展示逻辑和视图逻辑混在一起

### 1.2 ViewModel 的职责

```
原始 API 数据 ──→ ViewModel ──→ 前端可用的干净数据

      数据获取层              数据展示层
      (spider/API)           (ViewModel)
```

ViewModel 在数据获取和数据展示之间形成一个中间层，将"如何转换数据"的逻辑集中管理。

---

## 二、单本书塑形 — BookViewModel

### 2.1 cloudBook 的实现

**定义**（`app/view_models/book.py:6-16`）：

```python
class BookViewModel:
    def __init__(self, book):
        self.id = book['id']
        self.title = book['title']
        self.author = book['author']        # API 返回的原始字段
        self.binding = book['binding']
        self.publisher = book['publisher']
        self.price = book['price']
        self.image = book['images']         # 字段重命名：images → image
        self.summary = book['summary']
        self.isbn = book['isbn']

# 使用
book_model = BookViewModel(book=book.books[0])
# book_model 现在有 id, title, author, image, summary, isbn 等属性
```

**这个实现做的转换**：
- `book['images']` → `self.image`（字段重命名）
- 只保留前端需要的字段（裁剪）

### 2.2 fisher_end 更完善的实现

**定义**（`fisher/app/view_models/book.py`）：

```python
class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.publisher = data['publisher']
        self.pages = data['pages'] or ""                 # None → ""
        self.author = "、".join(data['author'])           # 列表 → 字符串
        self.price = data['price']
        self.summary = (data['summary'] or "")[:100]     # None → "" + 截取
        self.image = data['images']
        self.isbn = data['isbn']
        self.pubdate = data['pubdate']
        self.binding = data['binding']
```

**这个实现做了更多转换**：
1. `pages = data['pages'] or ""` — None 值转为空字符串
2. `author = "、".join(data['author'])` — 作者列表转为可读字符串（`['鲁迅', '朱自清']` → `'鲁迅、朱自清'`）
3. `summary = (data['summary'] or "")[:100]` — None 转为空字符串后截取前 100 字
4. `image = data['images']` — 字段重命名（images → image）

### 2.3 对比总结

| 转换类型 | fisher_end | cloudBook |
|---------|-----------|-----------|
| 字段裁剪 | 仅保留需要字段 | 仅保留需要字段 |
| 字段重命名 | `images→image` | `images→image` |
| None 处理 | `or ""` | 无（直传） |
| 数据类型转换 | `join(author)` | 无（直传） |
| 文本截取 | `summary[:100]` | 无（直传） |
| 日期格式化 | `pubdate` | 无 |

**评价**：fisher_end 的 ViewModel 更加完善，cloudBook 的 ViewModel 只是一个精简版本，缺少了最关键的数据清洗步骤。

---

## 三、集合塑形 — BookCollection

### 3.1 cloudBook 的实现

**定义**（`app/view_models/book.py:19-31`）：

```python
class BookCollection:
    def __init__(self):
        self.books = []       # 要返回的书列表
        self.total = 0        # 总数
        self.keyword = ''     # 搜索关键词

    def collect_book(self, books_info, keyword=""):
        self.total = books_info.total
        self.keyword = keyword
        # 列表推导式：将每本书的原始数据转为 BookViewModel
        self.books = [BookViewModel(b) for b in books_info.books]
```

**使用方式**：

```python
# 控制器中
book_collection = BookCollection()
book_collection.collect_book(books_spider, keyword=q)
return json.dumps(obj=book_collection, default=lambda o: o.__dict__)
```

**返回的 JSON 结构**：
```json
{
  "books": [
    {"id": 1, "title": "...", "author": "...", "image": "...", ...},
    ...
  ],
  "total": 100,
  "keyword": "python"
}
```

### 3.2 列表推导式解析

```python
self.books = [BookViewModel(b) for b in books_info.books]
```

这行代码做了：
1. 遍历 `books_info.books`（原始 API 数据列表）
2. 对每本书 `b`，调用 `BookViewModel(b)` 进行塑形
3. 生成 `BookViewModel` 对象列表

**带条件过滤的推导式**：
```python
# 只处理价格低于 100 的书
[BookViewModel(b) for b in books if b.get('price', 0) < 100]

# 处理并添加索引
[{**BookViewModel(b).__dict__, 'index': i} for i, b in enumerate(books)]
```

### 3.3 Fisher 的演进：classmethod → 实例方法

**fisher5 的 classmethod 版本**（无状态）：

```python
class BookCollection:
    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            "books": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            returned["total"] = data.get("total", 0)
            returned["books"] = [
                cls.__cut__book_data(book) for book in data["books"]
            ]
        return returned

    @classmethod
    def __cut__book_data(cls, data):
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "pages": data["pages"] or "",
            ...
        }
        return book

# 调用：BookCollection.package_collection(result, q)
```

**fisher6 的实例方法版本**（有状态）：

```python
class BookCollection:
    def __init__(self):
        self.keyword = ""
        self.total = 0
        self.books = []

    def fill(self, yushu_book, keyword):
        self.keyword = keyword
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]

# 调用：
books = BookCollection()
books.fill(yushu_book, q)
```

**为什么改**：classmethod 无状态（输入→输出纯函数），实例方法可以在对象上保存中间状态，多个方法可以操作同一份数据。cloudBook 从一开始就用的是实例方法模式。

---

## 四、json.dumps default 序列化

### 4.1 问题：jsonify 无法序列化自定义对象

```python
books = BookCollection()
books.collect_book(spider, q)

# 这会报错
return jsonify(books)
# TypeError: Object of type BookCollection is not JSON serializable
```

**原因**：`jsonify()` 底层调用 `json.dumps()`，后者只能序列化 `dict`, `list`, `str`, `int`, `float`, `bool`, `None` 这些基本类型。

### 4.2 解决方案：default 参数

```python
# 使用 json.dumps 的 default 参数
return json.dumps(obj=book_collection, default=lambda o: o.__dict__)
```

**`default` 参数**：当 json.dumps 遇到无法序列化的对象时，调用该函数。`o.__dict__` 将对象转为属性字典（dict 可以被正常序列化）。

### 4.3 对比

| 方法 | 自定义对象 | Content-Type | 使用场景 |
|------|-----------|-------------|---------|
| `jsonify(dict)` | 不支持 | 自动 `application/json` | 返回纯字典时最方便 |
| `json.dumps(obj, default=lambda o: o.__dict__)` | 支持 | 需手动设置 | 返回 ViewModel 对象时 |
| `json.dumps(obj.__dict__)` | 需要手动转 | 需手动设置 | 也可行但多一步 |

### 4.4 解释权反转

```python
# 默认模式：json 模块控制序列化方式
json.dumps(books)  # → json 遇到未知类型 → 报错

# default 模式：对象自己决定如何被序列化（解释权反转）
json.dumps(books, default=lambda o: o.__dict__)
# → json 遇到未知类型 → 调用 default → 对象提供自己的字典表示
```

**设计意义**：将"如何序列化"的控制权从 json 模块转移到业务对象自身。这与 ViewModel 的核心理念一致——数据如何展示由 ViewModel 决定，而非由调用方决定。

---

## 五、序列化方式总结

### 5.1 cloudBook 的方式

```python
# 1. 创建 BookViewModel（单本书塑形）
book_model = BookViewModel(book=books_info.books[0])

# 2. 序列化 BookViewModel 对象
return json.dumps(obj=book_model, default=lambda o: o.__dict__)

# 3. 或创建 BookCollection（多本书塑形）
book_collection = BookCollection()
book_collection.collect_book(books_spider, keyword=q)
return json.dumps(obj=book_collection, default=lambda o: o.__dict__)
```

### 5.2 直接返回 __dict__ 的问题

```python
class BookCollection:
    def __init__(self):
        self.books = []
        self.total = 0
        self.keyword = ''

# __dict__ = {"books": [BookViewModel对象, ...], "total": 100, "keyword": "python"}
# 每个 BookViewModel 也是对象，default=lambda o: o.__dict__ 会递归转换
```

注意：`default=lambda o: o.__dict__` 是**递归**的——如果 `self.books` 列表里的元素也是自定义对象，json.dumps 遇到它们时也会调用 `default`。

### 5.3 更好的序列化方式：在 ViewModel 中定义 to_dict()

```python
class BookCollection:
    def __init__(self):
        self.books = []
        self.total = 0
        self.keyword = ''

    def to_dict(self):
        return {
            "books": [b.to_dict() if hasattr(b, 'to_dict') else b.__dict__
                      for b in self.books],
            "total": self.total,
            "keyword": self.keyword
        }

# 使用
return json.dumps(book_collection.to_dict())   # 不需要 default 参数
```

这种方式更可控、更安全——你可以精确控制哪些字段被暴露，而不是一股脑地把 `__dict__` 全部倒出去。

---

## 六、ViewModel 与前后端分离

在前后端分离架构中，ViewModel 的价值更加明显：

```
前端期望的数据格式 ← ViewModel 屏蔽差异 → 后端 API 返回的原始数据

如果 API 源从 YuShuBook 切换到 Google Books：
  - 只需修改 ViewModel，前端代码不变
  - 控制器代码不变（只依赖 ViewModel 接口）
```

**接口隔离**：
```python
# 控制器只依赖 ViewModel，不依赖具体数据源
book_collection = BookCollection()
book_collection.collect_book(books_spider, keyword=q)
# 无论 books_spider 的数据来自哪个 API，ViewModel 保证输出格式一致
return json.dumps(obj=book_collection, default=lambda o: o.__dict__)
```

---

## 七、最佳实践总结

| 实践 | 说明 |
|------|------|
| ViewModel 做数据裁剪 | 只暴露前端需要的字段，隐藏内部字段 |
| ViewModel 做数据清洗 | None → ""、list → str、文本截取等 |
| 实例方法而非 classmethod | 可以在对象上保存状态，支持链式调用 |
| `json.dumps(default=lambda o: o.__dict__)` | 序列化自定义对象的简单方式 |
| 控制器不碰原始 API 数据 | 所有数据转换逻辑都封装在 ViewModel 中 |
| to_dict() 显式序列化 | 比 __dict__ 更可控，明确暴露哪些字段 |
| ViewModel 屏蔽数据源差异 | 切换数据源只需改 ViewModel，无需改控制器 |
