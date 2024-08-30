import feedparser
import json
import os
from datetime import datetime
from config import Config
import time

def scrape_rss_feed(url):
    feed = feedparser.parse(url)
    articles = []
    
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'content': entry.summary,  # Use entry.content if available for full content
            'published_date': entry.published if 'published' in entry else None,
            'source': url
        }
        articles.append(article)
    
    return articles

def save_data_to_json(data, filename):
    filepath = os.path.join(Config.OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def fetch_and_save_data():
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    all_articles = []
    for url in Config.RSS_URLS:
        articles = scrape_rss_feed(url)
        all_articles.extend(articles)
        print(f"Scraped {len(articles)} articles from {url}")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    news_filename = f'news_articles_{timestamp}.json'
    save_data_to_json(all_articles, news_filename)
    print(f"Saved {len(all_articles)} articles to {news_filename}")

if __name__ == "__main__":
    while True:
        print("Starting data fetch...")
        fetch_and_save_data()
        print("Data fetched and saved. Waiting for the next iteration...")
        time.sleep(3600)  # Wait for 1 hour before the next iteration