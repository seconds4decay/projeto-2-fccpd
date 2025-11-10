from flask import Flask, jsonify
import threading
import time
import requests
import logging

app = Flask(__name__)
status = {"ultima_resposta": None}
logging.basicConfig(level=logging.INFO, filename='comunicacao.log')

def requisitar_periodicamente():
    while True:
        try:
            r = requests.get("http://server:8080")
            status["ultima_resposta"] = r.text
            logging.info(f"Resposta do servidor: {r.text}")
            
        except Exception as e:
            status["ultima_resposta"] = f"Erro: {e}"
            logging.error(f"Erro ao conectar: {e}")
        time.sleep(5)

@app.route('/')
def home():
    return jsonify(status)

if __name__ == "__main__":
    threading.Thread(target=requisitar_periodicamente, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
