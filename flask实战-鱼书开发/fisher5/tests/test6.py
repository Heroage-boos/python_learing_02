
from werkzeug.local import LocalStack

# push ，pop，top

s = LocalStack()  
s.push(1)
print(s.top) # 1
print(s.top) # 1
print(s.pop()) # 1
print(s.top) # None

s.push(1)
s.push(2)
# 栈 后进先出
print(s.top) # 2
print(s.top)  # 2
print(s.pop()) # 2 
print(s.top) # 1
