from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import requests
import secrets

app = Flask(__name__)
CORS(app) 

users = [
    {"id": 1, "username": "user1", "password": "pass1"},
    {"id": 2, "username": "user2", "password": "pass2"}
]

tokens = {} 
TOKEN_EXPIRATION_SECONDS = 600

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    # Verificar si ya existe el usuario
    if any(u['username'] == data['username'] for u in users):
        return jsonify({'error': 'El usuario ya existe'}), 409

    user_id = len(users) + 1
    new_user = {
        'id': user_id,
        'username': data['username'],
        'password': data['password']
    }

    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({'error': 'Missing username or password'}), 400

    user = next((user for user in users if user['username'] == request.json['username']), None)
    if not user or user['password'] != request.json['password']:
        return jsonify({'error': 'Invalid username or password'}), 401

    token = secrets.token_hex(16)
    expires = time.time() + TOKEN_EXPIRATION_SECONDS
    tokens[token] = {"user_id": user['id'], "expires": expires}

    return jsonify({"message": "Logged in successfully", "token": token}), 200

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(users), 200

@app.route('/validate_token', methods=['POST'])
def validate_token():
    data = request.json
    token = data.get("token")
    if not token or token not in tokens:
        return jsonify({"error": "Token inválido"}), 403

    if time.time() > tokens[token]['expires']:
        return jsonify({"error": "Token expirado"}), 403

    return jsonify({"message": "Token válido"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
