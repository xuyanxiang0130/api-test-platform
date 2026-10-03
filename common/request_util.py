# 导入requests库，用来发送http接口请求
import requests

class HttpRequest:
    """http请求封装类，统一处理所有接口请求"""
    def send(self, method, url, headers=None, data=None):
        """
        发送http请求
        :param method: 请求方法 GET POST PUT
        :param url: 完整接口地址
        :param headers: 请求头字典
        :param data: post请求的body，字典
        :return: response对象
        """
        # 如果headers为空，赋值空字典，避免后续报错
        headers = headers if headers else {}
        try:
            print(f"正在发送请求：{method} {url}")
            # 发送请求，timeout超时10秒，防止接口卡死
            res = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                timeout=10
            )
            print(f"请求成功，status_code={res.status_code}")
            # 返回响应对象
            return res
        except Exception as e:
            # 捕获异常，打印错误信息
            print(f"❌ 请求异常：{e}")
            # 异常时返回None，后续代码做判断
            return None
