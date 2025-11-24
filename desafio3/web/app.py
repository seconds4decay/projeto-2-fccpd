from flask import Flask
import psycopg2
import redis
import os

app = Flask(__name__)

db_host = os.getenv("DATABASE_HOST", "db")
redis_host = os.getenv("REDIS_HOST", "cache")

@app.route("/")
def index():
    # Teste de conexão ao banco de dados
    try:
        conn = psycopg2.connect(
            dbname="meubanco",
            user="user",
            password="secret",
            host=db_host
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        conn.close()
    except Exception as e:
        db_version = f"Erro ao conectar no DB: {e}"

    # Teste de conexão ao Redis
    try:
        r = redis.Redis(host=redis_host, port=6379)
        r.set("mensagem", "Conexao com Redis OK!")
        cache_msg = r.get("mensagem").decode("utf-8")
    except Exception as e:
        cache_msg = f"Erro ao conectar no Redis: {e}"

    return {
        "database_version": db_version,
        "cache_message": cache_msg
    }
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
