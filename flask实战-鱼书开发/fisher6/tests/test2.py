class MyResource:
    def __enter__(self):
        print("connect to resource")
        return self
    
    # __exit__即使发生异常也会被执行
    def __exit__(self):
        print("disconnect to resource")
        # 返回False表示异常会被抛出 ，返回True表示异常不会被抛出
        return True

    def query(self):
        print("query data")
        
with MyResource() as resource:
    resource.query()