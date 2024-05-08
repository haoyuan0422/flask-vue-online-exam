from flask import Blueprint
from flask import jsonify
from flask import request
from db_utils import get_conn


student_bp = Blueprint("student", __name__)

#搜索考试信息
@student_bp.route('/exams/<int:current>/<int:size>/<string:inputValue>', methods=['GET'])
def searchExams(current, size, inputValue):
    try:
        con = get_conn()
        cur = con.cursor()

        source = inputValue
        # 根据分页参数查询相应的考试信息
        cur.execute("SELECT * FROM exam_manage where source = %s", (source,))
        exams = cur.fetchall()

        # 获取搜索到的考试总数
        total = len(exams)

        response_data = {
            'pagination': {
                'current': current,
                'total': total,
                'size': size,
                'records': exams
            }
        }

        return jsonify({'code': 200, 'data': response_data})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if con:
            con.close()



#获取当前用户的考试总数
@student_bp.route('/exams/<int:current>/<int:size>', methods=['GET'])
def get_exams(current, size):
    try:
        print("进入")
        con = get_conn()
        cur = con.cursor()

        # 根据分页参数查询相应的考试信息
        cur.execute("SELECT * FROM exam_manage LIMIT %s OFFSET %s", (size, (current - 1) * size))
        exams = cur.fetchall()
        # print(exams)

        # 获取考试总数
        cur.execute("SELECT COUNT(*) as total FROM exam_manage")
        total = cur.fetchone()['total']

        response_data = {
            'pagination':{
                'current':current,
                'total':total,
                'size':size,
                'records': exams
            }
        }

        return jsonify({'code': 200,'data': response_data})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if con:
            con.close()

# 获取考试详情页
@student_bp.route('/exam/<int:examCode>', methods=['GET'])
def get_examDetails(examCode):
    try:
        print(examCode)
        con = get_conn()
        cur = con.cursor()

        # 查询试卷详细信息
        cur.execute("SELECT * FROM exam_manage WHERE examCode = %s", (examCode,))
        exam_details = cur.fetchone()
        print(exam_details)

        # 查询试卷的题目信息（这里假设有个 paperId 字段关联试卷和题目，你需要根据实际情况调整）
        paperId = exam_details.get('paperId')
        cur.execute("SELECT * FROM paper_manage WHERE paperId = %s", (paperId,))
        paper_details = cur.fetchall()

        response_data = {
            'examData': exam_details,
            'paperId': paperId
        }

        return jsonify({'data': response_data})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if con:
            con.close()


# 获取考试题目的详情页
@student_bp.route('/paper/<int:paperId>', methods=['GET'])
def get_paperDetails(paperId):
    try:
        con = get_conn()
        cur = con.cursor()

        # 查询试卷详细信息
        cur.execute("SELECT * FROM paper_manage WHERE paperId = %s", (paperId,))
        paper_details = cur.fetchone()

        if not paper_details:
            return jsonify({'message': '未找到试卷'}), 404

        # 查询试卷包含的题目
        cur.execute("SELECT questionId, questionType FROM paper_manage WHERE paperId = %s", (paperId,))
        questions = cur.fetchall()

        # 初始化存储题目详情的列表
        choices = []
        fill_questions = []
        judges = [] 

        # 根据题目类型去不同的题目表中查询题目详情
        for question in questions:
            question_id = question['questionId']
            question_type = question['questionType']

            if question_type == 1:  # 选择题
                cur.execute("SELECT * FROM multi_question WHERE questionId = %s", (question_id,))
                choice = cur.fetchone()
                choices.append(choice)
            elif question_type == 2:  # 填空题
                cur.execute("SELECT * FROM fill_question WHERE questionId = %s", (question_id,))
                fill = cur.fetchone()
                fill_questions.append(fill)
            elif question_type == 3:  # 判断题
                cur.execute("SELECT * FROM judge_question WHERE questionId = %s", (question_id,))
                judge = cur.fetchone()
                judges.append(judge)

        exam_data = {
            'choices': choices,
            'fills': fill_questions,
            'judges': judges
        }

        return jsonify({'data': exam_data})

    except Exception as e:
        print(e)
        return jsonify({'error': '内部服务器错误'}), 500
    finally:
        if con:
            con.close()

# 将考试的成绩录入score表
@student_bp.route('/score', methods=['POST'])
def enter_score():
    data = request.get_json()

    exam_code = data.get('examCode')
    student_id = data.get('studentId')
    subject = data.get('subject')
    et_score = data.get('etScore')
    answer_date = data.get('answerDate')

    try:
        con = get_conn()
        cur = con.cursor()

        # 执行插入数据的 SQL 查询
        sql = f"INSERT INTO score (examCode, studentId, subject, score, answerDate) VALUES ('{exam_code}', '{student_id}', '{subject}', {et_score}, '{answer_date}')"
        cur.execute(sql)

        # 提交事务
        con.commit()

        return jsonify({'code': 200, 'message': 'Data inserted successfully'})
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if con:
            con.close()

