from flask import Flask, render_template, jsonify, request
import random
import os

application = Flask(__name__)

@application.route('/')
def main():
    return 'hello'


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)