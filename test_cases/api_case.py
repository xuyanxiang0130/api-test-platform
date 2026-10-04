import pytest   # 导入pytest测试框架
import json    # 导入json，用来把字符串转字典
from common.request_util import HttpRequest  # 导入我们封装的请求类
from models.db_model import get_all_cases    # 导入读取数据库用例的函数

# 实例化请求对象
req = HttpRequest()
# 调用方法从数据库拿到全部用例
cases = get_all_cases()

# parametrize参数化，循环遍历cases里面每一条用例
@pytest.mark.parametrize("case",cases)
def test_api(case):
    """接口自动化测试用例，从mysql读取数据驱动执行"""
    # 获取接口地址
    url = case["url"]
    # 获取请求方法GET/POST
    method = case["method"]

    # 安全读取headers，如果没有这个key，返回None
    headers_str = case.get("headers", None)
    # 如果headers_str不为空，解析json，否则空字典
    headers = json.loads(headers_str) if headers_str else {}

    # 安全读取params，没有key返回None
    params_str = case.get("params", None)
    # params_str不为空才解析，否则赋值None
    body = json.loads(params_str) if params_str else None
    
    # 预期状态码
    expect_code = case["expect_code"]
    # 调用send方法发送请求
    resp = req.send(method, url, headers, body)
    # 增加保护：如果resp是None，直接断言失败
    assert resp is not None, "接口请求失败，返回空"
    # 断言响应状态码和预期一致，失败pytest标记用例失败
    assert resp.status_code == expect_code
    # 如果配置了预期结果文本，额外断言响应包含该文本
    if case.get("expect_result"):
        assert case["expect_result"] in resp.text
