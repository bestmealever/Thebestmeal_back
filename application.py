from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import os
from flaskext.mysql import MySQL
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


application = Flask(__name__)

mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = os.environ["MYSQL_DATABASE_USER"]
application.config['MYSQL_DATABASE_PASSWORD'] = os.environ["MYSQL_DATABASE_PASSWORD"]
application.config['MYSQL_DATABASE_DB'] = os.environ["MYSQL_DATABASE_DB"]
application.config['MYSQL_DATABASE_HOST'] = os.environ["MYSQL_DATABASE_HOST"]
mysql.init_app(application)

SECRET_KEY = 'SPARTA'

cors = CORS(application, resources={r"/*": {"origins": "*"}})

@application.route('/')
def main():
    return 'hello'

@application.route('/test', methods=['POST'])
def test():
    return {'msg': 'testtesttest'}


# @application.route('/sign_in', methods=['POST'])
# def sign_in():
#     # 로그인
#     username_receive = request.form['username_give']
#     password_receive = request.form['password_give']
#
#     pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
#     result = db.users.find_one({'username': username_receive, 'password': pw_hash})
#
#     if result is not None:
#         payload = {
#             'id': username_receive,
#             'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#
#         return jsonify({'result': 'success', 'token': token})
#     # 찾지 못하면
#     else:
#         return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@application.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM user_info WHERE name = '{username_receive}'")
    value = cursor.fetchall()

    if value == ():
        exists = True
    else:
        exists = False
    conn.commit()
    conn.close()
    return jsonify({'result': 'success', 'exists': exists})


@application.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT max(idx) as max FROM user_info")
    value = cursor.fetchall()
    idx = value[0]['max']
    cursor.execute(f"insert into user_info (idx, id, pw, created_at) value({idx + 1}, {username_receive}, {password_hash}, {created_at})")
    conn.commit()
    conn.close()

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)