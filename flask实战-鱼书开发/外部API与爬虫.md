# 外部 API 与爬虫 — HTTP 调用封装与数据获取

> 基于 fisher_end 和 flask-cloudBook 两个项目的外部 API 调用实践

---

## 一、HTTP 工具类封装

### 1.1 基础版本 — cloudBook

**定义**（`app/libs/http_helper.py`）：

```python
import requests
from requests import Response

class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r: Response = requests.get(url)

        if r.status_code != 200:
            return {} if return_json else ''

        if return_json:
            try:
                return r.json()
            except requests.exceptions.JSONDecodeError:
                return {}
        else:
            return r.text
```

**设计要点**：

| 要点 | 说明 |
|------|------|
| `@staticmethod` | 纯工具方法，不依赖类或实例状态 |
| 类型注解 | `r: Response` 利用 PyCharm/VSCode 代码提示 |
| 状态码处理 | 非 200 → 返回空（不抛异常，业务层判断） |
| JSON 解析保护 | `try/except JSONDecodeError` — API 可能返回非 JSON |
| 双模式返回 | `return_json=True` → 解析为 dict；`False` → 返回原始文本 |

### 1.2 对比：直接用 requests vs 封装

```python
# 没有封装：每次都要写一堆重复代码
r = requests.get(url)
if r.status_code != 200:
    return {}
try:
    result = r.json()
except:
    result = {}

# 有封装：一行搞定
result = HTTP.get(url)
```

### 1.3 使用示例

```python
from app.libs.http_helper import HTTP

# 在 BookSpider 中使用
url = "http://t.talelin.com/v2/book/isbn/9787544291163"
book_data = HTTP.get(url)   # 返回 dict 或 {}
```

---

## 二、BookSpider 爬虫类（cloudBook）

### 2.1 完整实现

**定义**（`app/spider/book.py`）：

```python
from app.libs.http_helper import HTTP

class BookSpider:
    """spider for book"""
    # API URL 模板（类变量）
    isbn_url = "http://t.talelin.com/v2/book/isbn/{}"
    id_url = "http://t.talelin.com/v2/book/{}"
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&&start={}&count={}"

    def __init__(self, data):
        self.books = []     # 搜索结果列表
        self.total = ""     # 搜索结果总数

    def __single__(self, data):
        """填充单本书数据"""
        if data:
            self.total = 1
            self.books.append(data)

    def __collection__(self, data):
        """填充多本书数据"""
        self.books = data['books']
        self.total = data['total']

    def isbn_search(self, isbn):
        """按 ISBN 搜索（返回单本书）"""
        url = BookSpider.isbn_url.format(isbn)
        r = HTTP.get(url)
        self.__single__(r)

    def id_search(self, book_id):
        """按 ID 搜索（返回单本书）"""
        url = BookSpider.id_url.format(book_id)
        r = HTTP.get(url)
        self.__single__(r)

    def keyword_search(self, keyword, start=1, count=15):
        """按关键字搜索（返回多本书）"""
        url = BookSpider.keyword_url.format(keyword, start, count)
        r = HTTP.get(url)
        self.__collection__(r)
```

### 2.2 架构分析

```
            ┌─────────────────────┐
            │     BookSpider      │
            │                     │
            │  isbn_url (类变量)   │
            │  keyword_url (类变量) │
            │  id_url (类变量)     │
            │                     │
            │  __init__()         │ ← self.books = [], self.total = ""
            │  isbn_search()      │ ← 拼接 URL → HTTP.get() → __single__()
            │  keyword_search()   │ ← 拼接 URL → HTTP.get() → __collection__()
            │  id_search()        │
            │                     │
            │  __single__()       │ ← 填充单本书到 self.books
            │  __collection__()   │ ← 填充多本书到 self.books
            └─────────────────────┘
```

### 2.3 使用流程

```python
# 1. 创建爬虫实例
books = BookSpider(q)

# 2. 执行搜索（数据填充到实例的 books 和 total 属性）
if text_type == "isbn":
    books.isbn_search(q)
elif text_type == "key":
    books.keyword_search(q)

# 3. 通过 ViewModel 塑形后返回
book_collection = BookCollection()
book_collection.collect_book(books, keyword=q)
return json.dumps(obj=book_collection, default=lambda o: o.__dict__)
```

### 2.4 类变量 URL 模板

```python
class BookSpider:
    isbn_url = "http://t.talelin.com/v2/book/isbn/{}"
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&&start={}&count={}"
```

类变量存储在类上（而非实例上），所有实例共享同一个 URL 模板。如果要在子类中修改 URL，只需覆盖类变量即可。

---

## 三、YuShuBook（fisher 的演进）

### 3.1 fisher4/5：classmethod 模式（无状态）

```python
class YuShuBook:
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&count={}&start={}"

    @classmethod
    def search_by_isbn(cls, isbn_no):
        url = cls.isbn_url.format(isbn_no)
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        url = cls.keyword_url.format(keyword, 15, cls.calculate_start(page))
        result = HTTP.get(url)
        return result

    @classmethod
    def calculate_start(cls, page):
        return (page - 1) * 15

# 调用方式
result = YuShuBook.search_by_isbn('9787544291163')
result = YuShuBook.search_by_keyword('python')
```

