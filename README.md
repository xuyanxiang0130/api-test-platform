# 接口自动化测试平台（Flask + Pytest + MySQL + Allure + GitHub Actions CI）
## 项目介绍
基于Python Flask搭建轻量级Web接口自动化测试平台，采用数据库数据驱动。
支持网页管理测试用例、CSV批量导入/导出用例，一键执行pytest接口自动化，自动生成Allure可视化报告；
集成测试执行历史记录；接入GitHub Actions CI流水线，代码提交自动触发接口测试。

## 技术栈
- 后端：Python3.9 + Flask
- 测试框架：Pytest
- 数据库：MySQL，存储接口测试用例、测试执行历史
- 接口请求：requests
- 测试报告：Allure2
- CI流水线：GitHub Actions
- 数据导入导出：CSV文件解析
- 前端：原生HTML

## 平台功能清单
1. 用例管理
   - Web页面新增、删除单条接口测试用例
   - CSV批量导入测试用例（容错机制：单行数据异常不会中断整批导入）
   - CSV一键导出全部数据库内测试用例，实现用例导入导出闭环
2. 测试执行
   - 网页一键触发Pytest自动化测试
   - 自动统计用例执行结果，存入测试历史记录表
   - 支持查看Allure可视化测试报告
3. 执行历史
   - 记录每一轮测试：执行时间、任务状态、通过数、失败数
   - 支持查看单次执行详情
4. CI持续集成
   - 提交代码到GitHub仓库，自动触发CI任务
   - CI环境自动初始化MySQL，自动执行全套接口自动化测试


# 项目目录结构
- api-test-platform/
  - app.py # Flask 主服务，所有 web 路由
  - common/
    - request_util.py # 接口请求封装工具类
  - config/
    - settings.py # 配置文件，数据库配置，兼容本地 & CI环境变量
  - models/
    - db_model.py # 数据库建表、查询、操作函数
  - test_cases/
    - api_case.py # pytest 测试脚本，从 MySQL 读取用例做数据驱动
  - templates/ # HTML前端页面
  - .github/workflows/
    - ci.yml # GitHub Actions CI 流水线配置
  - requirements.txt # 项目依赖
  - .gitignore # git 忽略文件
  - README.md # 项目说明文档


## 本地部署步骤
### 1. 环境准备
1. 安装 MySQL 5.7/8.0，新建数据库 `api_platform`
2. 安装Python3.9
3. 安装Allure命令行工具，并配置环境变量

### 2. 克隆项目
```bash
git clone https://github.com/xuyanxiang0130/api-test-platform.git
cd api-test-platform

# 创建虚拟环境
python -m venv venv
# 激活虚拟环境 Windows
venv\Scripts\activate
# 安装全部依赖
pip install -r requirements.txt

# 两种运行方式
#方式 1：启动 Web 平台，手动管理用例，一键执行测试
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
> ⚠️ CI 使用临时 Ubuntu 虚拟机，流水线销毁后数据全部丢失，仅用于本次提交的回归测试。

csv用例模板说明：
模板字段顺序：
`case_name,url,method,headers,params,expect_code,expect_result,env_id`
字段	            说明	                填写规则
case_name	    用例名称	            自定义
url	            接口地址	            完整 http/https 地址
method	        请求方式	            GET / POST / PUT / DELETE
headers	        请求头	            JSON 字符串，为空写{}
params	        请求体	            JSON 字符串，为空写{}
expect_code	    预期状态码	        数字，如 200、201
expect_result	预期结果关键字	        在返回 JSON 中查找该字段
env_id	        环境 ID	            数字，本地默认填 1
⚠️注意：CSV 单元格内部包含双引号时，需要遵循 CSV 转义规范，避免导入字段错位。