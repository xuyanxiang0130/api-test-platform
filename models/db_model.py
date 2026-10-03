# 数据库读写代码
import pymysql
from config.settings import DB_CONFIG

def get_db_conn():
    """获取数据库连接对象"""
    # 使用配置里面的参数建立数据库连接
    conn = pymysql.connect(**DB_CONFIG)
    # 返回连接，给外部函数调用
    return conn

# 获取全部用例
def get_all_cases():
    """读取test_case表中全部接口用例，返回列表"""
    # 调用函数拿到数据库连接
    conn = get_db_conn()
    # 创建游标，DictCursor代表查询结果以字典形式返回
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM test_case"
    # 执行sql语句
    cursor.execute(sql)
    # 获取查询结果
    result = cursor.fetchall()
    # 关闭游标，释放资源
    cursor.close()
    # 关闭数据库连接
    conn.close()
    # 返回所有用例数据
    return result

# 新增用例
def add_case(case_name,url,method,headers,params,expect_code,expect_result,env_id):
    """新增接口用例到数据库
        :param case_name: 用例名称
        :param url: 接口路径
        :param method: 请求方式 GET/POST
        :param headers: 请求头json字符串
        :param params: 请求体json字符串
        :param expect_code: 预期响应码
        :param expect_result: 预期包含文本
        :param env_id: 环境id，关联test_env表
        """
    # 获取数据库连接
    conn = get_db_conn()
    # 创建游标
    cursor = conn.cursor()
    sql = """INSERT INTO test_case(case_name,url,method,headers,params,expect_code,expect_result,env_id)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (case_name, url, method, headers, params, expect_code, expect_result, env_id))
    conn.commit()
    cursor.close()
    conn.close()