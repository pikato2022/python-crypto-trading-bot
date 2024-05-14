from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from utils.my_log import config_logging

config_logging(logging, logging.INFO)


def init_consumer(topic):
    consumer = KafkaConsumer(
        topic, value_deserializer=lambda m: json.loads(m.decode("ascii"))
    )  # use default localhost:9092 as server
    return consumer


def init_producer():
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda m: json.dumps(m).encode("ascii"),
    )
    return producer


def broadcast_kafka(producer: KafkaProducer, topic: str, message: str | bytes):
    logging.info(f"Push to Kafka {message}")
    message = json.loads(message)
    producer.send(topic, message)
