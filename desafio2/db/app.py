import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def criar_dados():
    conn = sqlite3.connect('/data/meubanco.db')  # caminho persistente
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT)')
    c.execute('INSERT INTO usuarios (nome) VALUES ("Lucas"), ("Maria"), ("João")')
    conn.commit()
    conn.close()
    return jsonify({"status": "dados inseridos!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
