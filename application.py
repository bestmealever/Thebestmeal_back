from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import os

application = Flask(__name__)

cors = CORS(application, resources={r"/*": {"origins": "*"}})

@application.route('/')
def main():
    return 'hello'

@application.route('/test')
def test():
    return {'msg': 'testtesttest'}

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)