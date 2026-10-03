# 从flask框架导入需要的能力
# Flask：核心web实例；render_template：渲染html页面；request：接收表单提交的数据
# redirect：页面跳转；url_for：根据函数名拿到路由地址
from flask import Flask, render_template, request, redirect, url_for
# pymysql：python操作mysql数据库的库
import pymysql
# subprocess 用来调用系统命令，执行pytest
import subprocess
# os 用来处理路径
import os
# 打开浏览器的库
import webbrowser
# 新增导入json模块，用来解析pytest输出统计用例数量
import json
# 导入刚刚写的建表函数
from models.db_model import create_test_history_table


# 创建Flask应用实例，__name__代表当前模块
app = Flask(__name__)

# =====================数据库配置=====================
db_config = {
    "host": "127.0.0.1",   # mysql本机地址
    "port": 3306,          # mysql端口，默认3306
    "user": "root",        # mysql用户名
    "password": "@Xyx5201314", # mysql密码
    "database": "api_platform", # 使用的数据库名
    "charset": "utf8mb4"    # 字符集，支持中文
}

# 函数：获取数据库连接
def get_db_conn():
    # 使用上面配置，建立和mysql的连接
    conn = pymysql.connect(**db_config)
    return conn


# =============路由1：首页，展示所有用例 GET请求===============
# @app.route 是路由装饰器：访问 http://127.0.0.1:5000/ 就会执行下面index函数
@app.route('/')
def index():
    # 1.获取数据库连接
    conn = get_db_conn()
    # 创建游标，DictCursor 代表查询结果以【字典】返回，方便html读取
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # 执行sql，查询test_case表全部数据
    cursor.execute("select * from test_case")
    # fetchall()拿到全部查询结果，是一个列表，里面每一条是字典
    case_list = cursor.fetchall()
    # 关闭数据库连接，释放资源
    conn.close()
    # render_template渲染templates文件夹里index.html页面
    # 把case_list传给html模板，html里就可以循环展示数据
    return render_template("index.html", cases=case_list)


