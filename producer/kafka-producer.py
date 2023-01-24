# Publieshed a topic Environment Sensor reading to Kafka broker at kafka:9092


import csv

csv_data = csv.DictReader(open("/home/opambour/Desktop/myspark/bin/Environmental-Sensor-Real-Time/producer/iot_telemetry_data.csv"))
posts_data = []
for i in csv_data:
    posts_data.append(i)

from kafka import KafkaProducer
import time
from json import dumps

KAFKA_TOPIC = "Environment-Readings"
KAFKA_SERVER = "kafka:9092"

if __name__ == "__main__":
    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda m: dumps(m).encode('ascii'))
    for i in posts_data:
        print(i)
        kafka_producer.send(topic=KAFKA_TOPIC, key=dumps(i).encode("utf-8"), value=i)
        time.sleep(1)