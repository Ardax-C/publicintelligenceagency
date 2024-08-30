from kafka import KafkaProducer, KafkaConsumer
import json
from pymongo import MongoClient
from config import Config

producer_config = {
    'bootstrap_servers': [Config.KAFKA_BOOTSTRAP_SERVERS],
    'value_serializer': lambda v: json.dumps(v).encode('utf-8')
}

consumer_config = {
    'bootstrap_servers': [Config.KAFKA_BOOTSTRAP_SERVERS],
    'group_id': 'data-ingestion-group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
    'value_deserializer': lambda v: json.loads(v.decode('utf-8'))
}

def publish_to_kafka(topic, data):
    producer = KafkaProducer(**producer_config)
    try:
        producer.send(topic, value=data)
        producer.flush()
        print(f"Data published to topic '{topic}': {data}")
    except Exception as e:
        print(f"Error publishing data to topic '{topic}': {str(e)}")
    finally:
        producer.close()

def consume_from_kafka(topic):
    consumer = KafkaConsumer(topic, **consumer_config)
    try:
        for message in consumer:
            data = message.value
            print(f"Data consumed from topic '{topic}': {data}")
            process_data(data)
    except Exception as e:
        print(f"Error consuming data from topic '{topic}': {str(e)}")
    finally:
        consumer.close()

def process_data(data):
    cleaned_data = clean_data(data)
    store_data(cleaned_data)

def clean_data(data):
    cleaned_data = {
        'title': data['title'].replace('/', '').lower(),
        'content': data['content'].replace('/', '').lower()
    }
    return cleaned_data

def store_data(data):
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DATABASE_NAME]
    collection = db[Config.PROCESSED_NEWS_COLLECTION]
    collection.insert_one(data)
    client.close()

if __name__ == "__main__":
    consume_from_kafka(Config.KAFKA_NEWS_TOPIC)
    consume_from_kafka(Config.KAFKA_GOV_TOPIC)