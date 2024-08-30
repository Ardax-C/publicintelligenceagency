from pymongo import MongoClient
import json
import os
from config import Config

def store_data_in_mongodb(data, collection_name):
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DATABASE_NAME]
    collection = db[collection_name]

    if isinstance(data, list):
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")
    else:
        result = collection.insert_one(data)
        print(f"Inserted document with ID {result.inserted_id} into {collection_name}")

    client.close()

def retrieve_data_from_mongodb(collection_name, query=None):
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DATABASE_NAME]
    collection = db[collection_name]

    if query:
        results = collection.find(query)
    else:
        results = collection.find()

    data = list(results)
    client.close()
    return data

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def process_and_store_news_articles(news_data):
    cleaned_news_data = []
    for article in news_data:
        if 'title' in article and 'content' in article and 'published_date' in article and 'source' in article:
            cleaned_article = {
                'title': article['title'],
                'content': article['content'],
                'published_date': article['published_date'],
                'source': article['source']
            }
            cleaned_news_data.append(cleaned_article)

    store_data_in_mongodb(cleaned_news_data, Config.NEWS_COLLECTION)

def process_and_store_government_data(gov_data):
    if 'agency' in gov_data and 'report' in gov_data:
        cleaned_gov_data = {
            'agency': gov_data['agency'],
            'report': gov_data['report']
        }

        store_data_in_mongodb(cleaned_gov_data, Config.GOV_DATA_COLLECTION)
    else:
        print("Invalid government data format")

def process_and_store_data_from_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            data = load_json_data(file_path)

            if 'news_articles' in filename:
                process_and_store_news_articles(data)
            elif 'government_data' in filename:
                process_and_store_government_data(data)

if __name__ == "__main__":
    process_and_store_data_from_files(Config.OUTPUT_DIR)

    news_articles = retrieve_data_from_mongodb(Config.NEWS_COLLECTION)
    print(f"Retrieved {len(news_articles)} news articles from MongoDB")

    gov_data = retrieve_data_from_mongodb(Config.GOV_DATA_COLLECTION, query={'agency': 'Example Agency'})
    print(f"Retrieved {len(gov_data)} government data entries for 'Example Agency' from MongoDB")