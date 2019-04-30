# coding: utf-8

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return jsonify("Hello World")


@app.route('/test')
def test():
    return jsonify("Test réussi")


if __name__ == "__main__":
    app.run()
