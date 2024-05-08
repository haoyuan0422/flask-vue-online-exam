from flask import Blueprint
from flask import jsonify
from flask import request
from db_utils import get_conn


admin_bp = Blueprint("admin", __name__)

#获取教师信息
@admin_bp.route('/seacheradmin/<int:adminId>', methods=['GET'])
def get_teacherDetails(adminId):
    try:
        con = get_conn()
        cur = con.cursor()

        # 根据分页参数查询相应的教师信息
        cur.execute("SELECT * FROM admin where adminId = %s", adminId)
        admin_details = cur.fetchone()
        # print(admin_details)


        response_data = {
            'records':admin_details
        }


        return jsonify({'code': 200,'data': response_data})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if con:
            con.close()


# 编辑管理员信息
@admin_bp.route('/admin/edit', methods=['POST'])
def edit_teacherDetails():
    try:
        con = get_conn()
        cur = con.cursor()

        # 从前端请求中获取数据
        admin_data = request.get_json()
        adminId = request.get_json().get('adminId')

        cur.execute("""
            UPDATE admin
            SET
                adminName = %s,
                sex = %s,
                tel = %s,
                email = %s,
                cardId = %s,
                role = %s
            WHERE adminId = %s
        """, (
            admin_data.get('adminName'),
            admin_data.get('sex'),
            admin_data.get('tel'),
            admin_data.get('email'),
            admin_data.get('cardId'),
            admin_data.get('role'),
            adminId
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