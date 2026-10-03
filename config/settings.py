# 导入pymysql,用于连接数据库
import pymysql

# 数据库配置
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "@Xyx5201314",
    "database": "api_platform"
}

# 多环境基础地址
ENV = {
    "test": "http://httpbin.org",               # 测试环境，httpbin模拟接口
    "pre": "https://jsonplaceholder.typicode.com" #预发环境
}

# 失败用例重试次数
RETRY_COUNT = 1