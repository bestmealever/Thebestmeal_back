from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import os
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGO_DB_PATH"))

db = client.bestmealever

application = Flask(__name__)

SECRET_KEY = 'bestmealever'

cors = CORS(application, resources={r"/*": {"origins": "*"}})

@application.route('/')
def main():
    return render_template('index.html')

@application.route('/test', methods=['POST'])
def test():
    return {'msg': 'testtesttest'}


@application.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@application.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.user_info.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@application.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    user_info_count = db.user_info.count()

    if user_info_count == 0:
        max_value = 1
    else:
        max_value = db.user_info.find_one(sort=[("idx", -1)])['idx'] + 1

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    doc = {
        "idx": max_value,
        "id": username_receive,
        "pw": password_hash,
        "profile": "",
        "profile_pic": "",
        "created_at": created_at,
        "updated_at": ""
    }

    db.user_info.insert_one(doc)

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)