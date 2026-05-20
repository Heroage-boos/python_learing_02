'''如何使用正则表达式
对字符串操作的一种逻辑公式，用特定字符组成一个规则字符串，用这个规则字符串来进行匹配、查找、替换等操作
'''

'''正则表达式应用场景
1. 数据验证：手机号，邮箱，网址，身份证号，密码强度
2. 文本处理：搜索与替换，分割与组合，提取与验证
3. 网站爬虫：从网页中提取所需信息，过滤广告，整理数据
'''

# 导入正则表达式库
import re
# 导入操作系统库
import os

# 匹配出文本中的数字

regex = r'[0-9]+'
ss = '2'

script_dir = os.path.dirname(os.path.abspath(__file__))
content_path = os.path.join(script_dir, 'content.txt')

with open(content_path, mode='r', encoding='utf-8') as file:
    content=file.read()
    print(content)

    #返回字符串中pattern的所有非重叠匹配项作为字符串列表
    print("======re.findal",re.findall(ss,content))  #['2', '2', '2', '2', '2', '2', '2', '2']
    print("======re.findal22",re.findall(regex,content))  #['2025', '80', '1', '22', '4', '2025', '23', '2', '1', '12333134134', '2', '12345678987', '3', '1233313413412', '4', '12333134', '5', '15326545874']


    # 匹配出文本中的数字
    match = re.search(regex, content)
    print('match_number',match) #match_number <re.Match object; span=(169, 173), match='2025'>

    # 获取到手机号码
    match_phone = re.findall(r'\d{11}', content)
    print('match_phone',match_phone) #match_phone ['12333134134', '12345678987', '12333134134', '15326545874']
    

    # 提取邮箱
    match_email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
    print('match_email',match_email)  #match_email ['1323658@qq.com', '223@163.com']

    # 使用正则验证账号是否合法
    username = "admin2w"
    # re.match 从字符串的开头开始匹配,如果字符串中间不符合，也不会返回  不匹配返回None
    print(re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$', username)) #<re.Match object; span=(0, 7), match='admin2w'>
    # if re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$', username):
    #     print('用户名合法')
    # else:
    #     print('用户名不合法')


    # 匹配网页中的url #兼容http和https ,.com 或 .con 顶级域名
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    print('urls',urls)  # urls ["http://www.baidu.com", 'https://www.google.com']

