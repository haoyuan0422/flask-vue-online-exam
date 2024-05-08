import pymysql
from pymysql import cursors

def get_conn():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='21201722',
        port=3306,
        db='bigjob',
        cursorclass=cursors.DictCursor
    )