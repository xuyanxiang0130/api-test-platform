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
    headers = json.loads(case["headers"]) if case["headers"] else {}
    # 请求参数字符串转字典，没有body就赋值None
    body = json.loads(case["params"]) if case["params"] else None
    # 预期状态码
    expect_code = case["expect_code"]

    # 调用send方法发送请求
    resp = req.send(method, url, headers, body)
    # 增加保护：如果resp是None，直接断言失败
    assert resp is not None, "接口请求失败，返回空"
    # 断言响应状态码和预期一致，失败pytest标记用例失败
    assert resp.status_code == expect_code

    # 如果配置了预期结果文本，额外断言响应包含该文本
    if case["expect_result"]:
        assert case["expect_result"] in resp.text

