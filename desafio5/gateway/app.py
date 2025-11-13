from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# URLs internas para os microsserviços
SERVICE_USERS_URL = os.getenv("SERVICE_USERS_URL", "http://service_users:5000")
SERVICE_ORDERS_URL = os.getenv("SERVICE_ORDERS_URL", "http://service_orders:5001")

@app.route("/users")
def proxy_users():
    try:
        resp = requests.get(f"{SERVICE_USERS_URL}/users")
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": f"Falha ao acessar service_users: {str(e)}"}), 500

@app.route("/orders")
def proxy_orders():
    try:
        resp = requests.get(f"{SERVICE_ORDERS_URL}/orders")
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": f"Falha ao acessar service_orders: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
