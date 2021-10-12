from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import random
import os

app = Flask(__name__)

@app.route('/')
def main():
    return 'hello'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)