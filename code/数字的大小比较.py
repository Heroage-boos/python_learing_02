num_1 = 1233
num_2 = 1234

print(num_1 > num_2)
print(num_1 >= num_2)
print(num_1 < num_2)
print(num_1 <= num_2)
print(num_1 == num_2)
print(num_1 != num_2)


# 在数字大小比较运算中，实际项目中常用的场景和运算符包括：

## 基础比较运算符

# | 运算符 | 含义 | 示例 |
# |--------|------|------|
# | `>` | 大于 | `a > b` |
# | `<` | 小于 | `a < b` |
# | `>=` | 大于等于 | `a >= b` |
# | `<=` | 小于等于 | `a <= b` |
# | `==` | 等于 | `a == b` |
# | `!=` | 不等于 | `a != b` |

## 实际项目中的常见应用场景

### 1. 数据验证与边界检查
# 年龄范围验证
age = 25
if 0 <= age <= 150:
    # 有效年龄
    pass

page_size = 5
# 分页参数校验
if page_size > 0 and page_size <= 100:
    # 合法的分页大小
    pass


### 2. 排序与查找算法
# 冒泡排序、二分查找等
arr = [1, 2, 3, 4, 5]
target = 3
left = 0
right = len(arr) - 1
for mid in range(left, right + 1):
    if arr[mid] < target:
        left = mid + 1
    elif arr[mid] > target:
        right = mid - 1

### 3. 排行榜/Top N 计算
# 维护前K大元素
if len(heap) < k:
    heapq.heappush(heap, num)
elif num > heap[0]:
    heapq.heapreplace(heap, num)

### 4. 价格/数值区间判断
# 会员等级判定
if total_amount >= 10000:
    level = "钻石"
elif total_amount >= 5000:
    level = "铂金"
elif total_amount >= 1000:
    level = "黄金"

### 5. 时间戳比较
# 判断过期时间
if current_timestamp > expire_timestamp:
    # 已过期
    pass

### 6. 浮点数比较（注意精度问题）
import math

# 避免直接用 == 比较浮点数
if math.isclose(a, b, rel_tol=1e-9):
    # 近似相等
    pass

## 常用函数/方法
# | 语言 | 函数/方法 | 用途 |
# |------|-----------|------|
# | Python | `max(a, b)`, `min(a, b)` | 取最大/最小值 |
# | Python | `sorted()`, `list.sort()` | 排序 |
# | Python | `bisect` 模块 | 二分查找插入 |
# | Python | `heapq` 模块 | 堆操作（Top K） |
# | JavaScript | `Math.max()`, `Math.min()` | 取最大/最小值 |
# | Java | `Collections.max()`, `Collections.min()` | 取最大/最小值 |

## 实际开发建议

# 1. **注意浮点数精度**：不要用 `==` 直接比较浮点数
# 2. **考虑溢出**：大数比较时注意数据类型范围
# 3. **空值处理**：比较前先判断是否为 `None`/`null`/`undefined`
# 4. **类型一致性**：确保比较的是相同类型（如字符串和数字比较会先转换）