# ======路由2：新增用例页面，支持GET和POST两种请求====
# GET：访问页面（打开表单）；POST：表单提交，保存数据到数据库
@app.route("/add", methods=["GET","POST"])
def add_case():
    # 判断：如果是POST请求，代表用户点击了【提交保存】，表单数据已经发过来了
    if request.method == "POST":
        # request.form 接收前端表单输入框的数据，name对应html里面input的name属性
        case_name = request.form["case_name"]
        url = request.form["url"]
        method = request.form["method"]
        headers = request.form["headers"]
        params = request.form["params"]
        expect_code = request.form["expect_code"]
        expect_result = request.form["expect_result"]
        env_id = request.form["env_id"]

        # 拿到数据后写入mysql
        conn = get_db_conn()
        cursor = conn.cursor()
        # 插入sql语句，%s是占位符，防止sql注入
        sql = """
        INSERT INTO test_case(case_name,url,method,headers,params,expect_code,expect_result,env_id)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行sql，把表单获取的值依次填充占位符
        cursor.execute(sql, (case_name, url, method, headers, params, expect_code, expect_result, env_id))
        # commit提交事务，数据库才真正写入这条记录
        conn.commit()
        conn.close()
        # 保存完成，自动跳转到首页（index函数对应的页面）
        return redirect(url_for("index"))

    # 如果是GET请求：只是访问/add页面，返回add.html表单页面
    return render_template("add.html")


# ====路由3：删除用例======
# <int:case_id>：url路径参数，例如 /delete/2，case_id=2
@app.route("/delete/<int:case_id>")
def delete_case(case_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    # 根据id删除对应用例
    cursor.execute("DELETE FROM test_case WHERE id=%s",(case_id,))
    conn.commit()
    conn.close()
    # 删除完跳转回首页
    return redirect(url_for("index"))


# ======新增：一键执行测试路由====
@app.route("/run_test")
def run_test():
    try:
        # 1. 获取app.py所在的项目根目录
        base_path = os.getcwd()
        # 拼接allure结果文件夹完整路径
        allure_result_dir = os.path.join(base_path, "allure-results")
        # 拼接虚拟环境里python.exe的绝对路径，强制使用venv的python，避免环境错乱
        python_exe_path = os.path.join(base_path, "venv", "Scripts", "python.exe")

        # 2. 如果allure结果文件夹存在，先删除旧数据，防止报告混杂
        if os.path.exists(allure_result_dir):
            # shell命令：windows rmdir 删除目录，/s包含子文件，/q静默不提示
            subprocess.run(
                f'rmdir /s /q "{allure_result_dir}"',
                shell=True,
                cwd=base_path,
                capture_output=True,
                text=True
            )

        # 3. 组装pytest执行命令，使用venv内python执行
        # --json-report：让pytest输出json报告，用来自动统计通过失败数量
        # --json-report-file=report.json 把统计结果保存到report.json文件
        pytest_cmd = fr'"{python_exe_path}" -m pytest test_cases/api_case.py -v --alluredir="{allure_result_dir}"'

        # 4. 调用系统命令执行pytest
        # shell=True Windows下开启cmd执行命令
        # cwd 指定命令在项目根目录运行
        # capture_output=True 捕获控制台输出
        # text=True 将输出转为字符串，方便读取
        result = subprocess.run(
            pytest_cmd,
            shell=True,
            cwd=base_path,
            capture_output=True,
            text=True
        )


        # 初始化统计变量
        pass_count = 0
        fail_count = 0
        task_status = "success"
        report_url = "/report"

        # 读取生成的report.json，解析用例执行效果
        report_file_path = os.path.join(base_path,"report.json  ")
        # json文件是否存在
        if os.path.exists(report_file_path):
            # 打开文件读取
            with open(report_file_path, "r", encoding="utf-8") as f:
                report_data = json.load(f)
                # 读取通过用例数量，取不到默认返回0
                pass_count = report_data["summary"].get("passed", 0)
                # 读取失败用例数量，取不到默认返回0
                fail_count = report_data["summary"].get("failed", 0)
                # 如果失败数>0，任务状态修改为fail
                if fail_count > 0:
                    task_status = "fail"
        #===本次执行记录插入历史表===
        conn = get_db_conn()
        cursor = conn.cursor()
        # sql语句插入
        insert_sql = """
            INSERT INTO test_history(status, pass_count, fail_count, report_url, remark)
            VALUES (%s, %s, %s, %s, %s) """
        #拼接备注信息，总用例
        remark_info = f"本次执行总用例书：{pass_count + fail_count}"
        # 执行插入语句
        cursor.execute(insert_sql,(task_status, pass_count, fail_count, report_url, remark_info))
        # 提交事务，写入数据库
        conn.commit()
        cursor.close()
        conn.close()

# 根据统计结果设置提示信息
        if task_status == "success":
            msg = f"执行完成，通过:{pass_count}条，失败：{fail_count}条"

        else:
            msg = f"测试执行完成，存在失败用例。通过：{pass_count}，失败：{fail_count}条\n控制台错误信息：{result.stderr}"
    except Exception as e:
        msg = f"执行测试异常：{str(e)}"
    return render_template("index.html", msg=msg)


# =========新增路由：打开allure报告无需终端命令打开页面 =====
@app.route("/report")
def open_allure_report():
    try:
        base_path = os.getcwd()
        allure_result_dir = os.path.join(base_path, "allure-results")
        # 判断allure原始结果文件夹是否存在，并且里面有文件
        if not os.path.exists(allure_result_dir) or len(os.listdir(allure_result_dir)) == 0:
        # 没有测试结果，返回提示消息，跳回首页
            msg = " 没有测试结果，请先执行测试用例！"
            return render_template("index.html", msg=msg)
        # 组装allureserve命令，在项目根目录执行
        allure_cmd = f"allure serve {allure_result_dir}"
    # subprocess.Popen：后台启动进程（不阻塞flask！！重点，不能用run）
    # Popen不会等待命令执行结束，直接往下走，不会卡住网页
        subprocess.Popen(
            allure_cmd,
            shell=True,
            cwd=base_path
        )
        msg = "Allure报告服务已启动，正在自动打开浏览器..."
    except Exception as e:
        msg = f"打开报告异常：{str(e)}"
    # 返回首页并携带提示信息
    return render_template("index.html", msg=msg)

# ====新增路由：查看测试历史====
@app.route("/history")
def show_history():
    """查询所有测试记录传到前端页面渲染"""
    conn = get_db_conn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # 查询test_history,按照时间倒叙
    cursor.execute("SELECT * FROM test_history ORDER BY execute_time DESC")
    # fetchall拿到全部查询结果
    history_list = cursor.fetchall()
    # 关闭数据库资源
    cursor.close()
    conn.close()
    # 返回首页，history_list传给前端
    return render_template("index.html", msg="",history_list=history_list)


# ==

# 程序入口：直接运行python app.py时，启动flask服务
if __name__ == '__main__':
    # 程序启动，自动创建测试历史表
    create_test_history_table()
    # debug=True，修改代码自动重启服务，开发用；上线必须关闭
    app.run(debug=True)
