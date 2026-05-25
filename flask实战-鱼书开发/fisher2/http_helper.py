'''两种请求方式
urlib : python自带
requests: third party

将 http.py 重命名为不与标准库冲突的名字
'''
import requests

class HTTP:
    @staticmethod
    def get(url,return_json=True):
        r = requests.get(url)
        # restful  json
        # 如果是json格式就调用json()方法
        if r.status_code != 200:
            return {} if return_json else ''
        if return_json:
            try:
                return r.json()
            except requests.exceptions.JSONDecodeError:
                return {}
        return r.text