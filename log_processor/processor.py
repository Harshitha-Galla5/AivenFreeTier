from kafka import KafkaConsumer
import json
import os
from dotenv import load_dotenv
from db import get_connection
from rules import detect_issue

# load env variables
load_dotenv()

# read env
KAFKA_HOST = os.getenv("KAFKA_HOST")
SSL_CA = os.getenv("SSL_CA")
SSL_CERT = os.getenv("SSL_CERT")
SSL_KEY = os.getenv("SSL_KEY")

# DB connection
conn = get_connection()
cursor = conn.cursor()

# create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    service VARCHAR(50),
    status VARCHAR(20),
    message TEXT,
    timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    service VARCHAR(50),
    issue TEXT,
    action TEXT
)
""")

conn.commit()

# Kafka consumer
consumer = KafkaConsumer(
    'logs',
    bootstrap_servers=KAFKA_HOST,
    security_protocol="SSL",
    ssl_cafile=SSL_CA,
    ssl_certfile=SSL_CERT,
    ssl_keyfile=SSL_KEY,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='processor-groupv1'
)

print("Processor running... ")

for msg in consumer:
    log = msg.value

    # safe timestamp
    timestamp = log.get('timestamp', 'N/A')

    # store logs
    cursor.execute(
        "INSERT INTO logs (service, status, message, timestamp) VALUES (%s, %s, %s, %s)",
        (log['service'], log['status'], log['message'], timestamp)
    )
    conn.commit()

    print("Stored log:", log)

    # detect issue
    action = detect_issue(log)

    if action:
        cursor.execute(
            "INSERT INTO incidents (service, issue, action) VALUES (%s, %s, %s)",
            (log['service'], log['message'], action)
        )
        conn.commit()

        print(f"Incident created → {action} for {log['service']}")
