# Flask轻量接口测试平台（测试开发练手项目）
> 技术栈：Python + Flask + Pytest + Allure + MySQL

## 项目功能
1. 测试用例管理：新增、删除接口测试用例，存储在MySQL数据库
2. 一键执行自动化：网页点击按钮调用pytest执行接口自动化
3. Allure报告：一键拉起Allure可视化测试报告，查看执行结果

## 目录结构
api-test-platform/
├── app.py                  # flask项目入口，启动文件
├── requirements.txt        # 项目依赖包列表
├── README.md               # 项目说明文档
├── .gitignore              # git忽略文件配置
├── venv/                   # python虚拟环境目录
├── common/                 # 公共工具模块
│   ├── allure_report.py    # allure报告相关封装
│   └── request_util.py      # 请求工具类，封装requests
├── config/                 # 配置文件目录
│   └── settings.py         # 项目全局配置
├── logs/                   # 日志存放目录
├── models/                 # 数据库模型
│   └── db_model.py         # orm数据库模型定义
├── reports/                # 测试报告输出目录（allure报告）
├── templates/              # flask网页模板，jinja2 html页面
│   ├── add.html            # 添加用例页面
│   └── index.html          # 用例列表首页
└── test_cases/             # 自动化测试用例
    └── api_case.py         # 接口自动化用例


## 启动步骤
1. 创建虚拟环境 `python -m venv venv`
2. 激活虚拟环境 `venv\Scripts\activate`
3. 安装依赖 `pip install flask pymysql pytest allure-pytest`
4. 启动项目 `python app.py`
5. 浏览器访问 http://127.0.0.1:5000

## 项目拓展方向
- 当前版本同步执行，Web会阻塞；生产可引入Celery+Redis异步任务队列
- 增加历史测试任务记录，保存多轮执行报告
