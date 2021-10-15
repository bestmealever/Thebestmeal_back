# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
import random
import os
import boto3

app = Flask(__name__)

# 배포서버
client = MongoClient(os.environ.get("MONGO_DB_PATH"))

# 로컬서버
client = MongoClient('localhost', 27017)

db = client.team_project


class WhatYouWantForMeal:
    def __init__(self):
        self.for_reverse = ['korean', 'chinese', 'japanese', 'western', 'snack', 'bread', 'supper', 'fastfood', 'salad']
        self.retry_num = 0
        self.recommend = ''
        self.address = ''
        self.want = list()
        self.feel = list()
        self.chosen = list()
        self.choice_num = list()

    def want_receive(self, want_give):
        self.want = want_give

    def yesterday(self, yesterday_give):
        yesterday_give_receive_reverse = []
        for i in self.for_reverse:
            if i not in yesterday_give:
                yesterday_give_receive_reverse.append(i)
            else:
                pass
        self.want = yesterday_give_receive_reverse

    def yesterday_no(self):
        self.want = ['korean', 'chinese', 'japanese', 'western', 'snack', 'bread', 'supper', 'fastfood', 'salad']

    def feeling(self, feel):
        self.chosen = []
        self.feel = feel

        for i in self.want:
            for j in self.feel:
                self.chosen.append(
                    db.team_project.find_one({'category': i, 'emotion': j}, {'_id': False, 'name': True, 'url': True}))

        if self.chosen == [None]:
            self.chosen = [{'name': '추천 할게 없어요 ㅠㅠ',
                            'url': 'https://blog.kakaocdn.net/dn/cCSIPC/btqKdFDO51a/vuyWbKS5CqBtWnDgyl3pv0/img.jpg'}]
        else:
            self.choice_num = [i for i in range(len(self.chosen))]
            random.shuffle(self.choice_num)

    def retry(self):
        self.retry_num += 1


what_you_want = WhatYouWantForMeal()


# HTML을 주는 부분
@app.route('/')
def home():
    # global what_you_want
    # what_you_want = WhatYouWantForMeal()
    # print('객체 새로 만듬')
    # return render_template('index.html')
    return 'hello'


@app.route('/kakao')
def kakao():
    return render_template('kakao.html')


@app.route('/want', methods=['POST'])
def want():
    want_give_receive = request.form.getlist('want_give[]')
    if want_give_receive == []:
        return jsonify({'result': 'fail', 'msg': '하나 이상 선택해 주세요!'})
    else:
        what_you_want.want_receive(want_give_receive)
        print(what_you_want.want)
        return jsonify({'result': 'success'})


@app.route('/want_no', methods=['POST'])
def want_no():
    return {'msg': '먹고 싶은게 없다니...'}


@app.route('/yesterday', methods=['POST'])
def yesterday():
    yesterday_give_receive = request.form.getlist('yesterday_give[]')
    if yesterday_give_receive == []:
        return jsonify({'result': 'fail', 'msg': '하나 이상 선택해 주세요!'})
    else:
        what_you_want.yesterday(yesterday_give_receive)
        print(what_you_want.want)
        return jsonify({'result': 'success'})


@app.route('/yesterday_no', methods=['POST'])
def yesterday_no():
    what_you_want.yesterday_no()
    print(what_you_want.want)
    return {'msg': '어제 먹은게 기억이 안나요??'}


@app.route('/feeling', methods=['POST'])
def feeling():
    feeling_give_receive = request.form.getlist('feeling_give[]')
    if feeling_give_receive == []:
        return jsonify({'result': 'fail', 'msg': '하나 이상 선택해 주세요!'})
    else:
        what_you_want.feeling(feeling_give_receive)
        if len(what_you_want.chosen) == 1:
            return jsonify({'result': 'success', 'msg1': '', 'chosen': what_you_want.chosen[0], 'msg2': ''})
        else:
            num = what_you_want.retry_num
            return jsonify(
                {'result': 'success', 'msg1': '오늘은,', 'chosen': what_you_want.chosen[what_you_want.choice_num[num]],
                 'msg2': '어때요?!'})


@app.route('/feeling_no', methods=['POST'])
def feeling_no():
    return {'msg': '하나 이상 선택해줘야 추천을 하지...!!!'}


@app.route('/retry', methods=['POST'])
def retry():
    what_you_want.retry()
    num = what_you_want.retry_num
    if what_you_want.retry_num >= len(what_you_want.choice_num):
        return jsonify({'result': 'success', 'msg1': '', 'chosen': {'name': '더 이상 추천 할게 없어요 ㅠㅠ',
                                                                    'url': 'https://blog.kakaocdn.net/dn/cCSIPC/btqKdFDO51a/vuyWbKS5CqBtWnDgyl3pv0/img.jpg'},
                        'msg2': ''})
    else:
        return jsonify(
            {'result': 'success', 'msg1': '그러면~', 'chosen': what_you_want.chosen[what_you_want.choice_num[num]],
             'msg2': '어때요?!'})


@app.route('/to_kakao', methods=['POST'])
def to_kakao():
    what_you_want.address = request.form['address_give']
    what_you_want.recommend = request.form['recommend_give']
    return render_template('kakao.html')


@app.route('/get_keyword', methods=['POST'])
def get_keyword():
    print('여기까진 ok')
    search = f'{what_you_want.address} {what_you_want.recommend}'
    print(search)
    return {'search': search}


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
