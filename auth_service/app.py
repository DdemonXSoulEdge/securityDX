from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import secrets
import pyotp
import qrcode
import io
import base64


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

    if any(u['username'] == data['username'] for u in users):
        return jsonify({'error': 'El usuario ya existe'}), 409

    user_id = len(users) + 1
    otp_secret = pyotp.random_base32()
    new_user = {
        'id': user_id,
        'username': data['username'],
        'password': data['password'],
        'otp_secret': otp_secret
    }

    users.append(new_user)

    totp = pyotp.TOTP(otp_secret)
    otp_uri = totp.provisioning_uri(name=data['username'], issuer_name="MiApp MFA")

    qr_img = qrcode.make(otp_uri)
    buffered = io.BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({
        "message": "Usuario registrado",
        "user": {"id": user_id, "username": data['username']},
        "otp_secret": otp_secret,
        "qr_code_base64": qr_base64
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'otp' not in data:
        return jsonify({'error': 'Missing credentials or OTP'}), 400

    user = next((u for u in users if u['username'] == data['username']), None)
    if not user or user['password'] != data['password']:
        return jsonify({'error': 'Invalid username or password'}), 401

    totp = pyotp.TOTP(user['otp_secret'])
    if not totp.verify(data['otp']):
        return jsonify({'error': 'Invalid OTP'}), 401

    token = secrets.token_hex(16)
    expires = time.time() + TOKEN_EXPIRATION_SECONDS
    tokens[token] = {"user_id": user['id'], "expires": expires}

    return jsonify({"message": "Login con MFA exitoso", "token": token}), 200

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
