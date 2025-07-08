from flask import Flask, jsonify, request
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

AUTH_SERVICE_URL = "http://127.0.0.1:5001"
USER_SERVICE_URL = "http://user_service:5002"

@app.route("/auth/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def auth_proxy(path):
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response, 200

    url = f"{AUTH_SERVICE_URL}/{path}"
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            json=request.get_json(silent=True),
            headers=headers
        )
        try:
            data = resp.json()
            response = jsonify(data)
        except ValueError:
            response = resp.text
        return response, resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error en la conexión con auth_service: {str(e)}"}), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
