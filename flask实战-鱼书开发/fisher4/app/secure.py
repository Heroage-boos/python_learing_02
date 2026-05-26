'''  config.py -> secure.py
               -> setting.py
配置文件
配置文件中的命名一般都大写（常量）

secure.py 是flask中用于处理跨站请求伪造（CSRF）的模块
保存一些敏感数据，不应该上传到github（远程仓库）

生产环境和测试环境配置也不同
'''

DEBUG = True