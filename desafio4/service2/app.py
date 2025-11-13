from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

SERVICE1_URL = os.getenv("SERVICE1_URL", "http://172.17.0.2:5000")

@app.route("/info")
def get_info():
    try:
        response = requests.get(f"{SERVICE1_URL}/users")
        users = response.json()
    except Exception as e:
        return jsonify({"error": f"Falha ao acessar o serviço 1: {str(e)}"}), 500

    combined = [
        f"Usuario {u['name']} tem ID {u['id']}"
        for u in users
    ]
    return jsonify(combined)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
