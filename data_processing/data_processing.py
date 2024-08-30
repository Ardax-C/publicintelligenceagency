import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
import re
from config import Config

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def process_news_articles():
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DATABASE_NAME]
    news_collection = db[Config.NEWS_COLLECTION]
    processed_news_collection = db[Config.PROCESSED_NEWS_COLLECTION]

    news_articles = news_collection.find()

    for article in news_articles:
        preprocessed_title = preprocess_text(article['title'])
        preprocessed_content = preprocess_text(article['content'])

        processed_article = {
            'title': preprocessed_title,
            'content': preprocessed_content,
            'published_date': article['published_date'],
            'source': article['source']
        }

        processed_news_collection.insert_one(processed_article)

    client.close()
    print("News articles processed and stored in the processed collection.")

def process_government_data():
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DATABASE_NAME]
    gov_data_collection = db[Config.GOV_DATA_COLLECTION]
    processed_gov_data_collection = db[Config.PROCESSED_GOV_DATA_COLLECTION]

    gov_data = gov_data_collection.find()

    for data in gov_data:
        preprocessed_agency = preprocess_text(data['agency'])
        preprocessed_report = preprocess_text(data['report'])

        processed_gov_data = {
            'agency': preprocessed_agency,
            'report': preprocessed_report
        }

        processed_gov_data_collection.insert_one(processed_gov_data)

    client.close()
    print("Government data processed and stored in the processed collection.")

def process_data():
    process_news_articles()
    process_government_data()

if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    process_data()