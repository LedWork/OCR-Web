import os

from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient

from app.core.db import get_db

app = Flask(__name__)


@app.route('/')
def ping_server():
    return "Welcome to the world of animals."


@app.route('/hello')
def hey():
    return "hello."


@app.route('/animal', methods=['POST'])
def create_todo():
    data = request.get_json(force=True)
    if 'animal' not in data:
        return jsonify({"error": "Missing 'todo' field in the request"}), 400
    item = {'animal': data['animal']}
    get_db().todo.insert_one(item)
    return jsonify(status=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