#读取当前用户的成绩单
@student_bp.route('/score/<int:current>/<int:size>//<int:studentId>', methods=['GET'])
def get_score(current,size,studentId):
    try:
        con = get_conn()
        cur = con.cursor()

        cur.execute("SELECT * FROM score WHERE studentId = %s LIMIT %s OFFSET %s", (studentId, size, (current - 1) * size))
        score_details = cur.fetchall()

        cur.execute("SELECT COUNT(*) as total FROM score WHERE studentId = %s",studentId)
        total = cur.fetchone()['total']
        print("-------------------------------------------------------------------------------------------------------------------")
        print(score_details)

        
        response_data = {
            'records': score_details,
            'pagination':{
                'current':current,
                'total':total,
                'size':size
            }
        }

        return jsonify({'code': 200,'data': response_data},)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if con:
            con.close()

#获取学生信息
@student_bp.route('/seacherStudent/<int:studentId>', methods=['GET'])
def get_teacherDetails(studentId):
    try:
        con = get_conn()
        cur = con.cursor()

        # 根据分页参数查询相应的教师信息
        cur.execute("SELECT * FROM student where studentId = %s", studentId)
        student_details = cur.fetchone()
        # print(admin_details)


        response_data = {
            'records':student_details
        }


        return jsonify({'code': 200,'data': response_data})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if con:
            con.close()

# 编辑学生信息
@student_bp.route('/student/edit', methods=['POST'])
def edit_teacherDetails():
    try:
        con = get_conn()
        cur = con.cursor()

        # 从前端请求中获取数据
        student_data = request.get_json()
        studentId = request.get_json().get('studentId')

        cur.execute("""
            UPDATE student
            SET
                studentName = %s,
                major = %s,
                clazz = %s,
                tel = %s,
                email = %s,
                pwd = %s,
                cardId = %s,
                sex = %s,
                role = %s
            WHERE studentId = %s
        """, (
            student_data.get('studentName'),
            student_data.get('major'),
            student_data.get('clazz'),
            student_data.get('tel'),
            student_data.get('email'),
            student_data.get('pwd'),
            student_data.get('cardId'),
            student_data.get('sex'),
            student_data.get('role'),
            studentId
        ))

        # Commit changes to the database
        con.commit()
        return jsonify({'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if con:
            con.close()

#分页查询所有考生信息
@student_bp.route('/students/<int:current>/<int:size>', methods=['GET'])
def get_all_students(current, size):
    print (current)
    print (size)
    print("查询考生信息")
    try:
        con = get_conn()
        cur = con.cursor()

        # 根据当前页和每页大小计算偏移量
        offset = (current - 1) * size

        # 从数据库中检索分页的学生信息
        query = "SELECT studentName, studentId, institute, major, grade, clazz, sex, tel FROM student LIMIT %s OFFSET %s"
        cur.execute(query, (size, offset))
        rows = cur.fetchall()

        # 检索用于分页的记录总数
        total_query = "SELECT COUNT(*) FROM student"
        cur.execute(total_query)
        total = cur.fetchone()['COUNT(*)']

        # 将结果以字典格式准备好
        result = {
            'current': current,
            'total': total,
            'size': size,
            'data': [
                {
                    'studentName': row['studentName'],
                    'studentId': row['studentId'],
                    'institute': row['institute'],
                    'major': row['major'],
                    'grade': row['grade'],
                    'clazz': row['clazz'],
                    'sex': row['sex'],
                    'tel': row['tel'],
                } for row in rows
            ]
        }
        return jsonify({'code': 200, 'data': result})
    except Exception as e:
        print(e)
        return jsonify({'error': '内部服务器错误'}), 500
    finally:
        cur.close()
        con.close()

# #提交留言
# @student_bp.route('/message', methods=['GET', 'POST'])
# def submit_message():
#     data = request.json
#     title = data.get('title')
#     content = data.get('content')
#     time = data.get('date')

#     try:
#         con = get_conn()
#         cur = con.cursor()
#         with cur as cursor:
#             # 执行留言插入操作
#             sql = "INSERT INTO message (title, content, time) VALUES (%s, %s, %s)"
#             cursor.execute(sql, (title, content, time))
#         con.commit()
#         return '200'
#     except:
#         con.rollback()
#         return '400'
#     finally:
#         con.close()


# # #显示留言内容
# # @student_bp.route('/messages/<int:current>/<int:size>', methods=['GET', 'POST'])
# # def get_all_message(current, size):
    
