import json
from flask import Flask, jsonify

app = Flask(__name__)

def success_response(message, data):
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return json.dumps(response, default=str).lower(), 200, {'Content-Type': 'application/json'}

def fail_response(message, code=500):
    response = {
        "success": False,
        "message": message,
    }
    return json.dumps(response, default=str).lower(), code, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
