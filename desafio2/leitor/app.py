import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def ler_dados():
    conn = sqlite3.connect('/data/meubanco.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    dados = c.fetchall()
    conn.close()
    return jsonify({"usuarios": dados})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
