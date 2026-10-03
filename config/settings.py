# 导入pymysql,用于连接数据库
import pymysql
import os

# 读取环境变量，CI流水线会注入下面这些环境变量；本地没有环境变量，就使用默认本地配置
# os.getenv("变量名", 默认值)：如果系统没有这个环境变量，就取后面默认值
# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "@Xyx5201314"),
    "database": os.getenv("DB_DATABASE", "api_platform"),
    "charset": "utf8mb4",
}

# 多环境基础地址
ENV = {
    "test": "http://httpbin.org",               # 测试环境，httpbin模拟接口
    "pre": "https://jsonplaceholder.typicode.com" #预发环境
}

# 失败用例重试次数
RETRY_COUNT = 1