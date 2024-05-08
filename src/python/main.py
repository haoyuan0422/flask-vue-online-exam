from flask import Flask, jsonify, session
from flask import request
from student import student_bp
from teacher import teacher_bp
from admin import admin_bp
from db_utils import get_conn
from flask_cors import CORS
import secrets


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = secrets.token_hex(16)

# 注册蓝图
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(admin_bp)

app.route('/')
def hello_world():  # put student_bplication's code here
    return 'Hello World!'

#登录端口
@app.route('/login', methods=['POST'])
def login():
    print("进入")
    #获取前端账号信息
    data = request.json  # 假设前端发送的是 JSON 数据
    user_id = data.get('username')
    password = data.get('password')

    #获取数据库信息
    con = get_conn()
    cur = con.cursor()

    #根据用户账号获取对应的登录角色
    cur.execute("SELECT userRole FROM UserRole WHERE userId = %s", (user_id))
    loginRole = cur.fetchone()
    print(loginRole)
    print(loginRole['userRole'])

    # 根据登录角色查询对应的用户表
    if loginRole['userRole'] == 0:  # 0:超级管理员
        cur.execute(f"SELECT adminName, adminId, pwd, role FROM admin WHERE adminId = %s", (user_id,))
        return authenticate_user(cur,password,'adminId','adminName')
    elif loginRole['userRole'] == 1:  # 1:教师
        cur.execute(f"SELECT teacherName, teacherId, pwd, role FROM teacher WHERE teacherId = %s", (user_id,))
        return authenticate_user(cur,password,'teacherId','teacherName')
    elif loginRole['userRole'] == 2:  # 2:学生
        cur.execute(f"SELECT studentName, studentId, pwd, role FROM student WHERE studentId = %s", (user_id,))
        return authenticate_user(cur,password,'studentId','studentName')

#登录信息比对方法  
def authenticate_user(cur,password,primary_key,userName):
    user = cur.fetchone()
    if user and user['pwd'] == password:
        # 用户验证成功
        session[primary_key]=user[primary_key]
        session['role']=int(user['role'])
        response_data = {
            'userId': user[primary_key],
            'userName': user[userName],
            'role': user['role']
            # 根据需要添加其他字段
        }
        return jsonify({'data': response_data})
    else:
        return jsonify({'data': None, 'message': '无效的凭证'})
    
# 设置服务器端拦截器
@app.before_request
def before():
    url = request.path  # 当前请求的 URL
    passUrl = ["/login", "/regist"]

    if url in passUrl:
        pass
    elif request.method == 'OPTIONS':
        # 设置允许的方法和头信息
        response_headers = {
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return '', 200, response_headers
    else:
        role = session.get("role")
        userId = None  # 默认值为 None

        if role == 0:
            userId = session.get("adminId", None)
            print(userId)
        elif role == 1:
            userId = session.get("teacherId", None)
            print(userId)
        elif role == 2:
            userId = session.get("studentId", None)
            print(userId)

        if not userId:
            return jsonify({"msg": "Bad username or password"}), 401

    # 在这里添加 return 语句
    return None


if __name__ == '__main__':
    app.run(host='192.168.239.155',port=5000)

