from kafka import KafkaProducer
import json
import time
import random
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# read from env
KAFKA_HOST = os.getenv("KAFKA_HOST")
SSL_CA = os.getenv("SSL_CA")
SSL_CERT = os.getenv("SSL_CERT")
SSL_KEY = os.getenv("SSL_KEY")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_HOST,
    security_protocol="SSL",
    ssl_cafile=SSL_CA,
    ssl_certfile=SSL_CERT,
    ssl_keyfile=SSL_KEY,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

services = ["payment", "auth", "orders"]

errors = [
    "connection refused",
    "timeout",
    "disk full",
    "null pointer"
]

while True:
    log = {
        "service": random.choice(services),
        "status": random.choice(["SUCCESS", "FAILED"]),
        "message": random.choice(errors),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    producer.send("logs", value=log)
    print("Sent:", log)

    time.sleep(3)
