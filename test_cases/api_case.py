import pytest
import json
from common.request_util import HttpRequest
from models.db_model import get_all_cases

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
    method = case["method"]
    # 先安全取出headers，如果不存在，默认赋值None
    headers_str = case.get("headers", None)
    # 判断：有字符串就json解析，没有就空字典
    headers = json.loads(headers_str) if headers_str else {}

    # 请求参数字符串转字典，没有body就赋值None
    params_str = case.get("params", None)
    body = json.loads(params_str) if params_str else None
    # 预期状态码
    expect_code = case["expect_code"]

    # 调用send方法发送请求
    resp = req.send(method, url, headers, params=body, json_body=body)
    # 增加保护：如果resp是None，直接断言失败
    assert resp is not None, "接口请求失败，返回空"
    # 断言响应状态码和预期一致，失败pytest标记用例失败
    assert resp.status_code == expect_code

    # 如果配置了预期结果文本，额外断言响应包含该文本
    if case["expect_result"]:
        assert case["expect_result"] in resp.text

