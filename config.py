import os

class Config:
    # MongoDB
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'mydatabase')
    NEWS_COLLECTION = os.environ.get('NEWS_COLLECTION', 'news_articles')

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_NEWS_TOPIC = os.environ.get('KAFKA_NEWS_TOPIC', 'news_topic')
    KAFKA_GOV_TOPIC = os.environ.get('KAFKA_GOV_TOPIC', 'gov_topic')

    # Elasticsearch
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost')
    ELASTICSEARCH_PORT = int(os.environ.get('ELASTICSEARCH_PORT', 9200))
    ELASTICSEARCH_INDEX = os.environ.get('ELASTICSEARCH_INDEX', 'search_index')

    # RSS Feeds
    OUTPUT_DIR = os.path.join('..', 'data')
    RSS_URLS = [
        'https://feeds.reuters.com/reuters/topNews',
        'https://feeds.npr.org/1001/rss.xml',
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://www.theguardian.com/world/rss',
        'https://apnews.com/apf-topnews?format=rss'
    ]

    # Other settings
    OUTPUT_DIR = os.environ.get('OUTPUT_DIR', os.path.join('..', 'data'))