**特点**：
- 全是 `@classmethod`，不创建实例
- 纯函数：输入 → 输出，不保存状态
- 搜索结果的解析在控制器中完成

### 3.2 fisher6 及之后：实例方法模式（有状态）

```python
class YuShuBook:
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = "http://t.talelin.com/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total = 0
        self.books = []   # 搜索结果保存在实例上

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, 15, self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books = [data]

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

# 调用方式
yushu_book = YuShuBook()          # 创建实例
yushu_book.search_by_isbn(isbn)   # 数据填充到 self
books = yushu_book.books          # 从实例属性读取结果
```

**改进点**：
- 搜索结果保存在实例上，清晰的"填充"语义
- 控制器不需要管理中间变量
- 可以链式操作

### 3.3 cloudBook 的 BookSpider = fisher6 的 YuShuBook

cloudBook 的 `BookSpider` 从一开始就采用了实例方法模式，`__single__` 和 `__collection__` 方法对应 fisher 的 `__fill_single` 和 `__fill_collection`。

---

## 四、URL 参数拼接

### 4.1 str.format() 方式

```python
# 位置参数
url = "http://t.talelin.com/v2/book/isbn/{}".format(isbn)

# 关键字参数
url = "http://t.talelin.com/v2/book/search?q={q}&start={start}&count={count}".format(
    q=keyword, start=0, count=15
)
```

### 4.2 is_isbn_or_keyword 分类器

```python
def is_isbn_or_keyword(q):
    # ISBN: 10 位或 13 位的纯数字
    if len(q) in [10, 13] and q.isdigit():
        return 'isbn'
    return 'key'
```

**使用**：

```python
text_type = is_isbn_or_keyword(q)

if text_type == "isbn":
    books.isbn_search(q)       # 精确搜索，返回 1 本
elif text_type == "key":
    books.keyword_search(q)    # 模糊搜索，返回多本
```

这是"同一个接口区分搜索类型"的关键——根据输入格式自动选择最合适的 API 端点。

---

## 五、API 返回数据格式化

### 5.1 原始 API 返回的问题字段

```python
# YuShuBook API 返回的原始数据
{
    "author": ["鲁迅", "朱自清"],    # 列表，前端需要字符串
    "pages": null,                    # Python None
    "summary": "很长的摘要...",       # 可能太长
    "images": {                       # 复杂的嵌套结构
        "large": "https://...",
        "medium": "https://..."
    }
}
```

### 5.2 ViewModel 中的格式化

```python
class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.author = "、".join(data['author'])          # 列表 → 字符串
        self.pages = data['pages'] or ""                  # None → ""
        self.summary = (data['summary'] or "")[:100]      # None → "" + 截取
        self.image = data['images']                       # 字段重命名
```

### 5.3 格式化方法总结

| 手段 | 代码 | 效果 |
|------|------|------|
| None → 空字符串 | `data['pages'] or ""` | `None` → `""` |
| 列表 → 字符串 | `"、".join(data['author'])` | `['鲁','朱']` → `'鲁、朱'` |
| 截取 | `data['summary'][:100]` | 长文本截断 |
| 字段重命名 | `self.image = data['images']` | `images` → `image` |
| 默认值 | `data.get('price', 0)` | key 不存在时返回 0 |
| 类型注解 | `r: Response = requests.get(url)` | IDE 代码提示 |

---

## 六、错误处理

### 6.1 HTTP 工具类的容错

```python
class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''    # 非 200 → 空值
        if return_json:
            try:
                return r.json()
            except JSONDecodeError:
                return {}                       # 非 JSON → 空值
        return r.text
```

**三层防护**：
1. HTTP 状态码非 200 → 返回空
2. JSON 解析失败 → 返回空
3. 网络连接失败 → requests 库会抛异常（由调用方处理）

### 6.2 数据填充的容错

```python
def __single__(self, data):
    if data:               # 只处理非空数据
        self.total = 1
        self.books.append(data)
```

如果 `HTTP.get()` 返回了 `{}`（空字典），`if data:` 为 False（空字典的布尔值为 False），不会意外添加空数据。

### 6.3 前端查询的容错

```python
# cloudBook: 控制器中
@web.route("/api/book/search")
def search() -> str:
    form = SearchFrom(request.form)
    if form.validate():      # 参数校验
        q = request.args.get("q", "")  # 默认空字符串
        # ...
    else:
        return jsonify({"msg": "参数错误"})
```

---

## 七、最佳实践总结

| 模式 | 说明 |
|------|------|
| HTTP 工具类封装 | 统一的异常处理、JSON 解析保护，避免散落的重复代码 |
| `@staticmethod` 工具方法 | 无状态纯函数，适合 HTTP 调用 |
| 类变量 URL 模板 | 方便修改和子类覆盖 |
| 实例方法保存搜索结果 | `self.books` 和 `self.total` 替代返回值和中间变量 |
| `is_isbn_or_keyword` 分类器 | 同一接口智能分发到不同 API |
| `str.format()` 拼接 URL | 清晰直观，优于字符串拼接 |
| ViewModel 格式化原始数据 | 将格式化逻辑从控制器分离到 ViewModel |
| `or ""` 处理 None | Python 中使用最广泛的 None 防御手段 |
| `if data:` 空值防护 | 防止空字典/空列表污染搜索结果 |
