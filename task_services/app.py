from flask import Flask, request, jsonify
import sqlite3
from functools import wraps
import requests

app = Flask(__name__)
app.config['DEBUG'] = True

AUTH_SERVICE_URL = "http://127.0.0.1:5001/validate_token"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token requerido"}), 401

        try:
            response = requests.post(AUTH_SERVICE_URL, json={"token": token})
            if response.status_code != 200:
                return jsonify({"error": "Token inválido o expirado"}), 403
        except Exception:
            return jsonify({"error": "Error de comunicación con el servicio de autenticación"}), 500

        return f(*args, **kwargs)
    return decorated

def bd():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STATUS (
            id_status INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT
        )
    """)

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS TASKS (
            id_task INTEGER PRIMARY KEY AUTOINCREMENT,
            name_task TEXT,
            desc_task TEXT,
            created_of DATE,
            deadline DATE,
            status INTEGER,
            isActive BOOLEAN,
            Created_by TEXT,
            FOREIGN KEY (status) REFERENCES STATUS(id_status)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM STATUS")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO STATUS (status_name) VALUES (?)", [
            ('In progress',),
            ('Revision',),
            ('Completed',),
            ('Paused',)
        ])

    cursor.execute("SELECT COUNT(*) FROM TASKS")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO TASKS (name_task, desc_task, created_of, deadline, status, isActive, Created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            ('Task 1', 'Task 1 description', '2020-01-01', '2020-01-05', 1, 1, 'user1'),
            ('Task 2', 'Task 2 description', '2020-01-01', '2020-01-05', 2, 1, 'user1'),
            ('Task 3', 'Task 3 description', '2020-01-01', '2020-01-05', 3, 1, 'user1'),
            ('Task 4', 'Task 4 description', '2020-01-01', '2020-01-05', 1, 1, 'user2'),
        ])

    conn.commit()
    conn.close()

@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TASKS")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify({"tasks": tasks})

@app.route('/tasks/<int:id_task>', methods=['GET'])
@token_required
def get_task(id_task):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TASKS WHERE id_task = ?", (id_task,))
    task = cursor.fetchone()
    conn.close()
    if task:
        return jsonify({"task": task})
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
@token_required
def create_task():
    data = request.json
    if not all(k in data for k in ("name_task", "desc_task", "created_of", "deadline", "status", "isActive", "Created_by")):
        return jsonify({'error': 'Missing fields'}), 400

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TASKS (name_task, desc_task, created_of, deadline, status, isActive, Created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data['name_task'], data['desc_task'], data['created_of'], data['deadline'],
          data['status'], data['isActive'], data['Created_by']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/tasks/<int:id_task>', methods=['PUT'])
@token_required
def update_task(id_task):
    data = request.json
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TASKS WHERE id_task = ?", (id_task,))
    if cursor.fetchone() is None:
        return jsonify({'error': 'Task not found'}), 404

    cursor.execute("""
        UPDATE TASKS
        SET name_task = ?, desc_task = ?, created_of = ?, deadline = ?, status = ?, isActive = ?, Created_by = ?
        WHERE id_task = ?
    """, (data.get('name_task'), data.get('desc_task'), data.get('created_of'), data.get('deadline'),
          data.get('status'), data.get('isActive'), data.get('Created_by'), id_task))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/tasks/<int:id_task>', methods=['DELETE'])
@token_required
def delete_task(id_task):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TASKS WHERE id_task = ?", (id_task,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == '__main__':
    bd()
app.run(host="0.0.0.0", port=5003, debug=True)
