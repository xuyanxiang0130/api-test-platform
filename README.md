# API接口自动化测试平台（测试开发项目）
> 基于Flask + MySQL + Pytest + Allure 轻量接口测试平台，集成GitHub Actions持续集成流水线
> 项目用途：测试开发练手项目，实现人工Web手动执行 + CI代码提交自动回归两套执行方案

##  项目简介
本平台是轻量化接口自动化测试管理平台，区分两种使用场景：
1. 人工操作场景：Web页面管理接口测试用例（新增、查看用例），一键执行测试，保存测试历史记录，查看Allure测试报告
2. CI自动回归场景：接入GitHub Actions，代码push到仓库自动拉起流水线，自动搭建环境、初始化数据库、执行接口自动化，生成并保存Allure报告，用作版本质量门禁

##  技术栈
- 后端框架：Flask（Web后台）
- 数据库：MySQL，pymysql做数据库读写
- 自动化框架：Pytest + requests
- 测试报告：Allure
- CI流水线：GitHub Actions
- Python版本：3.9

##  项目目录结构

api-test-platform
├── .github/workflows
│   └── ci.yml          # GitHub Actions CI 流水线配置文件
├── config
│   └── settings.py     # 配置文件，支持环境变量，本地 / CI 多环境适配
├── common              # 公共工具包
│   └── request_util.py  # http 请求封装工具
├── models
│   └── db_model.py      # 数据库读写函数
├── test_cases
│   └── api_case.py      # pytest 测试执行逻辑，从 mysql 读取用例
├── templates           # Flask 网页 html 模板
├── app.py              # Flask 主程序，web 路由
├── requirements.txt    # python 依赖包
├── README.md



##  本地部署运行
### 1. 环境准备
1. 安装MySQL，新建数据库 `api_platform`
2. Python 3.9
3. 安装Allure命令行工具

### 2. 安装依赖
# 创建虚拟环境
python -m venv venv
# 激活虚拟环境
venv\Scripts\activate
# 安装依赖
pip install -r requirements.txt

# 3. 数据库配置
修改 `config/settings.py`
本地 MySQL 账号密码写入默认值；CI 流水线会自动通过环境变量覆盖数据库配置，业务代码无需改动。

# 4. 初始化数据库表
执行建表 SQL：创建 test_case（用例表）、test_history（测试历史表）

# 5. 两种运行方式

## 方式 1：启动 Web 平台，手动管理用例，一键执行测试
python app.py

浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 方式 2：直接执行 pytest 自动化（本地）
python -m pytest test_cases/api_case.py -v --alluredir=allure-results
# 查看报告
allure serve allure-results

## CI 流水线介绍（GitHub Actions）
触发规则：代码 push 到 main 分支，自动触发流水线
流水线执行步骤：

1. 拉取仓库代码
2. 配置 Python3.9 环境，安装项目依赖
3. 启动 MySQL 容器
4. 自动创建数据库表，预置测试用例
5. 注入数据库环境变量，自动切换 CI 数据库配置
6. 执行 pytest 接口自动化
7. 生成 Allure HTML 报告
8. 将报告打包为产物，可下载查看

> 
> ⚠️ CI 使用临时 Ubuntu 虚拟机，流水线销毁后数据全部丢失，仅用于本次提交的回归测试。