from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/orders")
def get_orders():
    orders = [
        {"id": 101, "user_id": 1, "item": "Teclado Mecânico", "total": 350.00},
        {"id": 102, "user_id": 2, "item": "Mouse Gamer", "total": 200.00},
        {"id": 103, "user_id": 3, "item": "Monitor 27''", "total": 1200.00},
    ]
    return jsonify(orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
