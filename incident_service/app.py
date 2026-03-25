from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

# load env
load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.route("/")
def home():
    return {"message": "DevOps Incident API Running 🚀"}

@app.route("/incidents", methods=["GET"])
def get_incidents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents ORDER BY id DESC;")
    data = cursor.fetchall()

    result = []
    for row in data:
        result.append({
            "id": row[0],
            "service": row[1],
            "issue": row[2],
            "action": row[3]
        })

    conn.close()
    return jsonify(result)

@app.route("/logs", methods=["GET"])
def get_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50;")
    data = cursor.fetchall()

    result = []
    for row in data:
        result.append({
            "id": row[0],
            "service": row[1],
            "status": row[2],
            "message": row[3],
            "timestamp": row[4]
        })

    conn.close()
    return jsonify(result)

# observability upgrade 
@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/metrics")
def metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total_logs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM incidents")
    total_incidents = cursor.fetchone()[0]

    conn.close()

    return {
        "total_logs": total_logs,
        "total_incidents": total_incidents
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
